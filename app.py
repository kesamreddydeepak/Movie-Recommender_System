import pickle
import streamlit as st
import requests

# Page setup
st.set_page_config(layout="wide", page_title="🎬 Movie Recommender")

# Custom CSS for modern UI
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
        color: #fff;
        font-family: 'Segoe UI', sans-serif;
    }

    .movie-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 20px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        padding: 12px;
    }

    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(255, 204, 0, 0.3);
    }

    .movie-title {
        font-size: 17px;
        font-weight: 600;
        margin-top: 10px;
        color: #ffcc00;
    }

    .recommend-btn {
        background-color: transparent;
        color: #ff4c4c;
        border: 2px solid #ff4c4c;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .recommend-btn:hover {
        background-color: #ff4c4c;
        color: white;
        transform: scale(1.05);
    }

    .dropdown-label {
        font-weight: bold;
        font-size: 16px;
        color: #d1d1d1;
    }

    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #ffcc00;'>🎥 Movie Recommender System</h1>", unsafe_allow_html=True)

# Load model
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("🎬 Type or select a movie from the dropdown", movie_list)

# Poster fetch function
def fetch_poster(movie_id):
    placeholder_url = "https://via.placeholder.com/500x750?text=No+Poster"
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c3d88fe12280ff0f00b4d4ea2b671ced&language=en-US"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return placeholder_url
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return placeholder_url
    except Exception as e:
        return placeholder_url

# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Button and layout
if st.button("🎯 Show Recommendations", key="recommend", use_container_width=True):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{posters[i]}" style="width:100%; border-radius:16px;"
                     onerror="this.onerror=null; this.src='https://via.placeholder.com/500x750?text=No+Poster';">
                <div class="movie-title">{names[i]}</div>
            </div>
            """, unsafe_allow_html=True)
