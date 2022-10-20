from tkinter import *
from tkinter.ttk 
from PyPDF2 import *
from pdf2image import convert_from_path
from PIL import Image
from PDFNetPython3.PDFNetPython import PDFDoc, SDFDoc, Optimizer, PDFNet
#from fitz import *
import gc
import os
        
        

def progressBar(process, total, label=''):
    percent = 100 * (process/total)
    bar = f"\r|{'█'*int(percent)}{'-'*int(100-percent)}|{percent:.2f}%"
    print(bar, end='\r')
    if process == total:
        print(bar)
    

def mergePDF(files_path, output_path : str):
    pdf = PdfMerger()
    for index, f_path in enumerate(files_path):
        with open(f_path, 'rb') as f:
            pdf.append(f)
        progressBar(index+1, len(files_path))
    pdf.write(f'{output_path}')
    pdf.close()
    del pdf, files_path, f_path, f
    gc.collect()
    print('-- Merged file complete --')



def splitPDF(file_path, output_path, start, end):
    rd = PdfFileReader(file_path)
    wd = PdfFileWriter()
    for i in range(start, end+1):
        current_page = rd.getPage(i)
        wd.add_page(current_page)
    wd.write(output_path)
    del rd, wd
    gc.collect()
    print( gc.get_count() )
    print('-- Splited file complete --')



