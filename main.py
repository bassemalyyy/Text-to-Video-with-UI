# Step 1: Install Necessary Libraries
pip install torch diffusers accelerate

import streamlit as st
import torch
from diffusers.pipelines.pipeline_utils import DiffusionPipeline
from diffusers.utils.export_utils import export_to_video
import os

# Streamlit app title
st.title("Text-to-Video Generator")

# Sidebar information
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Enter a prompt in the text box below.
2. Click "Generate Video" to create a video.
3. View the video on the page and download it if desired.
""")

# Text input for the prompt
prompt = st.text_input("Enter your prompt:", placeholder="e.g., Penguin dancing happily")

# Button to generate the video
if st.button("Generate Video"):
    if prompt.strip():
        # Inform user the process is starting
        st.write("Generating video... This may take some time. Please wait.")
        
        # Load the model (only once for efficiency)
        @st.cache_resource
        def load_model():
            pipe = DiffusionPipeline.from_pretrained(
                "damo-vilab/text-to-video-ms-1.7b",
                torch_dtype=torch.float16,
                variant="fp16"
            )
            return pipe.to("cuda")

        pipe = load_model()

        # Generate the video
        num_iterations = 4  # Number of iterations to create frames
        all_frames = []

        for _ in range(num_iterations):
            video_frames = pipe(prompt).frames[0]
            all_frames.extend(video_frames)

        # Export video to a file
        video_path = export_to_video(all_frames)
        
        # Display video in Streamlit
        st.video(video_path)

        # Add a download button
        with open(video_path, "rb") as video_file:
            st.download_button(
                label="Download Video",
                data=video_file,
                file_name=os.path.basename(video_path),
                mime="video/mp4"
            )
    else:
        st.error("Please enter a prompt before generating the video.")
