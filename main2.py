import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

from integralImage import doubleIntegral
from detectEyes import DetectEye, ExtractDetectedEye
from readImage import readImage

pathAndSizeKernal = [
    ("Image 1.jpeg", 330), ("Image 2.jpeg", 250),
    ("Image 3.jpeg", 150), ("Image 4.jpeg", 150),
    ("Image 5.jpeg", 90),  ("Image 6.jpeg", 160),
    ("Image 7.jpeg", 170), ("Image 8.jpeg", 220)
]
base_path = "Images/"

i = 0  # start index
fig, axarr = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(bottom=0.2)  # space for Prev/Next buttons

def set_titles(idx, img_path, n):
    # Window title (works on most backends)
    try:
        fig.canvas.manager.set_window_title(f"Figure {idx+1}: {img_path}")
    except Exception:
        pass
    # Visible title inside the figure
    fig.suptitle(f"Figure {idx+1}: {img_path}  (n={n})", fontsize=13)

def show_image(idx):
    img_path, n = pathAndSizeKernal[idx]
    img = readImage(base_path + img_path)
    I = doubleIntegral(img)
    center = DetectEye(I, n)
    masked, bbox = ExtractDetectedEye(img, center, n)

    for ax in axarr:
        ax.clear()

    # ----- Left: original + center + bbox
    axL = axarr[0]
    axL.imshow(img, cmap='gray')
    axL.scatter(center[1], center[0], s=60)
    # draw bbox
    top, left, bottom, right = bbox
    axL.add_patch(Rectangle((left, top), (right - left + 1), (bottom - top + 1),
                            fill=False, linewidth=2))
    axL.set_title("Original + detected center + bbox")
    axL.axis("off")

    # ----- Right: masked
    axR = axarr[1]
    axR.imshow(masked, cmap='gray')
    axR.set_title(f"Masked  |  bbox={bbox}")
    axR.axis("off")

    set_titles(idx, img_path, n)
    fig.canvas.draw_idle()

def next_image(event=None):
    global i
    i = (i + 1) % len(pathAndSizeKernal)
    show_image(i)

def prev_image(event=None):
    global i
    i = (i - 1) % len(pathAndSizeKernal)
    show_image(i)

# Buttons
axprev = plt.axes([0.30, 0.05, 0.10, 0.075])
axnext = plt.axes([0.60, 0.05, 0.10, 0.075])
bprev = Button(axprev, 'Prev')
bnext = Button(axnext, 'Next')
bprev.on_clicked(prev_image)
bnext.on_clicked(next_image)

# Keyboard shortcuts: ← / →
def on_key(event):
    if event.key in ("right",):
        next_image()
    elif event.key in ("left",):
        prev_image()
fig.canvas.mpl_connect('key_press_event', on_key)

# Kick off
show_image(i)
plt.show()
