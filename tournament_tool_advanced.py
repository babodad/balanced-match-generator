
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Magic Turnierplaner – Multimodus")

# Spielermodi definieren
spielmodi = {
    "2 Spieler – 5 Decks": {"spieler": 2, "decks": 5},
    "3 Spieler – 2 Decks": {"spieler": 3, "decks": 2},
    "3 Spieler – 3 Decks": {"spieler": 3, "decks": 3},
    "3 Spieler – 4 Decks": {"spieler": 3, "decks": 4},
    "4 Spieler – 4 Decks": {"spieler": 4, "decks": 4},
    "4 Spieler – 6 Decks": {"spieler": 4, "decks": 6},
}

modus = st.selectbox("Turniermodus wählen:", list(spielmodi.keys()))
spieleranzahl = spielmodi[modus]["spieler"]
deckanzahl = spielmodi[modus]["decks"]

spieler_input = st.text_input(f"{spieleranzahl} Spieler (kommagetrennt)", ", ".join([f"Spieler{i+1}" for i in range(spieleranzahl)]))
deck_input = st.text_input(f"{deckanzahl} Decks (kommagetrennt)", ", ".join([f"Deck{i+1}" for i in range(deckanzahl)]))

rueckrunde_option = st.checkbox("Dynamische Rückrunde aktivieren")

if st.button("Turnierplan generieren"):
    players = [p.strip() for p in spieler_input.split(",") if p.strip()]
    decks = [d.strip() for d in deck_input.split(",") if d.strip()]

    result = []
    punkte_spieler = {p: 0 for p in players}
    punkte_decks = {d: 0 for d in decks}

    runden = min(len(decks), 10)
    for i in range(runden):
        spieler1 = players[i % len(players)]
        spieler2 = players[(i + 1) % len(players)]
        deck1 = decks[i % len(decks)]
        deck2 = decks[(i + 1) % len(decks)]

        gewinner = spieler1 if i % 2 == 0 else spieler2
        gewinner_deck = deck1 if gewinner == spieler1 else deck2

        punkte_spieler[gewinner] += 1
        punkte_decks[gewinner_deck] += 1

        result.append({
            "Runde": i + 1,
            "Spieler 1": spieler1,
            "Deck 1": deck1,
            "Spieler 2": spieler2,
            "Deck 2": deck2,
            "Gewinner": gewinner,
            "Deck des Gewinners": gewinner_deck
        })

    if rueckrunde_option:
        st.subheader("Rückrunde (dynamisch)")
        for i in range(runden):
            spieler1 = players[i % len(players)]
            spieler2 = players[(i + 2) % len(players)]
            sorted_decks = sorted(decks, key=lambda d: punkte_decks[d])
            sorted_players = sorted([spieler1, spieler2], key=lambda p: punkte_spieler[p])
            deck1 = sorted_decks[-1]
            deck2 = sorted_decks[0]
            spieler1, spieler2 = sorted_players[0], sorted_players[1]

            gewinner = spieler1 if i % 2 == 1 else spieler2
            gewinner_deck = deck1 if gewinner == spieler1 else deck2

            punkte_spieler[gewinner] += 1
            punkte_decks[gewinner_deck] += 1

            result.append({
                "Runde": runden + i + 1,
                "Spieler 1": spieler1,
                "Deck 1": deck1,
                "Spieler 2": spieler2,
                "Deck 2": deck2,
                "Gewinner": gewinner,
                "Deck des Gewinners": gewinner_deck
            })

    df = pd.DataFrame(result)
    st.dataframe(df, use_container_width=True)

    st.subheader("Punkte Spieler")
    df_spieler = pd.DataFrame(punkte_spieler.items(), columns=["Spieler", "Punkte"]).sort_values("Punkte", ascending=False)
    st.dataframe(df_spieler)

    st.subheader("Punkte Decks")
    df_decks = pd.DataFrame(punkte_decks.items(), columns=["Deck", "Punkte"]).sort_values("Punkte", ascending=False)
    st.dataframe(df_decks)

    # Diagramm Spielerpunkte
    st.subheader("Visualisierung – Spielerpunkte")
    fig1, ax1 = plt.subplots()
    ax1.bar(df_spieler["Spieler"], df_spieler["Punkte"], color="skyblue")
    ax1.set_ylabel("Punkte")
    ax1.set_title("Spielerwertung")
    st.pyplot(fig1)

    # Diagramm Deckpunkte
    st.subheader("Visualisierung – Deckpunkte")
    fig2, ax2 = plt.subplots()
    ax2.bar(df_decks["Deck"], df_decks["Punkte"], color="lightgreen")
    ax2.set_ylabel("Punkte")
    ax2.set_title("Deckwertung")
    st.pyplot(fig2)

    # CSV Export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("CSV herunterladen", csv, "turnierplan.csv", "text/csv")

    st.success("Turnierplan, Punktetracking und Auswertung erstellt.")
