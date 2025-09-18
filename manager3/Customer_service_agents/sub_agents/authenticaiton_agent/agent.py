from google.adk.agents import Agent

authentication_agent = Agent(
    name="authentication_agent",
    model="gemini-1.5-flash",
    description="Handles user authentication and authorization",
    instruction= """
    You are an authentication agent responsible for verifying user identities.
      After successful authentication, say "Authentication successful" and stop"""
)
