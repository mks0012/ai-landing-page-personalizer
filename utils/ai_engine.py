import google.generativeai as genai

def generate_personalization(ad_image, original_content, api_key):
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('models/gemini-2.5-flash-lite')
    
    # Ultra-short prompt to save input tokens
    prompt = f"Ad: [Image]. Page: H1={original_content['h1']}, CTA={original_content['cta']}. Rewrite H1/CTA for ad-match. Output JSON: {{'personalized_h1':'', 'personalized_cta':'', 'explanation':''}}"

    try:
        # Pass  image and the  prompt
        response = model.generate_content([prompt, ad_image])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"