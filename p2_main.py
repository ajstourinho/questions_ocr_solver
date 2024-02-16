import base64
import requests
import json
import os
import concurrent.futures
import sys

from p0_configuration import API_KEY
from p0_configuration import MAX_TOKENS_PER_API_CALL
from p0_assistant_instructions import assistant_instructions

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
    "max_tokens": MAX_TOKENS_PER_API_CALL
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

    # Add JSON extension
    filename += ".json"
    
    # Write the 'choices' data to a file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(parsed_json, file, indent=2, ensure_ascii=False)

def user_check(message):
    check = input(message)

    if check.lower() != "y":
        print("Python script terminated by user.")
        sys.exit()

def fake_request(image_file):
    class MyJSONObject:
        def __init__(self, json_string):
            self.data = json.loads(json_string)
        
        @property
        def json(self):
            return json.dumps(self.data)
    

    json_string =  """{
  "id": "chatcmpl-8sJOVL1RpBcSKJUSq7RuC0X4bGvhD",
  "object": "chat.completion",
  "created": 1707954955,
  "model": "gpt-4-1106-vision-preview",
  "usage": {
    "prompt_tokens": 1033,
    "completion_tokens": 300,
    "total_tokens": 1333
  },
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "```json\n{\n  \"enunciado\": \"Um paciente em investigação para síndrome de má-absorção foi submetido a múltiplas biópsias do duodeno. O exame histológico mostrou atrofia de vilos, numerosos linfócitos intraepiteliais e regeneração de criptas. A imuno-histoquímica mostrou tratar-se de linfócitos CD8+. Os achados são consistentes com:\",\n  \"tipo\": \"Objetiva\",\n  \"resposta\": {\n    \"a\": {\n      \"alternativa\": \"Linfoma do Intestino Delgado\",\n      \"textoExplicativo\": \"A atrofia de vilos, presença de linfócitos intraepiteliais e regeneração de criptas sugerem doença celíaca, e não necessariamente linfoma.\"\n    },\n    \"b\": {\n      \"alternativa\": \"Doença de Crohn\",\n      \"textoExplicativo\": \"Embora a Doença de Crohn possa apresentar inflamação, os achados de atrofia de vilos, linfócitos intraepiteliais e regeneração de criptas são mais típicos da doença celíaca.\"\n    },\n    \"c\": {\n      \"alternativa\": \"Do"
      },
      "finish_reason": "length",
      "index": 0
    }
  ]
}"""
    obj = MyJSONObject(json_string)

    print("fake request made")

    return obj
    

if __name__ == "__main__":

    # Path to your images
    images_path = "output_0_areas"

    # List all files in the specified directory
    all_entries = os.listdir(images_path)

    # Filter images files and sort them alphabetically
    image_filter = lambda file: file.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"))
    images = list(filter(image_filter , all_entries))
    images = sorted(images)

    # Define list of files for the multithread api calls
    files = [os.path.join(images_path, f) for f in images]


    # Initialize error counter
    error_count = 0
    
    while len(files) != 0:

        # Check with user to make all the API Calls
        user_check(f"There will be made {len(files)} api calls with {MAX_TOKENS_PER_API_CALL} max_tokens each.\nWrite y to procede: ")

        # Use ThreadPoolExecutor to make requests in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # api_response = {executor.submit(gpt_request, image_file): image_file for image_file in files}
            api_response = {executor.submit(fake_request, image_file): image_file for image_file in files}
            for future in concurrent.futures.as_completed(api_response):

                image_file = api_response[future]

                try:
                    # Define file names
                    file_name = os.path.basename(image_file)
                    file_name_without_extension, _ = os.path.splitext(file_name)

                    # Define response and data from the gpt_request response
                    response = future.result()
                    data = response.json()
                    
                    # Save the data as a JSON file
                    save_data_as_json(file_name_without_extension, data)

                    # Pop out the completed file from files list
                    files.remove(image_file)
                    print(len(files))
                except Exception as e:
                    print(e)
                    error_count += 1

        if error_count != 0:
            print(f"There was {error_count} errors in the API calls. You may want to try again")
            # Reinitialize error counter
            error_count = 0


    # Check the errors
    # print(f"Number of errors in the api requests: {len(errors)}")
    # for el in errors:
    #     print(el)

    # Script ends here
    os.system("""
            osascript -e 'display notification "Script has finished running." with title "Python Script Notification"'
            """)
