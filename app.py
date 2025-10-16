import os
import streamlit as st
import google.generativeai as genai

# Configure Gemini API key: prefer env var, fallback to provided key for out-of-the-box use
GEMINI_API_KEY=st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

st.title("AiGuru - AI Content Generator")
st.subheader("Generate content from your prompts easily!")

user_prompt = st.text_area("Enter your prompt:", height=150)
model_choice = st.selectbox(
    "Choose AI model:",
    [
        "gemini-1.5-flash",  # fast and cost-effective
        "gemini-1.5-pro",    # higher quality, more capable
    ],
    index=0,
)

if st.button("Generate Content"):
    if user_prompt.strip():
        with st.spinner("Generating content..."):
            try:
                model = genai.GenerativeModel(
                    model_name=model_choice,
                    system_instruction="You are a helpful AI content generator.",
                )
                response = model.generate_content(
                    user_prompt,
                    generation_config={
                        "max_output_tokens": 500,
                        "temperature": 0.7,
                    },
                )

                # Extract text output
                output_text = getattr(response, "text", None)
                if not output_text and hasattr(response, "candidates"):
                    # Fallback if SDK shape differs
                    candidates = response.candidates or []
                    if candidates and hasattr(candidates[0], "content") and candidates[0].content and candidates[0].content.parts:
                        output_text = "".join(getattr(p, "text", "") for p in candidates[0].content.parts)

                if output_text:
                    st.success("Content Generated Successfully!")
                    st.write(output_text)
                else:
                    st.error("No content returned by the model.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt to generate content.")

st.markdown("---")
st.caption("Using Google Gemini. Set GEMINI_API_KEY env var to override the bundled key.")
st.markdown("Developed by AiGuru Team")
