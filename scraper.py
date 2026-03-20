import requests
import pandas as pd
import time
import os

def scrape_movies(num_pages=10):
    """
    Scrape popular movies from TMDB (no API key needed for basic popular endpoint).
    Fetches title, genres, overview. Saves to data/movies.csv.
    """
    base_url = "https://api.themoviedb.org/3/movie/popular"
    movies = []

    for page in range(1, num_pages + 1):
        params = {'page': page}
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.status_code}")
            continue
        
        data = response.json()
        for movie in data['results']:
            title = movie['title']
            genres = ' '.join([g['name'] for g in movie.get('genres', [])])
            overview = movie.get('overview', '').lower()
            # Combine genres and overview for better TF-IDF
            features = f"{genres} {overview}"
            movies.append({'title': title, 'genres': genres, 'overview': overview, 'features': features})
        
        print(f"Fetched page {page}/{num_pages}")
        time.sleep(0.1)  # Rate limit courtesy
    
    # Create data dir if not exists
    os.makedirs('data', exist_ok=True)
    
    df = pd.DataFrame(movies)
    df.to_csv('data/movies.csv', index=False)
    print(f"Saved {len(df)} movies to data/movies.csv")
    return df

if __name__ == "__main__":
    scrape_movies()

