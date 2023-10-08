import os
from PyPDF2 import PdfReader, PdfWriter

# Function to split a PDF file into individual pages
def split_pdf(input_pdf, output_folder):
    # Open the PDF file
    pdf = PdfReader(input_pdf)
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through each page in the PDF
    for page_num, page in enumerate(pdf.pages, start=1):
        # Create a new PDF writer for each page
        pdf_writer = PdfWriter()
        pdf_writer.add_page(page)
        
        # Construct the output file name
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_file = os.path.join(output_folder, f"page_{page_num}_of_{base_name}.pdf")
        
        # Write the page to the output file
        with open(output_file, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

if __name__ == "__main__":
    # Replace 'input.pdf' with the path to your input PDF file
    PATH = 'collected_pdfs/'
    for i, file in enumerate(os.listdir(PATH)):
      input_pdf = PATH + file
      
      # Replace 'output_folder' with the path to the folder where you want to save the split PDF pages
      output_folder = "splitted_pdfs/PDF_"+file
      
      split_pdf(input_pdf, output_folder)
      print(f'{i + 1}/{len(os.listdir(PATH))} done.')
