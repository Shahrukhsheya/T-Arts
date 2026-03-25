import streamlit as st
import requests

st.set_page_config(page_title="T-Arts: Ultimate Image Search", layout="wide")
st.title("🎨 T-Arts: Ultimate Image Search")
st.write("Web, Movies, Celebrities, and Stock Images—all in one place!")

UNSPLASH_API_KEY = "2KvEQu8W69PeEHtVR8CW4HiPudld_TzzGl0yWQvat9c"
PEXELS_API_KEY = "IuQKyToABsqchwUub0Ij2B2PT5uVb1T4A5ZKHlRXVOGlh5lT0fdwxHMS"
giphy_api_key = "sgLvVdGwg68DlurSXSAyPzoBQ4V1TGdk"
pixeby_api_key = "53815545-66e5dc4e7fd837fef7817e906"
GOOGLE_API_KEY = "AIzaSyBZPdZuS8oHn_4j6JgzbSevV6oG3hT_ZLo"
SEARCH_ENGINE_ID = "<script async src="https://cse.google.com/cse.js?cx=229bff70d98bd43d7">
</script>
<div class="gcse-search"></div>"

# सर्च बॉक्स (बिना बटन के, Enter दबाते ही काम करेगा)
query = st.text_input("🔍 What do you want to find? (Press 'Enter' to search)")

# 3 Tabs का डिज़ाइन
tab_photos, tab_gifs, tab_videos = st.tabs(["📷 Photos", "🎞️ GIF (Coming Soon)", "🎥 Videos (Coming Soon)"])

# GIF Tab
with tab_gifs:
    st.info("🚀 GIF search feature is under development and will be available soon!")

# Video Tab
with tab_videos:
    st.info("🚀 Video and B-Rolls search feature is under development and will be available soon!")

# Photos Tab (Main Working Area)
with tab_photos:
    # Filters का डिज़ाइन
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        bg_filter = st.radio("Background:", ["Any", "Without BG (Transparent)"], horizontal=True)
    with col_f2:
        file_type = st.radio("Format:", ["Any", "JPG", "PNG"], horizontal=True)

    # अगर सर्च बॉक्स में कुछ लिखा गया है और Enter दबाया गया है
    if query:
        st.info(f"🌐 Searching Google's database for '{query}'...")
        
        # Google API का लिंक तैयार करना
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&searchType=image&num=10"

        # अगर Without BG सिलेक्ट किया है
        if bg_filter == "Without BG (Transparent)":
            url += "&imgType=transparent"
        
        # अगर Format सिलेक्ट किया है
        if file_type == "JPG":
            url += "&fileType=jpg"
        elif file_type == "PNG":
            url += "&fileType=png"

        try:
            res = requests.get(url).json()
            images_list = []
            
            if "items" in res:
                for item in res["items"]:
                    images_list.append(item["link"])

            # स्क्रीन पर फोटो दिखाना
            if len(images_list) > 0:
                st.success("🎉 Awesome! Found perfect matches.")
                
                c1, c2, c3 = st.columns(3)
                for i, img_url in enumerate(images_list):
                    if i % 3 == 0:
                        with c1:
                            st.image(img_url, use_container_width=True)
                            st.link_button("⬇️ Download", img_url, use_container_width=True)
                    elif i % 3 == 1:
                        with c2:
                            st.image(img_url, use_container_width=True)
                            st.link_button("⬇️ Download", img_url, use_container_width=True)
                    else:
                        with c3:
                            st.image(img_url, use_container_width=True)
                            st.link_button("⬇️ Download", img_url, use_container_width=True)
            else:
                st.error("No images found. Try a different keyword.")
        except Exception as e:
            st.error("⚠️ Error connecting to Google API. Please check your API Keys.")
