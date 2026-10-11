import json
import re
from pathlib import Path

import pandas as pd


# --------------------
# Configuration
# --------------------

PAPERS_FILE = Path("output/papers.json")
ANALYSIS_FILE = Path("output/paper_analysis.json")

KEYWORD_GROUPS = {
    "Machine learning": r"\bmachine learning\b",
    "Deep learning": r"\bdeep learning\b",
    "NLP": r"\b(nlp|natural language processing)\b",
    "Transformers": r"\b(transformers?|bert|roberta)\b",
    "LLMs": r"\b(llms?|large language models?|gpt-\d*)\b",
    "Speech and audio": r"\b(speech|voice|audio|acoustic)\b",
    "Social media": r"\b(social media|twitter|reddit)\b",
    "EEG": r"\beeg\b",
}

METHOD_KEYWORDS = [
    "Random Forest",
    "Support Vector Machine",
    "SVM",
    "Logistic Regression",
    "Linear Regression",
    "Decision Tree",
    "XGBoost",
    "Gradient Boosting",
    "K-Nearest Neighbors",
    "KNN",
    "Naive Bayes",
    "Neural Network",
    "Convolutional Neural Network",
    "CNN",
    "Recurrent Neural Network",
    "RNN",
    "LSTM",
    "GRU",
    "Transformer",
    "BERT",
]

DATASET_KEYWORDS = [
    "wearable",
    "smartphone",
    "sensor data",
    "social media data",
    "electronic health records",
    "survey data",
    "self-reported",
    "self-report",
    "longitudinal data",
    "public dataset",
    "publicly available dataset",
]

INPUT_KEYWORDS = [
    "mood",
    "emotion",
    "energy",
    "sleep",
    "physical activity",
    "heart rate",
    "steps",
    "location",
    "context",
    "wearable data",
    "sensor data",
    "self-report",
]

TARGET_KEYWORDS = [
    "mood prediction",
    "depression prediction",
    "emotion recognition",
    "activity prediction",
    "behavior prediction",
    "mental health prediction",
    "stress prediction",
    "energy prediction",
    "daily activity",
]

METRIC_KEYWORDS = [
    "accuracy",
    "precision",
    "recall",
    "f1-score",
    "f1 score",
    "auc",
    "area under the curve",
    "mean squared error",
    "root mean squared error",
    "mae",
    "mean absolute error",
]


# --------------------
# Helper functions
# --------------------

def is_missing(value):
    """Check whether a scalar value is missing, including pandas NaN."""

    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def clean_json_value(value):
    """Convert missing and NumPy/pandas scalar values to JSON-safe values."""

    if is_missing(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


# --------------------
# Load and prepare data
# --------------------

def load_papers(file_path):
    """Load paper records from a JSON file."""

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict):
        data = data.get("papers", [])

    if not isinstance(data, list):
        raise ValueError("papers.json must contain a list of papers.")

    if not all(isinstance(paper, dict) for paper in data):
        raise ValueError("Each item in papers.json must be a paper object.")

    return pd.DataFrame(data)


def prepare_data(df):
    """Prepare the columns used in the analysis."""

    required_columns = [
        "id",
        "title",
        "year",
        "citations",
        "abstract",
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce",
    )

    df["citations"] = pd.to_numeric(
        df["citations"],
        errors="coerce",
    )

    df["abstract"] = (
        df["abstract"]
        .fillna("")
        .astype(str)
    )

    return df


# --------------------
# Basic statistics
# --------------------

def get_summary(df):
    """Calculate basic statistics for the collected papers."""

    years = df["year"].dropna()
    citations = df["citations"].dropna()

    return {
        "paper_count": len(df),
        "citation_mean": (
            float(citations.mean())
            if not citations.empty
            else None
        ),
        "citation_median": (
            float(citations.median())
            if not citations.empty
            else None
        ),
        "first_year": (
            int(years.min())
            if not years.empty
            else None
        ),
        "last_year": (
            int(years.max())
            if not years.empty
            else None
        ),
    }


def get_top_cited_papers(df, limit=10):
    """Return the papers with the highest citation counts."""

    columns = [
        "title",
        "year",
        "citations",
    ]

    return (
        df.dropna(subset=["citations"])
        .sort_values(
            "citations",
            ascending=False,
        )
        .head(limit)[columns]
    )


def get_yearly_publications(df):
    """Count the number of papers published each year."""

    yearly = (
        df.dropna(subset=["year"])
        .groupby("year")
        .size()
        .reset_index(name="paper_count")
        .sort_values("year")
    )

    if not yearly.empty:
        yearly["year"] = yearly["year"].astype(int)

    return yearly


# --------------------
# Keyword analysis
# --------------------

