from groq import Groq
import os
import json

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_explanation(recommendation):
    """
    Generates a concise procurement explanation
    using the Groq LLM.

    The LLM explains the recommendation but
    does not make procurement decisions.
    """

    prompt = f"""
You are a senior procurement analyst preparing insights for a procurement manager.

Your role is to explain the recommendation already made by the recommendation engine.
Do NOT change or question the recommendation.

Return ONLY valid JSON in the following format:

{{
    "summary": "",
    "risk_assessment": "",
    "recommended_action": ""
}}

Guidelines:

1. SUMMARY
- Write 2-3 complete sentences.
- Explain why the supplier was selected.
- Mention the supplier's risk band and inventory situation only if relevant.
- The explanation should sound natural and professional.

2. RISK_ASSESSMENT
- Write 2-3 complete sentences.
- Explain the risks associated with this recommendation.
- If all suppliers are high risk, clearly mention that no low-risk sourcing options are currently available.
- Explain the business impact in simple language.

3. RECOMMENDED_ACTION
- Write 1-2 complete sentences.
- Clearly state what the procurement team should do next.
- If alternate suppliers should be evaluated, mention that naturally.

Important:
- Use professional business English.
- Write complete sentences, not bullet points or short phrases.
- Do not repeat the same information across sections.
- Do not invent information that is not present in the recommendation.
- Return ONLY valid JSON.

Recommendation Data:

{json.dumps(recommendation, indent=2)}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a procurement analyst. "
                    "Always return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1

    )

    explanation = response.choices[0].message.content

    return json.loads(explanation)