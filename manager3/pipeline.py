import asyncio

from Customer_service_agents.agent import customer_service_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

# Initial state
DEFAULT_INITIAL_STATE = {
    "user_name": "User",
}

session_service = InMemorySessionService()  

async def main_pipeline():
    # Constants
    app_name = "Zephlen Telecom"
    user_id = "user_123"
    # Create a new session
    new_session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        state=DEFAULT_INITIAL_STATE
    )
    # Get the session ID
    session_id = new_session.id
    print(f"Created new session: {session_id}")
    # Create a runner with the customer service agent
    runner = Runner(
        agent=customer_service_agent,
        app_name="Zephlen Telecom",
        session_service=session_service,
    )

    # Interactive conversation loop
    print("\nWelcome to Zephlen Telecom Customer Service!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ")
        # Check if user wants to exit
        if user_input.lower() in {"exit", "quit"}:
            print("Ending conversation. Goodbye!")
            break

        # Add user query to history
        await add_user_query_to_history(
            session_service, app_name, user_id, session_id, user_input
        )

        # Call the agent asynchronously
        agent_reply = await call_agent_async(runner, user_id, session_id, user_input)
        if agent_reply:
            print(f"Agent: {agent_reply}")

        # Debug: verify interaction_history
        check = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
        print("interaction_history size:", len(check.state.get("interaction_history", [])))

        final_session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        print("\nFinal Session State:")
        for k, v in final_session.state.items():
            print(f"{k}: {v}")

def main():
    """Entry point for the application."""
    asyncio.run(main_pipeline())

if __name__ == "__main__":
    main()