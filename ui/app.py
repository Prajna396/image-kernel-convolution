import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Image Kernel Convolution Engine")

st.title("🖼️ Image Kernel Convolution Engine")
st.write("Upload an image, select a kernel, and view the transformed output.")

# Upload image
uploaded_file = st.file_uploader(
    "Upload Image (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"]
)

# Kernel selection
kernel = st.selectbox(
    "Choose Kernel",
    ["blur", "sharpen", "edge", "emboss", "custom"]
)

# Predefined kernel descriptions
kernel_info = {
    "blur": "Smooths the image by averaging neighboring pixels.",
    "sharpen": "Enhances edges and details.",
    "edge": "Detects edges in the image.",
    "emboss": "Creates a 3D embossed effect.",
    "custom": "User-defined custom convolution kernel."
}

st.info(kernel_info[kernel])

# Kernel matrices
kernel_matrices = {
    "blur": [[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]],
    "sharpen": [[0,-1,0],[-1,5,-1],[0,-1,0]],
    "edge": [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]],
    "emboss": [[-2,-1,0],[-1,1,1],[0,1,2]]
}

custom_kernel = None

# Show kernel matrix
if kernel != "custom":
    st.write("### Kernel Matrix")
    st.table(kernel_matrices[kernel])
else:
    st.write("### Enter Custom Kernel (3×3 or 5×5)")
    st.caption("Example:\n1 0 -1\n1 0 -1\n1 0 -1")

    kernel_text = st.text_area("Kernel Matrix")

    if kernel_text:
        try:
            custom_kernel = [
                list(map(float, row.split()))
                for row in kernel_text.strip().split("\n")
            ]
            st.write("### Custom Kernel Matrix")
            st.table(custom_kernel)
        except:
            st.error("Invalid format. Use space-separated numbers.")

if uploaded_file and st.button("Apply Convolution 🚀"):

    files = {"image": uploaded_file}
    params = {"kernel_name": kernel}

    if kernel == "custom":
        if custom_kernel is None:
            st.error("Please enter a valid custom kernel.")
            st.stop()
        params["custom_kernel"] = str(custom_kernel)

    with st.spinner("Applying convolution..."):
        response = requests.post(
            "http://127.0.0.1:8000/transform/convolution",
            files=files,
            params=params
        )

    # ✅ response is guaranteed to exist here
    if response.status_code == 200:
        st.subheader("Results")

        col1, col2 = st.columns(2)

        with col1:
            st.image(uploaded_file, caption="Original Image", use_container_width=True)

        with col2:
            result_image = Image.open(io.BytesIO(response.content))
            st.image(result_image, caption="Transformed Image", use_container_width=True)

        st.download_button(
            "Download Transformed Image",
            response.content,
            file_name="output.png",
            mime="image/png"
        )
    else:
        st.error("Error applying convolution")
