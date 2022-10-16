from PyPDF2 import *

def meargePDF(files, path : str):
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



if __name__ == '__main__':
    files = list()
    n = int()
    while True:
        files.append(input(f'Enter file name no.{n+1} : '))
        if files[-1] == '0':
            del files[-1] 
            break
        n += 1
    meargePDF(files)