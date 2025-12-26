import streamlit as st
from util import analyze_text, analyze_image, analyze_audio, generate_image_from_prompt

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
st.title(" AI Assistant (Gemini + LangChain)")
st.markdown("Interact with AI through *Text, **Image, or **Audio* inputs.")

mode = st.sidebar.radio("Select Mode", ["Text","Image Generation", "Image", "Audio"])

if mode == "Text":
    text_input = st.text_area("Enter your text prompt:")
    if st.button("Analyze Text"):
        if text_input.strip():
            st.write(analyze_text(text_input))
        else:
            st.warning("Please enter a message.")

# elif mode == "Image Generation":
#     st.subheader(" AI Image Generator")
#     prompt = st.text_input("Enter a prompt for image generation:")
    
#     if prompt and st.button("Generate Image"):
#         generated_path = generate_image_from_prompt(prompt)
#         st.image(generated_path, caption="Generated Image", width=600)

elif mode == "Image Generation":
    st.subheader("AI Image Generator")
    prompt = st.text_input("Enter a prompt for image generation:")

    if prompt and st.button("Generate Image"):
        generated_path = generate_image_from_prompt(prompt)

        # Show the generated image
        st.image(generated_path, caption="Generated Image", width=600)

        # Read the image as binary
        with open(generated_path, "rb") as f:
            image_bytes = f.read()

        # Add a download button
        st.download_button(
            label=" Download Image",
            data=image_bytes,
            file_name="generated_image.png",
            mime="image/png"
        )




elif mode == "Image":
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    prompt = st.text_input("Ask something about the image:")
    if uploaded_image and st.button("Analyze Image"):
        with open("temp_img.png", "wb") as f:
            f.write(uploaded_image.read())
        st.image(uploaded_image)
        st.write(analyze_image("temp_img.png", prompt or "Describe this image."))

elif mode == "Audio":
    uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "wav"])
    prompt = st.text_input("What do you want to know about this audio?")
    if uploaded_audio and st.button("Analyze Audio"):
        with open("temp_audio.mp3", "wb") as f:
            f.write(uploaded_audio.read())
        st.audio(uploaded_audio)

        st.write(analyze_audio("temp_audio.mp3", prompt or "Transcribe this audio."))
