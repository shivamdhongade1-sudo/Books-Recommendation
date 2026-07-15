"""
Book Recommender System
------------------------
A Streamlit application that recommends similar books based on a
precomputed similarity matrix.

Required files (same directory as this script):
    - cleaned_books.csv : must contain a 'title' column
    - similarity.pkl    : a square similarity matrix (list/ndarray),
                           where row i holds similarity scores for book i
                           against every other book in the dataframe.
"""

from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
DATA_PATH = Path("cleaned_books.csv")
SIMILARITY_PATH = Path("similarity.pkl")
NUM_RECOMMENDATIONS = 5

st.set_page_config(
    page_title="Book Recommender",
    page_icon="📚",
    layout="centered",
)


# --------------------------------------------------------------------------- #
# Data loading (cached so files are read only once per session)
# --------------------------------------------------------------------------- #
@st.cache_data(show_spinner="Loading book catalogue...")
def load_books(path: Path) -> pd.DataFrame:
    """Load the book catalogue from CSV."""
    df = pd.read_csv(path)
    if "title" not in df.columns:
        raise ValueError("Expected a 'title' column in cleaned_books.csv")
    df = df.reset_index(drop=True)
    return df


@st.cache_resource(show_spinner="Loading similarity matrix...")
def load_similarity_matrix(path: Path):
    """Load the precomputed similarity matrix."""
    with open(path, "rb") as file:
        return pickle.load(file)


def get_index_from_title(df: pd.DataFrame, title: str) -> int:
    """Return the dataframe index matching a (normalized) book title, or -1."""
    normalized_target = title.strip().lower().replace(" ", "").replace("-", "")
    normalized_titles = (
        df["title"].astype(str).str.lower().str.replace(" ", "").str.replace("-", "")
    )
    matches = df.index[normalized_titles == normalized_target]
    return int(matches[0]) if len(matches) else -1


def get_title_from_index(df: pd.DataFrame, index: int) -> str:
    """Return the book title for a given dataframe index."""
    if 0 <= index < len(df):
        return str(df.loc[index, "title"])
    return ""


def get_recommendations(
    df: pd.DataFrame, similarities, book_index: int, n: int = NUM_RECOMMENDATIONS
) -> list[tuple[str, float]]:
    """
    Return the top-n most similar books (title, score) for a given book index,
    excluding the book itself.
    """
    scored = list(enumerate(similarities[book_index]))
    scored.sort(key=lambda pair: pair[1], reverse=True)

    recommendations = []
    for idx, score in scored:
        if idx == book_index:
            continue
        title = get_title_from_index(df, idx)
        if title:
            recommendations.append((title, score))
        if len(recommendations) == n:
            break
    return recommendations


# --------------------------------------------------------------------------- #
# App
# --------------------------------------------------------------------------- #
def main() -> None:
    st.title("📚 Book Recommender System")
    st.caption("Select a book you've enjoyed and get similar recommendations.")

    # Guard against missing data files with a clear, actionable error message.
    missing = [p for p in (DATA_PATH, SIMILARITY_PATH) if not p.exists()]
    if missing:
        st.error(
            "Missing required file(s): "
            + ", ".join(str(p) for p in missing)
            + ". Please make sure they are in the same directory as app.py."
        )
        st.stop()

    try:
        df = load_books(DATA_PATH)
        similarities = load_similarity_matrix(SIMILARITY_PATH)
    except Exception as exc:  # noqa: BLE001 - surface any load error to the user
        st.error(f"Failed to load data: {exc}")
        st.stop()

    books = df["title"].dropna().tolist()
    selected_book = st.selectbox("Select a book you've read", books)

    if st.button("Recommend", type="primary"):
        book_index = get_index_from_title(df, selected_book)

        if book_index == -1:
            st.warning("Book not found. Please check the spelling and try again.")
            return

        recommendations = get_recommendations(df, similarities, book_index)

        if not recommendations:
            st.info("No recommendations could be found for this book.")
            return

        st.subheader(f"Because you read '{selected_book}':")
        for rank, (title, score) in enumerate(recommendations, start=1):
            st.write(f"**{rank}. {title}**  \nSimilarity score: {score:.3f}")


if __name__ == "__main__":
    main()