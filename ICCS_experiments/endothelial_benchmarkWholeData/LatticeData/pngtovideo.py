import os
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as iio

# Configuration
input_folder = r".\ICCS_experiments\endothelial_benchmarkWholeData\LatticeData"  # Folder containing PNG files
output_video = r".\ICCS_experiments\endothelial_benchmarkWholeData\LatticeData\output_video.mp4"
font_path = r".\ICCS_experiments\endothelial_benchmarkWholeData\LatticeData\ShinyCrystal-Yq3z4.ttf"  # Path to a TTF font file
font_size = 80
text_color = (0, 0, 0)  # Black color for text
text_position = (300, 800)  # Position where text will be drawn
crop_box = (205, 150, 960, 900)  # Define the crop box (left, upper, right, lower)
fixed_size = (900, 900)  # Resize all images to this size after cropping

# Iterations for screenshots
screenshot_iterations = [0, 24, 72, 100]  # Save screenshots at these iterations
screenshot_folder = r".\ICCS_experiments\endothelial_benchmarkWholeData\LatticeData\screenshots"  # Folder to save screenshots

# Ensure screenshot folder exists
os.makedirs(screenshot_folder, exist_ok=True)

# Load font
try:
    font = ImageFont.truetype(font_path, font_size)
except IOError:
    raise Exception("Font file not found. Please adjust the font_path variable.")

# Prepare list of frames
frames = []

for i in range(101):  # Loop through all file numbers (0 to 100)
    # Generate filename based on number format
    if i < 10:
        filename = f"videoanimation.000{i}.png"
    elif i < 100:
        filename = f"videoanimation.00{i}.png"
    else:
        filename = f"videoanimation.0{i}.png"

    filepath = os.path.join(input_folder, filename)

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue

    try:
        # Open image and process it
        with Image.open(filepath) as img:
            # Crop the image
            img = img.crop(crop_box)

            # Resize to ensure consistent dimensions
            img = img.resize(fixed_size)

            # Draw text on the image
            draw = ImageDraw.Draw(img)
            # if i == 0:
            #     text = "MCS: 0"
            # else:
            #     text = f"MCS: {i * 10000}"
            # draw.text(text_position, text, fill=text_color, font=font, stroke_width=5)

            # Convert to RGB mode if necessary (imageio requires RGB format)
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Save screenshot if current iteration matches screenshot_iterations
            if i in screenshot_iterations:
                screenshot_path = os.path.join(screenshot_folder, f"screenshot_{i}.png")
                img.save(screenshot_path)
                print(f"Screenshot saved: {screenshot_path}")

            # Append frame to list for video
            frames.append(img)
    except Exception as e:
        print(f"Error processing file {filename}: {e}")
        continue

# Save frames as an MP4 video
if frames:
    try:
        iio.imwrite(output_video, frames, fps=12)  # Adjust FPS as needed
        print(f"Video saved as {output_video}")
    except Exception as e:
        print(f"Error saving video: {e}")
else:
    print("No valid images were processed.")
