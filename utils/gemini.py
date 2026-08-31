from google import genai
from google.genai import types

# ==========================================
# Gemini API Configuration
# ==========================================

import os

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


# ==========================================
# AI Summary Generator
# ==========================================

def generate_summary(total, fraud, genuine, fraud_rate):

    prompt = f"""
You are a senior financial fraud analyst working for a multinational bank.

Write a professional financial fraud analysis report.

Dataset Statistics:
- Total Transactions: {total:,}
- Fraud Transactions: {fraud:,}
- Genuine Transactions: {genuine:,}
- Fraud Rate: {fraud_rate:.2f}%

Requirements:
- Write between 180 and 220 words.
- Write ONE continuous paragraph.
- Do NOT use markdown.
- Do NOT use bullet points.
- Do NOT use headings.
- Do NOT use numbering.
- Explain the overall dataset, fraud percentage, risk assessment, business impact, recommendations and conclusion.

Return ONLY the paragraph.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=600,
    thinking_config=types.ThinkingConfig(
        thinking_budget=0
    ),
),
        )

        print("=" * 80)
        print("FULL RESPONSE OBJECT")
        print(response)
        print("=" * 80)

        print("FINISH REASON:")
        print(response.candidates[0].finish_reason)

        print("=" * 80)
        print("CANDIDATE")
        print(response.candidates[0])
        print("=" * 80)

        print("TEXT RETURNED")
        print(response.text)
        print("Length:", len(response.text))
        print("=" * 80)

        summary = response.text.strip()

        return summary

    except Exception as e:

        print("=" * 80)
        print("GEMINI ERROR")
        print(e)
        print("=" * 80)

        return (
            f"This analysis examined {total:,} financial transactions, of which "
            f"{fraud:,} were identified as fraudulent and {genuine:,} were classified "
            f"as genuine, resulting in a fraud rate of {fraud_rate:.2f}%. Although "
            f"the percentage of fraudulent transactions is relatively low, even a "
            f"small number of successful fraud attempts can lead to significant "
            f"financial losses, operational disruption, and reputational damage for "
            f"financial institutions. Continuous monitoring of transaction behavior, "
            f"machine learning-based fraud detection, regular model retraining, "
            f"multi-factor authentication, and real-time risk scoring are recommended "
            f"to strengthen security and improve fraud prevention."
        )