def image2pdf(files_path, output_path, mode):
    def page_size_converter(img : Image, output_path, page_size=(int(), int())):
        size = (int(page_size[0]//2.778), int(page_size[1]//2.778))
        print(size)
        page = Image.new(mode='RGB', size=size, color='white')
        ori_img_size = img.size
        if (ori_img_size[0] > size[0]) or (ori_img_size[1] > size[1]):
            if ori_img_size[0] > size[0]:
                diff_ratio = (ori_img_size[0]-size[0])*100/ori_img_size[0]
            else:
                diff_ratio = (ori_img_size[1]-size[1])*100/ori_img_size[1]
            conv_img_size = [int(ori_img_size[0]*(1-diff_ratio/100)), int(ori_img_size[1]*(1-diff_ratio/100))]
            img_new = img.resize((conv_img_size[0],conv_img_size[1]))
            x_pos = (size[0]//2-(conv_img_size[0]//2))
            y_pos = (size[1]//2-(conv_img_size[1]//2))
            Image.Image.paste(page, img_new, (x_pos, y_pos))
            page.save(output_path)
            page.close()
        else:
            diff_ratio = (size[0] - ori_img_size[0])*100/ori_img_size[0]
            conv_img_size = [int(ori_img_size[0] + (ori_img_size[0]*diff_ratio/100)), int(ori_img_size[1] + (ori_img_size[1]*diff_ratio/100))]
            if conv_img_size[1] > size[1]:
                diff_ratio = (size[1] - ori_img_size[1])*100/ori_img_size[1]
                conv_img_size = [int(ori_img_size[0] + (ori_img_size[0]*diff_ratio/100)), int(ori_img_size[1] + (ori_img_size[1]*diff_ratio/100))]
            x_pos = (size[0]//2-(conv_img_size[0]//2))
            y_pos = (size[1]//2-(conv_img_size[1]//2))
            img_new = img.resize( (conv_img_size[0], conv_img_size[1]) )
            Image.Image.paste(page, img_new, (x_pos, y_pos))
            page.save(output_path)
            page.close()
        del page, img, img_new
        gc.collect()
        print( gc.get_count())
        print('-- Converted complete --')
    
    def deleteCache(path):
        files = os.listdir(path)
        for file in files:
            os.remove(f'{path}/{file}')
        os.removedirs(path)
    
    page_size = {'Fit': None,
                 'A4': (2480, 3508),
                 'Letter': (2550, 3300)}
    page_size = page_size.get(mode)
    
    #0 เช็คถ้ายังมีไฟล์ cache ให้ลบทิ้ง
    dir_path = output_path.split('/')
    dir_path = '/'.join(dir_path[0:-1])
    cache_path = f"{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__"
    if os.path.exists(cache_path):
        deleteCache(cache_path)
    
    #1 Convert Image to PDF
    os.mkdir(f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__')
    try:
        if page_size == None:
            for index, f in enumerate(files_path):
                image = Image.open(f)
                image = image.convert(mode='RGB')
                size = image.size
                out = f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__/Page{index+1}.pdf'
                page_size_converter(image, out, size)
                image.close()
        else:
            size = page_size
            for index, f in enumerate(files_path):
                image = Image.open(f)
                image = image.convert(mode='RGB')
                out = f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__/Page{index+1}.pdf'
                page_size_converter(image, out, size)
                image.close()
    except:
        del image
        deleteCache(cache_path)
        gc.collect()
        print( gc.get_count() )
        print('-- Something error on convert img to pdf --')
        raise Exception
    
    #2 Merge File
    files_name = os.listdir(f'{cache_path}')
    files_path2 = [f"{cache_path}/{f_name}" for f_name in files_name]
    try:
        mergePDF(files_path2, output_path)
    except:
        del image
        deleteCache(cache_path)
        gc.collect()
        print( gc.get_count() )
        print('-- Something error on merge pdf --')
        raise Exception
    del image
    deleteCache(cache_path)
    gc.collect()
    print( gc.get_count() )
    print('-- Converted image to pdf complete --')



def pdf2image(files_path : list, output_directory_path, format): # Not Complete
    for index1, file in enumerate(files_path):
        print(file)
        didrectory_name = file.split('/')[-1]
        didrectory_name = didrectory_name.split('.')
        didrectory_name = didrectory_name[0]
        assert not(os.path.exists(f'{output_directory_path}/{didrectory_name}')), f'-- There is the same folder --\n-> {didrectory_name}'
    for index1, file in enumerate(files_path):
        didrectory_name = file.split('/')[-1]
        didrectory_name = didrectory_name.split('.')
        didrectory_name = didrectory_name[0]
        os.mkdir(f'{output_directory_path}/{didrectory_name}')
        print(index1)
        images = convert_from_path(file)
        print(images)
        for index2, image in enumerate(images):
            progressBar(index2+1, len(images))
            image.save(f'{output_directory_path}/{didrectory_name}/Page{index2}.{format}')
            del image
        del images
    gc.collect()
    print( gc.get_count() )



def compressPDF(files_path, output_directory_path, compress_level):
    # https://www.pdftron.com/api/PDFTronSDK/dotnetcore/pdftron.PDF.PDFDoc.html
    # เอกสารข้อมูลเพิ่มเติม
    def compress_pdf(initial_path, output_path): # ใช้ API จาก PDFTRON เข้ามาช่วย
        PDFNet.Initialize('demo:1665945704140:7ac023d503000000003a6d603a78d7996b18609c47a3e0e84cbbf6a419')
        pdf = PDFDoc(initial_path) # เปิดไฟล์
        Optimizer.Optimize(pdf) # ส่วนสำคัญ class และ method ตัวนี้จะทำให้ pdf มีขนาดที่ลดลง "ด้วยการลบ redundant(ความซับซ้อน)"
        pdf.Save(output_path, SDFDoc.e_linearized)
        pdf.Close()
        del pdf
        gc.collect()
    for f_path in files_path:
        f_name = f_path.split('/')[-1]
        f_name = f_name.split('.')[0]
        output_path = f'{output_directory_path}/{f_name}_compressed.pdf'
        compress_pdf(f_path, output_path)
    print( gc.get_count() )
        
        
        
def protectPFD(file_path, output_path, password):
    rd = PdfFileReader(file_path)
    wd = PdfFileWriter()
    for index in range(rd.numPages):
        page = rd.getPage(index)
        wd.add_page(page)
    wd.encrypt(password)
    wd.write(output_path)



if __name__ == '__main__':
    
    #file = [r"C:\Users\MSI Ryzen5\Downloads\Assignment-8.pdf".replace('\\', '/')]
    #output = r'C:/Users/MSI Ryzen5/Downloads/output'
    #format = 'png'
    #pdf2image(file, output, format)
    
    #out = 'out3.pdf'
    #page_size_converter(file_path=r"C:\Users\MSI Ryzen5\Pictures\Banner.jpg", output_path=out)
    pass