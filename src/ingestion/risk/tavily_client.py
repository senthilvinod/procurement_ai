import os
from tavily import TavilyClient
from datetime import datetime, timedelta


class TavilyRiskClient:

    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


    # -----------------------------
    # Generic search function
    # -----------------------------
    def search(self, query: str, max_results: int = 3):
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            days= 10,

            include_answer=False,
            include_raw_content=True
        )

        results = []

        for r in response.get("results", []):
            results.append({
                "title": r.get("title"),
                "content": r.get("content"),
                "url": r.get("url"),
                "published_date": r.get("published_date") or r.get("date")
            })

        return results

    # -----------------------------
    # 1. Geopolitical news
    # -----------------------------
    def get_geopolitical_news(self, location: str, company: str):
        query = f"Find recent geopolitical news affecting {company} in {location}. Focus on political tensions, government policies, trade restrictions, sanctions, diplomatic conflicts, military developments, and regulatory changes that may impact business operations or supply chains. Return only relevant news with title, date, source, and summary"
        return self.search(query)

    # -----------------------------
    # 2. Operational news
    # -----------------------------
    def get_operational_news(self, location: str, company: str):
        query = f"Find recent logistics disruption events affecting {company} in {location}. Focus only on actual incidents in the last 30 days: factory shutdowns, production delays, shipping disruptions, supplier failures, material shortages, utility outages, and natural disasters. Return title, date, source, and summary only. Exclude reports, studies, historical analysis"
        return self.search(query)

    # -----------------------------
    # 3. Financial news
    # -----------------------------
    def get_financial_news(self, company: str):
        query = f"Find recent financial analysis and reports for {company} related to operational financial strength. Focus on liquidity, cash flow, debt, capital expenditure, profitability, capacity investment and financial indicators affecting production continuity. Return only financial data, analysis, and reports with title, date, source, and summary. Exclude stock price, valuation, and investment advice."
        return self.search(query)

    # -----------------------------
    # MASTER FUNCTION
    # -----------------------------
    def fetch_all_news(self, company: str, location: str):

        geo_news = self.get_geopolitical_news(location, company)
        ops_news = self.get_operational_news(location, company)
        fin_news = self.get_financial_news(company)


        return {
            "geopolitical_news": geo_news,
            "operational_news": ops_news,
            "financial_news": fin_news
        }