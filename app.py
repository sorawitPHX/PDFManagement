from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import Combobox
from PIL import ImageTk
from PyPDF2 import PdfFileReader
import os
import gc # module ตัวนี้สำคัญมาก ไว้สำหรับใช้ clear memory ที่่เป็น cache
from mainFunction import pdfFunction

def MenuMergePDF(): # Complete
    # เมื่อกำการคลิก Menu ย่อยจาก MainMenu
    # จากนั้นจพทำการทำลาย window ของ MainMenu ทิ้ง (root.destoty)
    # โปรแกรมจะ สั่งให้ MainMenu ออกจาก mainloop (root.quit)
    # แล้ว MainMenu จะทำการ return เพื่อหยุดการทำงาน function เพื่อป้องกันการเปิด recursive (Run คำสั่งด้านล่าง stagement root.mainloop)
    global counter 
    counter = 1 
    root.destroy()
    root.quit()
    
    w1 = Tk()
    w1.title('Merge PDF')
    w1.geometry('1000x550+300+100')
    w1.resizable(False, False)
    
    
    # backend
    def back2Main():
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
            path = asksaveasfilename(filetypes=[('PDF File', '*.pdf')], defaultextension=[('PDF File', '*.pdf')])
            if path:
                files = list()
                for order in range(lib1.size()):
                    files.append(lib1.get(order))
                try:
                    #files = [open(i, 'rb') for i in files]
                    pdfFunction.mergePDF(files, path)
                    if os.path.exists(path):
                        showinfo('Success', 'Export file success!')
                    else:
                        showwarning('Fail', 'Unable to export file')
                except:
                    showerror('Fail', 'Something wrong')
                finally:
                    #[i.close() for i in files]
                    #print([i.closed for i in files])
                    del files
        else:
            showwarning('Cannot Merge', 'There are no files')
    
    
    # widget
    f0 = Frame(w1)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='left')
    f0.pack()
    
    f1 = Frame(w1, bd=10, cursor='arrow')
    f1.option_add('*font', '"Angsana New" 18')
    lb1 = Label(f1, text='- PDF Merger -', font='Impact 20')
    lb2 = Label(f1, text='Choose Files')
    lib1 = Listbox(f1, width=80, height=8)
    bn1 = Button(f1, text='Open Files', width=10, command=openFiles)
    lb1.grid(row=0, columnspan=3)
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    lib1.grid(row=1, column=1)
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
    bn6 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn6.grid(row=2, columnspan=3, pady=20, sticky='n')
    f1.pack(pady=20) 
    
    w1.mainloop()
    print('ออกจาก mainloop Menu1')
    return
    
    
    
def MenuSplitPDF(): # Complete
    global counter
    counter = 1
    root.destroy()
    root.quit()
    
    w2 = Tk()
    w2.title('Split PDF')
    w2.geometry('800x500+200+200')
    w2.resizable(False, False)
    
    # Backend 
    def back2Main():
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
            #print(gc.get_count())
                        
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
                        pdfFunction.splitPDF(f_name, path, start_page, end_page)
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
    
    f1 = Frame(w2)
    f1.option_add('*font', '"Angsana New" 18')
    lb0 = Label(w2, text='- Split PDF -', font='Impact 20')
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
    
    

def MenuImage2PDF(): # Complete
    global counter
    counter = 1
    root.destroy()
    root.quit()
    
    w3 = Tk()
    w3.title('Image to PDF')
    w3.geometry('1000x550+200+200')
    w3.resizable(False, False)
    
    # Backend 
    def back2Main():
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
                #files = [open(f, mode='rb') for f in files_path]
                try:
                    pdfFunction.image2pdf(files_path, output_path)
                    if os.path.exists(output_path):
                        showinfo('Success', 'Export file Success!')
                    else:
                        showwarning('Fail', 'Unable to export file')
                except:
                    showerror('Something error', 'There is something happened')
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
    lb2 = Label(f1, text='Choose Files')
    lib1 = Listbox(f1, width=80, height=8)
    bn1 = Button(f1, text='Open Files', width=8, command=openFiles)
    lb1.grid(row=0, columnspan=3)
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    lib1.grid(row=1, column=1)
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
    bn6 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn6.grid(row=2, columnspan=3, pady=20, sticky='n')
    f1.pack(pady=20)
    
    w3.mainloop()
    
    print('ออกจาก mainloop w3')
    return    



