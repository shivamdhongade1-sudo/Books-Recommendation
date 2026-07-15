This is a **Book Recommendation System** built as a Streamlit web app. Here's what it does:

## Overview
It's a content-based recommender that suggests books similar to one a user has already read and liked, using a precomputed similarity matrix (likely built from book metadata/descriptions via something like cosine similarity on TF-IDF or count vectors).

## How it works

**1. Required data files**
- `cleaned_books.csv` — a catalogue of books with at least a `title` column
- `similarity.pkl` — a pickled square matrix where row *i* contains similarity scores between book *i* and every other book in the dataset

**2. Core components**
- **Data loading**: Uses `@st.cache_data` and `@st.cache_resource` decorators so the CSV and similarity matrix are only loaded once per session (performance optimization).
- **Title matching** (`get_index_from_title`): Normalizes book titles (lowercase, strips spaces/hyphens) to find a book's index even with minor formatting differences.
- **Recommendation engine** (`get_recommendations`): Given a book's index, sorts all other books by similarity score (descending) and returns the top 5 matches, excluding the book itself.

**3. User flow**
1. User sees a dropdown (`st.selectbox`) listing all available book titles.
2. They pick a book and click "Recommend."
3. The app looks up that book's index, retrieves its similarity row, and displays the top 5 most similar books with their similarity scores.

**4. Error handling**
- Checks that required files exist before running, with a clear error message if not.
- Wraps data loading in a try/except to surface any load failures gracefully.
- Handles the case where a selected book isn't found in the normalized index.

## Tech stack
- **Streamlit** — UI framework
- **Pandas** — data handling
- **Pickle** — loading the precomputed similarity matrix

This is a classic pattern for a book/movie/product recommender demo — the actual ML (computing the similarity matrix) happens offline beforehand; this app just serves the results interactively. Would you like me to review the code for bugs/improvements, or help you generate the missing `cleaned_books.csv` / `similarity.pkl` files?
