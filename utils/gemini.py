import os

API_KEY = os.getenv("GEMINI_API_KEY")
client = None

if API_KEY:
    from google import genai
    client = genai.Client(api_key=API_KEY)


def generate_summary(total, fraud, genuine, fraud_rate):
    if client:
        try:
            prompt = f"""
            Analyse these financial transactions:
            Total: {total}
            Fraudulent: {fraud}
            Genuine: {genuine}
            Fraud rate: {fraud_rate}%

            Explain the risk, business impact and recommendations.
            """
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            if response.text:
                return response.text.strip()
        except Exception as e:
            print("Gemini unavailable:", e)

    return (
        f"The analysis examined {total:,} transactions. "
        f"{fraud:,} were classified as fraudulent and "
        f"{genuine:,} as genuine, giving a fraud rate of "
        f"{fraud_rate:.2f}%. High-risk transactions should be "
        "reviewed promptly. Continuous transaction monitoring, "
        "strong authentication and periodic model evaluation "
        "are recommended to strengthen fraud prevention."
    )
