from google.adk import Agent
from tools.authenticaiton import authenticate_user


def billing_agent():
    return Agent(
        name="billing_agent",
        model="gemini-2.0-flash",
        description="An agent that handles billing inquiries and payments for users.",
        instructions="""
        You are a billing assistant agent. Your primary responsibilities include:
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