import base64
import requests
import json
import os

from configuration import API_KEY
from assistant_instructions import assistant_instructions

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')



def gpt_request(image_path):
    print(f"Making request for OpenAI API...")

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
    }

    # Define parameters for API call
    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": assistant_instructions
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 600
    }

    # Make API call 
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response

def save_data_as_json(img_name, data):
    print(f"Saving data as JSON: image {img_name}")

    # Extract the 'choices' field from the response
    choices_data = data['choices']

    # Define the content string
    content = choices_data[0]['message']['content']

    # Clean content string
    content = content.replace("```", "")
    content = content.replace("json", "")
    content = content.replace("\n", "")

    # Transform content string to JSON
    try:
        # Attempt to load the string as JSON
        parsed_json = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    # Create output folder for the JSON files
    output_folder = 'outputs'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Specify the filename you want to write to
    filename = os.path.join(output_folder, img_name)

    # Write the 'choices' data to a file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(parsed_json, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":

    # Path to your images
    images_path = "questions_crop_imgs"

    # List all files in the specified directory
    all_entries = os.listdir(images_path)

    # Filter images and sort them alphabetically
    image_filter = lambda file: file.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"))
    images = list(filter(image_filter , all_entries))
    images = sorted(images)


    # Loop api request for all images
    for img_name in images:
        response = gpt_request(os.path.join(images_path, img_name))
        data = response.json()

        img_name_wo_ext = img_name.split('.')[0]
        save_data_as_json(img_name_wo_ext, data)


    # Script ends here
    os.system("""
            osascript -e 'display notification "Script has finished running." with title "Python Script Notification"'
            """)
