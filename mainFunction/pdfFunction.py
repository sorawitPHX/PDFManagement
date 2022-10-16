from PyPDF2 import *
from pdf2image import convert_from_path
from PIL import Image
import os


def mergePDF(files, path : str):
    new = PdfMerger()
    for f in files:
        try:
            new.append(f.name)
        except FileNotFoundError as ferr:
            print('-- File Not Found! --')
            print(ferr)
    new.write(f'{path}')
    print('-- Merged file complete --')
    new.close()
    


def splitPDF(file, path, start, end):
    rd = PdfFileReader(file)
    wd = PdfFileWriter()
    for i in range(start, end+1):
        current_page = rd.getPage(i)
        wd.add_page(current_page)
    wd.write(path)



def image2pdf(files, path=''):
    temp_dir_path = path.split('/')
    dir_path = '/'.join(temp_dir_path[0:-1])
    os.mkdir(f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__')
    for index, f in enumerate(files):
        image = Image.open(f)
        conv_image = image.convert(mode='RGB')
        conv_image.save(f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__/{index+1}.pdf', 'pdf')
        image.close()
        conv_image.close()
    temp = os.listdir(f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__')
    new_files = [open(f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__/{i}', mode='rb') for i in temp]
    mergePDF(new_files, path)
    for i in new_files:
        i.close()
        
    for i in temp:
        os.remove(f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__/{i}')
    os.removedirs(f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__/')
    print('-- Success --')



def pdf2image(files : list, path, format):
    for index1, file in enumerate(files):
        file_name = file.split('/')[-1]
        file_name = file_name.split('.')
        file_name = file_name[0]
        print(file_name)
        os.mkdir(f'{path}/{file_name}')
        pdf = convert_from_path(file)
        for index2, page in enumerate(pdf):
            page.save(f'{path}/{file_name}/Page{index2}.{format}')


def compressPDF(files, path):
    
    pass



def protectPFD(file, path, password):
    rd = PdfFileReader(file)
    wd = PdfFileWriter()
    for index in range(rd.numPages):
        page = rd.getPage(index)
        wd.add_page(page)
    wd.encrypt(password)
    wd.write(path)



if __name__ == '__main__':
    pass
    #pdf2image([r"C:/Users/MSI Ryzen5\Downloads/TEST10.pdf"], r"C:/Users/MSI Ryzen5/Downloads", 'png')