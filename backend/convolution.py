import numpy as np

def apply_convolution(image_array, kernel):
    """
    Applies convolution to a grayscale image using a given kernel.
    Implemented from scratch using NumPy.
    """

    kernel = np.array(kernel)
    image_array = image_array.astype(float)

    k_height, k_width = kernel.shape
    pad_h = k_height // 2
    pad_w = k_width // 2

    # Pad image to handle borders
    padded_image = np.pad(
        image_array,
        ((pad_h, pad_h), (pad_w, pad_w)),
        mode="edge"
    )

    output = np.zeros_like(image_array)

    # Convolution operation
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            region = padded_image[i:i+k_height, j:j+k_width]
            output[i, j] = np.sum(region * kernel)

    # Clip values to valid image range
    return np.clip(output, 0, 255)
