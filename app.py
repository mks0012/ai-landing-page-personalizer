import streamlit as st
import os
import json
import time
from dotenv import load_dotenv
from PIL import Image
from utils.scraper import scrape_landing_page
from utils.ai_engine import generate_personalization

# 1. Load Environment and CSS
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Set Page Config
st.set_page_config(page_title="Troopod AI Personalizer", layout="wide")

# Apply custom CSS
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass  # Silently skip if style.css is missing

# 2. UI Header
st.title("🎯 Troopod AI: Ad-to-LP Personalization")
st.write("Aligning Ad Creative intent with Landing Page content.")

# 3. Sidebar Inputs
with st.sidebar:
    st.header("Input Data")
    ad_image = st.file_uploader("Upload Ad Creative", type=['jpg', 'jpeg', 'png'])
    lp_url = st.text_input("Landing Page URL", value="https://example.com")
    process_btn = st.button("Generate Personalization")

# 4. Execution Logic (ONLY runs when button is clicked)
if process_btn:
    if not ad_image or not lp_url:
        st.error("Missing Inputs: Please upload an image and a URL.")
    else:
        with st.spinner("Analyzing... (Applying 2s buffer for API limits)"):
            # Rate limit safety
            time.sleep(2)
            
            # SScrape the landing page
            original_data = scrape_landing_page(lp_url)
            
            # Validation Gate
            if original_data is None:
                st.error("Invalid URL or Page Not Found. Please check the link and try again.")
            else:
                #  Call AI Engine
                img = Image.open(ad_image)
                raw_output = generate_personalization(img, original_data, API_KEY)
                
                #  Handle Rate Limits and JSON Parsing
                if "429" in str(raw_output):
                    st.warning("⚠️ Rate Limit Hit: The Free Tier allows 5 requests per minute. Please wait 30 seconds.")
                else:
                    try:
                        # Extract JSON 
                        start = raw_output.find('{')
                        end = raw_output.rfind('}') + 1
                        json_str = raw_output[start:end]
                        result = json.loads(json_str)

                        # Display Results
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("Original Page")
                            st.info(f"**H1:** {original_data['h1']}")
                            st.info(f"**CTA:** {original_data['cta']}")
                            st.image(img, caption="Ad Creative", use_container_width=True)

                        with col2:
                            st.subheader("🚀 Personalized Result")
                            st.success(f"**New H1:** {result.get('personalized_h1')}")
                            st.success(f"**New CTA:** {result.get('personalized_cta')}")
                            
                            with st.expander("CRO Logic"):
                                st.write(result.get('explanation'))
                    
                    except Exception as e:
                        st.error("AI returned non-JSON text. See raw output below.")
                        st.code(raw_output)