# Questions OCR Solver

This project receives as input a PDF or multiple images of an exam.
After a few manual operations, it then uses the OpenAI API to generate as output all the Optically Recognized Characters from each question in the exam, and includes its solution.

## Configuration (Linux or Mac)

1. Clone this repository
2. Inside the directory, run `python3 -m venv venv`
3. Run `source venv/bin/activate` to activate the virtual environment
4. Now within the virtual environment, run `pip install -r requirements.txt`
5. In the `configuration.py` file, write the correct value for the OpenAI `"API_KEY"`

## Usage

1. Inside the directory, create a folder called `inputs`.
2. Inside the `inputs` folder, add the original files. It can either be one PDF or multiple images.
3. Back to the original directory, make sure to activate the virtual environment with the command `source venv/bin/activate`
4. Within the virtual environment, run the command `python3 prepare_input.py`
5. An interface will be opened, and for each question in sight, you must click on its 4 corners with the right button of the mouse, defining the desired question area in red. This must be done for all questions of each page. To go to the next page, press Enter. After going through all pages, pressing Enter will close the interface.
4. Run the command `python3 main.py`.
5. The code will run and a notification will alert when it stops. It will be created a folder called `outputs` and inside that another one called `json_outputs` containing the JSON files for all questions.

> Extra step: To transform the JSON files into one single PDF, back in the original directory you can run the command `python3 json_outputs_to_pdf.py`. This will create a folder called `pdf_outputs` inside the `outputs` folder. There will be 1 PDF called `questions_ocr_and_answers.pdf` with one question (image and OCR transform) and its solution per page.