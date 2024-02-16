# Questions OCR Solver

This project receives as input a PDF or multiple images of an exam.
After a few manual operations, it then uses the OpenAI API to generate as output all the Optically Recognized Characters from each question in the exam, and includes its solution.

## Configuration (Linux or Mac)

1. Clone this repository
2. Inside the directory, run `python3 -m venv venv`
3. Run `source venv/bin/activate` to activate the virtual environment
4. Now within the virtual environment, run `pip install -r requirements.txt`
5. Create a `configuration.py` file with the following content (changing for your desired constants):
```
API_KEY = "<your_openai_api_key>"
MAX_TOKENS_PER_API_CALL = 1000
```

## Usage

1. Inside the directory, create a folder called `inputs`.
2. Inside the `inputs` folder, add the original files. It can be either one PDF or multiple images.
3. Back to the original directory, make sure to activate the virtual environment with the command `source venv/bin/activate`
4. Within the virtual environment, run the command `python3 prepare_inputs.py`
5. An interface will be opened.
    - For each question in sight, you must click on its 4 corners with the right button of the mouse, defining the desired question area in red. The clicking should start at the top-left and go clockwise.
    - This must be done for all questions of each page.
    - To go to the next page, press Enter.
    - After going through all pages, pressing Enter will close the interface.
    > After all that, a folder called `questions_crop_imgs` will be created with all the cropped images of the questions.
    > A good practice is to check if the images in the `questions_crop_imgs` are well-formatted.
4. Run the command `python3 main.py`.
5. The code will run and a notification will alert when it stops. It will be created a folder called `outputs` containing the JSON files for all questions.

> Extra step: To transform the JSON files into one single PDF, back in the original directory you can run the command `python3 jsons_converter.py`. This will create a folder called `converted_outputs`, where there will be 1 PDF and 1 docx file, each with one question (image and OCR transform) per page with its solution.
