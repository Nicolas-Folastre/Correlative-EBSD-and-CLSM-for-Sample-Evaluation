import numpy as np
from PIL import Image

# Generate a small float image in Numpy array
grey32 = np.random.randn(4096,4096).astype(np.float32)                                           

# Convert to PIL Image and save
Image.fromarray(grey32).save('test.tif')                                                   

# Read back from disk and convert to Numpy array
reloaded = np.array(Image.open('test.tif'))  