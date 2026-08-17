import streamlit as st
from PIL import Image

from vision import generate_caption
from story_generator import generate_story


st.title("📖 AI Memory Maker")

st.write(
    "Upload an image and let AI turn it into a creative story."
)


uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)


story_style = st.selectbox(
    "🎭 Choose Story Style",
    [
        "Adventure",
        "Funny",
        "Emotional",
        "Mystery",
        "Cinematic"
    ]
)


story_length = st.selectbox(
    "📏 Story Length",
    [
        "Short",
        "Medium",
        "Long"
    ]
)


custom_instruction = st.text_input(
    "✨ Additional instruction",
    placeholder="e.g. Make it nostalgic..."
)


if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image"
    )


    if st.button("✨ Generate Story"):

        with st.spinner("Understanding the image..."):

            caption = generate_caption(image)


        st.subheader("👁️ What AI Sees")

        st.write(caption)


        st.subheader("📖 Your AI Memory")

        story_stream = generate_story(
            caption,
            story_style,
            story_length,
            custom_instruction
        )

        story = st.write_stream(story_stream)


        # Download button
        st.download_button(
            label="📥 Download Story",
            data=story,
            file_name="my_ai_memory.txt",
            mime="text/plain"
        )