def MenuPDF2Image():
    global counter
    counter = 1
    root.destroy()
    root.quit()
    
    w4 = Tk()
    w4.title('PDF to Image')
    w4.geometry('1000x600+200+200')
    w4.resizable(False, False)
    
    # Backend 
    def back2Main():
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
            path = askdirectory()
            if path:
                files_path = [lib1.get(order) for order in range(lib1.size())]
                format = cb.get()
                format = (format.split('.')[-1]).lower()
                print(format)
                try:
                    output = pdfFunction.pdf2image(files_path, path, format)
                    if output == False:
                        showwarning('Fail', 'Unable to export file because the same files have been exist')
                        return
                    if os.path.exists(path):
                        showinfo('Success', 'Export file success!')
                    else:
                        showwarning('Fail', 'Unable to export file')
                except:
                    showerror('Error', 'Something error')
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
    lb2 = Label(f1, text='Choose Files')
    lib1 = Listbox(f1, width=80, height=8)
    bn1 = Button(f1, text='Open Files', width=8, command=openFiles)
    lb1.grid(row=0, columnspan=3)
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    lib1.grid(row=1, column=1)
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
    
    cb = Combobox(f1)
    cb['values'] = ('*.PNG', '*.JPG', '*.JPEG')
    cb['state'] = 'readonly'
    cb.current(0)
    lb3 = Label(f1, text='Choose Format')
    lb3.grid(row=2, columnspan=3)
    cb.grid(row=3, columnspan=3)
    bn7 = Button(f1, text='Export', bg='green', fg='white', width=8, command=compute)
    bn7.grid(row=4, columnspan=3, pady=10, sticky='n')
    f1.pack(pady=20)
    
    w4.mainloop()
    
    print('ออกจาก mainloop w4')
    return

    

def MenuCompressPDF():
    global counter
    counter = 1
    root.destroy()
    root.quit()
    
    w5 = Tk()
    w5.title('Compress PDF')
    w5.geometry('1000x600+200+200')
    w5.resizable(False, False)
    
    # Backend 
    def back2Main():
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
                pdfFunction.compressPDF(files_path, path, compre_lev)
                showinfo('Success', 'Export file success')
                '''
                try:
                    pdfFunction.compressPDF(files_path, path, compre_lev)
                    if os.path.exists(path):
                        showinfo('Success', 'Export file success')
                    else:
                        showwarning('Fail', 'Unable to export file')
                except:
                    showerror('Error', 'Something error')
                '''
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
    lb2 = Label(f1, text='Choose Files')
    lib1 = Listbox(f1, width=80, height=8)
    bn1 = Button(f1, text='Open Files', width=8, command=openFiles)
    lb1.grid(row=0, columnspan=3)
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    lib1.grid(row=1, column=1)
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



def MenuProtectPDF():
    global counter
    counter = 1
    root.destroy()
    root.quit()
    
    w6 = Tk()
    w6.title('Protect PDF')
    w6.geometry('1000x500+200+200')
    w6.resizable(False, False)
    
    # Backend 
    def back2Main():
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
                            pdfFunction.protectPFD(f, path, password)
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


def mainMenu():
    # ในโปรแกรมย่อยจะให้ counter = 1 คือ การ loop MainMenu ไปเรื่อยๆ 
    # ใน MainMenu จะให้ counter = 0 นั่นคือไม่มีการเปิดในงาน Menuอื่นๆ และโปรแกรมก็จะสามารถออกจาก Loop ได้แล้วจบการทำงานได้อย่างสมบูรณ์ ถ้าไม่มีการคลิกเปิด Menu ย่อยขึ้นมา
    # ถ้าไม่มีการประกาศตัวแปร counter ขึ้นมา เราจะไม่สามารถปิด MainMenu ได้ เพราะมันจะโดน Loop ไปเรื่อยๆ
    global root, counter
    counter = 0
    menu_func = [MenuMergePDF
             ,MenuSplitPDF
             ,MenuImage2PDF
             ,MenuPDF2Image
             ,MenuCompressPDF
             ,MenuProtectPDF]
    
    root = Tk()
    root.title('PDF Management (pre-release 0.1.0)')
    root.geometry('1280x720+100+10')
    root.resizable(width=False, height=False)
    root.configure(background='#f3f0ec')
    
    menu_bar = Menu(root)
    menu_bar_about = Menu(menu_bar, tearoff=0)
    menu_bar_about.add_command(label='About us', command='')
    menu_bar_about.add_command(label='About us', command='')
    menu_bar_about.add_command(label='About us', command='')
    menu_bar.add_cascade(label='Help', menu=menu_bar_about)

    top_img = ImageTk.PhotoImage(file='image/Top.png')
    Label(root, image=top_img).pack()

    main_img = ImageTk.PhotoImage(file='image/FrameMain.png')
    frame_main = Frame(root, width=1158, height=532, bg='#ffffff')
    main_img_background = Label(frame_main, image=main_img).pack()
    frame_main.place(x=61, y=170)

    fm_title = Frame(height=40, bg='#ffffff')
    fm_items = Frame()
    items_top = Frame(fm_items, bg='#ffffff')
    items_below = Frame(fm_items, bg='#ffffff')

    #Label(text='Select Menu', font='Kanit 24', bg='#ffffff').pack()
    btn_img = {1: PhotoImage(file='image/item_top_1.png'),
            2: PhotoImage(file='image/item_top_2.png'),
            3: PhotoImage(file='image/item_top_3.png'),
            4: PhotoImage(file='image/item_top_4.png'),
            5: PhotoImage(file='image/item_top_5.png'),
            6: PhotoImage(file='image/item_top_6.png')}
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
    fm_items.pack()
    
    root.mainloop()
    print('ออกจาก mainloop MainMenu')
    return    



if __name__ == '__main__':
    while True:
        mainMenu()
        if counter == 0:
            break
        gc.collect()
        print(gc.get_count())
        print('เคลียร์ memmory Return MainMenu')
    gc.collect()
    print(gc.get_count())
    print('จบการทำงานโปรแกรมอย่างสมบูรณ์')