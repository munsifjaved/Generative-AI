# 🤖 Generative AI Multi-Agent Repository

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
Generative-AI/
│
├─ Finance Advisor Agent.py       # Finance Advisor Agent
├─ Health Assistant Agent.py      # Health Assistant Agent
├─ Travel Planner Agent.py        # Travel Planner Agent
├─ requirements.txt               # Python dependencies
├─ Dockerfile                     # Docker configuration (optional)
├─ README.MD                      # Project documentation
└─ .env                           # Environment variables (API keys)
