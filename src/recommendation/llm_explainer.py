from groq import Groq
import os
import json


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



def generate_explanation(recommendation):

    """
    Generates human-readable procurement explanation
    using Groq LLM.

    The LLM only explains the recommendation.
    It does not make decisions.
    """


    prompt = f"""

You are an expert supply chain procurement analyst.

Analyze the supplier recommendation below.

Generate a concise procurement explanation covering:

1. Inventory situation
2. Recommended supplier justification
3. Supplier risk analysis
4. Procurement action recommendation


Important rules:
- Do not change the recommended supplier.
- Do not suggest another supplier.
- Use only the provided information.
- Clearly highlight risks.
- Write for procurement managers.


Recommendation Data:

{json.dumps(recommendation, indent=2)}


Generate the explanation.

"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content":
                "You are a supply chain risk and procurement expert."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.2

    )


    return response.choices[0].message.content