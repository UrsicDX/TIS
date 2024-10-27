import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from math import sqrt, cos, pi


def dct(input_signal):
    size = input_signal.shape[0]
    dct_output = np.zeros_like(input_signal, dtype=float)

    for i in range(size):
        c = sqrt(2 / size) if i == 0 else sqrt(1 / (2 * size))
        sum_val = 0
        for j in range(size):
            sum_val += input_signal[j] * cos(pi * (2 * j + 1) * i / (2 * size))
        dct_output[i] = c * sum_val

    return dct_output


def idct(dct_signal):
    size = dct_signal.shape[0]
    output = np.zeros_like(dct_signal, dtype=float)

    for i in range(size):
        c = sqrt(2 / size) if i == 0 else sqrt(1 / (2 * size))
        sum_val = 0
        for j in range(size):
            sum_val += dct_signal[j] * c * \
                cos(pi * (2 * j + 1) * i / (2 * size))
        output[i] = sum_val

    return output


def dct2(block):
    """Performs 2D DCT on the input block."""
    return np.array([dct(row) for row in block]).T


def idct2(block):
    """Performs 2D IDCT on the input block."""
    return np.array([idct(row) for row in block]).T


def quantize_coefficients(coefficients, q_matrix):
    # Perform forward quantization
    coefficients -= 128
    coefficients_quant = np.round(coefficients / q_matrix) * q_matrix
    # Perform inverse quantization
    coefficients_quant += 128
    return coefficients_quant


def naloga4(slika: np.array, velikostOkna: int) -> float:
    """
    Simplify the image using DCT, quantization and calculate PSNR.
    """
    H, W = slika.shape
    N = velikostOkna
    q_matrix = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                         [12, 12, 14, 19, 26, 58, 60, 55],
                         [14, 13, 16, 24, 40, 57, 69, 56],
                         [14, 17, 22, 29, 51, 87, 80, 62],
                         [18, 22, 37, 56, 68, 109, 103, 77],
                         [24, 35, 55, 64, 81, 104, 113, 92],
                         [49, 64, 78, 87, 103, 121, 120, 101],
                         [72, 92, 95, 98, 112, 100, 103, 99]])

    # Ensure the quantization matrix matches the block size
    if q_matrix.shape[0] != N or q_matrix.shape[1] != N:
        raise ValueError("Quantization matrix size does not match block size")

    # DCT and Quantization
    blocks = [slika[i:i+N, j:j+N]
              for i in range(0, H, N) for j in range(0, W, N)]
    reconstructed_image = np.zeros_like(slika)

    for idx, block in enumerate(blocks):
        if block.shape[0] == N and block.shape[1] == N:
            dct_block = dct2(block)
            quantized_block = quantize_coefficients(dct_block, q_matrix)
            idct_block = idct2(quantized_block)
            i, j = (idx // (W // N)) * N, (idx % (W // N)) * N
            reconstructed_image[i:i+N, j:j+N] = idct_block

    # Calculate PSNR
    mse = np.mean((slika - reconstructed_image) ** 2)
    psnr = 20 * np.log10(255) - 10 * np.log10(mse)
    return psnr


# Load the image
image_path = r'C:\Users\domin\Desktop\Tis\TIS-DN4\primeri\slike\1.png'
image = Image.open(image_path).convert(
    'L')  # Convert to grayscale if necessary
image_array = np.array(image)

# Calculate PSNR and show the quantization matrix
psnr_value = naloga4(image_array, 8)
print(f"PSNR: {psnr_value}")

# Display the image
plt.imshow(image_array, cmap='gray')
plt.title("Original Image")
plt.show()
