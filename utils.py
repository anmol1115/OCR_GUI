import os
import socket
import pyqrcode
from PIL import Image

QR_CODE_FOLDER = "./images/qr_code"

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def get_qr_code(ip):
    url = f"http://{ip}:8080/upload"
    qr = pyqrcode.create(url)

    qr.png(os.path.join(QR_CODE_FOLDER, "0.png"), scale=6)

def get_file_names(path):
    res = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return res

def create_project_fs():
    try:
        os.makedirs("./images/qr_code")
    except:
        pass

    try:
        os.makedirs("./files")
    except:
        pass

def scale_image(path, max_width=1000, max_height=1000):
    img = Image.open(path)
    width, height = img.size

    if width > max_width or height > max_height:
        aspect_ratio = width / height
        new_width = min(max_width, int(max_height*aspect_ratio))
        new_height = min(max_height, int(max_width/aspect_ratio))

        img = img.resize((new_width, new_height))

        return img
    return img


if __name__ == "__main__":
    # files = get_file_names("./images")
    # print(files)

    scale_image("./images/IMG_0236.png")