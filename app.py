import streamlit as st
import google.generativeai as genai

# ------------------------------
# Configure Gemini API Key
# ------------------------------
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None)
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in Streamlit secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ------------------------------
# Streamlit App UI
# ------------------------------
st.set_page_config(page_title="AiGuru - AI Content Generator", layout="wide")
st.title("AiGuru - AI Content Generator")
st.subheader("Generate high-quality content from your prompts!")

# User input
user_prompt = st.text_area("Enter your prompt:", height=150)
model_choice = st.selectbox(
    "Choose AI model:",
    [
        "gemini-2.5-flash",  # fast and cost-effective
        "gemini-2.5-pro",    # higher quality, more capable
    ],
    index=0,
)

# ------------------------------
# Generate Content
# ------------------------------
if st.button("Generate Content"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt to generate content.")
    else:
        with st.spinner("Generating content..."):
            try:
                # Create model with improved system prompt
                model = genai.GenerativeModel(
                    model_name=model_choice,
                    system_instruction="""
                    You are AiGuru, a professional AI content generator. 
                    Your task is to generate clear, engaging, and high-quality content based on the user's prompt. 
                    - Keep the output concise but informative.
                    - Use proper grammar and structure.
                    - Adapt the tone based on the context (formal, friendly, or persuasive if needed).
                    - Include examples, bullet points, or headings if relevant.
                    - Avoid filler content and repetitions.
                    - Always stay helpful, creative, and professional.
                    """
                )

                # Generate content
                response = model.generate_content(
                    user_prompt,
                    generation_config={
                        "max_output_tokens": 500,
                        "temperature": 0.7,
                    },
                )

                # ------------------------------
                # Robust Text Extraction
                # ------------------------------
                output_text = ""

                # Option 1: direct 'text' attribute
                if getattr(response, "text", None):
                    output_text = response.text
                # Option 2: fallback to candidates
                elif getattr(response, "candidates", None):
                    for candidate in response.candidates:
                        content = getattr(candidate, "content", None)
                        if content and getattr(content, "parts", None):
                            for part in content.parts:
                                output_text += getattr(part, "text", "")

                # ------------------------------
                # Display Results
                # ------------------------------
                if output_text.strip():
                    st.success("✅ Content Generated Successfully!")
                    st.markdown("---")
                    st.markdown(output_text)
                else:
                    st.error("⚠️ No content returned by the model. Try a different prompt or model.")

            except Exception as e:
                st.error(f"❌ Error generating content: {e}")

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.caption("Powered by Google Gemini. Set GEMINI_API_KEY in Streamlit secrets to override.")
st.markdown("Developed by AiGuru Team")
