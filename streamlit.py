import streamlit as st
import requests
import os

port = os.environ.get("PORT", 8501)

st.title("📰 Topic Summarizer")
topic = st.text_input("Enter a topic (e.g. AI, SpaceX, Bitcoin):")

if st.button("Summarize"):
    with st.spinner("Fetching and summarizing..."):
        try:
            response = requests.post(
                "https://summarizer-flask.onrender.com",  # Update with your Render backend URL
                json={"topic": topic}
            )
            st.code(response.text)

            data = response.json()
            
            st.subheader("📌 Consolidated Summary")
            st.write(data["consolidated"])
            
            st.subheader("📄 Individual Articles")
            
            for article in data["summaries"]:
                st.markdown(f"**{article['title']}**")
                st.markdown(f"[Read more]({article['link']})")
                st.write(article["summary"])
        except Exception as e:
            st.error(f"Error: {e}")

        st.download_button("Download Summary", data["consolidated"], file_name="summary.txt")
