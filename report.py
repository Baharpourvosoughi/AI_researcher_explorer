import json
from pathlib import Path


OUTPUT_FOLDER = Path("output")


def save_papers(papers):
    """Save all collected papers as JSON."""

    OUTPUT_FOLDER.mkdir(exist_ok=True)

    file_path = OUTPUT_FOLDER / "papers.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            papers,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print(f"Paper data saved to: {file_path}")


def create_report(papers):
    """Create a readable research report."""

    OUTPUT_FOLDER.mkdir(exist_ok=True)

    file_path = OUTPUT_FOLDER / "research_report.md"

    with open(file_path, "w", encoding="utf-8") as file:

        file.write("# AI Research Explorer\n\n")

        file.write("## Research Overview\n\n")

        file.write(
            "This report collects academic works related to "
            "personalized machine learning, mood prediction, "
            "daily activity prediction, energy and behavior, "
            "and context-aware recommendation systems.\n\n"
        )

        file.write(
            f"Total unique records collected: {len(papers)}\n\n"
        )

        file.write(
            "> This is an initial literature collection. "
            "Relevance, research methods, results, and limitations "
            "must be checked before drawing conclusions.\n\n"
        )

        file.write("---\n\n")

        for number, paper in enumerate(papers, start=1):

            title = paper.get("title") or "Untitled"

            authors = paper.get("authors") or []
            authors_text = ", ".join(authors)

            year = paper.get("year") or "Unknown"
            paper_type = paper.get("type") or "Unknown"
            citations = paper.get("citations")

            if citations is None:
                citations = "Unknown"

            abstract = paper.get("abstract")

            if not abstract:
                abstract = "No abstract available in OpenAlex."

            file.write(f"## {number}. {title}\n\n")

            file.write(f"- **Authors:** {authors_text or 'Unknown'}\n")
            file.write(f"- **Year:** {year}\n")
            file.write(f"- **Type:** {paper_type}\n")
            file.write(f"- **Citations:** {citations}\n")
            file.write(f"- **Source:** {paper.get('source', 'Unknown')}\n")

            doi = paper.get("doi")

            if doi:
                file.write(f"- **DOI:** {doi}\n")

            file.write("\n### Abstract\n\n")
            file.write(f"{abstract}\n\n")

            file.write("---\n\n")

    print(f"Research report saved to: {file_path}")