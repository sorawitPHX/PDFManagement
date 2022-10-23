# Project นี้ถูกพัฒนาโดย 
# กลุ่ม NonSenior Dev
# นักศึกษาชั้นปีที่ 1 (ปี 2565)
# สาขาเทคโนโลยีสารสนเทศ (โครงการพิเศษ) 
# วิทยาลัยการคอมพิวเตอร์ 
# มหาวิทยาลัยขอนแก่น (Khon Kaen University)
try:
    from PyPDF2 import PdfFileReader
except ModuleNotFoundError as mne:
    print(f'''
          {"-"*40}
          !!-- ไม่สามารถเปิด Project app.py ได้ --!!
          เนื่องจาก {mne}
          {"-"*40}
          
          {"-"*74}
          {"!!-- วิธีแก้ไข --!!":^74}
          -- วิธีที่ 1.1 เปิด Virtual Environment --
            โดยเปิด cmd ที่ folder โปรเจค
            แล้วพิมพ์ env\\scripts\\activate.bat (ใช้ได้กับ Windows เท่านั้น)
            แล้วพิมพ์ py app.py หรือ python app.py
            
          -- วิธีที่ 1.2 ใช้ Virtual Environment ผ่าน VScode(Visual Studio code) --
            เปิด folder โปรเจคไปที่ VScode
            แล้วเลือก Interpreter เป็น "Python 3.10.6 ('env': venv)"
          
          -- วิธีที่ 2 ติดตั้ง Libary --
            โดยเปิด cmd ที่ folder โปรเจค
            แล้วพิมพ์ pip install -r requirment.txt
            
          ปล. เลือกวิธีใดวิธีหนึ่ง
          {"-"*74}
          ''')
    input('กด Enter เพื่อดำเนินการต่อ . . .')
    quit()
from MyPackage import MyPdfFunc # Module สร้างขึ้นมาเอง (function หลักที่คำนวณและเซฟไฟล์)
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import Combobox
import os
import gc # module ตัวนี้สำคัญมาก ไว้สำหรับใช้ clear memory ที่่ไม่ได้ใช้แล้ว แต่ยังค้างอยู่ใน memory

version = 'Release 1.0.6'

