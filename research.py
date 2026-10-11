import requests


URL = "https://api.openalex.org/works"

SEARCH_QUERIES = [
    "personalized machine learning",
    "personalized mood prediction",
    "mood and activity prediction",
    "daily energy and behavior prediction",
    "context-aware recommender systems",
    "behavior prediction using machine learning",
]


def reconstruct_abstract(abstract_index):
    """Reconstruct an abstract from OpenAlex's inverted index."""

    if not abstract_index:
        return None

    words = []

    for word, positions in abstract_index.items():
        for position in positions:
            words.append((position, word))

    words.sort(key=lambda item: item[0])

    return " ".join(word for position, word in words)


def collect_papers():
    """Search OpenAlex and collect unique papers."""

    all_papers = []
    seen_ids = set()

    for query in SEARCH_QUERIES:
        print(f"Searching: {query}")

        params = {
            "search": query,
            "per-page": 50,
        }

        response = requests.get(
            URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        for paper in data.get("results", []):
            paper_id = paper.get("id")

            if not paper_id or paper_id in seen_ids:
                continue

            seen_ids.add(paper_id)

            authors = []

            for author_info in paper.get("authorships", []):
                author = author_info.get("author", {})
                author_name = author.get("display_name")

                if author_name:
                    authors.append(author_name)

            paper_info = {
                "id": paper_id,
                "doi": paper.get("doi"),
                "title": paper.get("title"),
                "authors": authors,
                "year": paper.get("publication_year"),
                "type": paper.get("type"),
                "citations": paper.get("cited_by_count"),
                "abstract": reconstruct_abstract(
                    paper.get("abstract_inverted_index")
                ),
                "source": "OpenAlex",
            }

            all_papers.append(paper_info)

    print(f"\nTotal unique papers collected: {len(all_papers)}")

    return all_papers