from research import collect_papers
from report import save_papers, create_report


def main():
    print("=" * 50)
    print("AI Research Explorer")
    print("=" * 50)

    print("\nStarting literature collection...\n")

    try:
        papers = collect_papers()

    except Exception as error:
        print("\nAn error occurred while collecting papers.")
        print(f"Error: {error}")
        return

    if not papers:
        print("No papers were collected.")
        return

    save_papers(papers)

    create_report(papers)

    print("\nProject completed successfully!")
    print("Check the output folder for the results.")


if __name__ == "__main__":
    main()