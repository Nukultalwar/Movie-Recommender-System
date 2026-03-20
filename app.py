import streamlit as st
import pandas as pd
from recommender import get_recs

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")
st.markdown("Enter a movie title to get similar movie recommendations based on cosine similarity of descriptions and genres.")

# Lazy init recommender
@st.cache_data
def load_data():
    from recommender import init_recommender
    init_recommender()
    return pd.read_csv('data/movies.csv')['title'].tolist()

movie_list = load_data()

col1, col2 = st.columns([1, 3])

with col1:
    selected_movie = st.selectbox(
        "Select a movie:",
        movie_list,
        help="Choose from scraped popular movies."
    )

with col2:
    top_k = st.slider("Number of recommendations", 5, 20, 10)

if st.button("Get Recommendations", type="primary"):
    with st.spinner("Computing recommendations..."):
        recs = get_recs(selected_movie, top_k)
    
    if recs.empty:
        st.error("Movie not found. Try another.")
    else:
        st.success(f"Top {len(recs)} similar movies to **{selected_movie}**:")
        
        for _, row in recs.iterrows():
            with st.expander(f"🎥 {row['title']} (sim: {row['similarity']:.3f})"):
                st.write(f"**Genres:** {row['genres']}")
                st.write(f"**Overview:** {row['overview'][:300]}...")
        
        st.metric("Total Movies in Dataset", len(pd.read_csv('data/movies.csv')))

st.markdown("---")
st.markdown("**Built with:** Python, scikit-learn (TF-IDF + Cosine Sim), Streamlit, TMDB data.")