def find_keywords(text, keywords):
    """Find which keywords from a list appear in a text."""

    if is_missing(text):
        text = ""
    elif not isinstance(text, str):
        text = str(text)

    found = []

    for keyword in keywords:
        pattern = (
            r"(?<!\w)"
            + re.escape(keyword)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            found.append(keyword)

    return found


def count_keyword_mentions(df):
    """Count abstracts mentioning each keyword group."""

    results = []

    for category, pattern in KEYWORD_GROUPS.items():
        count = df["abstract"].str.contains(
            pattern,
            case=False,
            regex=True,
            na=False,
        ).sum()

        results.append({
            "category": category,
            "papers_mentioned": int(count),
        })

    return (
        pd.DataFrame(results)
        .sort_values(
            "papers_mentioned",
            ascending=False,
        )
        .reset_index(drop=True)
    )


# --------------------
# Scientific content analysis
# --------------------

def analyze_paper(paper):
    """
    Extract preliminary scientific clues from an abstract.

    These are keyword-based findings, not verified scientific conclusions.
    """

    raw_abstract = paper.get("abstract")

    if is_missing(raw_abstract):
        abstract = ""
    elif isinstance(raw_abstract, str):
        abstract = raw_abstract
    else:
        abstract = str(raw_abstract)

    paper_id = clean_json_value(paper.get("id"))
    title = clean_json_value(paper.get("title"))
    year = clean_json_value(paper.get("year"))

    if year is not None:
        try:
            year_number = float(year)

            if year_number.is_integer():
                year = int(year_number)
            else:
                year = year_number
        except (TypeError, ValueError, OverflowError):
            year = None

    methods = find_keywords(
        abstract,
        METHOD_KEYWORDS,
    )

    datasets = find_keywords(
        abstract,
        DATASET_KEYWORDS,
    )

    possible_inputs = find_keywords(
        abstract,
        INPUT_KEYWORDS,
    )

    possible_targets = find_keywords(
        abstract,
        TARGET_KEYWORDS,
    )

    metrics = find_keywords(
        abstract,
        METRIC_KEYWORDS,
    )

    personalization_terms = find_keywords(
        abstract,
        [
            "personalized",
            "personalised",
            "individualized",
            "individualised",
            "person-specific",
            "personalization",
            "personalisation",
        ],
    )

    if not abstract.strip():
        analysis_status = "No abstract available"
    else:
        analysis_status = "Preliminary keyword analysis"

    return {
        "paper_id": paper_id,
        "title": title,
        "year": year,
        "research_question": None,
        "methods_mentioned": methods,
        "dataset_clues": datasets,
        "possible_input_variables": possible_inputs,
        "possible_target_variables": possible_targets,
        "personalization_terms": personalization_terms,
        "evaluation_metrics_mentioned": metrics,
        "main_results": None,
        "limitations": None,
        "analysis_status": analysis_status,
        "note": (
            "Findings are based on abstract keyword matching. "
            "They do not confirm the actual methods, variables, "
            "results, or limitations of the study."
        ),
    }


def analyze_all_papers(df):
    """Analyze the abstracts of all collected papers."""

    analyses = []

    for _, row in df.iterrows():
        paper = row.to_dict()
        analysis = analyze_paper(paper)
        analyses.append(analysis)

    return analyses


# --------------------
# Save analysis
# --------------------

def save_analysis(analyses):
    """Save analysis records as a JSON file."""

    ANALYSIS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ANALYSIS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            analyses,
            file,
            ensure_ascii=False,
            indent=4,
            allow_nan=False,
        )

    print(f"\nScientific analysis saved to: {ANALYSIS_FILE}")


# --------------------
# Main program
# --------------------

def main():
    if not PAPERS_FILE.exists():
        print(f"Paper file not found: {PAPERS_FILE}")
        print("Run main.py first to collect papers.")
        return

    df = load_papers(PAPERS_FILE)
    df = prepare_data(df)

    if df.empty:
        print("No papers found in papers.json.")
        return

    # Basic statistics
    summary = get_summary(df)

    print("\n=== Overall Summary ===")
    print(f"Number of papers: {summary['paper_count']}")

    if summary["citation_mean"] is not None:
        print(
            f"Mean citations: "
            f"{summary['citation_mean']:.2f}"
        )
        print(
            f"Median citations: "
            f"{summary['citation_median']:.2f}"
        )
    else:
        print("Citation information is unavailable.")

    if summary["first_year"] is not None:
        print(
            f"Publication years: "
            f"{summary['first_year']}–{summary['last_year']}"
        )
    else:
        print("Publication years are unavailable.")

    # Most cited papers
    print("\n=== Top 10 Most Cited Papers ===")

    top_papers = get_top_cited_papers(df)

    if top_papers.empty:
        print("Citation information is unavailable.")
    else:
        print(top_papers.to_string(index=False))

    # Publications by year
    print("\n=== Publications by Year ===")

    yearly = get_yearly_publications(df)

    if yearly.empty:
        print("Publication year information is unavailable.")
    else:
        print(yearly.to_string(index=False))

    # Keyword groups
    print("\n=== Keyword Mentions in Abstracts ===")

    keyword_results = count_keyword_mentions(df)
    print(keyword_results.to_string(index=False))

    # Scientific content analysis
    print("\n=== Scientific Content Analysis ===")

    analyses = analyze_all_papers(df)

    for analysis in analyses[:5]:
        print(f"\nTitle: {analysis['title']}")
        print(f"Methods mentioned: {analysis['methods_mentioned']}")
        print(f"Dataset clues: {analysis['dataset_clues']}")
        print(
            "Possible inputs: "
            f"{analysis['possible_input_variables']}"
        )
        print(
            "Possible targets: "
            f"{analysis['possible_target_variables']}"
        )
        print(
            "Evaluation metrics: "
            f"{analysis['evaluation_metrics_mentioned']}"
        )
        print(
            "Personalization terms: "
            f"{analysis['personalization_terms']}"
        )

    save_analysis(analyses)

    print("\nAnalysis completed.")


if __name__ == "__main__":
    main()
