import csv
import os
import shutil

import PyPDF2
from jinja2 import Environment, FileSystemLoader
from weasyprint import CSS, HTML

mapped_data = []

file_name = input("Enter path to file: ").strip()


# Read the CSV file
csv_file = f"{file_name}"
with open(csv_file, mode="r") as file:
    csv_reader = csv.DictReader(file)
    for row_id, row in enumerate(csv_reader):
        mapped_row = {
            "id": str(row_id),
            "story": "Galdrakarlin í Oz",
            "childe_name": row["Fullt nafn barns"],
            "childe_ssn": row["Kennitala barns"],
            "childe_age": row["Aldur"],
            "childe_other": row["Annað sem þarf að koma fram"],
            "childe_friends": row[
                "Tengist barnið einhverjum öðrum sem kemur í sumarbúðirnar"
            ],
            "guardian_one_name": row["Fullt nafn forráðamanns 1"],
            "guardian_one_phone": row["Símanúmer forráðamanns 1"],
            "guardian_one_email": row["Netfang forráðamanns 1"],
            "guardian_two_name": row["Fullt nafn forráðamanns 2"],
            "guardian_two_phone": row["Símanúmer forráðamanns 2"],
            "guardian_two_email": row["Netfang forráðamanns 2"],
            "guardian_three_name": row["Fullt nafn forráðamanns 3"],
            "guardian_three_phone": row["Símanúmer forráðamanns 3"],
            "guardian_three_email": row["Netfang forráðamanns 3"],
            "concent": row[
                "Mér er kunnugt að Söguheimar tryggir ekki skráð barn/börn á meðan það/þau eru í sumarbúðunum."
            ],
        }
        mapped_data.append(mapped_row)


# Create jinja2 environment
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template/template.html")

# Ensure output directories exist
html_output_dir = "./output/html"
pdf_output_dir = "./output/pdf"
os.makedirs(html_output_dir, exist_ok=True)
os.makedirs(pdf_output_dir, exist_ok=True)

for item in mapped_data:
    # Render the template with the current data
    html_content = template.render(mapped_data=[item])

    # Save the rendered HTML to a file
    html_filename = f"{html_output_dir}/file_{item['id']}.html"
    with open(html_filename, "w") as f:
        f.write(html_content)

    # Convert the HTML content to a PDF using WeasyPrint
    pdf_filename = f"{pdf_output_dir}/file_{item['id']}.pdf"
    HTML(string=html_content).write_pdf(
        target=pdf_filename, stylesheets=[CSS("./template/style.css")]
    )


def remove_folder(output_dir, type=""):
    """Clean up files and remove the directory"""
    try:
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        shutil.rmtree(output_dir)
        print(f"{type} files and folder removed")
    except Exception as e:
        print(f"Error removing HTML files or folder: {e}")


def combine_files(directory_path, output_path):
    """Combines all pdf files in a given directory"""
    merger = PyPDF2.PdfMerger()

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory_path, filename)
            merger.append(filepath)

    file_name = str(input("Enter a file name: ").strip() or "combined")
    print()
    output_file_path = os.path.join(output_path, file_name + ".pdf")
    merger.write(output_file_path)
    merger.close()
    return file_name


# Paths to directories
input_directory = "./output/pdf"
output_directory = os.path.dirname(file_name) + "/"


file = combine_files(input_directory, output_directory)

# remove html files and folder
html_type = "HTML"
remove_folder(html_output_dir, html_type)


# remove pdf files and folder
pdf_type = "PDF"
remove_folder(pdf_output_dir, pdf_type)

print(f"{file} exported to {output_directory}")
