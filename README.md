# AI-Powered Landing Page Personalizer

I developed this tool to bridge the gap between Ad Creatives and Landing Pages. When a user clicks an ad with a specific hook (e.g., "3 Days Free"), the landing page should immediately reflect that. This agent automates that "Message Match."

### Technical Highlights
* **Optimized Scraper:** Standard landing pages are heavy. I built a scraper that strips 90% of the HTML noise (scripts/styles) before the LLM sees it. This saves tokens and cuts latency.
* **Resilience Testing:** I’ve stress-tested this for 404s, missing H1 tags (tested on Google.com), and API rate limits. 
* **Model:** Built using Gemini 2.5 Flash Lite for a balance of speed and multimodal reasoning.

### How to Run
1. Clone this repo.
2. Create a `.env` file with your `GEMINI_API_KEY`.
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `streamlit run app.py`