from tkinter import *
from tkinter.filedialog import *
from unicodedata import name
from mainFunction import pdfFunction

def Back2Main():
    pass


def MenuMergePDF():
    root.destroy()
    w1 = Tk()
    w1.geometry('800x600')
    
    
    # backend
    def openFiles():
        global fs
        fs = askopenfiles(mode='r', filetypes=[('PDF File', '*.pdf')])
        show = str()
        for index, f in enumerate(fs):
            f = f.name.split('/')
            show += f'{index+1}. {f[-1]}\n'
        show_label_choose_file.configure(text='- Selected Files -')
        show_choose_files.configure(text=show)
        
    def compute():
        path = asksaveasfile(filetypes=[('PDF File', '*.pdf')], defaultextension=[('PDF File', '*.pdf')])
        pdfFunction.meargePDF(fs, path.name)
    
    
    # widget
    f1 = Frame(w1, bd=10, cursor='arrow')
    Label(f1, text='Choose Files', font='Arial 16').grid(row=0, column=0, padx=5, sticky='e')
    Button(f1, text='Open Files', font='Arial 10', command=openFiles).grid(row=0, column=1, padx=5, sticky='n')
    Button(f1, text='Merge', font='Arial 10', command=compute).grid(row=1, columnspan=2, padx=20, sticky='n')
    f1.pack(pady=20)    
    
    Label(w1).pack()
    f2 = Frame(w1)
    show_label_choose_file = Label(f2, font='Arial 16')
    show_choose_files = Label(f2, font='Arial 10')
    show_label_choose_file.pack()
    show_choose_files.pack()
    f2.pack()
    
    
def MenuSplitPDF():
    root.destroy()
    w2 = Tk()
    

def MenuImage2PDF():
    root.destroy()
    w3 = Tk()
    

def MenuPDF2Image():
    root.destroy()
    w4 = Tk()

def MenuCompressPDF():
    root.destroy()
    w5 = Tk()

def MenuProtectPDF():
    root.destroy()
    w6 = Tk()

menu_func = [MenuMergePDF
             ,MenuSplitPDF
             ,MenuImage2PDF
             ,MenuPDF2Image
             ,MenuCompressPDF
             ,MenuProtectPDF]
def main():
    global root
    root = Tk()
    root.title('PDF Management (Beta Designed #02)')
    root.geometry('1280x720+100+10')
    root.resizable(width=False, height=False)
    root.configure(background='#f3f0ec')

    top_img = PhotoImage(file='image/Top.png')
    Label(root, image=top_img).pack()

    main_img = PhotoImage(file='image/FrameMain.png')
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
    

if __name__ == '__main__':
    main()