import streamlit as st
import wikipediaapi
import google.generativeai as genai

# --- Configuration ---
# Set up the Wikipedia API (requires a custom user agent)
wiki_wiki = wikipediaapi.Wikipedia('MyResearchApp/1.0', 'en')

# Configure your AI API Key here
# Replace "YOUR_API_KEY" with your actual Gemini API key
GENAI_API_KEY = "AIzaSyC9746xKzxlWiTjeHSmLlfMVeaBjK0Rq7o" 
if GENAI_API_KEY != "YOUR_API_KEY":
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

# --- App UI ---
st.set_page_config(page_title="Proton Legal Research Bot", page_icon="♾️")
st.title("♾️ Proton Official AI Researcher")
st.write("Search for a topic, and I'll fetch the facts and summarize them for you in a simple way.")

# User Input
topic = st.text_input("What do you want to learn about today?", placeholder="e.g., Galaxies, Black Holes...")

if st.button("Enter"):
    if not topic:
        st.warning("Please enter a topic first!")
    elif GENAI_API_KEY == "YOUR_API_KEY":
        st.error("Please add your Gemini API Key to the code to enable AI summaries.")
    else:
        with st.spinner(f"Searching Wikipedia for '{topic}'..."):
            page = wiki_wiki.page(topic)
            
            if not page.exists():
                st.error("I couldn't find a Wikipedia page for that topic. Try being more specific.")
            else:
                st.success("Information found! Generating summary...")
                wiki_text = page.text[:2000] 
                
                prompt = f"""
                You are a helpful research assistant. Read the following text extracted from an encyclopedia.
                Provide a quick, easy-to-understand summary. 
                Include:
                1. A one-sentence simple definition.
                2. 3-4 key bullet points with the most important facts.
                
                Text:
                {wiki_text}
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 📝 AI Summary")
                    st.write(response.text)
                    
                    with st.expander("Show Original Source Text (Wikipedia)"):
                        st.write(wiki_text + "...")
                        st.markdown(f"[Read full article here]({page.fullurl})")
                        
                except Exception as e:
                    st.error(f"An error occurred while generating the summary: {e}")
st.markdown("---")
st.caption("© 2026 Proton AI Tools | Built for JEE Research")
st.caption("Legal Disclaimer: This tool uses AI. Information may be inaccurate. Always verify with official textbooks.")