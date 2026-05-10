import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def fallback_response(user_query, instances, stopped_instances, buckets):
    user_query = user_query.lower()

    if "hi" in user_query or "hello" in user_query:
        return "👋 Hello! I can help you analyze your AWS resources."

    # EC2
    if "instance" in user_query:
        return f"📊 You have {len(instances)} EC2 instance(s)."

    # stopped
    if "stopped" in user_query or "unused" in user_query:
        if not stopped_instances:
            return "✅ No stopped instances found."
        else:
            return f"⚠️ You have {len(stopped_instances)} stopped instance(s)."

    # S3 FIXED 🔥
    if "bucket" in user_query or "s3" in user_query:
        return f"🪣 You have {len(buckets)} bucket(s): {buckets}"

    # cost
    if "cost" in user_query:
        return "💰 Stopped instances may still cost you due to storage."

    return "🤖 Ask me about AWS resources (instances, buckets, cost)."


def generate_ai_response(user_query, instances, stopped_instances, buckets):
    try:
        context = f"""
        AWS Data:
        Instances: {instances}
        Buckets: {buckets}
        """

        prompt = f"""
        You are an AWS Cloud Assistant.

        {context}

        User question:
        {user_query}
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        print("⚠️ AI failed, using fallback...")
        return fallback_response(user_query, instances, stopped_instances, buckets)