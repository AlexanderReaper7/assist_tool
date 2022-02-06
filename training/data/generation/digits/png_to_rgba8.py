# convert png image to rgba8
import numpy as np
from PIL import Image
import os
from pathlib import Path

path_prefix = Path(__file__).parent.absolute().__str__() + "\\mask_"

# print current working directory


for i in range(10):
    path = path_prefix + str(i) + ".png"
    print("converting " + path)
    img = Image.open(path)
    img = np.array(img)
    img = img.astype(np.uint8)
    with open(path_prefix + str(i) + ".rgba8", "wb") as f:
        f.write(img.tobytes())