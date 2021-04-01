import requests as rq
import json
from io import BytesIO, StringIO
from PIL import Image
import matplotlib.pyplot as plt


def print_one_image():
    png_url = "http://httpbin.org/image/png"
    r = rq.get(png_url)
    f = BytesIO(r.content)
    img = Image.open(f)
    print(img.size)
    img.show()
    plt.figure("show angone image")
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    print_one_image()
