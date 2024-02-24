import streamlit as st
import together
import base64
import time
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def main():
    st.title("SyncThree Image Generation")

    together.api_key = os.getenv("TOGETHER_API_KEY")
    
    prompt = st.text_input("Prompt")
    num_images = st.number_input("Number of Images to Generate", min_value=1, value=1)
    seed = st.slider("Select Seed", min_value=0, max_value=100, value=42)

    if st.button("Generate Image"):
        if prompt:
            try:
                response = together.Image.create(
                    prompt=prompt,
                    model="stabilityai/stable-diffusion-xl-base-1.0",
                    width=1024,
                    height=1024,
                    steps=25,
                    seed=seed,
                    results=num_images
                )
                for i in range(num_images):
                    image = response["output"]["choices"][i]
                    with open(f"generated_image_{i}.png", "wb") as f:
                        f.write(base64.b64decode(image["image_base64"]))
                    st.image(f"generated_image_{i}.png")
            except together.RateLimitError as e:
                st.error("Rate limit exceeded. Please try again later.")
                time.sleep(1)
            except Exception as e:
                st.error("Error: " + str(e))
        else:
            st.error("Please enter a prompt before generating the image.")

if __name__ == '__main__':
    main()
