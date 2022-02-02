import numpy as np
from PIL import Image
from pathlib import Path

# tint image with a color leave alpha channel intact
def tint_image(img, color):
    img = np.array(img)
    img = img.astype(np.float32)
    img[:, :, 0] = img[:, :, 0] * color[0]
    img[:, :, 1] = img[:, :, 1] * color[1]
    img[:, :, 2] = img[:, :, 2] * color[2]
    img = img.astype(np.uint8)
    img = Image.fromarray(img)
    return img

# load and tint all mask images
path_prefix = Path(__file__).parent.absolute().__str__() + "\\mask_"

for i in range(10):
    path = path_prefix + str(i) + ".png"
    print("converting " + path)
    img = Image.open(path)
    img = tint_image(img, (1, 0, 0))
    img.show()