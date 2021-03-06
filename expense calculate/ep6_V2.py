from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

GUI = Tk()
GUI.title('โปรแกรมคำนวนค่าใช้จ่าย')
GUI.geometry('700x645')
GUI.iconbitmap('icons1.ico')

FONT1 = (None, 25)
FONT2 = (None, 18)

menubar = Menu(GUI)
GUI.config(menu=menubar)

filemenu = Menu(menubar, tearoff=0)  # tearoff=0 คือ เอาเส้นปะ ใน menu ออก ใน mac ไม่มีอยู่แล้ว
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Import .CSV')
filemenu.add_command(label='Exit',command=lambda: GUI.withdraw())

def About():
    messagebox.showinfo('About', 'นี่คือรายการคำนวนค่าใช้จ่าย\nสามารถคำนวนแล้วดูประวัติย้อนหลังได้\nถ้าใช้งานได้ดีสามารถ Donate ได้')

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=About)

def Donate():
    messagebox.showinfo('Donate', 'คุณสามารถ Donate ได้ที่\nDOGE Coin : DGTZaMmkP5gPiWEvKaoKS5Y7torxHnUgjC\nขอบคุณที่ให้การสนับสนุนครับ')

donatemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Donate', menu=donatemenu)
donatemenu.add_command(label='Donate', command=Donate)

Tab = ttk.Notebook(GUI)

T1 = Frame(Tab)
T2 = Frame(Tab)

Tab.pack(fill=BOTH, expand=True)  # วาง Tab ลงไป

T1_img = PhotoImage(file='T1.png')
T2_img = PhotoImage(file='T2.png')


Tab.add(T1, text=f'{"คำนวนค่าใช้จ่าย": ^{20}}', image=T1_img, compound='left')
Tab.add(T2, text=f'{"สรุปค่าใช้จ่าย": ^{20}}', image=T2_img, compound='left')

def read_csv_treeview():
    with open('ep6.csv', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        return list(reader)


L = Label(T2, text='ตารางแสดงผลลัพธ์', font=FONT1).pack(pady=5)

header = ['วัน-เวลา', 'รายการ', 'ราคา', 'จำนวน', 'รวม']

resulttable = ttk.Treeview(T2, columns=header, show='headings', height=20)
resulttable.pack()

[resulttable.heading(h, text=h) for h in header]

headerwidth = [150, 170, 80, 80, 80]

for h, w in zip(header, headerwidth):
    resulttable.column(h, width=w)

def update_table():
    resulttable.delete(*resulttable.get_children())
    # for c in resulttable.get_children():
    #     resulttable.delete(c)
    # ก่อนที่จะทำการ update เราจะต้องลบ update เก่าที่แสดงอยู่ออกก่อน ไม่งั้นอันใหม่มันจะมาต่ออันเก่า
    data = read_csv_treeview()
    for d in data:
        resulttable.insert('', 0, value=d)

F1 = Frame(T1)
F1.pack(pady=20)


bg = PhotoImage(file='noun_Cashier_2407109.png').subsample(8)
bg_img = Label(F1, image=bg)
bg_img.pack()


L = Label(F1, text='รายการค่าใช้จ่าย', font=FONT1).pack(pady=5)

v_expense = StringVar()
E1 = Entry(F1, textvariable=v_expense, font=FONT1)
E1.pack()

L = Label(F1, text='ราคา (บาท)', font=FONT1).pack(pady=5)

v_price = StringVar()
E2 = Entry(F1, textvariable=v_price, font=FONT1)
E2.pack()

L = Label(F1, text='จำนวน', font=FONT1).pack(pady=5)

v_ea = StringVar()
E3 = Entry(F1, textvariable=v_ea, font=FONT1)
E3.pack()

days = {'Mon': 'จันทร์',
        'Tue': 'อังคาร',
        'Wed': 'พุธ',
        'Thu': 'พฤหัส',
        'Fri': 'ศุกร์',
        'Sat': 'เสาร์',
        'Sun': 'อาทิตย์'}


def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    ea = v_ea.get()
    dt = datetime.now()

    if expense == '':
        messagebox.showwarning('Error', 'กรุณากรอกข้อมูล')
        return
    elif price == '':
        price = 1
    elif ea == '':
        ea = 1

    try:
        total = (int(price) * int(ea))

        print('รายการ : {} ราคา {} บาท จำนวน {} ชิ้น'.format(expense, price, ea))
        print('รวมแล้วราคา {} บาท'.format(total))

        v_expense.set("")
        v_price.set("")
        v_ea.set("")


        today = datetime.now().strftime('%a')
        dt = datetime.now().strftime('%Y-%m-%d-%H:%M:%S'.format(days[today]))
        dt = days[today] + '-' + dt

        with open('ep6.csv', 'a', encoding='utf-8', newline='') as f:
             fw = csv.writer(f)
             data = [dt, expense, price, ea, total]
             fw.writerow(data)

        update_table()

        v_result.set('รายการ : {} ราคา {} บาท จำนวน {} ชิ้น\nรวมแล้วราคา {} บาท'.format(expense, price, ea, total))
        E1.focus()
    except Exception as e:
        print('ERROR', e)
        messagebox.showinfo('ERROR', 'กรุณากรอกเฉพาะตัวเลข')
        v_expense.set("")
        v_price.set("")
        v_ea.set("")
        E1.focus()


E1.focus()
E1.bind('<Return>', lambda x: E2.focus())  # ถ้าไม่สร้าง lambda เราต้องสร้าง def ถึง bind ปุ่มได้
E2.bind('<Return>', lambda x: E3.focus())
E3.bind('<Return>', Save)

B1_img = PhotoImage(file='icons8.png').subsample(2)

B1 = Button(F1, text=f'{"Save": >{5}}', command=Save, image=B1_img, compound='left')
B1.pack(ipadx=60, ipady=15, pady=10)

v_result = StringVar()
v_result.set('---------- ผลลัพธ์ ----------')
result = Label(F1, textvariable=v_result, font=FONT2, fg='green')  # ถ้าเป็น ttk.Label ใช้ foreground='green' // ถ้า ไม่มี ttk ใช้ fg=''
result.pack(pady=15)

GUI.mainloop()

