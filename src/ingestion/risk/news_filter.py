MAX_SUMMARY_LENGTH = 400
def filter_news(news):

    filtered = {}

    for category, articles in news.items():

        filtered[category] = []

        seen_titles = set()

        for article in articles:

            title = article.get("title", "").strip()

            if title.lower() in seen_titles:
                continue

            seen_titles.add(title.lower())

            filtered[category].append({

                "title": title,

                "summary": article.get("content","")[:MAX_SUMMARY_LENGTH],

                "date": article.get("published_date")

            })

    return filtered