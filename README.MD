# 🤖 Multi-Agent Assistant Repository

This repository contains **three fully-featured AI agents** built with **Chainlit** and **Hugging Face Spaces**. Each agent is **self-contained** with:

- **Guardrails** – safety rules to avoid unsafe or illegal queries.  
- **Handrails** – gentle guidance for vague or incomplete inputs.  
- **Function Tools** – domain-specific computations (BMI, investment returns, mock travel tools, etc.).  
- **Basic features** – dynamic responses and structured outputs.  

Agents included:  

1. **Finance Advisor Agent** – investment calculations and general finance advice.  
2. **Health Assistant Agent** – BMI calculations and wellness guidance.  
3. **Travel Planner Agent** – mock flight and hotel suggestions.

---

## 📁 Repository Structure

```text
multi-agent-assistant/
│
├─ finance_agent.py       # Finance Advisor Agent
├─ health_agent.py        # Health Assistant Agent
├─ travel_agent.py        # Travel Planner Agent
├─ requirements.txt       # Python dependencies
├─ .env                   # Environment variables (API keys)
└─ README.md              # Project documentation
