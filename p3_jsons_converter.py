import json
import os
from docx import Document
from docx2pdf import convert
import glob
from docx.shared import Inches
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def find_image_matching_json(json_name, search_directory):
    # Strip the .json extension to get the base name
    json_basename = os.path.splitext(json_name)[0]
    
    # Create a pattern to match files with the same base name as the JSON but with common image extensions
    pattern = os.path.join(search_directory, f"{json_basename}.*")
    
    # Use glob to find files matching the pattern
    for filename in glob.glob(pattern):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            return filename  # Return the first matching image found
    
    return None  # No matching image found

def load_json_data(file_path):
    """Load and return JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

# def create_pdf_from_docx(docx_path):
#     """Convert a .docx file to PDF (may require admin permisions)."""
#     convert(docx_path)

def add_data_docx(data, doc, file_name):
    """Add content from JSON data to a .docx file."""

    # Add original picture of questions
    image_filename = find_image_matching_json(file_name, "output_0_areas")
    doc.add_picture(image_filename, width=Inches(6.0))

    # Add content from JSON

    doc.add_paragraph().add_run(data['enunciado']).bold = True

    for key, value in data['resposta'].items():
        if key != "alternativaCorreta":
            p1 = doc.add_paragraph()
            p1.add_run(key.upper() + ')  ' + value['alternativa']).bold = True
            
            p2 = doc.add_paragraph(value['textoExplicativo'])
            p2.style = 'List Bullet'

    doc.add_paragraph('\n')

    doc.add_paragraph('Alternatica correta: ' + data['resposta']['alternativaCorreta'])

def add_content_to_pdf(canvas, data):
    """Add content from JSON data to a single page in a PDF."""
    canvas.drawString(72, 800, data['enunciado'])
    y_position = 780

    for key, value in data['resposta'].items():
        if key != 'alternativaCorreta':
            text = f"{key.upper()}. {value['alternativa']}: {value['textoExplicativo']}"
            canvas.drawString(72, y_position, text)
            y_position -= 20 * (1 + len(text) // 90)  # Adjust y position based on text length

if __name__ == "__main__":


    # Define JSON folder
    jsons_folder = 'output_1_jsons'

    # Create folder for the output files
    output_folder = 'output_2_docx_pdf'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    # Create docx
    docx_path = os.path.join(output_folder, 'questions.docx')
    doc = Document()

    # Create docx
    pdf_path = os.path.join(output_folder, 'questions.pdf')
    pdf = canvas.Canvas(pdf_path, pagesize=letter)
  
    # Iterate over each JSON file in the directory
    for file_name in os.listdir(jsons_folder):
        if file_name.endswith('.json'):
            file_path = os.path.join(jsons_folder, file_name)
            data = load_json_data(file_path)
            
            # Add JSON content to docx
            add_data_docx(data, doc, file_name)

            # Add JSON content to pdf
            add_data_docx(data, doc, file_name)
            add_content_to_pdf(pdf, data)

            # Add page break only if it is not the last one
            if file_name != os.listdir(jsons_folder)[-1]:
                doc.add_page_break()

                pdf.showPage()

    # Save .docx document
    doc.save(docx_path)

    # Save .pdf document
    pdf.save()
            
    # # Save the .pdf converted from .docx
    # create_pdf_from_docx(docx_path)