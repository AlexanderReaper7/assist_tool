# use the digit masks and background samples to generate the data
import numpy as np
from PIL import Image
from pathlib import Path
import time

def tint_image(img, color):
    img = np.array(img)
    img = img.astype(np.float32)
    img[:, :, 0] = img[:, :, 0] * color[0]
    img[:, :, 1] = img[:, :, 1] * color[1]
    img[:, :, 2] = img[:, :, 2] * color[2]
    img = img.astype(np.uint8)
    img = Image.fromarray(img)
    return img

def u8_color_to_f32(u8):
    return u8 / 255.0

DIGIT_DIMENSIONS = (50, 35, 4)
Y_OFFSET = 1.3
X_OFFSET = -12
print("loading digit masks")
DIGIT_MASKS = [Image.open(Path(__file__).parent.absolute().__str__() + "\\digits\\mask_" + str(i) + ".png") for i in range(10)]
HEALTH_STATES = ["normal", "overshields", "no shields", "invulnerable", "dead", "scrambled"]
NORMAL_HEALTH_COLOR = (255, 49, 65)
NORMAL_SHIELD_COLOR = (0, 255, 255)
OVERSHIELD_COLOR = (255, 0, 255)
INVULNERABLE_HEALTH_COLOR = (170, 170, 170)
INVULNERABLE_SHIELD_COLOR = (255, 255, 255)
print("tiniting digits")
tinted_digits = [[tint_image(digit.copy(), (u8_color_to_f32(red),u8_color_to_f32(green),u8_color_to_f32(blue))) for digit in DIGIT_MASKS] for (red, green, blue) in [NORMAL_HEALTH_COLOR, NORMAL_SHIELD_COLOR, OVERSHIELD_COLOR, INVULNERABLE_HEALTH_COLOR, INVULNERABLE_SHIELD_COLOR]]

IMAGE_DIMENSIONS = (305, 58, 3)
BACKGROUNDS_COUNT = 43
BACKGROUNDS_DIMENSIONS = (3840, 2160)
print("loading backgrounds")
BACKGROUNDS = [Image.open(Path(__file__).parent.absolute().__str__() + "\\backgrounds\\bg_" + str(i) + ".png") for i in range(1, BACKGROUNDS_COUNT)]

def get_synthetic_sample():
    # first time setup
    # repeat
    while True:
        # print("generating sample")
        # get a random sampling of the backgrounds
        background_num = np.random.randint(0, BACKGROUNDS_COUNT-1)
        # print("background: " + str(background_num))
        background = BACKGROUNDS[background_num]
        x = np.random.randint(0, BACKGROUNDS_DIMENSIONS[0]-IMAGE_DIMENSIONS[0])
        y = np.random.randint(0, BACKGROUNDS_DIMENSIONS[1]-IMAGE_DIMENSIONS[1])
        # print("x: " + str(x) + " y: " + str(y))
        image = background.crop((x, y, x+IMAGE_DIMENSIONS[0], y+IMAGE_DIMENSIONS[1]))
        # generate a random shield and health value
        health = np.random.randint(1, 1999) # TODO: use a distribution that is more likely to be a real value# split number generation into basenumber of 1 to 999 times 1 to 10 with probablility distribution
        shields = np.random.randint(0, 1999) # TODO: use a distribution that is more likely to be a real value# split number generation into basenumber of 1 to 999 times 1 to 10 with probablility distribution
        # health = 1290
        # shields = 1300
        digit_count = 0
        for state in (0, 1):
            if state == 0:
                value = health
            else:
                value = shields
            digits = [int(d) for d in str(value)] 
            for digit in reversed(digits):
                image.paste(tinted_digits[state][digit], (IMAGE_DIMENSIONS[0]-((DIGIT_DIMENSIONS[0]+X_OFFSET) * digit_count)-DIGIT_DIMENSIONS[0]+16, int(Y_OFFSET*digit_count)), tinted_digits[state][digit])
                digit_count += 1
        # print("health: " + str(health) + " shield: " + str(shields))
        yield (image, health, shields, background_num, x, y)
    
def show_test_samples(count):
    for i, sample in enumerate(get_synthetic_sample()):
        (image, health, shields) = sample
        image.show(title="health: " + str(health) + " shield: " + str(shields) + " offset_x: " + str(X_OFFSET) + " offset_y: " + str(Y_OFFSET))
        if i >= count:
            break

def save_training_data(count):
    start = time.time()
    print("starting to save training data")
    for i, sample in enumerate(get_synthetic_sample()):
        print("saving sample " + str(i))
        (image, health, shields, background, x, y) = sample
        image.save(Path(__file__).parent.parent.absolute().__str__() + "\\generated_health\\" + "h" + str(health) + "s" + str(shields) + "b" + str(background) + "x" + str(x) + "y" + str(y) + ".png")
        if i >= count:
            break
    end = time.time()
    print("finished saving training data in " + str(end-start) + " seconds")


save_training_data(59000)