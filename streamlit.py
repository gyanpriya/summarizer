import streamlit as st
import requests
import os

port = os.environ.get("PORT", 8501)

st.title("📰 Topic Summarizer")
topic = st.text_input("Enter a topic (e.g. AI, SpaceX, Bitcoin):")

if st.button("Summarize"):
    with st.spinner("Fetching and summarizing..."):
        response = requests.post(
            "https://summarizer-flask.onrender.com",  # Update with your Render backend URL
            json={"topic": topic}
        )
        data = response.json()

        st.subheader("📌 Consolidated Summary")
        st.write(data["consolidated"])

        st.subheader("📄 Individual Articles")
        for article in data["summaries"]:
            st.markdown(f"**[{article['title']}]({article['link']})**")
            st.write(article["summary"])

        st.download_button("Download Summary", data["consolidated"], file_name="summary.txt")
