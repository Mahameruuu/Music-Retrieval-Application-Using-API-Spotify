import streamlit as st
import pandas as pd
from model import getToken, getPlaylistItems

def main():
    st.title("Music Retrieval Application")

    st.write("""
    ## Instructions:
    - Enter your Spotify API credentials (Client ID and Client Secret)
    - Enter the Playlist ID you want to analyze
    - Click on "Get Data" to fetch the playlist and analyze it
    """)

    client_id = st.text_input("Client ID", '')
    client_secret = st.text_input("Client Secret", '', type="password")
    playlist_id = st.text_input("Playlist ID", '')

    if st.button("Get Data"):
        token = getToken(client_id, client_secret)
        st.write(f"Access token: {token}")
        getPlaylistItems(token, playlist_id)
        
        st.write("### Playlist Data")
        data = pd.read_csv('dataset.csv')
        data['artist'] = data['artist'].map(lambda x: str(x)[2:-1])
        data['name'] = data['name'].map(lambda x: str(x)[2:-1])
        data = data[data['name'] != '']
        data = data.reset_index(drop=True)
        
        st.dataframe(data)

        search_query = st.text_input("Search for a song or artist", '')
        if search_query:
            search_results = data[
                data.apply(lambda row: search_query.lower() in row['name'].lower() or search_query.lower() in row['artist'].lower(), axis=1)
            ]
            st.write(f"### Search Results for '{search_query}'")
            st.dataframe(search_results)

if __name__ == "__main__":
    main()
