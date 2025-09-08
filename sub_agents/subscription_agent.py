from google.adk import Agent
from tools.authenticaiton import authenticate_user

def subscription_agent():
    return Agent(
        name="subscription_agent",
        model="gemini-2.0-flash",
        description="An agent that handles subscription inquiries and management for users.",
        instructions="""
        You are a subscription assistant agent. Your primary responsibilities include:
        1. Verifying user identity using their Name and TC_Kimlik (Turkish ID number) by using the authenticate_user tool.
        2. If the user is authenticated, say hi {user_data['name']} you are authenticated and stop, if not say "Authentication failed."
        3. If the user says something unrelated take them back to the General agent.

        Example response format:
        "Hi {user_data['Name']}, you are authenticated."
        """,
        tools=[authenticate_user],
        max_iterations=5,
        max_execution_time=600,
    )