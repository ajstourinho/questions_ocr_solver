import matplotlib.pyplot as plt
from pdf2image import convert_from_path
import cv2
from PIL import Image
import numpy as np
import os
import img2pdf

def check_folder_contents_and_format(folder_path):
    """Function to check contents of the folder and identify the image format"""

    # Check if the folder exists
    if os.path.exists(folder_path):
        # List all files in the folder
        files_in_folder = os.listdir(folder_path)
        
        # Initialize counters for PDFs and images
        pdf_count = 0
        image_count = 0
        image_format = None
        
        # Define a list of image extensions to check
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif']
        
        # Loop through files to count PDFs and find the image format
        for file in files_in_folder:
            if file.lower().endswith('.pdf'):
                pdf_count += 1
            else:
                for ext in image_extensions:
                    if file.lower().endswith(ext):
                        image_count += 1
                        # Assume all images are of the same format, so capture the first one's format
                        if image_format is None:
                            image_format = ext.replace('.', '')
                        break
        
        # Determine the contents of the folder and the image format
        if pdf_count == 1 and image_count == 0:
            return ('pdf', 1)
        elif pdf_count == 0 and image_count > 0:
            return (image_format, image_count)
        else:
            return "Invalid inputs. "
    else:
        return "The folder 'inputs' does not exist."

def create_output_folder(output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def select_multiple_groups_of_points(image):
    groups_of_points = []
    current_points = []

    fig, ax = plt.subplots()
    ax.imshow(image)
    plt.title("Select 4 points for each area on this page. Press Enter when done.")

    def onclick(event):
        # Add point on click and immediately mark it
        if event.xdata is not None and event.ydata is not None:
            current_point = [event.xdata, event.ydata]
            current_points.append(current_point)
            # Immediately mark the selected point
            ax.plot(current_point[0], current_point[1], 'r+', markersize=12)

            if len(current_points) == 4:
                # Draw polygon after the fourth point is selected
                poly = plt.Polygon(current_points, color='red', alpha=0.4, fill=True)
                ax.add_patch(poly)
                groups_of_points.append(current_points.copy())
                current_points.clear()
            plt.draw()

    def onkeypress(event):
        # Finalize selection with Enter
        if event.key == 'enter':
            plt.close(fig)

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('key_press_event', onkeypress)
    plt.show()
    return groups_of_points

def perspective_transform_and_save(original_image, points, output_filename):
    points = np.array(points, dtype='float32')

    max_width = max(int(np.linalg.norm(points[0] - points[1])), int(np.linalg.norm(points[2] - points[3])))
    max_height = max(int(np.linalg.norm(points[0] - points[3])), int(np.linalg.norm(points[1] - points[2])))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype='float32')

    matrix = cv2.getPerspectiveTransform(points, dst)
    result = cv2.warpPerspective(np.array(original_image), matrix, (max_width, max_height))

    Image.fromarray(result).save(output_filename)

def process_pdf(pdf_path, output_folder):
    create_output_folder(output_folder)

    # Convert all pages of the PDF to images
    print("Processing PDF...")
    images = convert_from_path(pdf_path)
    
    for i, page_image in enumerate(images):
        print(f"Processing page {i+1}/{len(images)}...")
        groups_of_points = select_multiple_groups_of_points(page_image)

        for j, group in enumerate(groups_of_points):
            output_filename = os.path.join(output_folder, f"output_page_{i+1}_area_{j}.jpg")
            perspective_transform_and_save(page_image, group, output_filename)
            print(f"Saved {output_filename}")

def get_sole_pdf_name(folder_path):
    # Define the folder path
    folder_path = 'inputs'  # Adjust the path as necessary
    
    # Check if the folder exists
    if os.path.exists(folder_path):
        # List all files in the folder
        files_in_folder = os.listdir(folder_path)
        
        # Filter out the sole PDF file directly assuming it's unique and exists
        pdf_file = next((file for file in files_in_folder if file.lower().endswith('.pdf')), None)
        
        # Check if a PDF file was found
        if pdf_file:
            return pdf_file
        else:
            return "No PDF files found in the folder."
    else:
        return "The folder 'inputs' does not exist."

def images_to_pdf(directory, output_pdf_path):
    print("Processing input images...")

    # List to hold images that are converted to RGB mode
    img_list = []
    
    # Iterate over each image in the directory
    for img_name in sorted(os.listdir(directory)):
        if img_name.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")):
            img_path = os.path.join(directory, img_name)
            # Open the image using Pillow
            img = Image.open(img_path)
            # Convert the image to RGB if it is not already in that mode
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_list.append(img)

    # Convert the list of images to a single PDF
    if img_list:
        img_list[0].save(output_pdf_path, save_all=True, append_images=img_list[1:], resolution=100.0)
        print(f"PDF created successfully: {output_pdf_path}")
    else:
        print("No images found in the directory.")

if __name__ == "__main__":

    # Define the folder path
    folder_path = 'inputs'

    try:
        print("Preparing inputs...")
        
        (file_type, file_count) = check_folder_contents_and_format(folder_path)

        # Define the input_pdf_path based on file_type
        if file_type == 'pdf':
            input_pdf_path = os.path.join(folder_path, get_sole_pdf_name(folder_path))
        else:
            pdf_path = os.path.join(folder_path, "temporary.pdf")
            images_to_pdf(folder_path, pdf_path)
            input_pdf_path = pdf_path

        # Create a folder with all the cropped image areas from the PDF
        output_folder = 'output_0_areas'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        process_pdf(input_pdf_path, output_folder)

        # Remove temporary file
        temp_pdf_path = os.path.join(folder_path, "temporary.pdf")
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
            print(f"PDF removed successfully: {temp_pdf_path}")

    except Exception as e:
        print(f'Error: {e}')


