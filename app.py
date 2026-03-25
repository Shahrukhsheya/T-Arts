 import streamlit as st
import requests
from duckduckgo_search import DDGS

st.set_page_config(page_title="T-Arts: Pro Image Search", layout="wide")
st.title("🎨 T-Arts: Ultimate Image Search")
st.write("Web, Movies, Celebrities, and Stock Images—all in one place!")

UNSPLASH_API_KEY = "2KvEQu8W69PeEHtVR8CW4HiPudld_TzzGl0yWQvat9c"
PEXELS_API_KEY = "IuQKyToABsqchwUub0Ij2B2PT5uVb1T4A5ZKHlRXVOGlh5lT0fdwxHMS"
giphy_api_key = "sgLvVdGwg68DlurSXSAyPzoBQ4V1TGdk"
pixeby_api_key = "53815545-66e5dc4e7fd837fef7817e906"


query = st.text_input("What do you want to find? (e.g., Salman Khan, Avengers, Cyberpunk)")

if st.button("Search 100+ Images"):
    if query:
        st.info("🌐 Searching across the web and stock libraries. This may take 5-10 seconds...")
        images_list = []
        
        # 1. DuckDuckGo for Internet/Celeb images
        try:
            with DDGS() as ddgs:
                ddg_results = list(ddgs.images(query, max_results=60))
                for res in ddg_results:
                    images_list.append(res['image'])
        except Exception as e:
            st.warning("⚠️ High traffic on web search. Displaying stock photos only. Please try again in 10-15 minutes.")

        # 2. Unsplash images
        un_url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_API_KEY}&per_page=30&order_by=relevant"
        try:
            un_res = requests.get(un_url).json()
            if "results" in un_res:
                for img in un_res["results"]:
                    images_list.append(img["urls"]["regular"])
        except:
            pass 

        # 3. Pexels images
        px_url = f"https://api.pexels.com/v1/search?query={query}&per_page=30"
        headers = {"Authorization": PEXELS_API_KEY}
        try:
            px_res = requests.get(px_url, headers=headers).json()
            if "photos" in px_res:
                for img in px_res["photos"]:
                    images_list.append(img["src"]["large"])
        except:
            pass
            
        # 4. Display Images on Screen
        if len(images_list) > 0:
            st.success(f"🎉 Awesome! Found {len(images_list)} high-quality images. Keep scrolling 👇")
            
            col1, col2, col3 = st.columns(3)
            for i, img_url in enumerate(images_list):
                if i % 3 == 0:
                    with col1:
                        st.image(img_url, use_container_width=True)
                        st.link_button("⬇️ Download HD", img_url, use_container_width=True)
                elif i % 3 == 1:
                    with col2:
                        st.image(img_url, use_container_width=True)
                        st.link_button("⬇️ Download HD", img_url, use_container_width=True)
                else:
                    with col3:
                        st.image(img_url, use_container_width=True)
                        st.link_button("⬇️ Download HD", img_url, use_container_width=True)
        else:
            st.error("No images found. Please try a different keyword!")
    else:
        st.warning("Please enter a keyword in the search box first!")