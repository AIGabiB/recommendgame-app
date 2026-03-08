import streamlit as st
import pandas as pd

# -- Inställningar för sidan -- 
st.set_page_config(page_title="Steam Game Recommender", page_icon="🎮")

# -- Ladda data --  
@st.cache_data
def load_data():
    # Här laddar vi den sparade top-k DataFrame:n
    return pd.read_csv("steam_top_similarity_df.csv", index_col=0)

try:
    top_games_df = load_data()
except FileNotFoundError:
    st.error("Kunde inte hitta 'steam_top_similarity_df.pkl'")
    st.stop()

# -- Appens rubriker -- 
st.title("🎮 Steam Game Recommender")
st.markdown("Hitta nya spel baserat på vad andra Steam-användare gillar.")

# -- Användargränssnitt -- 
all_games = sorted(top_games_df.index.tolist())
selected_game = st.selectbox("Välj ett spel du gillar:", all_games)

num_recs = st.slider("Antal rekommendationer:", min_value=1, max_value=10, value=5)  # max = top_k

# -- Logiken --
if st.button("Visa liknande spel"):
    if selected_game in top_games_df.index:
        row = top_games_df.loc[selected_game]
        
        # Hämta spelnamn och likheter
        game_names = row[[f"top_{i+1}_game" for i in range(num_recs)]].tolist()
        game_scores = row[[f"top_{i+1}_sim" for i in range(num_recs)]].tolist()

        if game_names:
            st.subheader(f"Spel som liknar '{selected_game}':")
            
            # Skapa en snyggare presentation med progress bars
            for name, score in zip(game_names, game_scores):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{name}**")
                with col2:
                    st.write(f"{round(score * 100, 1)}% match")
                st.progress(float(score))
        else:
            st.warning("Hittade inga rekommendationer för detta spel.")
    else:
        st.error("Spelet hittades inte i databasen.")
