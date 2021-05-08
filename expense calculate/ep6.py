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

##### MENU #####

menubar = Menu(GUI)
GUI.config(menu=menubar)

# file menu
filemenu = Menu(menubar, tearoff=0)  # tearoff=0 คือ เอาเส้นปะ ใน menu ออก ใน mac ไม่มีอยู่แล้ว
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Import .CSV')
filemenu.add_command(label='Exit')

# help menu
def About():
    messagebox.showinfo('About', 'นี่คือรายการคำนวนค่าใช้จ่าย\nสามารถคำนวนแล้วดูประวัติย้อนหลังได้\nถ้าใช้งานได้ดีสามารถ Donate ได้')

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=About)

# donate menu
def Donate():
    messagebox.showinfo('Donate', 'คุณสามารถ Donate ได้ที่\nDOGE Coin : DGTZaMmkP5gPiWEvKaoKS5Y7torxHnUgjC\nขอบคุณที่ให้การสนับสนุนครับ')

donatemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Donate', menu=donatemenu)
donatemenu.add_command(label='Donate', command=Donate)




# Tab 1

Tab = ttk.Notebook(GUI)  # หลักการสร้่ง tab ไล่จากพื้นฐาน GUI > Tab > Frame > ข้างใน frame

T1 = Frame(Tab)  # สร้าง Frame ให้ Tab สามารถใส่ , width=400 , height ให้กับ Frame ได้ 
T2 = Frame(Tab)

Tab.pack(fill=BOTH, expand=True)  # วาง Tab ลงไป
# fill X คือให้มีการขยายในแนวแกน x
# ต้องใส่ expand ด้วย ถ้าไม่ใส่ fill และ expand ใน Frame ของ Tab จะมองไม่เห็น

T1_img = PhotoImage(file='T1.png')
T2_img = PhotoImage(file='T2.png')


Tab.add(T1, text=f'{"คำนวนค่าใช้จ่าย": ^{20}}', image=T1_img, compound='left')
Tab.add(T2, text=f'{"สรุปค่าใช้จ่าย": ^{20}}', image=T2_img, compound='left')
# f'{"รายรับ": ^{20}}' ไปดูใน file f string special คือ ทั้งหมด 20 อักษร ให้อักษรเราอยู่กลาง
# compound คือ การควบคุมรูปภาพ ให้อยู่ top left right bottom
##############



##### tree view #####


