# Capstone 2: Global Intelligent Fleet Assistant

Welcome to Capstone 2! This project focuses on building an **Intelligent Fleet Assistant** for Global drivers and fleet managers. You will combine advanced concepts (Retrieval-Augmented Generation, Multi-turn Context, Security, Guardrails, Evaluation) to build a robust, production-ready AI tool.

## Setup
Ensure your environment is active and your API keys are set up via a `.env` file just like in previous exercises.

## Exercise 1: Fleet Policy RAG System
**File:** `exercise1_fleet_rag.py`

Your goal is to build a basic RAG system that answers questions based strictly on the provided Global Fleet Management Driver Policy Guidelines.
- Load the document `data/global_fleet_policy.md`.
- Chunk and embed the text using a vector store of your choice (e.g. FAISS, Chroma, or a simple cosine similarity script).
- Create a prompt that injects the retrieved chunks to accurately answer: *"How often do I need to get an oil change?"*

## Exercise 2: Guardrailed Maintenance Chatbot
**File:** `exercise2_guardrailed_chat.py`

Extend the assistant to handle a multi-turn conversation with a driver experiencing vehicle issues, but ensure the chatbot stays on topic and safe.
- Implement a chat loop that remembers previous turns.
- Implement an **Input Guardrail** that rejects queries completely unrelated to vehicles or fleet management.
- Implement an **Output Guardrail** that prevents the bot from providing dangerous DIY repair instructions (e.g., instructing a user how to bypass a battery terminal).

## Exercise 3: Maintenance Invoice Evaluator
**File:** `exercise3_invoice_eval.py`

You have been tasked with automating invoice data extraction. To ensure the LLM is accurate before deploying to production, you need to build an evaluation harness.
- Load the dataset `data/invoice_dataset.json`.
- Write an LLM prompt that extracts the total cost and list of services from the messy invoice text.
- Compare the LLM's output against the `expected_total` and `expected_services` in the dataset.
- Calculate and print a final accuracy score (e.g., "4/5 invoices correctly parsed").