def MenuMergePDF(): # Complete
    # เมื่อกำการคลิก Menu ย่อยจาก MainMenu
    # จากนั้นจพทำการทำลาย window ของ MainMenu ทิ้ง (root.destoty)
    # โปรแกรมจะ สั่งให้ MainMenu ออกจาก mainloop (root.quit)
    # แล้ว MainMenu จะทำการ return เพื่อหยุดการทำงาน function เพื่อป้องกันการเปิด recursive (Run คำสั่งด้านล่าง stagement root.mainloop)
    global open_menu 
    root.destroy()
    root.quit()
    
    w1 = Tk()
    w1.title('Merge PDF')
    w1.iconbitmap('./image/Icon.ico')
    width = 1000
    height = 550
    # บรรทัดนี้คือการจัดให้ Window ที่ Popup ขึ้นมาจัดอยู่ตรงกลางจอ
    w1.geometry(f'{width}x{height}+{w1.winfo_screenwidth()//2-(width//2)}+{w1.winfo_screenheight()//2-(height//2)}')
    w1.resizable(False, False)
    
    
    # backend
    def back2Main():
        global open_menu
        open_menu = 1
        w1.destroy()
        w1.quit()
    
    def openFiles():
        fs = askopenfilenames(filetypes=[('PDF File', '*.pdf')])
        print(fs)
        for index, f in enumerate(fs):
            lib1.insert(index, f)
        
    def delete_ele():
        if lib1.size() > 0:
            select = lib1.curselection()
            lib1.delete(select)
            select_data = lib1.get(select)
            print(select)
            print(select_data)
    
    def up():
        if lib1.size() > 0:
            select = lib1.curselection()
            try:
                if select[0] != 0:
                    current_data = lib1.get(select)
                    data_above = lib1.get(select[0]-1)
                    lib1.delete(select[0]-1)
                    lib1.insert(select[0]-1, current_data)
                    lib1.delete(select)
                    lib1.insert(select, data_above)
            except:
                showwarning('Index out of range', 'Please select some elements to move')
    
    def down():
        if lib1.size() > 0:
            select = lib1.curselection()
            try:
                if select[0] != lib1.size()-1:
                    current_data = lib1.get(select)
                    data_below = lib1.get(select[0]+1)
                    lib1.delete(select[0]+1)
                    lib1.insert(select[0]+1, current_data)
                    lib1.delete(select)
                    lib1.insert(select, data_below)
            except:
                showwarning('Index out of range', 'Please select some elements to move')
    
    def clear():    
        lib1.delete(0, END)
        
    def compute():
        if lib1.size() != 0:
            output_path = asksaveasfilename(filetypes=[('PDF File', '*.pdf')], defaultextension=[('PDF File', '*.pdf')])
            if output_path:
                files_path = list()
                for order in range(lib1.size()):
                    files_path.append(lib1.get(order))
                try:
                    MyPdfFunc.mergePDF(files_path, output_path)
                except:
                    showerror('Error', 'There is something error')
                else:
                    if os.path.exists(output_path):
                        showinfo('Success', 'Export file success!')
                    else:
                        showwarning('Unable to export file', 'Unable to export file')
        else:
            showwarning('Cannot Merge', 'There are no files')
    
    
    # widget
    f0 = Frame(w1)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='left')
    f0.pack()
    
    f1 = Frame(w1, bd=10, cursor='arrow')
    f1.option_add('*font', '"Angsana New" 18')
    lb1 = Label(f1, text='- PDF Merger -', font='Impact 20')
    lb1.grid(row=0, columnspan=3)
    lb2 = Label(f1, text='Choose Files')
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    lib1 = Listbox(f1, width=80, height=8)
    lib1.grid(row=1, column=1)
    bn1 = Button(f1, text='Open Files', width=10, command=openFiles)
    bn1.grid(row=1, column=2, padx=5)
    
    f2 = Frame(f1)
    bn2 = Button(f2, text='Delete', width=8, command=delete_ele)
    bn2.pack()
    bn3 = Button(f2, text='Up', width=8, command=up)
    bn3.pack()
    bn4 = Button(f2, text='Down', width=8, command=down)
    bn4.pack()
    bn5 = Button(f2, text='Clear', width=8, command=clear)
    bn5.pack()
    f2.grid(row=1, column=0)
    
    bn6 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn6.grid(row=2, columnspan=3, pady=20, sticky='n')
    f1.pack(pady=20) 
    
    w1.mainloop()
    print('ออกจาก mainloop Menu1')
    return
    
    
    
