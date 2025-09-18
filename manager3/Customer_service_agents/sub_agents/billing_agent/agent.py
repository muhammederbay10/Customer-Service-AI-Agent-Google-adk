from google.adk.agents import Agent

billing_agent = Agent(
    name="billing_agent",
    model="gemini-1.5-flash",
    description="Handles billing and payment processing",
    instruction= """
    You are a billing agent responsible for managing customer billing inquiries and payment processing.
    Before anything, check if the user is authenticated by calling the authentication_agent. 
    If the user is not authenticated, say "Please authenticate first" and stop."""
)