def read_csv_treeview():
    with open('ep6.csv', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        return list(reader)


L = Label(T2, text='ตารางแสดงผลลัพธ์', font=FONT1).pack(pady=5)

header = ['วัน-เวลา', 'รายการ', 'ราคา', 'จำนวน', 'รวม']

resulttable = ttk.Treeview(T2, columns=header, show='headings', height=20)
resulttable.pack()
# column คือ ให้มี column ตาม header ที่เราสร้าง 
# show='headings' คือ ให้ header ที่เราสร้าง ไปอยู่บนหัว



[resulttable.heading(h, text=h) for h in header]

# for h in header:
#     resulttable.heading(h, text=h)

# for i in range(len(header)):
#     resulttable.heading(header[i], text=header[i])

# resulttable.heading(header[0], text=header[0])
# resulttable.heading(header[1], text=header[1])
# resulttable.heading(header[2], text=header[2])
# resulttable.heading(header[3], text=header[3])
# resulttable.heading(header[4], text=header[4])





# ปรับขนาด header วิธี 1 
# resulttable.column('วัน-เวลา', width=10)
# resulttable.column('รายการ', width=10)
# resulttable.column('ราคา', width=10)
# resulttable.column('จำนวน', width=10)
# resulttable.column('วัน-เวลา', width=10)

# ปรับขนาด header วิธี 2 
headerwidth = [150, 170, 80, 80, 80]

for h, w in zip(header, headerwidth):
    resulttable.column(h, width=w)



##### insert data #####
def update_table():
    resulttable.delete(*resulttable.get_children())
    # for c in resulttable.get_children():
    #     resulttable.delete(c)
    # ก่อนที่จะทำการ update เราจะต้องลบ update เก่าที่แสดงอยู่ออกก่อน ไม่งั้นอันใหม่มันจะมาต่ออันเก่า
    data = read_csv_treeview()
    for d in data:
        resulttable.insert('', 0, value=d)

# resulttable.insert('', 'end', value=['monday', 'food', 30, 5, 150])
# end คือ จบละต่อแถวใหม่ข้างล่าง (ล่าสุดอยู่ล่าง) // 0 คือ อันใหม่มาต่อบน (ล่าสุดอยู่บน)


###############

##### label show csv #####
'''
F2 = Frame(T2)
F2.pack(pady=20)

v_statusbar = StringVar()

statusbar = Label(F2, textvariable=v_statusbar)
statusbar.pack(fill=X)
v_statusbar.set('------')


def read_csv():
    with open('ep6.csv', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
    return list(reader)


def update_data():
    getdata = read_csv()
    text = ''
    for i in getdata[-1:-13:-1]:
        text = text + ' '.join(i) + '\n'
    return v_statusbar.set(text)


# def update_data():
#     getdata = read_csv()
#     text = ' '.join([' '.join(i) + '\n' for i in getdata[-1:-25:-1]])
#     print([' '.join(i) for i in getdata[-1:-25:-1]])
#     return v_statusbar.set(text)


# def update_data():
#     getdata = read_csv()
#     v_statusbar.set('')
#     text = ' '
#     for i in getdata:
#         for ii in i:
#             text = text + ii + ' '
#         text = text + '\n'
#     # return text
#     return v_statusbar.set(text)


    # for i in getdata:
    #     text = text + '{} {} {} {} {}\n'.format(i[0], i[1], i[2], i[3], i[4])
    #     return text

'''
##############


F1 = Frame(T1)
F1.pack(pady=20)

#####

bg = PhotoImage(file='noun_Cashier_2407109.png').subsample(8)  # subsample ในย่อยใช้ได้ เฉพาะ png ว่ายอไปกี่เท่า
bg_img = Label(F1, image=bg)
bg_img.pack()


#####
L = Label(F1, text='รายการค่าใช้จ่าย', font=FONT1).pack(pady=5)

v_expense = StringVar()
E1 = Entry(F1, textvariable=v_expense, font=FONT1)
E1.pack()
#####

#####
L = Label(F1, text='ราคา (บาท)', font=FONT1).pack(pady=5)

v_price = StringVar()
E2 = Entry(F1, textvariable=v_price, font=FONT1)
E2.pack()
#####

#####
L = Label(F1, text='จำนวน', font=FONT1).pack(pady=5)

v_ea = StringVar()
E3 = Entry(F1, textvariable=v_ea, font=FONT1)
E3.pack()
#####

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
        return  # return ทำให้ขึ้น No Data แล้วจบ ไม่ไปต่อ // คือ จบ function ไปเลย ข้างล่างไม่ต้องทำต่อ
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

        with open('ep6.csv', 'w', encoding='utf-8', newline='') as f:
             fw = csv.writer(f)
             data = [dt, expense, price, ea, total]
             fw.writerow(data)

        # updatedata = update_data()
        # v_statusbar.set(updatedata)
        # v_statusbar.set(update_data())
        # update_data()
        update_table()

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

# GUI.bind('<Return>', Save)

B1_img = PhotoImage(file='icons8.png').subsample(2)

B1 = Button(F1, text=f'{"Save": >{5}}', command=Save, image=B1_img, compound='left')
B1.pack(ipadx=60, ipady=15, pady=10)

v_result = StringVar()
v_result.set('---------- ผลลัพธ์ ----------')
result = Label(F1, textvariable=v_result, font=FONT2, fg='green')  # ถ้าเป็น ttk.Label ใช้ foreground='green' // ถ้า ไม่มี ttk ใช้ fg=''
result.pack(pady=15)

GUI.mainloop()

