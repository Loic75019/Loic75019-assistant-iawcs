import os

from pathlib import Path



import streamlit as st

from agent import PersonalAIAgent

from langchain_community.callbacks.streamlit import StreamlitCallbackHandler



st.set_page_config(page_title="Agent IA Personnel", page_icon="🤖")

st.title("🤖 Agent IA Personnel")



# === INITIALISATION DE L'AGENT ===

if "agent" not in st.session_state:

    st.session_state.agent = PersonalAIAgent()

    st.session_state.messages = []

    st.session_state.context_info = {}  # pour stocker prénom, etc.



agent = st.session_state.agent



# === BOUTON DE RÉINITIALISATION ===

if st.button("🧹 Réinitialiser la mémoire"):

    agent.clear_memory()

    st.session_state.messages = []

    st.session_state.context_info = {}

    st.success("Mémoire et historique réinitialisés.")



# === SECTION PDF ===

st.subheader("📄 Analyse de document PDF")



uploaded_file = st.file_uploader("Choisissez un PDF à analyser", type=["pdf"])



if uploaded_file is not None:

    # Crée le dossier si nécessaire

    os.makedirs("uploaded_pdfs", exist_ok=True)



    # Sauvegarde locale et conversion en chemin POSIX

    temp_path = os.path.join("uploaded_pdfs", uploaded_file.name)

    with open(temp_path, "wb") as f:

        f.write(uploaded_file.getbuffer())



    # Résolution en POSIX pour éviter les problèmes de backslashes

    abs_path = Path(temp_path).resolve().as_posix()



    st.success(f"✅ Fichier '{uploaded_file.name}' chargé avec succès.")



    user_question = st.text_input("Posez une question sur le document (laissez vide pour un résumé général)")



    if st.button("Analyser le PDF"):

        # Construis la requête en incluant la question si fournie

        full_query = f"file:{abs_path}"

        if user_question.strip():

            full_query += f" {user_question.strip()}"



        # Affiche la requête utilisateur

        with st.chat_message("user"):

            st.markdown(full_query)

        st.session_state.messages.append({"role": "user", "content": full_query})



        # Appel à l'agent et affichage du résultat

        with st.chat_message("assistant"):

            response_container = st.empty()

            stream_handler = StreamlitCallbackHandler(response_container)



            try:

                response = agent.chat(full_query, callback_handler=stream_handler)

            except Exception as e:

                response = f"❌ Erreur lors de l'analyse du PDF : {e}"



            response_container.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})



# === SECTION CHAT LIBRE ===

st.subheader("💬 Chat libre")



user_input = st.chat_input("Posez une question...")



if user_input:

    # Commande spéciale /reset

    if user_input.strip().lower() == "/reset":

        agent.clear_memory()

        st.session_state.messages = []

        st.session_state.context_info = {}

        st.success("Mémoire et historique réinitialisés 🧹")

        st.stop()



    # Détection du prénom

    if "je m'appelle" in user_input.lower():

        parts = user_input.lower().split("je m'appelle")

        if len(parts) > 1:

            prenom = parts[1].strip().split()[0].capitalize()

            st.session_state.context_info["prenom"] = prenom



    # Enrichissement du contexte

    message_to_send = user_input

    if "prenom" in st.session_state.context_info:

        message_to_send = (

            f"[L'utilisateur s'appelle {st.session_state.context_info['prenom']}]\n"

            f"{user_input}"

        )



    # Affichage message utilisateur

    with st.chat_message("user"):

        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})



    # Réponse de l'agent

    with st.chat_message("assistant"):

        response_container = st.empty()

        stream_handler = StreamlitCallbackHandler(response_container)



        try:

            response = agent.chat(message_to_send, callback_handler=stream_handler)

        except Exception as e:

            response = f"❌ Erreur : {e}"



        response_container.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})



# === HISTORIQUE DES ÉCHANGES ===

with st.expander("📜 Historique des échanges"):

    if st.session_state.messages:

        for i, msg in enumerate(st.session_state.messages, 1):

            st.markdown(f"**{i}. {msg['role'].capitalize()}** : {msg['content']}")

    else:

        st.markdown("_Aucun échange pour le moment._")
