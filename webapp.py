import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
import base64

def main():
    st.set_page_config(page_title="PalMira",
                       page_icon="./Images/icon.png", layout="centered")

    # Increase letter size of the title
    st.markdown("<h1 style='text-align: center; color: #87CEEB; font-style: italic; font-size: 90px;'>PalMira</h1>", unsafe_allow_html=True)
    
    # Catchy line
    st.markdown("<p style='text-align: center;color: #3A3B3C;font-size: 25px;'>Here Art Thou, All Lively and Lone", unsafe_allow_html=True)

    # Example Image
    st.image(image=r"./Images/demo2.gif", use_column_width=True)
    st.markdown("</br>", unsafe_allow_html=True)
    
    # Display sections for style image, content image, and synthesized image
    col1, col2, col3 = st.columns(3)

    # Boolean flags to track whether images are uploaded
    style_uploaded = False
    content_uploaded = False

    # Session state variables
    if 'content_image_original' not in st.session_state:
        st.session_state.content_image_original = None
    if 'content_image_current' not in st.session_state:
        st.session_state.content_image_current = None
    if 'enhancement_type' not in st.session_state:
        st.session_state.enhancement_type = "Original"

    with col1:
        st.markdown("<h2 style='text-align: center;'>Style <br> Image</h2>", unsafe_allow_html=True)
        # Placeholder for style image display
        placeholder_img = st.empty()  # Placeholder for style image
        style_image = st.file_uploader("Upload Style Image", type=["jpg", "jpeg", "png"])

        # Display uploaded style image or placeholder image
        if style_image is not None:
            placeholder_img.image(style_image, use_column_width=True)
            style_uploaded = True

    with col2:
        st.markdown("<h2 style='text-align: center;'>Content Image</h2>", unsafe_allow_html=True)
        # Placeholder for content image display
        placeholder_img2 = st.empty()  # Placeholder for content image
        content_image = st.file_uploader("Upload Content Image", type=["jpg", "jpeg", "png"])

        # Display uploaded content image or placeholder image
        if content_image is not None:
            img = Image.open(content_image)

            if not content_uploaded:
                st.session_state.content_image_original = img
                st.session_state.content_image_current = img

            # Image enhancement options
            st.header("Image Enhancement Options")

            # Option to select enhancement type
            enhancement_type = st.radio("Select Enhancement Type", ["Original", "Gray Scale", "Contrast", "Brightness", "Blur", "Sharpness", "Silhouette", "Invert Silhouette"])

            # Apply selected enhancement
            if enhancement_type != st.session_state.enhancement_type:
                st.session_state.enhancement_type = enhancement_type

            if enhancement_type == "Original":
                img = st.session_state.content_image_original
            elif enhancement_type == "Gray Scale":
                img = st.session_state.content_image_current.convert('L')
            elif enhancement_type == "Contrast":
                contrast_factor = st.slider("Contrast Factor", 0.0, 2.0, 1.0)
                enhancer = ImageEnhance.Contrast(st.session_state.content_image_current)
                img = enhancer.enhance(contrast_factor)
            elif enhancement_type == "Brightness":
                brightness_factor = st.slider("Brightness Factor", 0.0, 2.0, 1.0)
                enhancer = ImageEnhance.Brightness(st.session_state.content_image_current)
                img = enhancer.enhance(brightness_factor)
            elif enhancement_type == "Blur":
                blur_radius = st.slider("Blur Radius", 0, 10, 2)
                img = st.session_state.content_image_current.filter(ImageFilter.GaussianBlur(blur_radius))
            elif enhancement_type == "Sharpness":
                sharpness_factor = st.slider("Sharpness Factor", 0.0, 2.0, 1.0)
                enhancer = ImageEnhance.Sharpness(st.session_state.content_image_current)
                img = enhancer.enhance(sharpness_factor)
            elif enhancement_type == "Silhouette":
                img = create_silhouette(st.session_state.content_image_current)
            elif enhancement_type == "Invert Silhouette":
                img = create_inverted_silhouette(st.session_state.content_image_current)

            placeholder_img2.image(img, use_column_width=True)
            content_uploaded = True

            # Save, undo, apply, and download buttons
            if content_uploaded:
                col2_col1, col2_col2, col2_col3 = st.columns(3)
                if col2_col1.button("Save"):
                    # Save the enhanced image as the original content image
                    st.session_state.content_image_original = img
                    st.session_state.content_image_current = img
                    content_image_path = content_image.name
                    img.save(content_image_path)
                    st.success("Content image enhancements saved successfully!")
                if col2_col2.button("Undo"):
                    # Revert to the original content image
                    img = st.session_state.content_image_original
                    st.session_state.content_image_current = img
                    st.success("Content image reverted to original state!")
                if col2_col3.button("Apply"):
                    # Apply the enhancement to the original content image
                    st.session_state.content_image_current = img
                    st.success("Content image enhancement applied!")
                if st.button("Download"):
                    # Download the enhanced image
                    download_img(img, "enhanced_image.png")

    with col3:
        st.markdown("<h2 style='text-align: center;'>Synthesized Image</h2>", unsafe_allow_html=True)
        # Placeholder for synthesized image display
        placeholder_img3 = st.empty()  # Placeholder for synthesized image
        # Placeholder for synthesized image. You can add your synthesis process here

def create_silhouette(image):
    # Convert image to grayscale
    gray_image = image.convert('L')
    # Thresholding to create a binary image
    threshold_value = 128
    silhouette_image = gray_image.point(lambda p: p > threshold_value and 255)
    return silhouette_image

def create_inverted_silhouette(image):
    # Convert image to grayscale
    gray_image = image.convert('L')
    # Thresholding to create a binary image
    threshold_value = 128
    silhouette_image = gray_image.point(lambda p: p > threshold_value and 255)
    # Invert the silhouette image
    inverted_image = ImageOps.invert(silhouette_image)
    return inverted_image

def download_img(img, filename):
    # Save the image to a byte stream
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    # Encode the image data to base64
    img_base64 = base64.b64encode(img_byte_array.getvalue()).decode()
    # Offer the image for download
    href = f'<a href="data:image/png;base64,{img_base64}" download="{filename}">Download Image</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
