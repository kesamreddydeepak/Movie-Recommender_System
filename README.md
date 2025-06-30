1.Movie Recommender System

This is a content-based Movie Recommender System built with Python, Streamlit, and TMDB API. It suggests similar movies based on the one you select, using a precomputed similarity matrix derived from movie metadata like genre, cast, keywords, and more.

🔧 Features

Clean and modern UI with hover animations

TMDB poster integration with fallback handling

Optimized with .pbz2 compressed files for fast loading

Deployable directly to Streamlit Cloud

📦 Tech Stack

Streamlit for interactive web UI

Pandas, NumPy, Scikit-learn for preprocessing and similarity

TMDB API for fetching movie posters

scipy.sparse + bz2 for memory-efficient model loading

🚀 To Run Locally

pip install -r requirements.txt
streamlit run app.py

📁 File Structure

app.py
model/
  ├── movie_list.pbz2
  └── similarity.pbz2


  after Executing the movies.ipynb in notebook you will be having 2 model files (similarity.pkl,movie_list.pkl) but those are of with 180 mb totally, which git can't offer.
  The .pbz2 format is simply a compressed version of .pkl using the bz2 algorithm. It helps reduce the file size while preserving full functionality.
  When your .pkl file is too large for GitHub or slow to load in Streamlit Cloud.
To optimize deployment performance by reducing memory usage and download time.



to convert into pbz2:

import pickle, bz2

def compress_pickle(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        data = pickle.load(f_in)
    with bz2.BZ2File(output_path, 'wb') as f_out:
        pickle.dump(data, f_out)


to load data:

import pickle, bz2

with bz2.BZ2File('model/similarity.pbz2', 'rb') as f:
    similarity = pickle.load(f)