def MenuSplitPDF(): # Complete
    global open_menu
    root.destroy()
    root.quit()
    
    w2 = Tk()
    w2.title('Split PDF')
    w2.iconbitmap('./image/Icon.ico')
    width = 800
    height = 450
    w2.geometry(f'{width}x{height}+{w2.winfo_screenwidth()//2 - (width//2)}+{w2.winfo_screenheight()//2 - (height//2)}')
    w2.resizable(False, False)
    
    # Backend 
    def back2Main():
        global open_menu
        open_menu = 1
        w2.destroy()
        w2.quit()
        
    def chooseFile():
        global f
        f = askopenfilename(filetypes=[('PDF File', '*.pdf')])
        if f:
            rd = PdfFileReader(f)
            tb1.configure(state=NORMAL)
            tb1.delete(0, END)
            tb1.insert(0, f)
            tb1.configure(state=DISABLED)
            tb2.configure(state=NORMAL)
            tb2.delete(0, END)
            tb2.insert(0, rd.numPages)
            tb2.configure(state=DISABLED)
            del rd
            gc.collect()
                        
    def compute():
        try:
            if tb1.get() == '': raise NameError
        except NameError:
            showwarning('Choose File First', 'Please choose file first')
        else:
            try:
                pages = tb3.get().split('-')
                if len(pages) > 2: raise ValueError
                start_page = int( pages[0] )
                end_page = int( pages[-1] )
                if start_page > int(tb2.get()): raise IndexError
                if end_page > int(tb2.get()): raise IndexError
                if start_page > end_page: raise IndexError
            except ValueError:
                showwarning('Format input Error', 'Please input Correctly\nPage(start)-Page(end)')
            except IndexError:
                showwarning('Page out of range', 'Please input Correctly')
            else:
                path = asksaveasfilename(filetypes=[('PDF File', '*.pdf')], defaultextension=[('PDF File', '*.pdf')])
                if path:
                    f_name = tb1.get()
                    print(path)
                    print('start :', start_page)
                    print('end :', end_page)
                    try:
                        MyPdfFunc.splitPDF(f_name, path, start_page, end_page)
                        if os.path.exists(path):
                            showinfo('Success', 'Export file Success!')
                        else:
                            showwarning('Fail', 'Unable to export file')
                    except:
                        showerror('Error', 'Something error')
    
    def clear():
        tb1.configure(state=NORMAL)
        tb1.delete(0, END)
        tb1.configure(state=DISABLED)
        tb2.configure(state=NORMAL)
        tb2.delete(0, END)
        tb2.configure(state=DISABLED)
        tb3.delete(0, END)
        
        
    # Widget
    f0 = Frame(w2)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='top')
    Label(f0, height=3).pack()
    f0.pack()
    lb0 = Label(w2, text='- Split PDF -', font='Impact 20')
    lb0.pack()
    
    f1 = Frame(w2)
    f1.option_add('*font', '"Angsana New" 18')
    lb1 = Label(f1, text='Select PDF File:')
    lb1.grid(row=0, column=0)
    tb1 = Entry(f1, width=60, state=DISABLED)
    tb1.grid(row=0, column=1)
    
    f2 = Frame(f1)
    bn1 = Button(f2, text='Choose File', width=10, command=chooseFile)
    bn1.pack(side='left', padx=10, pady=20)
    bn3 = Button(f2, text='Clear', width=8, command=clear)
    bn3.pack(padx=10, pady=20)
    f2.grid(row=3, columnspan=2)
    
    lb2 = Label(f1, text='Total Pages:')
    lb2.grid(row=1, column=0)
    tb2 = Entry(f1, width=60, state=DISABLED)
    tb2.grid(row=1, column=1)
    lb3 = Label(f1, text='Select Pages from:')
    lb3.grid(row=2, column=0)
    tb3 = Entry(f1, width=60)
    tb3.grid(row=2, column=1)
    
    bn2 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn2.grid(row=4, columnspan=3)
    f1.pack()

    w2.mainloop()
    
    print('ออกจาก mainloop w2')
    return
    
    
    
def MenuImage2PDF(): 
    global open_menu
    root.destroy()
    root.quit()
    
    w3 = Tk()
    w3.title('Image to PDF')
    w3.iconbitmap('./image/Icon.ico')
    width = 1000
    height = 600
    w3.geometry(f'{width}x{height}+{w3.winfo_screenwidth()//2 - (width//2)}+{w3.winfo_screenheight()//2 - (height//2)}')
    w3.resizable(False, False)
    
    # Backend 
    def back2Main():
        global open_menu
        open_menu = 1
        w3.destroy()
        w3.quit()

    def openFiles():
        fs = askopenfilenames(filetypes=[('PDF File', '*.png'), ('JPEG Files', ('*.jpg', '*.jpeg'))])
        for index, f in enumerate(fs):
            lib1.insert(index, f)
        #print(fs)
        
    def delete_ele():
        if lib1.size() > 0:
            select = lib1.curselection()
            lib1.delete(select)
            select_data = lib1.get(select)
            print(select)
            print(select_data)
    
    def up():
        if lib1.size() > 0:
            select = lib1.curselection()
            if select[0] != 0:
                current_data = lib1.get(select)
                data_above = lib1.get(select[0]-1)
                lib1.delete(select[0]-1)
                lib1.insert(select[0]-1, current_data)
                lib1.delete(select)
                lib1.insert(select, data_above)
    
    def down():
        if lib1.size() > 0:
            select = lib1.curselection()
            if select[0] != lib1.size()-1:
                current_data = lib1.get(select)
                data_below = lib1.get(select[0]+1)
                lib1.delete(select[0]+1)
                lib1.insert(select[0]+1, current_data)
                lib1.delete(select)
                lib1.insert(select, data_below)
    
    def clear():
        lib1.delete(0, END)
        
    def compute():
        #print(fs)
        if lib1.size() > 0:
            output_path = asksaveasfilename(filetypes=[('PDF File', '*.pdf')], defaultextension=[('PDF File', '*.pdf')])
            if output_path:
                files_path = [lib1.get(order) for order in range(lib1.size())]
                page_size_mode = cb1.get()
                page_size_mode = page_size_mode.split(' ')[0]
                #MyPdfFunc.image2pdf(files_path, output_path, page_size_mode)
                try:
                    MyPdfFunc.image2pdf(files_path, output_path, page_size_mode)
                except:
                    showerror('Unable to export file', 'There is something error')
                else:
                    showinfo('Success', 'Export file Success!')
        else:
            showwarning('File not found', 'Please choose file first')
        

    # Widget
    f0 = Frame(w3)
    f0.option_add('*font', '"Angsana New" 20')
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='top')
    f0.pack()
    
    f1 = Frame(w3, bd=10, cursor='arrow')
    f1.option_add('*font', '"Angsana New" 18')
    lb1 = Label(f1, text='- Image to PDF Converter -', font='Impact 20')
    lb1.grid(row=0, columnspan=3)
    lb2 = Label(f1, text='Choose Files')
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    lib1 = Listbox(f1, width=80, height=8)
    lib1.grid(row=1, column=1)
    bn1 = Button(f1, text='Open Files', width=8, command=openFiles)
    bn1.grid(row=1, column=2, padx=5)
    
    f2 = Frame(f1)
    bn2 = Button(f2, text='Delete', width=8, command=delete_ele)
    bn2.pack()
    bn3 = Button(f2, text='Up', width=8, command=up)
    bn3.pack()
    bn4 = Button(f2, text='Down', width=8, command=down)
    bn4.pack()
    bn5 = Button(f2, text='Clear', width=8, command=clear)
    bn5.pack()
    f2.grid(row=1, column=0)
    
    f3 = Frame(f1)
    Label(f3, text='Page size').pack()
    cb1 = Combobox(f3, justify='center', width=28)
    cb1['values'] = ['Fit (Same page size as image)', 'A4 (297x210 mm)', 'Letter (215x279.4 mm)']
    cb1.current(1)
    cb1['state'] = 'readonly'
    cb1.pack()
    f3.grid(row=2, columnspan=3, pady=10)
    
    bn6 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn6.grid(row=3, columnspan=3, pady=10, sticky='n')
    f1.pack(pady=20)
    
    w3.mainloop()
    print('ออกจาก mainloop w3')
    return



