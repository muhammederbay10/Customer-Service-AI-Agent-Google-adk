from google.adk.agents import Agent

def user_database_lookup(user_name: str) -> dict:
    """
    Look up whether the given user_name exists in the customer database.

    Args:
        user_name: The person's name, e.g. "Muhammed".
    Returns:
        {"exists": bool} indicating if the name is found.
    """
    known_users = {"Muhammed", "Abdelrahman", "Furkan"}
    return {"exists": user_name in known_users}

authentication_agent = Agent(
    name="authentication_agent",
    model="gemini-1.5-flash",
    description="Handles user authentication and authorization",
    instruction="""
You are an authentication agent responsible for verifying user identities.
- Extract the user's name from their message.
- Call user_database_lookup(user_name=<extracted name>) to check if they exist.
- If exists is true, reply: "Authentication successful" and then ask what they need.
- If no clear name is given, ask them to provide their name.
- If exists is false, reply: "Authentication failed" and ask for a valid name.
""",
    tools=[user_database_lookup],
)
