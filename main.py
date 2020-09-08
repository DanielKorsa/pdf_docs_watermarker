#


import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
from os import path
from glob import glob


def watermark_pdf_doc(path_to_doc, document_recipient ):
    '''
    '''

    msg = 'Watermark: This document is intended for {}.'\
            'It contains privacy-sensitive data and falls under the Data Protection Law.'.format(document_recipient)
    
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica-Bold', 8)
    can.setFillColor('grey', alpha=0.3)
    can.rotate(45)
    can.drawCentredString(300, 0, msg)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(path_to_doc, "rb"))
    output = PdfFileWriter()
    i = 0
    for page in range(existing_pdf.getNumPages()):
        
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        i+=1
    # finally, write "output" to a real file
    
    
    signed_doc_name = path_to_doc.split('.')[0] + 'watermarked.pdf'
    
    #print(signed_doc_name)
    outputStream = open(signed_doc_name, "wb")
    output.write(outputStream)
    outputStream.close()
    
def choose_dir():
    '''
    Use TK to choose a dir - didnt work
    '''
    #path_to_dir = askdirectory(title='Select Folder') # shows dialog box and return the path
    root = Tk()
    root.withdraw()
    path_to_dir = askdirectory()
    
    return path_to_dir     
    
def get_list_pdf_files(pdf_dir):
    
    print(pdf_dir)
    
    return glob(path.join(pdf_dir,"*.{}".format('pdf')))

def merge_pdfs(pdf_files_list, output_file_name):
    
    merger = PdfFileMerger()

    for pdf in pdf_files_list:
        merger.append(pdf)

    merger.write(output_file_name)
    merger.close()


def main():
    
    #chosen_dir = choose_dir()
    RENTOR = 'HERR PIDOR'
    CHOSEN_DIR = '/Users/gesundmeister/dev/pdf_watermarker/docs'
    merged_doc_name = CHOSEN_DIR + '/docs_{}_.pdf'.format(RENTOR)
        
        
    pdf_files_list = get_list_pdf_files(CHOSEN_DIR) # get all pdf files
    merge_pdfs(pdf_files_list, merged_doc_name) # merge all pdf files in 1
    watermark_pdf_doc(merged_doc_name, RENTOR) # watermark file
    os.remove(merged_doc_name) # delete merged pdf doc


    


    
    
    
if __name__ == "__main__":
    main()