from tkinter import *
from mainFunction import pdfFunction

def Menu_MergePDF():
    print('Menu_MergePDF')
    w1 = Tk()
    w1.mainloop()
    pass
def Menu_SplitPDF():
    print('Menu_SplitPDF')
    pass
def Menu_Image2PDF():
    print('Menu_Image2PDF')
    pass
def Menu_PDF2Image():
    print('Menu_PDF2Image')
    pass
def CompressPDF():
    print('CompressPDF')
    pass
def ProtectPDF():
    print('ProtectPDF')
    pass
menu_func = [Menu_MergePDF
             ,Menu_SplitPDF
             ,Menu_Image2PDF
             ,Menu_PDF2Image
             ,CompressPDF
             ,ProtectPDF]

root = Tk()
root.title('PDF Management (Beta Designed #02)')
root.geometry('1280x720')
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