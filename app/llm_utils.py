# app/llm_utils.py

import requests
import streamlit as st

def ask_llm(question: str, schema: dict) -> str:
    """
    Sends a question and table schema to the Hugging Face LLM and returns SQL.
    """
    try:
       hf_token = st.secrets["huggingface"]["api_key"]
       model_id = st.secrets["huggingface"]["model_id"] 
    except KeyError:
        raise ValueError("❌ Hugging Face API key or model ID not found in secrets.toml")

    prompt = generate_prompt(question, schema)

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 128,
            "return_full_text": False
        }
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model_id}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()[0]['generated_text'].strip()
    else:
        raise Exception(f"🤖 LLM API call failed: {response.status_code}\n{response.text}")


def query_llm(prompt: str) -> str:
    """
    Sends a natural language prompt directly to Hugging Face LLM and returns plain answer.
    """
    try:
        hf_token = st.secrets["huggingface"]["api_key"]
        model_id = st.secrets["huggingface"]["model_id"]
    except KeyError:
        raise ValueError("❌ Hugging Face API key or model ID not found in secrets.toml")

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "return_full_text": False
        }
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model_id}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()[0]['generated_text'].strip()
    else:
        raise Exception(f"🤖 LLM API call failed: {response.status_code}\n{response.text}")


def generate_prompt(question: str, schema: dict) -> str:
    """
    Constructs the prompt to convert the question into SQL using table schema.
    """
    schema_lines = "\n".join([f"{col}: {dtype}" for col, dtype in schema.items()])
    return f"""### Given the table schema below:
{schema_lines}

### Convert this question to SQL:
Question: {question}
SQL:"""
