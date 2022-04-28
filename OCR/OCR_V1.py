import os
import glob
import shutil
from PIL import Image
import pytesseract as tess
from pathlib import Path, WindowsPath
from pdf2image import convert_from_path
tess.pytesseract.tesseract_cmd = r'C:\Users\nolha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

#install shutil: https://pypi.org/project/pytest-shutil/
#install poppler: https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows
#install pytesseract: https://github.com/tesseract-ocr/tesseract

actual_path = Path.cwd()
work_path = WindowsPath(str(actual_path) + '\work')
Output_path = WindowsPath(str(work_path) + '\Output')
Input_path = WindowsPath(str(work_path) + '\Input')
Temp_path = WindowsPath(str(work_path) + '\Temp')

if not os.path.exists(str(work_path)):
    os.makedirs(str(work_path))

if not os.path.exists(str(Input_path)):
    os.makedirs(str(Input_path))

if not os.path.exists(str(Output_path)):
    os.makedirs(str(Output_path))

all_pdf = list(Input_path.glob('*.pdf'))

for i in range(len(all_pdf)):

    if not os.path.exists(str(Temp_path)):
        os.makedirs(str(Temp_path))

    Dest_path = str(Temp_path) + '/' + str(all_pdf[i].name)
    shutil.copyfile(str(all_pdf[i]) , str(Dest_path) )

    pdf = Dest_path
    pages = convert_from_path(pdf)
    img = pdf.replace(".pdf","")
    name = all_pdf[i].name.replace(".pdf","")
    
    count = 0 

    for page in pages:
        count += 1
        jpeg = img + "-" + str(count) + ".jpeg"
        page.save(jpeg, 'JPEG')

    text_file = open(str(Output_path) + '/' + str(name) + '.txt' , "wt")

    j = 1

    while j < (count+1):
        img = Image.open(str(Temp_path) + '/' + str(name) + '-' + str(j) + '.jpeg')
        text = tess.image_to_string(img)
        text_file.write(text)
        j += 1

    text_file.close()

    shutil.rmtree(str(Temp_path))