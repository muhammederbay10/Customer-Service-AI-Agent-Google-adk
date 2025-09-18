import asyncio
from datetime import datetime
from google.genai import types

async def update_interaction(session_service, app_name, user_id, session_id, entry):
    """Append to interaction_history and persist when possible."""
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        history = list(session.state.get("interaction_history", []))
        history.append(entry)
        session.state["interaction_history"] = history

        if hasattr(session_service, "set_session_state"):
            await session_service.set_session_state(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                state=session.state,
            )
        elif hasattr(session_service, "update_state"):
            await session_service.update_state(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                state_delta={"interaction_history": history},
            )
    except Exception as e:
        print(f"Error updating interaction history: {e}")

async def add_user_query_to_history(session_service, app_name, user_id, session_id, query):
    await update_interaction(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "role": "user",
            "content": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )

async def add_agent_response_to_history(session_service, app_name, user_id, session_id, response):
    await update_interaction(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "role": "agent",
            "content": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )

async def process_message(event):
    """Extract text from ADK events without touching event.text (avoids warnings)."""
    texts = []

    # Prefer candidates[].content.parts if present
    candidates = getattr(event, "candidates", None)
    if candidates:
        for c in candidates:
            cont = getattr(c, "content", None)
            parts = getattr(cont, "parts", None) or []
            for p in parts:
                t = getattr(p, "text", None)
                if isinstance(t, str) and t:
                    texts.append(t)
        return "\n".join(texts) if texts else None

    # Fallback: event.content.parts
    content = getattr(event, "content", None)
    parts = getattr(content, "parts", None) if content is not None else None
    if parts:
        for p in parts:
            t = getattr(p, "text", None)
            if isinstance(t, str) and t:
                texts.append(t)
        return "\n".join(texts) if texts else None

    return None

async def call_agent_async(runner, user_id, session_id, query):
    """Send user message, persist via state_delta, return agent reply text."""
    user_content = types.Content(role="user", parts=[types.Part.from_text(text=query)])

    # Build new history snapshot to persist atomically via state_delta
    try:
        session = await runner.session_service.get_session(
            app_name=runner.app_name, user_id=user_id, session_id=session_id
        )
        history = list(session.state.get("interaction_history", []))
    except Exception:
        history = []
    user_entry = {
        "role": "user",
        "content": query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    new_history = history + [user_entry]

    final_response_text = None
    backoff = 1.0
    for attempt in range(3):
        try:
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_content,
                state_delta={"interaction_history": new_history},
            ):
                chunk = await process_message(event)
                if chunk:
                    final_response_text = chunk  
            break
        except Exception as e:
            msg = str(e)
            if "503" in msg or "UNAVAILABLE" in msg:
                if attempt == 2:
                    print(f"Error during agent run: {e}")
                    break
                await asyncio.sleep(backoff)
                backoff *= 2
                continue
            print(f"Error during agent run: {e}")
            break

    if final_response_text:
        await add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            final_response_text,
        )
    return final_response_text

