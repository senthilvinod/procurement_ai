import os
import json
from groq import Groq
from dotenv import load_dotenv


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


RISK_PROMPT = """
You are a Supply Chain Risk Analyst.

Assess the supplier's CURRENT delivery continuity risk based ONLY on the provided news.

Ignore news about stock price, revenue, profit, valuation, reputation, market share and investor sentiment unless they directly affect production or deliveries.

Evaluate only these risk categories:

1. Logistics (0.60)
- Factory shutdown
- Production interruption
- Capacity reduction
- Material shortage
- Utility shortage
- Shipment delay
- Transport or port disruption

2. Geopolitical (0.30)
- Export restrictions
- Trade sanctions
- Border closures
- Government restrictions
- Shipping route disruption

Do NOT increase geopolitical risk for political statements, military exercises or diplomatic tensions unless they currently affect production or deliveries.

3. Financial (0.10)
- Liquidity crisis
- Bankruptcy
- Debt affecting production
- Inability to procure materials

For every relevant event determine:

- Category
- Status: ACTIVE | ONGOING | EMERGING | HISTORICAL | RESOLVED
- Impact: DIRECT | INDIRECT

Before assigning any score answer:

"Does this event CURRENTLY reduce the supplier's ability to manufacture or deliver products?"

Rules:

YES → Score according to severity.

UNCERTAIN → Treat as Emerging Risk.

NO → Treat as Exposure only.

Exposure is NOT disruption.

Scoring Rules:

• ACTIVE and ONGOING events dominate.
• EMERGING events moderately increase risk.
• HISTORICAL events count only if effects continue.
• RESOLVED events contribute nothing.
• If operations are normal, the score should generally remain below 0.3.
• Scores above 0.6 require confirmed production disruption, shipment delays, export restrictions or capacity reduction.

Whenever possible, distinguish between:
Supplier-specific risk
Industry-wide risk
Regional risk
Do not assume an industry event directly impacts the supplier unless evidence supports it.

Risk Scale

0.0 : No Risk
0.1-0.2 : Normal
0.2-0.4 : Low
0.4-0.6 : Moderate
0.6-0.8 : High
0.8-1.0 : Critical

Current Status:
Normal
Watchlist
Potential Disruption
Active Disruption
Critical Disruption

Estimate confidence (0-1) based on:
- source reliability
- number of independent sources
- recency
- agreement between sources

Return ONLY valid JSON.

{
  "supplier":"",
  "confidence":{"score":0.0,"reason":""},
  "risk_breakdown":{
    "logistics_risk":{"score":0.0,"impact":"","evidence":[]},
    "geopolitical_risk":{"score":0.0,"impact":"","evidence":[]},
    "financial_risk":{"score":0.0,"impact":"","evidence":[]}
  },
  "overall_assessment":"",
  "current_status":"",
  "recommended_action":""
}
"""


def analyze_risk(
        supplier_name,
        news_data
):

    # Convert Tavily response into readable text

    news_text = json.dumps(
        news_data,
        indent=2
    )


    user_prompt = f"""

Supplier:
{supplier_name}


Tavily News:

{news_text}


Analyze the delivery continuity risk.

"""


    response = client.chat.completions.create(

        model="qwen/qwen3-32b",

        temperature=0,

        response_format={
            "type":"json_object"
        },

        messages=[

            {
                "role":"system",
                "content":RISK_PROMPT
            },

            {
                "role":"user",
                "content":user_prompt
            }

        ]
    )


    return json.loads(
        response.choices[0].message.content
    )