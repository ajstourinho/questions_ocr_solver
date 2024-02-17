# Questions OCR Solver

This project receives as input a PDF or multiple images of an exam.
After a few manual operations, it then uses the OpenAI API to generate as output all the Optically Recognized Characters from each question in the exam, and includes its solution.

## Configuration (Linux or Mac)

1. Clone this repository
2. Inside the directory, run `python3 -m venv venv`
3. Run `source venv/bin/activate` to activate the virtual environment
4. Now within the virtual environment, run `pip install -r requirements.txt`
5. Create a `p0_configuration.py` file with the following content (changing for your desired constants):
```
API_KEY = "<your_openai_api_key>"
MAX_TOKENS_PER_API_CALL = 1000
```

## Usage

1. Inside the directory, create a folder called `inputs`.
2. Inside the `inputs` folder, add the original files. It can be either one PDF or multiple images.
3. Back to the original directory, make sure to activate the virtual environment with the command `source venv/bin/activate`
4. Within the virtual environment, run the command `python3 p1_prepare_inputs.py`
5. An interface will be opened.
    - For each question in sight, you must click on its 4 corners, defining the desired question area in red. The clicking should start at the top-left and go clockwise.
    - This must be done for all questions of each page.
    - To go to the next page, press Enter.
    - After going through all pages, pressing Enter will close the interface.
    > After all that, a folder called `output_0_areas` will be created with all the cropped imagea areas of the questions.
    > A good practice is to check if the images in the `output_0_areas` are well-formatted.
4. Run the command `python3 p2_main.py`.
    > The code will run and a notification will alert when it stops or if an error occurs. It will be created a folder called `output_1_jsons` containing the JSON files for all questions.
5. To transform the JSON files into one single PDF, run the command `python3 p3_jsons_converter.py`.
    > This will create a folder called `output_2_docx_pdf`, where there will be 1 PDF and 1 docx file.
