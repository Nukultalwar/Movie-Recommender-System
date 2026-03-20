import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class MovieRecommender:
    def __init__(self, csv_path='data/movies.csv'):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"{csv_path} not found. Run scraper first!")
        
        self.df = pd.read_csv(csv_path)
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['features'])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix)
        print(f"Loaded {len(self.df)} movies. Ready for recommendations.")
    
    def get_recommendations(self, title, top_k=10):
        """
        Get top_k similar movies to given title using cosine similarity on TF-IDF features.
        """
        if title not in self.df['title'].values:
            return pd.DataFrame(columns=self.df.columns)
        
        idx = self.df[self.df['title'] == title].index[0]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_k+1]  # exclude self
        
        movie_indices = [i[0] for i in sim_scores]
        recs = self.df.iloc[movie_indices].copy()
        recs['similarity'] = [i[1] for i in sim_scores]
        return recs[['title', 'genres', 'overview', 'similarity']].sort_values('similarity', ascending=False)

# Global instance for app
recommender = None

def init_recommender():
    global recommender
    recommender = MovieRecommender()

def get_recs(title, top_k=10):
    if recommender is None:
        init_recommender()
    return recommender.get_recommendations(title, top_k)