def MenuPDF2Image(): 
    global open_menu
    root.destroy()
    root.quit()
    
    w4 = Tk()
    w4.title('PDF to Image')
    w4.iconbitmap('./image/Icon.ico')
    width = 1000
    height = 600
    w4.geometry(f'{width}x{height}+{w4.winfo_screenwidth()//2 - (width//2)}+{w4.winfo_screenheight()//2 - (height//2)}')
    w4.resizable(False, False)
    
    # Backend 
    def back2Main():
        global open_menu
        open_menu = 1
        w4.destroy()
        w4.quit()
            
    def openFiles():
        fs = askopenfilenames(filetypes=[('PDF File', '*.pdf')])
        for index, f in enumerate(fs):
            lib1.insert(index, f)
        
    def delete_ele():
        if lib1.size() > 0:
            select = lib1.curselection()
            lib1.delete(select)
            select_data = lib1.get(select)
            print(select)
            print(select_data)
    
    def up():
        if lib1.size() > 0:
            select = lib1.curselection()
            if select[0] != 0:
                current_data = lib1.get(select)
                data_above = lib1.get(select[0]-1)
                lib1.delete(select[0]-1)
                lib1.insert(select[0]-1, current_data)
                lib1.delete(select)
                lib1.insert(select, data_above)
    
    def down():
        if lib1.size() > 0:
            select = lib1.curselection()
            if select[0] != lib1.size()-1:
                current_data = lib1.get(select)
                data_below = lib1.get(select[0]+1)
                lib1.delete(select[0]+1)
                lib1.insert(select[0]+1, current_data)
                lib1.delete(select)
                lib1.insert(select, data_below)
    
    def clear():
        lib1.delete(0, END)
        
    def compute():
        if lib1.size() > 0:
            directory_path = askdirectory()
            if directory_path:
                files_path = [lib1.get(order) for order in range(lib1.size())]
                format = cb.get()
                format = (format.split('.')[-1]).lower()
                print(format)
                try:
                    MyPdfFunc.pdf2image(files_path, directory_path, format)
                    showinfo('Success', 'Export file success!')
                except AssertionError:
                    showwarning('Unable to export', 'Unable to export file because the same files have been exist')
                except:
                    showerror('Error', 'There is something error')
        else:
            showwarning('File not found', 'Please input file first')
        
        
    # Widget
    f0 = Frame(w4)
    f0.option_add('*font', '"Angsana New" 20')
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='top')
    f0.pack()
    
    f1 = Frame(w4, bd=10, cursor='arrow')
    f1.option_add('*font', '"Angsana New" 18')
    lb1 = Label(f1, text='- PDF to Image Converter -', font='Impact 20')
    lb1.grid(row=0, columnspan=3)
    lb2 = Label(f1, text='Choose Files')
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    lib1 = Listbox(f1, width=80, height=8)
    lib1.grid(row=1, column=1)
    bn1 = Button(f1, text='Open Files', width=8, command=openFiles)
    bn1.grid(row=1, column=2, padx=5)
    
    f2 = Frame(f1)
    f2.grid(row=1, column=0)
    bn2 = Button(f2, text='Delete', width=8, command=delete_ele)
    bn3 = Button(f2, text='Up', width=8, command=up)
    bn4 = Button(f2, text='Down', width=8, command=down)
    bn5 = Button(f2, text='Clear', width=8, command=clear)
    bn2.pack()
    bn3.pack()
    bn4.pack()
    bn5.pack()
    
    cb = Combobox(f1, justify='center')
    cb['values'] = ('*.PNG', '*.JPG', '*.JPEG')
    cb['state'] = 'readonly'
    cb.current(0)
    cb.grid(row=3, columnspan=3)
    lb3 = Label(f1, text='Choose Format')
    lb3.grid(row=2, columnspan=3)
    bn7 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn7.grid(row=4, columnspan=3, pady=10, sticky='n')
    f1.pack(pady=20)
    
    w4.mainloop()
    print('ออกจาก mainloop w4')
    return



