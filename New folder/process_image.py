import cv2
from pathlib import Path
from tkinter import Tk, filedialog
import numpy as np

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

def apply_canny(img_bgr, low_thresh=100, high_thresh=200):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=low_thresh, threshold2=high_thresh)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    combined = cv2.addWeighted(img_bgr, 0.8, edges_colored, 0.2, 0)
    return combined

# ----------- Main Program -----------
def main():
    Tk().withdraw()
    image_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )

    if not image_path:
        print(" No image selected.")
        return

    img_path = Path(image_path)
    img = cv2.imread(str(img_path))
    if img is None:
        print(" Failed to load the image.")
        return

    outdir = Path("outputs")
    outdir.mkdir(parents=True, exist_ok=True)

    # إعدادات التحسين
    clip = 2.0
    tile = 8
    ksize = 5
    sigma = 0.0
    low = 100
    high = 200

    # --------- معالجة الصورة ---------
    enhanced = apply_clahe_bgr(img, clip_limit=clip, tile_grid_size=(tile, tile))
    enhanced = apply_gaussian_blur(enhanced, ksize=ksize, sigma=sigma)
    enhanced = apply_canny(enhanced, low_thresh=low, high_thresh=high)

    max_width = 500
    h, w = enhanced.shape[:2]
    if w > max_width:
        scale = max_width / w
        new_h = int(h * scale)
        enhanced = cv2.resize(enhanced, (max_width, new_h), interpolation=cv2.INTER_AREA)

    # حفظ وعرض الصورة
    base = img_path.stem
    out_final = outdir / f"{base}_enhanced.png"
    cv2.imwrite(str(out_final), enhanced)

    print(f" Enhanced image saved in: {out_final}")
    cv2.imshow("Enhanced Image", enhanced)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
