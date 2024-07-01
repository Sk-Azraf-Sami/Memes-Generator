import numpy as np
from PIL import Image

def create_gaussian_kernel(kernel_size, sigma):
    """Create a Gaussian kernel."""
    ax = np.linspace(-(kernel_size - 1) / 2., (kernel_size - 1) / 2., kernel_size)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))
    return kernel / np.sum(kernel)

def apply_kernel(img, kernel):
    """Apply a convolution kernel to an image with padding to avoid black borders."""
    radius = kernel.shape[0] // 2
    height, width = img.shape[:2]
    # For simplicity, convert to float and normalize
    img = img.astype(np.float32) / 255
    
    # Pad the image to handle borders
    padded_img = np.pad(img, ((radius, radius), (radius, radius), (0, 0)), mode='reflect')
    
    # Output image
    blurred = np.zeros_like(padded_img)
    
    # Apply kernel to each pixel in the padded image
    for y in range(radius, height + radius):
        for x in range(radius, width + radius):
            for c in range(padded_img.shape[2]):
                blurred[y, x, c] = np.sum(padded_img[y-radius:y+radius+1, x-radius:x+radius+1, c] * kernel)
    
    # Remove padding from the blurred image
    blurred = blurred[radius:-radius, radius:-radius]
    
    # Convert back to 8-bit values
    blurred = np.clip(blurred * 255, 0, 255).astype(np.uint8)
    return blurred

def gaussian_blur(kernel_size, sigma, image_path):
    # Open the image with PIL and convert to a NumPy array
    img = np.array(Image.open(image_path))
    
    # Ensure kernel size is odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # Create Gaussian kernel
    kernel = create_gaussian_kernel(kernel_size, sigma)
    
    # Apply Gaussian blur
    if len(img.shape) == 2:  # Grayscale image
        blurred_img = apply_kernel(img.reshape(img.shape[0], img.shape[1], 1), kernel)
        blurred_img = blurred_img.reshape(img.shape[0], img.shape[1])
    else:  # Color image
        blurred_img = apply_kernel(img, kernel)
    
    # Save the blurred image
    meme_path = 'static/latest.jpg'
    Image.fromarray(blurred_img).save(meme_path)
    
    return meme_path