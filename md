# Image Kernel Convolution Engine – Backend Assessment

## Overview
This project implements an image kernel convolution engine where convolution is performed
from scratch using NumPy. The goal of the project is to demonstrate understanding of
matrix operations, image processing concepts, and backend API design.

The application includes:
- A FastAPI backend for image processing
- A Streamlit web application for visual interaction

---

## Tech Stack
- Python
- FastAPI
- NumPy
- Pillow (PIL)
- Streamlit

---

## Features
- Upload images (JPG, PNG, JPEG)
- Apply pre-built convolution kernels:
  - Blur
  - Sharpen
  - Edge Detection
  - Emboss
- Visual comparison of original and transformed images
- Download transformed image
- Clean and modular code structure

---

## Convolution Approach
- Images are converted to grayscale
- Represented as NumPy arrays
- Convolution is implemented manually using a sliding window approach
- Zero padding is used to handle image borders
- No OpenCV or high-level convolution functions are used

---

## Project Structure
```text
image_convolution_test/
├── convolution.py
├── main.py
├── streamlit_app.py
├── convolution_test.py
├── screenshots/
├── requirements.txt
├── README.md
```
---

## How to Run the Project

### Install Dependencies
pip install -r requirements.txt

### Run FastAPI Backend
python -m uvicorn main:app --reload

### Run Streamlit Web Application
python -m streamlit run streamlit_app.py

---

## Screenshots

### Image Upload:
![HomePage](Screenshots/Image_Upload.png)

### Kernel Selection:
![Kernel Selection](Screenshots/kernel_Selection.png)

### Custom Kernel Matrix:
![Custom Kernel Matrix](Screenshots/Custom_Kernel_Matrixe.png)

Original Image:
![Original Image](Screenshots/Original_Image.png)

Convolution Output:
![Convolution Output](Screenshots/Convolution_Output.png)

---

## Time Taken
Approximately 6 hours including learning, implementation, testing, and documentation.