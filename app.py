from openai import OpenAI
import streamlit as st
import os

# Load API key securely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("AiGuru - AI Content Generator")
st.subheader("Generate content from your prompts easily!")

user_prompt = st.text_area("Enter your prompt:", height=150)
model_choice = st.selectbox("Choose AI model:", ["gpt-3.5-turbo", "gpt-4"])

if st.button("Generate Content"):
    if user_prompt.strip():
        with st.spinner("Generating content..."):
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": "You are a helpful AI content generator."},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                st.success("Content Generated Successfully!")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt to generate content.")

st.markdown("---")
st.markdown("Developed by AiGuru Team")
