#
import io
import os
from glob import glob
from os import path
from tkinter import Tk
from tkinter.filedialog import askdirectory

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def watermark_pdf_doc(path_to_doc, document_recipient):
    """[summary]

    Args:
        path_to_doc ([str]): [Path to .pdf document to be watermarked]
        document_recipient ([str]): [Name in watermark text]
    """
    msg = 'Watermark: This document is intended for {}.'\
            'It contains privacy-sensitive data and falls under the Data Protection Law.'.format(document_recipient)

    packet = io.BytesIO()
    # create a new PDF with Reportlab & set font
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica-Bold', 8)
    can.setFillColor('grey', alpha=0.3)
    can.rotate(45)
    can.drawCentredString(300, 0, msg)
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read existing PDF
    existing_pdf = PdfFileReader(open(path_to_doc, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    for page in range(existing_pdf.getNumPages()):
        new_page = existing_pdf.getPage(page)
        new_page.mergePage(new_pdf.getPage(0))
        output.addPage(new_page)

    # Write "output" to a real file
    signed_doc_name = path_to_doc.split('.')[0] + 'watermarked.pdf'
    outputStream = open(signed_doc_name, "wb")
    output.write(outputStream)
    outputStream.close()

def choose_dir():
    '''
    Use TK to choose a dir - didnt work
    '''
    root = Tk()
    root.withdraw()
    curr_directory = os.getcwd()
    path_to_dir = askdirectory(initialdir=curr_directory)

    return path_to_dir

def get_list_pdf_files(pdf_dir):
    """[List .pdf files in folder]

    Args:
        pdf_dir ([str]): [Dir with pdf files]

    Returns:
        [list]: [Paths list]
    """
    return glob(path.join(pdf_dir,"*.{}".format('pdf')))

def merge_pdfs(pdf_files_list, output_file_name):
    """[summary]

    Args:
        pdf_files_list ([list]): [List of pdf files to be merged]
        output_file_name ([str]): [Result file name]
    """
    merger = PdfFileMerger()
    [merger.append(pdf) for pdf in pdf_files_list]
    merger.write(output_file_name)
    merger.close()

    return output_file_name

def main():

    LANDLORD = 'Bam' #? Enter name of landlord/ real estate agent
    docs_dir = choose_dir()
    merged_doc_name = path.join(docs_dir, 'docs_{}_.pdf'.format(LANDLORD)) # Windows
    pdf_files_list = get_list_pdf_files(docs_dir) # get all pdf files
    merge_pdfs(pdf_files_list, merged_doc_name) # merge all pdf files in 1
    watermark_pdf_doc(merged_doc_name, LANDLORD) # watermark file
    #os.remove(merged_doc_name) # delete merged pdf doc

if __name__ == "__main__":
    main()
