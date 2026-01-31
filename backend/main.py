from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import Response
from typing import Optional, List
from pydantic import BaseModel
from PIL import Image
import numpy as np
import io

app = FastAPI(title="Image Kernel Convolution Engine")

# Predefined kernels
KERNELS = {
    "blur": np.array([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]]),
    "sharpen": np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]),
    "edge": np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),
    "emboss": np.array([[-2,-1,0],[-1,1,1],[0,1,2]])
}

class CustomKernel(BaseModel):
    kernel: Optional[List[List[float]]] = None

def apply_convolution(image_array, kernel):
    h, w = image_array.shape
    k = kernel.shape[0]
    pad = k // 2

    padded = np.pad(image_array, pad, mode="edge")
    output = np.zeros_like(image_array)

    for i in range(h):
        for j in range(w):
            region = padded[i:i+k, j:j+k]
            output[i, j] = np.sum(region * kernel)

    return np.clip(output, 0, 255)

@app.get("/kernels/list")
def list_kernels():
    return {"kernels": list(KERNELS.keys()) + ["custom"]}

@app.post("/transform/convolution")
async def convolution_endpoint(
    image: UploadFile = File(...),
    kernel_name: str = Query("blur"),
    custom_kernel: str | None = Query(None)
):

    image_bytes = await image.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("L")
    img = img.resize((256, 256))

    img_array = np.array(img, dtype=np.float32)

    if kernel_name == "custom":
        if not custom_kernel:
            raise ValueError("Custom kernel not provided")

        kernel_list = eval(custom_kernel)
        kernel = np.array(kernel_list)
    else:
        kernel = KERNELS[kernel_name]



    result = apply_convolution(img_array, kernel)
    result_img = Image.fromarray(result.astype(np.uint8))

    buf = io.BytesIO()
    result_img.save(buf, format="PNG")

    return Response(content=buf.getvalue(), media_type="image/png")
