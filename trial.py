from tavily import TavilyClient

client = TavilyClient(api_key="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")

def get_news(query):

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        days= 10,
        include_raw_content=True,
        include_answer=False
    )

    results = []

    for r in response["results"]:
        results.append({
            "title": r["title"],
            "content": r["content"],
            "url": r["url"]
        })

    return results


news = get_news("Analyze the financial capability of TSMC in taiwan. Retrieve recent financial analysis covering cash position, profitability, cash flow, debt, capital expenditure, production investments, capacity expansion, cost pressures, and operational sustainability. Return source, date, and summary. Exclude stock price, valuation, and investment recommendations.")
for n in news:
    print("\n---")
    print(n["title"])
    print(n["content"])