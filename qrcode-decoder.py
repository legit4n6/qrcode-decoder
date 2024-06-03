import fitz  # PyMuPDF
from PIL import Image
import io
import numpy as np
from pyzbar.pyzbar import decode
from bs4 import BeautifulSoup
import os
import sys
import re

def extract_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)
        
        for img in image_list:
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            images.append(image)

    return images

def extract_images_from_html(html_path):
    with open(html_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    images = []
    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        if img_src and not img_src.startswith('http'):
            image_path = os.path.join(os.path.dirname(html_path), img_src)
            if os.path.exists(image_path):
                image = Image.open(image_path).convert("RGB")
                images.append(image)

    return images

def decode_qr_from_image(image):
    image_np = np.array(image)
    decoded_objects = decode(image_np)

    qr_data = []
    for obj in decoded_objects:
        qr_data.append(obj.data.decode('utf-8'))
    
    return qr_data

def defang_url(url):
    defanged_url = re.sub(r'\.', '[.]', url)
    defanged_url = re.sub(r':', '[:]', defanged_url)
    return defanged_url

def process_file(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    images = []

    if file_ext == '.pdf':
        images = extract_images_from_pdf(file_path)
    elif file_ext == '.html' or file_ext == '.htm':
        images = extract_images_from_html(file_path)
    elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        image = Image.open(file_path).convert("RGB")
        images.append(image)
    else:
        print(f"Unsupported file type: {file_ext}")
        return

    for i, image in enumerate(images):
        qr_data = decode_qr_from_image(image)
        if qr_data:
            defanged_data = [defang_url(data) for data in qr_data]
            print(f"QR code data from image {i+1}: {defanged_data}")
        else:
            print(f"No QR code found in image {i+1}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python qrcode-decoder.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    process_file(file_path)
