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

# Function Tool
@function_tool
def calculate_investment_return(principal: float, rate: float, years: int) -> str:
    future_value = principal * ((1 + rate / 100) ** years)
    return f"📈 Future Value after {years} years: ${future_value:.2f}"

# Guardrail & Handrail
def finance_guardrail(query: str) -> str | None:
    if "guaranteed profit" in query.lower():
        return "⚠️ I cannot provide guaranteed financial advice."
    banned_keywords = ["fraud", "scam"]
    if any(word in query.lower() for word in banned_keywords):
        return "⚠️ Unsafe query detected."
    return None

def finance_handrail(query: str) -> str | None:
    if len(query.strip()) < 5:
        return "🤔 Please provide more details about your financial question."
    return None

# Agent
finance_agent = Agent(
    name="finance_advisor",
    instructions="""
    You are a Finance Advisor Agent 💼.
    Guardrails: Do NOT provide personal financial advice or illegal tips.
    Handrails: Ask for clarification if question is vague.
    """,
    model=llm_model,
    tools=[calculate_investment_return]
)

# Chainlit Integration
@cl.on_chat_start
async def start():
    await cl.Message(content="👋 Welcome to Finance Advisor! Ask me about stocks or investments.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    query = message.content
    guard = finance_guardrail(query)
    if guard: 
        await cl.Message(content=guard).send()
        return
    handrail = finance_handrail(query)
    if handrail:
        await cl.Message(content=handrail).send()
        return
    result = await Runner.run(finance_agent, query)
    await cl.Message(content=getattr(result, "final_output", str(result))).send()
