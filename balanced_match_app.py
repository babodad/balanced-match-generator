
import streamlit as st
import pandas as pd
from itertools import combinations
import random

st.title("Balanced Match Generator")

players_input = st.text_input("Spielerliste (kommagetrennt)", "")
decks_input = st.text_input("Deckliste (kommagetrennt)", "")

if st.button("Turnierplan generieren"):
    players = [p.strip() for p in players_input.split(",") if p.strip()]
    decks = [d.strip() for d in decks_input.split(",") if d.strip()]

    if len(players) < 2 or len(decks) < 2:
        st.warning("Bitte mindestens 2 Spieler und 2 Decks angeben.")
    else:
        pairings = list(combinations(players, 2)) * 2  # Double round robin
        random.shuffle(pairings)
        deck_combos = [(d1, d2) for d1 in decks for d2 in decks if d1 != d2]

        deck_usage = {d: 0 for d in decks}
        player_decks = {p: set() for p in players}
        used_combos = set()
        result = []

        for i, (p1, p2) in enumerate(pairings, 1):
            assigned = False
            random.shuffle(deck_combos)
            for d1, d2 in deck_combos:
                key = f"{p1}-{p2}-{d1}-{d2}"
                if (
                    d1 not in player_decks[p1]
                    and d2 not in player_decks[p2]
                    and deck_usage[d1] < 4
                    and deck_usage[d2] < 4
                    and key not in used_combos
                ):
                    result.append({
                        "Runde": i,
                        "Spieler 1": p1,
                        "Deck 1": d1,
                        "Spieler 2": p2,
                        "Deck 2": d2
                    })
                    player_decks[p1].add(d1)
                    player_decks[p2].add(d2)
                    deck_usage[d1] += 1
                    deck_usage[d2] += 1
                    used_combos.add(key)
                    assigned = True
                    break
            if not assigned:
                result.append({
                    "Runde": i,
                    "Spieler 1": p1,
                    "Deck 1": "X",
                    "Spieler 2": p2,
                    "Deck 2": "X",
                    "Kommentar": "Nicht zuweisbar"
                })

        df = pd.DataFrame(result)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("CSV herunterladen", csv, "turnierplan.csv", "text/csv")

        st.success("Turnierplan fertig!")
