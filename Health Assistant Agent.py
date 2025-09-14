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
def bmi_calculator(weight: float, height: float) -> str:
    bmi = weight / (height ** 2)
    status = "Underweight" if bmi < 18.5 else "Normal" if bmi < 24.9 else "Overweight" if bmi < 29.9 else "Obese"
    return f"⚕️ Your BMI is {bmi:.1f} ({status})."

# Guardrail & Handrail
def health_guardrail(query: str) -> str | None:
    banned_keywords = ["self-harm", "emergency"]
    if any(word in query.lower() for word in banned_keywords):
        return "⚠️ This may be an emergency. Please consult a professional immediately."
    return None

def health_handrail(query: str) -> str | None:
    if len(query.strip()) < 5:
        return "🤔 Please provide more details about your health question."
    return None

# Agent
health_agent = Agent(
    name="health_assistant",
    instructions="""
    You are a Health Assistant 🩺.
    Guardrails: Do not provide diagnoses or emergency instructions.
    Handrails: Ask for clarification if vague.
    """,
    model=llm_model,
    tools=[bmi_calculator]
)

# Chainlit Integration
@cl.on_chat_start
async def start():
    await cl.Message(content="👋 Welcome to Health Assistant! Ask me about BMI or wellness.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    query = message.content
    guard = health_guardrail(query)
    if guard:
        await cl.Message(content=guard).send()
        return
    handrail = health_handrail(query)
    if handrail:
        await cl.Message(content=handrail).send()
        return
    result = await Runner.run(health_agent, query)
    await cl.Message(content=getattr(result, "final_output", str(result))).send()
