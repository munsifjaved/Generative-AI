import os
import chainlit as cl
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled

load_dotenv()
set_tracing_disabled(disabled=True)

# LLM Setup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
llm_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)

# Function Tools
@function_tool
def get_mock_flight(city_from: str, city_to: str) -> str:
    return f"✈️ Cheapest flight from {city_from} to {city_to}: $350, 1 stop, 7h travel."

@function_tool
def get_mock_hotel(city: str) -> str:
    return f"🏨 Top hotel in {city}: Grand Palace Hotel, $120/night."

# Guardrail & Handrail
def travel_guardrail(query: str) -> str | None:
    if "illegal" in query.lower():
        return "⚠️ Cannot provide information on illegal activities."
    return None

def travel_handrail(query: str) -> str | None:
    if len(query.strip()) < 5:
        return "🤔 Please provide city names or travel details."
    return None

# Agent
travel_agent = Agent(
    name="travel_planner",
    instructions="""
    You are a Travel Planner 🌍.
    Guardrails: Avoid illegal or unsafe advice.
    Handrails: Ask for missing info like city names.
    """,
    model=llm_model,
    tools=[get_mock_flight, get_mock_hotel]
)

# Chainlit Integration
@cl.on_chat_start
async def start():
    await cl.Message(content="👋 Welcome to Travel Planner! Ask about flights or hotels.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    query = message.content
    guard = travel_guardrail(query)
    if guard:
        await cl.Message(content=guard).send()
        return
    handrail = travel_handrail(query)
    if handrail:
        await cl.Message(content=handrail).send()
        return
    result = await Runner.run(travel_agent, query)
    await cl.Message(content=getattr(result, "final_output", str(result))).send()
