# Install streamlit first if not done already:
# pip install streamlit openai

import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# UI Title
st.title("AiGuru - AI Content Generator")
st.subheader("Generate content from your prompts easily!")

# Input section
user_prompt = st.text_area("Enter your prompt:", height=150)

# Model selection (optional)
model_choice = st.selectbox(
    "Choose AI model:",
    ["gpt-3.5-turbo", "gpt-4"]
)

# Button to generate content
if st.button("Generate Content"):
    if user_prompt.strip() != "":
        with st.spinner("Generating content..."):
            try:
                response = openai.ChatCompletion.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": "You are a helpful AI content generator."},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                generated_text = response['choices'][0]['message']['content']
                st.success("Content Generated Successfully!")
                st.write(generated_text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt to generate content.")

# Footer
st.markdown("---")
st.markdown("Developed by AiGuru Team")
