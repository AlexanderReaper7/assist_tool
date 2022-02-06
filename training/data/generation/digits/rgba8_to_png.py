# convert rgba8 to png image
import numpy as np
from PIL import Image
from pathlib import Path

path_prefix = Path(__file__).parent.absolute().__str__() + "\\mask_"

width = 35
height = 50

for i in range(10):
    path = path_prefix + str(i) + ".rgba8"
    print("converting " + path)
    with open(path, "rb") as f:
        img = np.fromfile(f, dtype=np.uint8)
    img = img.reshape((height, width, 4))
    img = Image.fromarray(img)
    img.save(path_prefix + str(i) + "_converted.png", format="PNG")
