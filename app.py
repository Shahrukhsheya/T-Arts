import streamlit as st
import requests
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="T-Arts: Ultimate Image Search", layout="wide")

SERPER_API_KEY = "8f6269e9c40729b56c89f24a1a232ad789049101"

st.title("🎨 T-Arts: Ultimate Image Search")
st.write("Web, Movies, Celebrities, and Stock Images—all in one place!")

# ==========================================
# ✂️ UNLIMITED AI CUTOUT STUDIO (100% FREE)
# ==========================================
with st.expander("✨ AI Auto-Cutout Studio (Make Any Image Transparent)", expanded=True):
    st.write("Right-click any image below, select **'Copy image address'**, paste it here, and let our Unlimited AI do the magic!")
    
    col_input, col_ai_btn = st.columns([10, 2])
    with col_input:
        ai_img_url = st.text_input("Paste Image Link:", placeholder="Paste image URL here...", label_visibility="collapsed")
    with col_ai_btn:
        process_btn = st.button("✂️ Remove BG")

    if process_btn and ai_img_url:
        with st.spinner("🤖 Advanced AI is cutting out the background... Please wait!"):
            try:
                # 1. URL से फोटो डाउनलोड करना
                img_response = requests.get(ai_img_url)
                if img_response.status_code == 200:
                    input_image = img_response.content
                    
                    # 2. Unlimited AI से बैकग्राउंड हटाना
                    output_image = remove(input_image)
                    
                    st.success("🎉 Background removed successfully! (Unlimited AI Powered)")
                    
                    # 3. रिजल्ट दिखाना
                    col_result1, col_result2 = st.columns(2)
                    with col_result1:
                        st.write("**Before (Original)**")
                        st.image(input_image, use_container_width=True)
                    with col_result2:
                        st.write("**After (Transparent PNG)**")
                        st.image(output_image, use_container_width=True)
                        
                        # Direct Download
                        st.download_button(
                            label="⬇️ Download True PNG",
                            data=output_image,
                            file_name="T-Arts-Transparent.png",
                            mime="image/png",
                            use_container_width=True
                        )
                else:
                    st.error("⚠️ Failed to load the image. Try a different URL.")
            except Exception as e:
                st.error("⚠️ Error processing the image. Please try another one.")

st.divider()

# 🔍 Search Bar with Icon (Button)
col_search, col_btn = st.columns([15, 1])
with col_search:
    query = st.text_input("Search", placeholder="Search for anything and press Enter...", label_visibility="collapsed")
with col_btn:
    search_btn = st.button("🔍")

# 3 Tabs
tab_photos, tab_gifs, tab_videos = st.tabs(["📷 Photos", "🎞️ GIF (Coming Soon)", "🎥 Videos (Coming Soon)"])

with tab_gifs:
    st.write("🚀 GIF search feature is under development and will be available soon!")

with tab_videos:
    st.write("🚀 Video and B-Rolls search feature is under development and will be available soon!")

with tab_photos:
    format_filter = st.selectbox(
        "Image Format & Filters:", 
        ["Any", "JPG", "JPEG", "PNG", "Transparent (Without BG)"], 
        index=0
    )

    if query or search_btn:
        if query:
            images_list = []
            
            # HYBRID LOGIC
            if format_filter in ["Transparent (Without BG)", "PNG"]:
                search_query = query + " transparent background png" if format_filter == "Transparent (Without BG)" else query + " png"
                url = "https://google.serper.dev/images"
                payload = {"q": search_query, "num": 100}
                headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
                try:
                    res = requests.post(url, headers=headers, json=payload).json()
                    if "images" in res:
                        for item in res["images"]:
                            images_list.append(item["imageUrl"])
                except:
                    pass
            else:
                try:
                    un_url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_API_KEY}&per_page=30&order_by=relevant"
                    un_res = requests.get(un_url).json()
                    if "results" in un_res:
                        for img in un_res["results"]:
                            images_list.append(img["urls"]["regular"])
                except:
                    pass
                    
                try:
                    px_url = f"https://api.pexels.com/v1/search?query={query}&per_page=80"
                    headers = {"Authorization": PEXELS_API_KEY}
                    px_res = requests.get(px_url, headers=headers).json()
                    if "photos" in px_res:
                        for img in px_res["photos"]:
                            images_list.append(img["src"]["large"])
                except:
                    pass
                    
                if format_filter != "Any":
                    search_query = f"{query} {format_filter}"
                else:
                    search_query = query

                try:
                    url = "https://google.serper.dev/images"
                    payload = {"q": search_query, "num": 100}
                    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
                    res = requests.post(url, headers=headers, json=payload).json()
                    if "images" in res:
                        for item in res["images"]:
                            images_list.append(item["imageUrl"])
                except:
                    pass

            if len(images_list) > 0:
                html_code = "<style>"
                html_code += ".gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; padding: 10px 0; }"
                html_code += ".img-box { position: relative; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }"
                html_code += ".img-box img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.3s ease; }"
                html_code += ".img-box:hover img { transform: scale(1.05); }"
                html_code += ".overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); display: flex; justify-content: center; align-items: center; opacity: 0; transition: opacity 0.3s ease; }"
                html_code += ".img-box:hover .overlay { opacity: 1; }"
                html_code += ".action-btn { background-color: rgba(255, 255, 255, 0.9); color: #000 !important; padding: 12px 24px; border-radius: 30px; text-decoration: none !important; font-weight: bold; font-size: 15px; transition: background-color 0.2s ease, transform 0.2s ease; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }"
                html_code += ".action-btn:hover { background-color: #fff; transform: scale(1.05); }"
                html_code += "</style>"
                
                html_code += '<div class="gallery">'
                for img_url in images_list:
                    html_code += f'<div class="img-box"><img src="{img_url}" loading="lazy"><div class="overlay"><a href="{img_url}" target="_blank" class="action-btn">👁️ View HD</a></div></div>'
                html_code += '</div>'
                
                st.markdown(html_code, unsafe_allow_html=True)
            else:
                st.error("No images found. Please check your API keys or try a different keyword.")