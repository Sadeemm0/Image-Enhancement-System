import cv2
import numpy as np
from flask import Flask, render_template, request
import base64

app = Flask(__name__)

# ----------- Helper Functions -----------
def apply_clahe_bgr(img_bgr, clip_limit=2.0, tile_grid_size=(8, 8)):
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l_eq = clahe.apply(l)
    lab_eq = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

def apply_gaussian_blur(img_bgr, ksize=5, sigma=0):
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(img_bgr, (ksize, ksize), sigmaX=sigma, sigmaY=sigma)

def apply_canny_enhanced(img_bgr, low_thresh=100, high_thresh=200):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=low_thresh, threshold2=high_thresh)
    return edges

# ----------- Main Page -----------
@app.route('/', methods=['GET', 'POST'])
def index():
    processed_img = None
    original_img = None
    error = None

    if request.method == 'POST':
        if 'image' not in request.files:
            error = "No image uploaded"
        else:
            image_file = request.files['image']
            if image_file.filename == '':
                error = "Please select an image first"
            else:
                file_bytes = np.frombuffer(image_file.read(), np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                if img is None:
                    error = "Please upload a valid image file"
                else:
                    enhanced = img.copy()
                    techniques = request.form.getlist('technique')

                    # حالة Canny وحده
                    if "canny" in techniques and len(techniques) == 1:
                        edges = apply_canny_enhanced(enhanced)
                        enhanced = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # خلفية سوداء وحواف بيضاء
                    else:
                        if "blur" in techniques:
                            enhanced = apply_gaussian_blur(enhanced)
                        if "clahe" in techniques:
                            enhanced = apply_clahe_bgr(enhanced)
                        if "canny" in techniques:
                            edges = apply_canny_enhanced(enhanced)
                            enhanced[edges != 0] = [255, 255, 255]

                    # تعديل حجم الصورة للعرض
                    max_width = 500
                    h, w = enhanced.shape[:2]
                    if w > max_width:
                        scale = max_width / w
                        new_h = int(h * scale)
                        enhanced = cv2.resize(enhanced, (max_width, new_h), interpolation=cv2.INTER_LINEAR)
                        img_display = cv2.resize(img, (max_width, new_h), interpolation=cv2.INTER_LINEAR)
                    else:
                        img_display = img

                    # تحويل الصور للعرض في HTML
                    _, buffer1 = cv2.imencode('.png', img_display)
                    _, buffer2 = cv2.imencode('.png', enhanced)
                    original_img = base64.b64encode(buffer1).decode('utf-8')
                    processed_img = base64.b64encode(buffer2).decode('utf-8')

    return render_template(
        'index.html',
        processed_img=processed_img,
        original_img=original_img,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)
