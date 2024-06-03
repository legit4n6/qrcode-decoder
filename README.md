# QR Code Decoder

This project is a Python script designed to extract and decode QR codes from various file types, including PDFs, HTML files, and image files. This can be particularly useful in cybersecurity scenarios, such as analyzing phishing emails that contain malicious QR codes.

## Requirements

- PyMuPDF
- pyzbar
- Pillow
- beautifulsoup4

You can install the required libraries using the following command:
```sh
pip install -r requirements.txt
```

## Usage
To use the script, run the following command:
```
python qrcode-decoder.py <file_path>
```

Replace `<file_path>` with the path to the PDF, HTML, or image file you want to process.

## Example
```
python qrcode-decoder.py example.pdf
```

## How It Works
1. Extract Images from PDF: The script uses PyMuPDF to extract all images from the provided PDF file.

2. Extract Images from HTML: The script uses BeautifulSoup to parse the HTML file and extract image URLs. It downloads the images and processes them.

3. Decode QR Code: The script converts the extracted images to a NumPy array and decodes any QR codes using the pyzbar library.

4. The output will be a defanged URL such as: `[https[:]//bad[.]example[.]com]`

## Supported File Types
* PDF
* HTML
* Common image formats (JPG, JPEG, PNG, BMP, GIF)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
