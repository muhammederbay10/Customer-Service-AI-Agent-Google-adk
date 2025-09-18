from google.adk.agents import Agent
from .sub_agents.authenticaiton_agent.agent import authentication_agent
from .sub_agents.billing_agent.agent import billing_agent
from .sub_agents.subscription_agent.agent import subscription_agent

customer_service_agent = Agent(
    name="customer_service_agent",
    model="gemini-1.5-flash",
    description="Customer service agent for managing subscriptions and billing",
    instruction="""
    You are a customer service agent for a telecom company called zephlen. 
    Your role is to help users with their subscription and billing inquiries.
    you have access to the following specialized agents:
    1. billing_agent
       - For questions about billing and payment processing

    2. subscription_agent
       - For questions about subscription management and inquiries
       - If the user asks about changing their subscription plan, escalate to the subscription_agent.""",
    sub_agents=[billing_agent, subscription_agent, authentication_agent],
    tools=[],
    )