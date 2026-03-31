import streamlit as st
import requests

st.set_page_config(page_title="T-Arts: Ultimate Image Search", layout="wide")

SERPER_API_KEY = "8f6269e9c40729b56c89f24a1a232ad789049101"
HUGGINGFACE_API_KEY = "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"

# ==========================================
# 🧠 SMART MEMORY (Session State)
# ==========================================
# Yeh app ko yaad rakhne me madad karega ki kya search kiya tha, taaki baar-baar API limit kharch na ho.
if "images_list" not in st.session_state:
    st.session_state.images_list = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "ai_target_url" not in st.session_state:
    st.session_state.ai_target_url = None

st.title("🎨 T-Arts: Ultimate Image Search")
st.write("Web, Movies, Celebrities, and Stock Images—all in one place!")

# 🔍 Search Bar with Icon
col_search, col_btn = st.columns([15, 1])
with col_search:
    query = st.text_input("Search", placeholder="Search for anything and press Enter...", label_visibility="collapsed")
with col_btn:
    search_btn = st.button("🔍")

format_filter = st.selectbox(
    "Image Format & Filters:", 
    ["Any", "JPG", "JPEG", "PNG", "Transparent (Without BG)"], 
    index=0
)

# ==========================================
# 🔍 SEARCH LOGIC (Only runs when you search something new)
# ==========================================
if query and (query != st.session_state.last_query or search_btn):
    st.session_state.last_query = query
    st.session_state.ai_target_url = None # Naya search karne par purana AI result hata dega
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
        except: pass
    else:
        try:
            un_url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_API_KEY}&per_page=30&order_by=relevant"
            un_res = requests.get(un_url).json()
            if "results" in un_res:
                for img in un_res["results"]:
                    images_list.append(img["urls"]["regular"])
        except: pass
            
        try:
            px_url = f"https://api.pexels.com/v1/search?query={query}&per_page=80"
            headers = {"Authorization": PEXELS_API_KEY}
            px_res = requests.get(px_url, headers=headers).json()
            if "photos" in px_res:
                for img in px_res["photos"]:
                    images_list.append(img["src"]["large"])
        except: pass
            
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
        except: pass
    
    st.session_state.images_list = images_list

# ==========================================
# ✨ AI RESULT STUDIO (Shows UP here when you click 'Get PNG' on any image)
# ==========================================
if st.session_state.ai_target_url:
    st.divider()
    st.subheader("✂️ AI Cutout Result")
    with st.spinner("🤖 Cloud AI is extracting the subject... Please wait!"):
        try:
            # Safe Image Downloader (Anti-Crash)
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_response = requests.get(st.session_state.ai_target_url, headers=headers, timeout=15)
            
            if img_response.status_code == 200:
                # Hugging Face API Call
                API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"
                hf_headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
                hf_response = requests.post(API_URL, headers=hf_headers, data=img_response.content)
                
                if hf_response.status_code == 200:
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        st.write("**Before**")
                        st.image(img_response.content, use_container_width=True)
                    with col2:
                        st.write("**After (True PNG)**")
                        st.image(hf_response.content, use_container_width=True)
                    with col3:
                        st.write("**Actions**")
                        st.download_button("⬇️ Download High-Res PNG", data=hf_response.content, file_name="T-Arts-Cutout.png", mime="image/png", use_container_width=True)
                        if st.button("❌ Close AI Window", use_container_width=True):
                            st.session_state.ai_target_url = None
                            st.rerun()
                else:
                    st.error(f"⚠️ AI Server busy. Try again. (Error {hf_response.status_code})")
            else:
                st.error("⚠️ Website blocked the image download. Please try a different photo.")
        except Exception as e:
            st.error("⚠️ Network connection broke (IncompleteRead). Please try clicking 'Get PNG' again or choose another image.")
    st.divider()

# ==========================================
# 🖼️ GALLERY UI (Native Streamlit Columns - Fast & Stable)
# ==========================================
if len(st.session_state.images_list) > 0:
    st.write(f"🎉 Found {len(st.session_state.images_list)} images!")
    
    c1, c2, c3 = st.columns(3)
    
    for i, img_url in enumerate(st.session_state.images_list):
        # Distribute images equally in 3 columns
        col = c1 if i % 3 == 0 else c2 if i % 3 == 1 else c3
        
        with col:
            # Display Image
            st.image(img_url, use_container_width=True)
            
            # Display Buttons Side-by-Side right under the image
            bc1, bc2 = st.columns(2)
            with bc1:
                st.link_button("👁️ View", img_url, use_container_width=True)
            with bc2:
                # DIRECT AI BUTTON
                if st.button("✂️ Get PNG", key=f"ai_btn_{i}", use_container_width=True):
                    st.session_state.ai_target_url = img_url
                    st.rerun() # Yeh app ko turant upar AI Studio me bhej dega!

elif query:
    st.error("No images found. Please check your API keys or try a different keyword.")