def MenuCompressPDF(): # Complete
    global open_menu
    root.destroy()
    root.quit()
    
    w5 = Tk()
    w5.title('Compress PDF')
    w5.iconbitmap('./image/Icon.ico')
    width = 1000
    height = 600
    w5.geometry(f'{width}x{height}+{w5.winfo_screenwidth()//2 - (width//2)}+{w5.winfo_screenheight()//2 - (height//2)}')
    w5.resizable(False, False)
    
    # Backend 
    def back2Main():
        global open_menu
        open_menu = 1
        w5.destroy()
        w5.quit()
        
    def openFiles():
        fs = askopenfilenames(filetypes=[('PDF File', '*.pdf')])
        for index, f in enumerate(fs):
            lib1.insert(index, f)
        
    def delete_ele():
        if lib1.size() > 0:
            select = lib1.curselection()
            lib1.delete(select)
            select_data = lib1.get(select)
            print(select)
            print(select_data)
    
    def up():
        if lib1.size() > 0:
            select = lib1.curselection()
            if select[0] != 0:
                current_data = lib1.get(select)
                data_above = lib1.get(select[0]-1)
                lib1.delete(select[0]-1)
                lib1.insert(select[0]-1, current_data)
                lib1.delete(select)
                lib1.insert(select, data_above)
    
    def down():
        if lib1.size() > 0:
            select = lib1.curselection()
            if select[0] != lib1.size()-1:
                current_data = lib1.get(select)
                data_below = lib1.get(select[0]+1)
                lib1.delete(select[0]+1)
                lib1.insert(select[0]+1, current_data)
                lib1.delete(select)
                lib1.insert(select, data_below)
    
    def clear():
        lib1.delete(0, END)
        
    def compute():
        if lib1.size() > 0:
            path = askdirectory()
            if path:
                files_path = [lib1.get(order) for order in range(lib1.size())]
                compre_lev = cb.get()
                try:
                    MyPdfFunc.compressPDF(files_path, path, compre_lev)
                except:
                    showerror('Error', 'There is something error')
                else:
                    showinfo('Success', 'Export file success')
        else:
            showwarning('File not found', 'Please input file first')
        
        
    # Widget
    f0 = Frame(w5)
    f0.option_add('*font', '"Angsana New" 20')
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='top')
    f0.pack()
    
    f1 = Frame(w5, bd=10, cursor='arrow')
    f1.option_add('*font', '"Angsana New" 18')
    lb1 = Label(f1, text='- Compress PDF -', font='Impact 20')
    lb1.grid(row=0, columnspan=3)
    lb2 = Label(f1, text='Choose Files')
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    lib1 = Listbox(f1, width=80, height=8)
    lib1.grid(row=1, column=1)
    bn1 = Button(f1, text='Open Files', width=8, command=openFiles)
    bn1.grid(row=1, column=2, padx=5)
    
    f2 = Frame(f1)
    bn2 = Button(f2, text='Delete', width=8, command=delete_ele)
    bn3 = Button(f2, text='Up', width=8, command=up)
    bn4 = Button(f2, text='Down', width=8, command=down)
    bn5 = Button(f2, text='Clear', width=8, command=clear)
    bn2.pack()
    bn3.pack()
    bn4.pack()
    bn5.pack()
    f2.grid(row=1, column=0)
    
    lb3 = Label(f1, text='Choose Compression Level')
    lb3.grid(row=2, columnspan=3)
    cb = Combobox(f1, width=28)
    #cb['values'] = ('Less quality, High Compression', 'Good quality, Good Compression', 'High Quality, Less Compression')
    cb['values'] = ['High Quality, Less Compression']
    cb['state'] = 'readonly'
    cb.current(0)
    cb.grid(row=3, columnspan=3)
    bn7 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn7.grid(row=4, columnspan=3, pady=10, sticky='n')
    f1.pack(pady=20)
    f1 = Frame()
    
    w5.mainloop()
    print('ออกจาก mainloop w4')
    return



