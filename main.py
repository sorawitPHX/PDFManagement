from tkinter import *
from tkinter.filedialog import *
from mainFunction import pdfFunction

def MenuMergePDF():
    root.destroy()
    w1 = Tk()
    w1.geometry('800x500')
    
    
    # backend
    def back2Main():
        w1.destroy()
        mainMenu()
    
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
        print(fs)
        path = asksaveasfile(filetypes=[('PDF File', '*.pdf')], defaultextension=[('PDF File', '*.pdf')])
        pdfFunction.meargePDF(fs, path.name)
    
    
    # widget
    f0 = Frame(w1)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='left')
    f0.pack()
    
    f1 = Frame(w1, bd=10, cursor='arrow')
    f1.option_add('*font', '"Angsana New" 18')
    lb1 = Label(f1, text='PDF Merger')
    lb1.grid(row=0, columnspan=3)
    lb2 = Label(f1, text='Choose Files')
    lb2.grid(row=1, column=0, padx=5, sticky='e')
    tb1 = Entry(f1, width=50)
    tb1.grid(row=1, column=1)
    bn1 = Button(f1, text='Open Files', command=openFiles)
    bn1.grid(row=1, column=2, padx=5, sticky='n')
    bn2 = Button(f1, text='Merge', bg='green', fg='white', width=8, command=compute)
    bn2.grid(row=2, columnspan=3, padx=20, sticky='n')
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
    w2.geometry('800x500')
    
    # Backend 
    def back2Main():
        w2.destroy()
        mainMenu()
        
    # Widget
    f0 = Frame(w2)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='left')
    f0.pack()
    
    f1 = Frame(w2)
    f1.option_add('*font', '"Angsana New" 18')
    
    lb1 = Label(f1, text='Select PDF File:')
    lb1.grid(row=0, column=0)
    tb1 = Entry(f1, width=50)
    tb1.grid(row=0, column=1)
    bn1 = Button(f1, text='Browse PDF', command='')
    bn1.grid(row=0, column=2)
    lb2 = Label(f1, text='Total Pages:')
    lb2.grid(row=1, column=0)
    tb2 = Entry(f1, width=50)
    tb2.grid(row=1, column=1)
    lb3 = Label(f1, text='Select Pages from:')
    lb3.grid(row=2, column=0)
    tb3 = Entry(f1, width=50)
    tb3.grid(row=2, column=1)
    
    bn2 = Button(f1, text='Split PDF', bg='green', fg='white', width=8)
    bn2.grid(row=3, columnspan=3)
    bn2 = Button(f1, text='Clear', width=8)
    bn2.grid(row=4, columnspan=3)
    
    
    f1.pack()
    
    

def MenuImage2PDF():
    root.destroy()
    w3 = Tk()
    w3.geometry('800x600')
    
    # Backend 
    def back2Main():
        w3.destroy()
        mainMenu()
        
    # Widget
    f0 = Frame(w3)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='left')
    f0.pack()
    
    

def MenuPDF2Image():
    root.destroy()
    w4 = Tk()
    w4.geometry('800x600')
    
    # Backend 
    def back2Main():
        w4.destroy()
        mainMenu()
        
    # Widget
    f0 = Frame(w4)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='left')
    f0.pack()
    


def MenuCompressPDF():
    root.destroy()
    w5 = Tk()
    w5.geometry('800x600')
    
    # Backend 
    def back2Main():
        w5.destroy()
        mainMenu()
        
    # Widget
    f0 = Frame(w5)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='left')
    f0.pack()



def MenuProtectPDF():
    root.destroy()
    w6 = Tk()
    w6.geometry('800x600')
    
    # Backend 
    def back2Main():
        w6.destroy()
        mainMenu()
        
    # Widget
    f0 = Frame(w6)
    Button(f0, text='Back to main', font='10', command=back2Main).pack(padx=10, side='left')
    f0.pack()



def mainMenu():
    menu_func = [MenuMergePDF
             ,MenuSplitPDF
             ,MenuImage2PDF
             ,MenuPDF2Image
             ,MenuCompressPDF
             ,MenuProtectPDF]
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
    mainMenu()