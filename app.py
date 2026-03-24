import streamlit as st
import requests

# ऐप की सेटिंग और डिज़ाइन
st.set_page_config(page_title="T-Arts: Pro Image Search", layout="wide")
st.title("🎨 T-Arts: Free Stock Images & B-Rolls")
st.write("अपने वीडियो एडिटिंग और डिज़ाइन के लिए बेहतरीन इमेजेस खोजें।")

UNSPLASH_API_KEY = "2KvEQu8W69PeEHtVR8CW4HiPudld_TzzGl0yWQvat9c"
PEXELS_API_KEY = "IuQKyToABsqchwUub0Ij2B2PT5uVb1T4A5ZKHlRXVOGlh5lT0fdwxHMS"
giphy_api_key = "sgLvVdGwg68DlurSXSAyPzoBQ4V1TGdk"
pixeby_api_key = "53815545-66e5dc4e7fd837fef7817e906"


# सर्च बॉक्स
query = st.text_input("क्या ढूँढना चाहते हैं? (जैसे: Cyberpunk city, Sad boy, Nature)")

# सर्च बटन का लॉजिक
if st.button("Search Perfect Images"):
    if query:
        st.info("परफेक्ट इमेजेस ढूँढ रहा हूँ, कृपया इंतज़ार करें...")
        images_list = []
        
        # 1. Unsplash से इमेजेस लाना
        un_url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_API_KEY}&per_page=6&order_by=relevant"
        try:
            un_res = requests.get(un_url).json()
            if "results" in un_res:
                for img in un_res["results"]:
                    images_list.append(img["urls"]["regular"])
        except Exception as e:
            pass 

        # 2. Pexels से इमेजेस लाना
        px_url = f"https://api.pexels.com/v1/search?query={query}&per_page=6"
        headers = {"Authorization": PEXELS_API_KEY}
        try:
            px_res = requests.get(px_url, headers=headers).json()
            if "photos" in px_res:
                for img in px_res["photos"]:
                    images_list.append(img["src"]["large"])
        except Exception as e:
            pass
            
        # 3. इमेजेस को स्क्रीन पर दिखाना (नए डाउनलोड बटन के साथ)
        if len(images_list) > 0:
            st.success(f"शानदार! {len(images_list)} बेस्ट इमेजेस मिल गईं!")
            
            # 3 Columns में फोटो और डाउनलोड बटन
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
            st.error("कोई फोटो नहीं मिली। कृपया कोई और शब्द ट्राई करें!")
    else:
        st.warning("पहले सर्च बॉक्स में कुछ लिखें!")