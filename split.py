import os
import uuid
import json
from PyPDF2 import PdfReader, PdfWriter


def split_pdf_to_single_pages(input_folder, output_folder):
  """Splits each PDF file in the input folder into single-page PDFs, stores them in folders named after the original PDF,
  and creates corresponding JSON files in the data folder with page information."""

  for filename in os.listdir(input_folder):
    if not filename.endswith(".pdf"):
      continue

    file_path = os.path.join(input_folder, filename)
    reader = PdfReader(file_path)

    # Create folder for the original PDF (if it doesn't exist)
    output_dir = os.path.join(output_folder, os.path.splitext(filename)[0])
    os.makedirs(output_dir, exist_ok=True)

    page_data = []

    for page_num in range(len(reader.pages)):
      page = reader.pages[page_num]

      # Create a new PDF writer for each page
      writer = PdfWriter()
      writer.add_page(page)

      # Generate unique filename with UUID v4 and ".pdf" extension
      output_filename = f"{uuid.uuid4()}.pdf"
      output_path = os.path.join(output_dir, output_filename)

      # Save the single-page PDF
      with open(output_path, "wb") as f:
        writer.write(f)

      # Create page data for JSON
      page_data.append({"original_page_number": page_num + 1, "new_filename": output_filename})

    # Create JSON file with page information
    data_filepath = os.path.join(data_folder, f"{os.path.splitext(filename)[0]}.json")
    with open(data_filepath, "w") as f:
      json.dump({"original_file": filename, "pages": page_data}, f, indent=4)

    print(f"\nCreated single-page PDFs and data file in folder: {filename}")


if __name__ == "__main__":
  input_folder = "input"  # Replace with your input folder path
  output_folder = "output"  # Replace with your desired output folder name
  data_folder = "data"  # Replace with your desired data folder name

  split_pdf_to_single_pages(input_folder, output_folder)

  print("\nProcess completed!")
