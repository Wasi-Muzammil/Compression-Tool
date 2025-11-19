import streamlit as st
from io import BytesIO
from algo import (
    compress_text, compress_image_file,
    compress_docx_file, compress_csv_file, compress_pdf_file,
    compress_audio_rle_file, compress_video_rle_file
)
from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
import matplotlib.pyplot as plt
import numpy as np
import wave

st.markdown("""
<style>
    .stTabs [data-baseweb="tab"] {
        color: white;
        text-decoration-color: white;
    }
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Main", "About"])

with tab1:
    st.set_page_config(page_title="Compressor", layout="centered")
    st.title("Files Compressor")
    st.write("Upload file(CSV,PDF,DOCX,TXT,IMG(JPG,JPEG,PNG),Audio(wav),Video(GIF,MP4,MOV)) here.")
    
    def display_compression_results(original_size, compressed_size):
        reduction = 100 * (1 - compressed_size / original_size)
        col1, col2, col3 = st.columns(3)
        col1.metric("Original Size", f"{original_size} bytes")
        col2.metric("Compressed Size", f"{compressed_size} bytes")
        col3.metric("Reduction Ratio", f"{reduction:.2f}%")
    
    def display_text_preview(text, title):
        st.subheader(title)
        st.text(text[:2000])
    
    def display_image_preview(image, caption):
        st.subheader(caption)
        st.image(image, use_container_width=True)
    
    def display_audio_preview(audio_array):
        plt.figure(figsize=(7, 5))
        plt.scatter(audio_array[:2500], range(2500), s=1)
        plt.xlabel("Amplitude")
        plt.ylabel("Size (Bytes)")
        plt.title("Original Audio")
        st.pyplot(plt)
        plt.close()
    
    def display_video_preview(frames,caption):
        gif_bytes = BytesIO()
        st.subheader(caption)
        frames[0].save(
            gif_bytes,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=100
        )
        st.image(gif_bytes.getvalue())
    
    uploaded_file = st.file_uploader(
        "Upload a file",
        type=["txt", "docx", "csv", "pdf", "png", "jpg", "jpeg", "wav", "mp4", "avi", "mov", "gif"]
    )
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        name, ext = filename.rsplit(".", 1)
        ext = ext.lower()
    
        if ext == "txt":
            compressed_data = compress_text(file_bytes)
            st.success("TXT compressed!")
            display_compression_results(len(file_bytes), len(compressed_data))
            display_text_preview(file_bytes.decode('latin1'), "Original Text")
            display_text_preview(compressed_data.decode('latin1', errors='replace'), "Compressed Preview")
            st.download_button("Download", compressed_data, file_name=name + "_compressed.bin")
    
        elif ext == "docx":
            compressed_data = compress_docx_file(file_bytes)
            st.success("DOCX compressed!")
            display_compression_results(len(file_bytes), len(compressed_data))
            try:
                docx_file = Document(BytesIO(file_bytes))
                full_text = "\n".join([para.text for para in docx_file.paragraphs])
                display_text_preview(full_text, "Original DOCX Text")
            except Exception as e:
                st.warning("Unable to extract text from DOCX: " + str(e))
            display_text_preview(compressed_data.decode('latin1', errors='replace'), "Compressed Preview")
            st.download_button("Download", compressed_data, file_name=name + "_compressed.bin")
    
        elif ext == "csv":
            compressed_data = compress_csv_file(file_bytes)
            st.success("CSV compressed!")
            display_compression_results(len(file_bytes), len(compressed_data))
            display_text_preview(file_bytes.decode('latin1'), "Original CSV")
            display_text_preview(compressed_data.decode('latin1', errors='replace'), "Compressed Preview")
            st.download_button("Download", compressed_data, file_name=name + "_compressed.bin")
    
        elif ext == "pdf":
            compressed_data = compress_pdf_file(file_bytes)
            st.success("PDF compressed!")
            display_compression_results(len(file_bytes), len(compressed_data))
            try:
                reader = PdfReader(BytesIO(file_bytes))
                pdf_text = ""
                for page in reader.pages:
                    pdf_text += page.extract_text() or ""
                display_text_preview(pdf_text, "Original PDF Text")
            except Exception as e:
                st.warning("Unable to extract PDF text: " + str(e))
            display_text_preview(compressed_data.decode('latin1', errors='replace'), "Compressed Preview")
            st.download_button("Download", compressed_data, file_name=name + "_compressed.bin")
    
        elif ext in ["png", "jpg", "jpeg"]:
            compressed_data = compress_image_file(file_bytes)
            st.success("Image compressed!")
            display_compression_results(len(file_bytes), len(compressed_data))
            image = Image.open(BytesIO(file_bytes))
            display_image_preview(image, "Original Image")
            gray = image.convert("L")
            display_image_preview(gray, "Grayscale Preview")
            st.download_button("Download", compressed_data, file_name=name + "_compressed.rle")
    
        elif ext == "wav":
            compressed_data = compress_audio_rle_file(file_bytes)
            st.success("Audio Compressed!")
            display_compression_results(len(file_bytes), len(compressed_data))
            try:
                with wave.open(BytesIO(file_bytes), 'rb') as wf:
                    frames = wf.readframes(wf.getnframes())
                    audio_array = np.frombuffer(frames, dtype=np.int16)
                display_audio_preview(audio_array)
            except Exception as e:
                st.warning("Unable to show original waveform: " + str(e))
            try:
                rle_bytes = compressed_data
                amplitudes = []
                rle_sizes = []
                i = 0
                run_index = 0
                while i < len(rle_bytes) - 2 and run_index < 500:
                    sample = int.from_bytes(rle_bytes[i:i+2], 'little', signed=True)
                    count = rle_bytes[i+2]
                    amplitudes.append(sample)
                    rle_sizes.append(run_index)
                    i += 3
                    run_index += 1
                plt.figure(figsize=(7, 5))
                plt.scatter(audio_array[:150], range(150), s=1)
                plt.xlabel("Amplitude")
                plt.ylabel("Size (Bytes)")
                plt.title("Compressed Audio")
                st.pyplot(plt)
                plt.close()
            except Exception as e:
                st.warning("Unable to show compressed waveform: " + str(e))
            st.download_button("Download Compressed Audio", compressed_data, file_name=name + "_compressed.rle")
    
        elif ext in ["mp4", "avi", "mov", "gif"]:
            try:
                compressed_data, color_frames, gray_frames = compress_video_rle_file(file_bytes)
                st.success("Video compressed!")
                display_compression_results(len(file_bytes), len(compressed_data))
                display_video_preview(color_frames,"Original preview")
                display_video_preview(gray_frames ,"Compressed preview")
                st.download_button("Download Compressed Video", compressed_data, file_name=name + "_compressed.rle")
            except Exception as e:
                st.error("Video compression failed: " + str(e))
    
with tab2:
    with open("ABout.txt", "r") as f:
        about_text = f.read()
    st.markdown(about_text)
    