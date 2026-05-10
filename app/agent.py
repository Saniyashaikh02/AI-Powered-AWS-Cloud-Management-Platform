from aws_utils import generate_recommendations
import os
from google import genai
from aws_utils import (
    list_ec2_instances,
    find_stopped_instances,
    list_s3_buckets,
    estimate_ec2_cost
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# ===== INTENT DETECTION =====
def detect_intent(user_query):
    q = user_query.lower()

    if any(x in q for x in ["hi", "hello", "how are", "kaise"]):
        return "chat"

    if any(x in q for x in ["bye", "by", "exit"]):
        return "exit"

    return "aws"


# ===== TOOL SELECTION =====
def ai_decide_tool(user_query):
    q = user_query.lower()

    # 🔥 cost trigger
    if "cost" in q or "save" in q:
        return "cost"

    try:
        prompt = f"""
        You are an AWS AI agent.

        Tools:
        - ec2 → instances
        - stopped → unused resources
        - s3 → buckets

        Query: {user_query}

        Reply ONLY: ec2, stopped, or s3
        """

        res = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return res.text.strip().lower()

    except:
        if "bucket" in q:
            return "s3"
        if "stopped" in q or "unused" in q:
            return "stopped"
        return "ec2"


# ===== TOOL EXECUTION =====
def execute_tool(tool):
    if tool == "s3":
        return list_s3_buckets()

    if tool == "stopped":
        return find_stopped_instances()

    if tool == "cost":
        stopped = find_stopped_instances()
        cost = estimate_ec2_cost(stopped)
        return {"stopped": stopped, "cost": cost}

    return list_ec2_instances()


# ===== RESPONSE GENERATION =====
def generate_ai_answer(user_query, tool, data):

    if tool == "chat":
        return "😊 I'm doing great! How can I help you with AWS today?"

    if tool == "exit":
        return "👋 Goodbye!"

    # 🔥 COST RESPONSE (direct)
    if tool == "cost":
        return f"💰 You have {len(data['stopped'])} stopped instance(s), costing approx ${data['cost']} per month. Consider removing unused resources."

    try:
        prompt = f"""
        You are a friendly AWS Cloud Assistant.

        User asked: {user_query}
        AWS data: {data}

        Explain clearly in simple language.
        Give helpful suggestions.
        """

        res = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return res.text

    except:
        return f"📊 Data: {data}"


# ===== MAIN AGENT =====
def run_agent(user_query):
    intent = detect_intent(user_query)

    print(f"🧠 Intent: {intent}")

    if intent in ["chat", "exit"]:
        return generate_ai_answer(user_query, intent, None)

    tool = ai_decide_tool(user_query)
    print(f"🔧 Tool: {tool}")

    data = execute_tool(tool)

    return generate_ai_answer(user_query, tool, data)