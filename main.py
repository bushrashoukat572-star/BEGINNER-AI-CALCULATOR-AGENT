import os
import json
from dotenv import load_dotenv

# UNSET conflicting keys BEFORE importing google-genai
if "GOOGLE_API_KEY" in os.environ:
    del os.environ["GOOGLE_API_KEY"]
if "GEMINI_API_KEY" in os.environ:
    del os.environ["GEMINI_API_KEY"]

from google import genai
from tools import *

# Load env with override to prioritize .env file
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Tool mapping
TOOLS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "power": power,
    "sqrt": sqrt
}

def run_agent(user_input):
    prompt = f"""
You are an AI calculator agent.

Your tasks:
1. Understand math query
2. Select correct function
3. Return structured JSON ONLY

Available tools:
{list(TOOLS.keys())}

Format:
{{
  "operation": "add",
  "a": 5,
  "b": 3
}}

User input: {user_input}
"""

    try:
        # Using gemini-flash-latest with JSON mode
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config={
                "max_output_tokens": 500,
                "temperature": 0.1,
                "response_mime_type": "application/json"
            }
        )
        
        text = response.text.strip()
        
        # Simple cleanup if model returns markdown
        if text.startswith("```json"):
            text = text.split("```json")[1].split("```")[0].strip()
        elif text.startswith("```"):
            text = text.split("```")[1].split("```")[0].strip()

        # Convert to JSON
        data = json.loads(text)

        operation = data.get("operation")
        a = data.get("a")
        b = data.get("b")

        if operation not in TOOLS:
            return {"error": f"Invalid operation: {operation}"}

        # Execute function
        if operation == "sqrt":
            result = TOOLS[operation](a)
        else:
            result = TOOLS[operation](a, b)

        # Save memory
        memory["last_result"] = result

        return {
            "operation": operation,
            "input": {"a": a, "b": b},
            "result": result,
            "memory": memory
        }

    except Exception as e:
        return {
            "error": str(e)
        }

if __name__ == "__main__":
    print("🔥 AI Calculator Agent Started (Gemini - New SDK)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        result = run_agent(user_input)
        print("\n🤖 Agent Response:")
        print(json.dumps(result, indent=2))
        print()
