import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct


def dct2(block):
    """Apply 2D DCT."""
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def idct2(block):
    """Apply 2D IDCT."""
    return idct(idct(block.T, norm='ortho').T, norm='ortho')


def quantize(block, q_matrix):
    """Quantize the block using a quantization matrix."""
    return np.round(block / q_matrix) * q_matrix


def calculate_psnr(original, reconstructed):
    """Calculate the PSNR between two images."""
    mse = np.mean((original - reconstructed) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel) - 10 * np.log10(mse)
    return psnr


def process_blocks(image, block_size, func, q_matrix=None):
    """Process all blocks of the image with the specified function."""
    h, w = image.shape
    processed_image = np.zeros_like(image)
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i+block_size, j:j+block_size]
            if block.shape == (block_size, block_size):
                processed_block = func(block)
                if q_matrix is not None:
                    processed_block = quantize(processed_block, q_matrix)
                processed_image[i:i+block_size,
                                j:j+block_size] = processed_block
    return processed_image


def main(image_path, block_size):
    # Load and convert image to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)

    # Define quantization matrix
    # Example quantization matrix
    q_matrix = np.full((block_size, block_size), 50)

    # Process the image
    dct_blocks = process_blocks(img_array, block_size, dct2)
    quantized_blocks = process_blocks(
        dct_blocks, block_size, lambda x: quantize(x, q_matrix))
    idct_blocks = process_blocks(quantized_blocks, block_size, idct2)

    # Calculate PSNR
    psnr = calculate_psnr(img_array, idct_blocks)
    print("PSNR:", psnr)

    # Display images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(img_array, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(idct_blocks, cmap='gray')
    plt.title('Reconstructed Image')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(np.abs(img_array - idct_blocks), cmap='hot')
    plt.title('Difference')
    plt.axis('off')

    plt.show()


if __name__ == "__main__":
    image_path = r'primeri\slike\1.png'  # Correct path to your image
    main(image_path, block_size=4)  # Example block size