def MenuProtectPDF(): # Complete
    global open_menu
    root.destroy()
    root.quit()
    
    w6 = Tk()
    w6.title('Protect PDF')
    w6.iconbitmap('./image/Icon.ico')
    width = 800
    height = 450
    w6.geometry(f'{width}x{height}+{w6.winfo_screenwidth()//2 - (width//2)}+{w6.winfo_screenheight()//2 - (height//2)}')
    w6.resizable(False, False)
    
    # Backend 
    def back2Main():
        global open_menu
        open_menu = 1
        w6.destroy()
        w6.quit()
        
    def chooseFile():
        global f
        f = askopenfilename(filetypes=[('PDF File', '*.pdf')])
        if f:
            global f_name
            f_name = f
            tb1.configure(state=NORMAL)
            tb1.delete(0, END)
            tb1.insert(0, f)
            tb1.configure(state=DISABLED)
            
    def compute():
        try:
            if not f_name: raise NameError
        except NameError:
            showwarning('File not found', 'Please choose file first')
        else:
            if tb2.get() != '' and tb3.get() != '':
                if tb2.get() == tb3.get():
                    path = asksaveasfilename(filetypes=[('PDF File', '*.pdf')], defaultextension=[('PDF File', '*.pdf')])
                    if path:
                        password = tb2.get()
                        try:
                            MyPdfFunc.protectPFD(f, path, password)
                            if os.path.exists(path):
                                showinfo('Success', 'Protected Success!')
                                clear_password()
                            else:
                                showwarning('Fail', 'Unable to export file')
                        except:
                            showerror('Error', 'Something error')
                else:
                    showwarning('Password not match', f'{"Password not match"}\n{"Please try again"}')
            else:
                showwarning('Wrong Format', f'Please input password')

    def clear_password():
        tb2.delete(0, END)
        tb3.delete(0, END)
    
    def clear():
        global f_name
        f_name = None
        tb1.configure(state=NORMAL)
        tb1.delete(0, END)
        tb1.configure(state=DISABLED)
        tb2.delete(0, END)
        tb3.delete(0, END)
        
        
    # Widget
    f0 = Frame(w6)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='top')
    Label(f0, height=3).pack()
    f0.pack()
    
    f1 = Frame(w6)
    f1.option_add('*font', '"Angsana New" 18')
    lb0 = Label(w6, text='- Protect PDF -', font='Impact 20')
    lb0.pack()
    lb1 = Label(f1, text='Select PDF File:')
    lb1.grid(row=0, column=0)
    tb1 = Entry(f1, width=60, state=DISABLED)
    tb1.grid(row=0, column=1)
    
    f2 = Frame(f1)
    bn1 = Button(f2, text='Choose File', width=10, command=chooseFile)
    bn1.pack(side='left', padx=10, pady=20)
    bn3 = Button(f2, text='Clear', width=8, command=clear)
    bn3.pack(padx=10, pady=20)
    f2.grid(row=3, columnspan=2)
    
    lb2 = Label(f1, text='Set password:')
    lb2.grid(row=1, column=0)
    tb2 = Entry(f1, width=60, show='*')
    tb2.grid(row=1, column=1)
    lb3 = Label(f1, text='Confirm Password:')
    lb3.grid(row=2, column=0)
    tb3 = Entry(f1, width=60, show='*')
    tb3.grid(row=2, column=1)
    
    bn2 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn2.grid(row=4, columnspan=3)
    f1.pack()
    
    w6.mainloop()
    print('ออกจาก mainloop w5')
    return



