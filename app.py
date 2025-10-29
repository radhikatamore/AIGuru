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
st.set_page_config(page_title="Write Wise- AI Content Generator", layout="wide")
st.title("Write Wise - AI Content Generator")
st.subheader("Generate high-quality content from your prompts!")

# User input
user_prompt = st.text_area("Enter your prompt:", height=150)

# Model selection
model_choice = st.selectbox(
    "Choose AI model:",
    [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
    ],
    index=0,
)

# Content depth selection
depth_choice = st.selectbox(
    "Select Content Depth (level of detail):",
    [
        "Shallow (high-level overview)",
        "Medium (moderate detail with examples)",
        "Deep (very detailed, nuanced, in-depth analysis)"
    ],
    index=1
)

# Map depth to system instructions
depth_instruction_map = {
    "Shallow (high-level overview)": "Provide a clear and simple overview. Focus on key points, avoid unnecessary details.",
    "Medium (moderate detail with examples)": "Provide a moderately detailed explanation with examples and supporting points.",
    "Deep (very detailed, nuanced, in-depth analysis)": "Provide an in-depth, thorough, and nuanced explanation. Include examples, multiple perspectives, reasoning, and insights."
}

depth_instruction = depth_instruction_map[depth_choice]

# ------------------------------
# Generate Content
# ------------------------------
if st.button("Generate Content"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt to generate content.")
    else:
        with st.spinner("Generating content..."):
            try:
                # Combine base system prompt with depth instruction
                system_prompt = f"""
                You are AiGuru, a professional AI content generator. 
                Your task is to generate high-quality content based on the user's prompt.
                {depth_instruction}
                Use proper grammar and structure, adapt tone appropriately, include headings or examples if needed, and avoid filler or repetition.
                """

                model = genai.GenerativeModel(
                    model_name=model_choice,
                    system_instruction=system_prompt
                )

                # Generate content with increased token limit
                response = model.generate_content(
                    user_prompt,
                    generation_config={
                        "max_output_tokens": 20000,  
                        "temperature": 0.35
                    },
                )

                # ------------------------------
                # Robust Text Extraction
                # ------------------------------
                output_text = ""

                # Safe extraction: check candidates and parts
                if hasattr(response, "candidates") and response.candidates:
                    for candidate in response.candidates:
                        content = getattr(candidate, "content", None)
                        if content and getattr(content, "parts", None):
                            for part in content.parts:
                                output_text += getattr(part, "text", "")
                
                # Fallback to response.text only if valid
                if not output_text and getattr(response, "text", None):
                    output_text = response.text

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
st.markdown("Developed by Write Wise Team")
