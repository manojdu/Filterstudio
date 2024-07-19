import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess  # For opening the file explorer

# Apply vivid effect to the image
def apply_vivid(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = hsv[..., 1] * 1.5  # Increase saturation
    img_vivid = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img_vivid

# Apply dramatic effect by enhancing contrast
def apply_dramatic(img):
    img_vivid = apply_vivid(img)
    img_dramatic = cv2.convertScaleAbs(img_vivid, alpha=1.5, beta=30)  # Increase contrast
    return img_dramatic

# Apply retro effect with sepia filter and vignette
def apply_retro(img):
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    img_sepia = cv2.transform(img, sepia_filter)
    img_sepia = np.clip(img_sepia, 0, 255)
    
    color_fade = np.full_like(img_sepia, (30, 20, 10), dtype=np.uint8)
    img_retro = cv2.addWeighted(img_sepia, 0.8, color_fade, 0.2, 0)
    
    # Create vignette effect
    rows, cols, _ = img_retro.shape
    vignette = np.zeros((rows, cols), dtype=np.uint8)
    cv2.circle(vignette, (cols // 2, rows // 2), min(rows, cols) // 2, 255, -1)
    vignette = cv2.GaussianBlur(vignette, (21, 21), 0)
    vignette = cv2.cvtColor(vignette, cv2.COLOR_GRAY2BGR)
    img_retro = cv2.addWeighted(img_retro, 0.9, vignette, 0.1, 0)
    
    return img_retro

# Apply silvertone effect (grayscale)
def apply_silvertone(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_silvertone = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    return img_silvertone

# Apply sketch effect
def apply_sketch(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_inv = 255 - img_gray
    img_blur = cv2.GaussianBlur(img_gray_inv, (21, 21), 0)
    img_sketch = cv2.divide(img_gray, 255 - img_blur, scale=256)
    return img_sketch

# Apply blur effect
def apply_blur(img):
    img_blur = cv2.GaussianBlur(img, (15, 15), 0)
    return img_blur

# Apply noise effect
def apply_noise(img):
    noise = np.random.normal(0, 25, img.shape).astype(np.uint8)
    img_noise = cv2.add(img, noise)
    return img_noise

# Apply vintage effect (retro + vignette)
def apply_vintage(img):
    img_sepia = apply_retro(img)
    rows, cols, _ = img_sepia.shape
    vignette = np.zeros((rows, cols), dtype=np.uint8)
    cv2.circle(vignette, (cols // 2, rows // 2), min(rows, cols) // 2, 255, -1)
    vignette = cv2.GaussianBlur(vignette, (21, 21), 0)
    vignette = cv2.cvtColor(vignette, cv2.COLOR_GRAY2BGR)
    img_vintage = cv2.addWeighted(img_sepia, 0.7, vignette, 0.3, 0)
    return img_vintage

# Apply sepia tone effect
def apply_sepia_tone(img):
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    img_sepia = cv2.transform(img, sepia_filter)
    img_sepia = np.clip(img_sepia, 0, 255)
    img_sepia = cv2.convertScaleAbs(img_sepia, alpha=1.2, beta=10)
    return img_sepia

# Update the video frame displayed in the Tkinter window
def update_frame():
    success, img = cap.read()
    if success:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgPIL = Image.fromarray(imgRGB)
        imgTK = ImageTk.PhotoImage(image=imgPIL)
        video_label.imgTK = imgTK
        video_label.config(image=imgTK)
    video_label.after(10, update_frame)  # Repeat after 10 milliseconds

# Capture and save the current image with all effects applied
def save_image():
    global count
    success, img = cap.read()
    if success:
        try:
            # Apply all effects
            vivid_img = apply_vivid(img)
            dramatic_img = apply_dramatic(img)
            retro_img = apply_retro(img)
            silvertone_img = apply_silvertone(img)
            sketch_img = apply_sketch(img)
            blur_img = apply_blur(img)
            noise_img = apply_noise(img)
            vintage_img = apply_vintage(img)
            sepia_img = apply_sepia_tone(img)
            
            # Define filenames for each effect
            vivid_filename = f'Sketches/Vivid_{count}.jpg'
            dramatic_filename = f'Sketches/Dramatic_{count}.jpg'
            retro_filename = f'Sketches/Retro_{count}.jpg'
            silvertone_filename = f'Sketches/Silvertone_{count}.jpg'
            sketch_filename = f'Sketches/Sketch_{count}.jpg'
            blur_filename = f'Sketches/Blur_{count}.jpg'
            noise_filename = f'Sketches/Noise_{count}.jpg'
            vintage_filename = f'Sketches/Vintage_{count}.jpg'
            sepia_filename = f'Sketches/Sepia_{count}.jpg'
            
            # Save images to files
            cv2.imwrite(vivid_filename, vivid_img)
            cv2.imwrite(dramatic_filename, dramatic_img)
            cv2.imwrite(retro_filename, retro_img)
            cv2.imwrite(silvertone_filename, silvertone_img)
            cv2.imwrite(sketch_filename, sketch_img)
            cv2.imwrite(blur_filename, blur_img)
            cv2.imwrite(noise_filename, noise_img)
            cv2.imwrite(vintage_filename, vintage_img)
            cv2.imwrite(sepia_filename, sepia_img)
            
            count += 1
            messagebox.showinfo("Images Saved", "Photos saved successfully!",
                                detail="Click 'View Photos' to open the folder with your images.",
                                command=open_folder)
        except Exception as e:
            messagebox.showwarning("Error", str(e))
    else:
        messagebox.showwarning("Error", "Failed to capture image for saving.")

# Open the folder containing saved images
def open_folder():
    path = os.path.abspath('Sketches')
    if os.name == 'nt':  # For Windows
        os.startfile(path)
    elif os.name == 'posix':  # For macOS and Linux
        subprocess.call(['open', path])  # For macOS
        # subprocess.call(['xdg-open', path])  # For Linux

# Quit the application
def quit_app():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

# Ensure the 'Sketches' directory exists
if not os.path.exists('Sketches'):
    os.makedirs('Sketches')

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Initialize Tkinter
root = tk.Tk()
root.title("Artistic Filters")

# Create video label
video_label = tk.Label(root)
video_label.pack()

# Create buttons
capture_button = tk.Button(root, text="Capture & Save", command=save_image)
capture_button.pack(pady=10)

view_button = tk.Button(root, text="View Photos", command=open_folder)
view_button.pack(pady=10)

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack(pady=10)

count = 1

# Start the video update in the background
update_frame()

# Start the Tkinter main loop
root.mainloop()
