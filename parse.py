import csv
import os
import shutil
import time

import PyPDF2
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm, trange
from tqdm.auto import tqdm
from weasyprint import CSS, HTML

path_to_css = "./template/style.css"


def get_file_name():
    return input("Enter path to file: ").strip()


def parse_csv(file_name):
    """Reads and maps the data from the csv"""
    mapped_list = []
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
            mapped_list.append(mapped_row)
        return mapped_list


def create_template():
    """Create html template and set up jinja environment"""
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template/template.html")
    return template


def create_directory(directory_name):
    """Create output directory and make sure that it exists"""
    try:
        os.makedirs(directory_name, exist_ok=True)
    except Exception as e:
        print("an error ocurred", directory_name, e)
    return directory_name


def convert_html_to_pdf(content, css, directory, number):
    pdf_filename = f"{directory}/file_{number}.pdf"
    HTML(string=content).write_pdf(target=pdf_filename, stylesheets=[CSS(f"{css}")])


def generate_html_template(mapped_list, template, html_dir, pdf_dir):
    number_of_items = len(mapped_list)
    progress_bar = tqdm(total=number_of_items)

    for row_id, row in enumerate(mapped_list):
        # Render the template with the current data
        html_content = template.render(mapped_data=[row])

        # Save the rendered HTML to a file
        html_filename = f"{html_dir}/file_{row_id}.html"
        with open(html_filename, "w") as f:
            f.write(html_content)

        convert_html_to_pdf(html_content, path_to_css, pdf_dir, row_id)

        progress_bar.update(1)
        time.sleep(0.1)
    progress_bar.close()


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


def remove_folder(output_dir):
    """Clean up files and remove the directory"""
    try:
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        shutil.rmtree(output_dir)
    except Exception as e:
        print(f"Error removing HTML files or folder: {e}")


def main():
    file_name = get_file_name()
    data = parse_csv(file_name)
    template = create_template()

    html_dir_name = "./html"
    html_dir = create_directory(html_dir_name)
    pdf_dir_name = "./pdf"
    pdf_dir = create_directory(pdf_dir_name)

    generate_html_template(data, template, html_dir, pdf_dir)

    # Paths to directories
    input_directory = "./pdf"
    output_directory = os.path.dirname(file_name) + "/"

    file = combine_files(input_directory, output_directory)

    # remove html files and folder
    remove_folder(html_dir)
    # remove pdf files and folder
    remove_folder(pdf_dir)

    print(f"{file} exported to {output_directory}")


if __name__ == "__main__":
    main()
