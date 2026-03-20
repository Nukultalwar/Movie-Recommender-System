# Movie Recommender System

Developed using Python, machine learning (cosine similarity on TF-IDF), web scraping (TMDB), Streamlit UI.

## Features
- Scrapes ~400 popular movies from TMDB (title, genres, overview).
- Recommends similar movies based on plot/genre similarity.
- Interactive Streamlit web app.

## Quick Start
1. Create virtual env:
   ```
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```

2. Install deps:
   ```
   pip install -r requirements.txt
   ```

3. Fetch movie data:
   ```
   python run_scraper.py
   ```
   (Creates `data/movies.csv`)

4. Run app:
   ```
   streamlit run app.py
   ```
   Open http://localhost:8501

## Files
- `scraper.py`: TMDB data collection.
- `recommender.py`: TF-IDF + cosine similarity logic.
- `app.py`: Streamlit interface.
- `run_scraper.py`: One-click data fetch.

## Update Data
Edit `num_pages=20` in `run_scraper.py` for more movies, rerun.

**Note:** TMDB rate limits; scraper sleeps between requests.

