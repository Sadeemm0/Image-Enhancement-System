# Image Enhancement System

**Course Project – Image Processing**

---

## Overview
This project is a simple web-based application that allows users to upload an image and apply basic enhancement techniques. The system is built using Python, Flask, OpenCV, and HTML, with the CSS embedded directly in the HTML file.

---

## Features
- **Contrast Enhancement (CLAHE):** Improves overall image contrast.
- **Smoothing (Gaussian Blur):** Reduces noise and smooths the image.
- **Edge Detection (Canny):** Extracts edges and important structures.
- **Web Interface:** User-friendly page built with HTML and internal CSS.

---

## Installation
1. Download or clone the project:
   ```
   git clone https://github.com/Sadeemm0/Image-Enhancement-System.git
   cd Image
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

---

## Usage
1. Run the application:
   ```
   python app.py
   ```

2. Open the browser at:
   ```
   http://127.0.0.1:5000/
   ```

3. Upload an image and select the desired enhancement method.

---

## Project Structure
```
Image Enhancement System/
├── app.py
├── templates/
│   └── index.html   # Contains HTML + internal CSS
├── README.md
└── requirements.txt
```

