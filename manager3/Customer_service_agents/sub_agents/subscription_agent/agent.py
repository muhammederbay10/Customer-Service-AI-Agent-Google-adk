from google.adk.agents import Agent

subscription_agent = Agent(
    name="subscription_agent",
    model="gemini-1.5-flash",
    description="Handles subscription management and inquiries",
    instruction= """
    You are a subscription agent responsible for managing customer subscriptions.
    Before anything, check if the user is authenticated by calling the authentication_agent.
    If the user is not authenticated, say "Please authenticate first" and stop."""
)
