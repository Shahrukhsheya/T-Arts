import streamlit as st
import requests

st.set_page_config(page_title="T-Arts: Ultimate Image Search", layout="wide")

# 🚨 YAHAN APNI TEENO KEYS DALEIN
SERPER_API_KEY = "8f6269e9c40729b56c89f24a1a232ad789049101"
PEXELS_API_KEY = "IuQKyToABsqchwUub0Ij2B2PT5uVb1T4A5ZKHlRXVOGlh5lT0fdwxHMS"
giphy_api_key = "sgLvVdGwg68DlurSXSAyPzoBQ4V1TGdk"
pixeby_api_key = "53815545-66e5dc4e7fd837fef7817e906"

# ⚙️ SIDEBAR (Side Menu for Filters)
with st.sidebar:
    st.header("⚙️ Search Filters")
    st.write("Apply filters to refine your results.")
    
    bg_filter = st.radio("Background:", ["Any", "Without BG (Transparent)"])
    file_type = st.radio("Format:", ["Any", "JPG", "PNG"])
    
    st.divider()
    st.info("💡 Tip: 'Without BG' feature uses our deep web engine to find perfect cutouts for your editing workflow.")

# MAIN PAGE UI
st.title("🎨 T-Arts: Ultimate Image Search")
st.write("Web, Movies, Celebrities, and Stock Images—all in one place!")

# 🔍 Professional Search Bar
query = st.text_input("Search", placeholder="🔍 Search for anything (e.g., Tiger, Salman Khan) and press Enter...", label_visibility="collapsed")

# 3 Tabs
tab_photos, tab_gifs, tab_videos = st.tabs(["📷 Photos", "🎞️ GIF (Coming Soon)", "🎥 Videos (Coming Soon)"])

with tab_gifs:
    st.info("🚀 GIF search feature is under development and will be available soon!")

with tab_videos:
    st.info("🚀 Video and B-Rolls search feature is under development and will be available soon!")

with tab_photos:
    if query:
        images_list = []
        
        # HYBRID LOGIC
        if bg_filter == "Without BG (Transparent)" or file_type == "PNG":
            st.info(f"🌐 Searching the Deep Web for '{query}' with transparent background...")
            
            # Use Only Serper for Transparent/PNGs
            search_query = query + (" transparent background png" if bg_filter == "Without BG (Transparent)" else " png")
            url = "https://google.serper.dev/images"
            payload = {"q": search_query, "num": 40}
            headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
            try:
                res = requests.post(url, headers=headers, json=payload).json()
                if "images" in res:
                    for item in res["images"]:
                        images_list.append(item["imageUrl"])
            except:
                pass
                
        else:
            st.info(f"⚡ Smart Search activated for '{query}'. Fetching from multiple sources to save limits...")
            
            # 1. Unsplash (Free)
            try:
                un_url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_API_KEY}&per_page=20&order_by=relevant"
                un_res = requests.get(un_url).json()
                if "results" in un_res:
                    for img in un_res["results"]:
                        images_list.append(img["urls"]["regular"])
            except:
                pass
                
            # 2. Pexels (Free)
            try:
                px_url = f"https://api.pexels.com/v1/search?query={query}&per_page=20"
                headers = {"Authorization": PEXELS_API_KEY}
                px_res = requests.get(px_url, headers=headers).json()
                if "photos" in px_res:
                    for img in px_res["photos"]:
                        images_list.append(img["src"]["large"])
            except:
                pass
                
            # 3. Serper (Deep Web - Sirf 10-20 photos layega Celebs ke liye)
            try:
                url = "https://google.serper.dev/images"
                payload = {"q": query, "num": 20}
                headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
                res = requests.post(url, headers=headers, json=payload).json()
                if "images" in res:
                    for item in res["images"]:
                        images_list.append(item["imageUrl"])
            except:
                pass

        # Display Images
        if len(images_list) > 0:
            st.success(f"🎉 Awesome! Found {len(images_list)} high-quality images.")
            
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
            st.error("No images found. Please check your API keys or try a different keyword.")