from PyPDF2 import *
from pdf2image import convert_from_path
from PIL import Image
from PDFNetPython3.PDFNetPython import PDFDoc, SDFDoc, Optimizer, PDFNet
import gc
import os



def progressBar(process, total):
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



def image2pdf(files_path, output_path='./'):
    def deleteCache(path):
        files = os.listdir(path)
        for file in files:
            os.remove(f'{path}/{file}')
        os.removedirs(path)
    
    dir_path = output_path.split('/')
    dir_path = '/'.join(dir_path[0:-1])
    cache_path = f"{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__"
    
    if os.path.exists(cache_path):
        deleteCache(cache_path)
        
    os.mkdir(f'{dir_path}/__PDFMANAGEMENT_PROJECT_TEMP__')
    try:
        for index, f in enumerate(files_path):
            image = Image.open(f)
            conv_image = image.convert(mode='RGB')
            conv_image.save(f'{cache_path}/{index+1}.pdf', 'pdf')
            image.close()
            conv_image.close()
    except:
        del image, conv_image
        deleteCache(cache_path)
        gc.collect()
        print( gc.get_count() )
        print('-- Something error on convert img to pdf --')
        raise Exception
    files_name = os.listdir(f'{cache_path}')
    files_path2 = [f"{cache_path}/{f_name}" for f_name in files_name]
    try:
        mergePDF(files_path2, output_path)
    except:
        del image, conv_image
        deleteCache(cache_path)
        gc.collect()
        print( gc.get_count() )
        print('-- Something error on merge pdf --')
        raise Exception
    del image, conv_image
    deleteCache(cache_path)
    gc.collect()
    print( gc.get_count() )
    print('-- Converted image to pdf complete --')



def pdf2image(files_path : list, output_directory_path, format):
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

def compressPDF(files, path, compress_level):
    # https://www.pdftron.com/api/PDFTronSDK/dotnetcore/pdftron.PDF.PDFDoc.html
    # เอกสารข้อมูลเพิ่มเติม
    def compress_pdf(initial_path, output_path): # ใช้ API จาก PDFTRON เข้ามาช่วย
        PDFNet.Initialize('demo:1665945704140:7ac023d503000000003a6d603a78d7996b18609c47a3e0e84cbbf6a419')
        pdf = PDFDoc(initial_path) # เปิดไฟล์
        Optimizer.Optimize(pdf) # ส่วนสำคัญ class และ method ตัวนี้จะทำให้ pdf มีขนาดที่ลดลง "ด้วยการลบ redundant(ความซับซ้อน)"
        pdf.Save(output_path, SDFDoc.e_linearized)
        pdf.Close()
    for f_path in files:
        f_name = f_path.split('/')[-1]
        f_name = f_name.split('.')[0]
        compress_pdf(f_path, f'{path}/{f_name}_compressed.pdf')
        
        
        
def protectPFD(file, path, password):
    rd = PdfFileReader(file)
    wd = PdfFileWriter()
    for index in range(rd.numPages):
        page = rd.getPage(index)
        wd.add_page(page)
    wd.encrypt(password)
    wd.write(path)



if __name__ == '__main__':
    file = [r"C:\Users\MSI Ryzen5\Downloads\Assignment-8.pdf".replace('\\', '/')]
    output = r'C:/Users/MSI Ryzen5/Downloads/output'
    format = 'png'
    pdf2image(file, output, format)
    pass