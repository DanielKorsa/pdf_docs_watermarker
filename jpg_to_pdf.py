from PIL import Image

def jpg_conv_pdf(jpg_path):
    """[Convert .jpg img into .pdf doc]

    Args:
        jpg_path ([type]): [description]
    """
    image1 = Image.open(jpg_path)
    im1 = image1.convert('RGB')
    pdf_path = jpg_path.replace('jpg', 'pdf')
    im1.save(pdf_path)

    return pdf_path



from tkinter import Tk
from tkinter.filedialog import askdirectory


dir_name = askdirectory()