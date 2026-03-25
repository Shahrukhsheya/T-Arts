import streamlit as st
import requests

st.set_page_config(page_title="T-Arts: Ultimate Image Search", layout="wide")
st.title("🎨 T-Arts: Ultimate Image Search")
st.write("Web, Movies, Celebrities, and Stock Images—all in one place!")

SERPER_API_KEY = "8f6269e9c40729b56c89f24a1a232ad789049101"

# 🔍 प्रोफेशनल सर्च बार
query = st.text_input("Search", placeholder="🔍 Search for anything (e.g., Tiger, Salman Khan) and press Enter...", label_visibility="collapsed")

# 3 Tabs
tab_photos, tab_gifs, tab_videos = st.tabs(["📷 Photos", "🎞️ GIF (Coming Soon)", "🎥 Videos (Coming Soon)"])

with tab_gifs:
    st.info("🚀 GIF search feature is under development and will be available soon!")

with tab_videos:
    st.info("🚀 Video and B-Rolls search feature is under development and will be available soon!")

with tab_photos:
    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        bg_filter = st.radio("Background:", ["Any", "Without BG (Transparent)"], horizontal=True)
    with col_f2:
        file_type = st.radio("Format:", ["Any", "JPG", "PNG"], horizontal=True)

    if query:
        st.info(f"🌐 Searching the web for '{query}'...")
        
        # सर्च को और स्मार्ट बनाना
        search_query = query
        if bg_filter == "Without BG (Transparent)":
            search_query += " transparent background png"
        if file_type != "Any":
            search_query += f" {file_type}"
            
        url = "https://google.serper.dev/images"
        payload = {
            "q": search_query,
            "num": 30  # एक बार में 30 फोटो लाएगा
        }
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }

        try:
            res = requests.post(url, headers=headers, json=payload).json()
            
            if "message" in res and "Unauthorized" in res["message"]:
                st.error("⚠️ API Key Error: Please check your Serper API Key.")
            else:
                images_list = []
                if "images" in res:
                    for item in res["images"]:
                        images_list.append(item["imageUrl"])

                if len(images_list) > 0:
                    st.success("🎉 Awesome! Found perfect matches.")
                    
                    c1, c2, c3 = st.columns(3)
                    for i, img_url in enumerate(images_list):
                        if i % 3 == 0:
                            with c1:
                                st.image(img_url, use_container_width=True)
                                st.link_button("⬇️ Download HD", img_url, use_container_width=True)
                        elif i % 3 == 1:
                            with c2:
                                st.image(img_url, use_container_width=True)
                                st.link_button("⬇️ Download HD", img_url, use_container_width=True)
                        else:
                            with c3:
                                st.image(img_url, use_container_width=True)
                                st.link_button("⬇️ Download HD", img_url, use_container_width=True)
                else:
                    st.error("No images found. Try a different keyword.")
        except Exception as e:
            st.error("⚠️ Error connecting to Search Server. Please check your connection.")