import json
from bs4 import BeautifulSoup
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Web Scraper Studio", page_icon="🕷️", layout="wide")

st.title("🕷️ Web Scraper for Headlines & Quotes")
st.markdown("Extract quotes safely using **Requests & BeautifulSoup**.")

# Target URL
target_url = "http://quotes.toscrape.com/"
st.write(f"**Target Website:** {target_url}")

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
}

if st.button("🚀 Run Scraper Now", use_container_width=True):
  with st.spinner("Fetching and parsing HTML..."):
    try:
      response = requests.get(target_url, headers=headers, timeout=10)
      response.raise_for_status()

      soup = BeautifulSoup(response.text, "html.parser")
      quotes_data = []

      items = soup.find_all("div", class_="quote")
      for item in items:
        text = item.find("span", class_="text").get_text(strip=True)
        author = item.find("small", class_="author").get_text(strip=True)
        tags = [t.get_text(strip=True) for t in item.find_all("a", class_="tag")]
        quotes_data.append({"quote": text, "author": author, "tags": tags})

      st.session_state["data"] = quotes_data
      st.success(f"Successfully scraped {len(quotes_data)} items!")

    except Exception as e:
      st.error(f"Error: {e}")

# Display data if scraped
if "data" in st.session_state and st.session_state["data"]:
  data = st.session_state["data"]

  st.markdown("### 📊 Extracted Results")

  # Tabs for view
  tab1, tab2 = st.tabs(["📋 Card View", "📦 JSON Download"])

  with tab1:
    for item in data:
      st.markdown(
          f"""
            <div style="background: #1e293b; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #6366f1;">
                <p style="color: #f8fafc; font-style: italic;">{item['quote']}</p>
                <p style="color: #94a3b8; font-size: 0.9rem;"><b>Author:</b> {item['author']}</p>
                <p style="color: #6366f1; font-size: 0.8rem;"><b>Tags:</b> {', '.join(item['tags'])}</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

  with tab2:
    st.json(data)
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    st.download_button(
        "📥 Download JSON File",
        json_str,
        file_name="quotes.json",
        mime="application/json",
    )