def MainMenu(): # Complete
    # ในการเปิดโปรแกรมย่อยขึ้นมา จะมีการ assign open_menu = 1 
    # นั่นคือเมื่อจบการทำงานของฟังก์ชั่นย่อยและ MainMenu จบการทำงาน จะส่งผลให้มีการเปิด MainMenu ขึ้นมาอีกครั้ง
    # ใน MainMenu จะ Assign open_menu = 0 
    # นั่นคือเมื่อไม่มีการเปิดในงานเมนูย่อยอื่นๆ เมื่อฟังก์ชั่นย่อยอื่นๆและฟังก์ชัน MainMenu จบการทำงาน
    # MainMenu จะไม่ถูกเรียกขึ้นมา และจบการทำงานของโปรแกรมในที่สุด
    # ถ้าไม่มีการประกาศตัวแปร open_menu ขึ้นมา เมนูจะไม่สามารถแสดงอีกครั้งได้หรือ
    global root, open_menu
    open_menu = 0
    menu_func = [MenuMergePDF
             ,MenuSplitPDF
             ,MenuImage2PDF
             ,MenuPDF2Image
             ,MenuCompressPDF
             ,MenuProtectPDF]
    # สร้างหน้าต่าง Window ขึ้นมา
    root = Tk()
    root.title(f'PDF Management with Simple GUI ({version})')
    root.iconbitmap('./image/Icon.ico')
    width = 1280
    height = 720
    root.geometry(f'{width}x{height}+{root.winfo_screenwidth()//2-(width//2)}+{root.winfo_screenheight()//2-(height//2)}')
    root.resizable(width=False, height=False)
    root.configure(background='#f3f0ec')

    top_img = PhotoImage(file='image/Top.png')
    Label(root, image=top_img).pack()

    main_img = PhotoImage(file='image/FrameMain(2).png')
    frame_main = Frame(root, width=1158, height=532, bg='#ffffff')
    main_img_background = Label(frame_main, image=main_img).pack()

    frame_items = Frame(root)
    items_top = Frame(frame_items, bg='#ffffff')
    items_below = Frame(frame_items, bg='#ffffff')

    btn_img = {1: PhotoImage(file='image/item_top_1(2).png'),
            2: PhotoImage(file='image/item_top_2(2).png'),
            3: PhotoImage(file='image/item_top_3(2).png'),
            4: PhotoImage(file='image/item_top_4(2).png'),
            5: PhotoImage(file='image/item_top_5(2).png'),
            6: PhotoImage(file='image/item_top_6(2).png')}
    btn = {1: Button(items_top, bd=0, bg='#ffffff', image=btn_img[1]),
        2: Button(items_top, bd=0, bg='#ffffff', image=btn_img[2]),
        3: Button(items_top, bd=0, bg='#ffffff', image=btn_img[3]),
        4: Button(items_below, bd=0, bg='#ffffff', image=btn_img[4]),
        5: Button(items_below, bd=0, bg='#ffffff', image=btn_img[5]),
        6: Button(items_below, bd=0, bg='#ffffff', image=btn_img[6])}
    for index, i in enumerate(btn.keys()):
        btn[i].configure(command=menu_func[index])
        btn[i].pack(side='left', padx=50, pady=20)
    items_top.pack()
    items_below.pack()
    frame_items.pack(pady=20)
    
    frame_main.place(x=61, y=170)
    root.mainloop()
    print('ออกจาก mainloop MainMenu')


# Main Program
open_menu = 1
if __name__ == '__main__':
    while open_menu == 1:
        MainMenu()
        gc.collect()
        print(gc.get_count())
        print('เคลียร์ memmory และ Return MainMenu')
    print('-- จบการทำงานโปรแกรมอย่างสมบูรณ์ --')