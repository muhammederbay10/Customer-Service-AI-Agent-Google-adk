from google.adk import Agent
import os 
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sub_agents.billing_agent.billing_agent import billing_agent
from sub_agents.subscription_agent.subscription_agent import subscription_agent

general_agent = Agent(
        name="manager",
        model="gemini-2.0-flash",
        description="A general customer service agent that can handle a variety of customer inquiries and direct them to specialized agents as needed.",
        instructions="""
        You are a general customer service agent. Your primary responsibilities include:
        1. Understanding customer inquiries and providing accurate information.
        2. If the inquiry is related to billing, transfer the request to the billing_agent.
        3. If the inquiry is related to subscriptions, transfer the request to the subscription_agent.
        4. If the inquiry is unrelated, provide a generic response or ask for clarification.
    """,
    sub_agents=[billing_agent, subscription_agent],
    )