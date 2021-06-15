from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

GUI = Tk()
GUI.title('โปรแกรมคำนวนค่าใช้จ่าย')
# GUI.geometry('850x645')
GUI.iconbitmap('icons1.ico')

##### ทำให้ GUI อยู่ที่ center ของจอ #####

w = 850
h = 645

ws = GUI.winfo_screenwidth()
hs = GUI.winfo_screenheight()

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

GUI.geometry('{}x{}+{:.0f}+{:.0f}'.format(w, h, x, y))

#####################################
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
    with open('savedata.csv', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        return list(reader)


L = Label(T2, text='ตารางแสดงผลลัพธ์', font=FONT1).pack(pady=5)

header = ['ID', 'วัน-เวลา', 'รายการ', 'ราคา', 'จำนวน', 'รวม']

resulttable = ttk.Treeview(T2, columns=header, show='headings', height=20)
resulttable.pack()

[resulttable.heading(h, text=h) for h in header]

headerwidth = [160, 200, 170, 80, 80, 80]

for h, w in zip(header, headerwidth):
    resulttable.column(h, width=w)


alltransection = {}

def update_table():
    resulttable.delete(*resulttable.get_children())
    # for c in resulttable.get_children():
    #     resulttable.delete(c)
    # ก่อนที่จะทำการ update เราจะต้องลบ update เก่าที่แสดงอยู่ออกก่อน ไม่งั้นอันใหม่มันจะมาต่ออันเก่า
    try:
        data = read_csv_treeview()
        for d in data:
            resulttable.insert('', 0, value=d) # คือการใส่ข้อมูลลงไปใน treeview 0 คือ ล่างขึ้นบน end คือ บนลงล่าง
            alltransection[d[0]] = d
        print('all', alltransection)
    except:
        print('Not found')


def UpdateCSV():
    with open('savedata.csv', 'w', encoding='utf-8', newline='') as f:
        fw = csv.writer(f)

        # for v in alltransection.values():
        #     with open('savedata.csv', 'a', encoding='utf-8', newline='') as f:
        #         fw.writerow(v)

        data = alltransection.values()
        fw.writerows(data) # writerows = multiple line frow nested list

    # update_table()


def DeleteRecord(event=None):
    check = messagebox.askyesno('Confirm?', 'Do you want to delete?')

    if check == True:
        print('delete')
        select = resulttable.selection()
        print(select)
        data = resulttable.item(select)
        data = data['values']
        transectionid = str(data[0])

        del alltransection[transectionid]

        UpdateCSV()
        update_table()
    else:
        print('cancle')


resulttable.bind('<Delete>', DeleteRecord)

BDelete = Button(T2, text='Delete', command=DeleteRecord)
BDelete.place(x=200, y=500)

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
        stamp = datetime.now()
        dt = stamp.strftime('%Y-%m-%d-%H:%M:%S'.format(days[today]))
        transactionid = stamp.strftime('%Y%m%d%H%M%f')
        dt = days[today] + '-' + dt

        with open('savedata.csv', 'a', encoding='utf-8', newline='') as f:
             fw = csv.writer(f)
             data = [transactionid, dt, expense, price, ea, total]
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


##### Right Click Menu #####

def EditRecord():
    POPUP = Toplevel() # Toplevel คล้ายๆ Tk() แต่ Tk() จะประกาศได้แค่ครั้งเดียว ฉะนั้นถ้าต้องการหน้าต่างเพิ่มอีกอันต้องใช้ Toplevel()
    # POPUP.geometry('600x450')

    w = 600
    h = 450

    ws = GUI.winfo_screenwidth()
    hs = GUI.winfo_screenheight()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    POPUP.geometry('{}x{}+{:.0f}+{:.0f}'.format(w, h, x, y))


    POPUP.title('Edit Record')

    L = Label(POPUP, text='รายการค่าใช้จ่าย', font=FONT1).pack(pady=5)

    v_expense = StringVar()
    E1 = Entry(POPUP, textvariable=v_expense, font=FONT1)
    E1.pack()

    L = Label(POPUP, text='ราคา (บาท)', font=FONT1).pack(pady=5)

    v_price = StringVar()
    E2 = Entry(POPUP, textvariable=v_price, font=FONT1)
    E2.pack()

    L = Label(POPUP, text='จำนวน', font=FONT1).pack(pady=5)

    v_ea = StringVar()
    E3 = Entry(POPUP, textvariable=v_ea, font=FONT1)
    E3.pack()

    def Edit():
        # print(transectionid)
        # print(alltransection)
        olddata = alltransection[transectionid]
        print('OLD : ', olddata)
        v1 = v_expense.get()
        v2 = int(v_price.get())
        v3 = int(v_ea.get())
        total = v2 * v3
        newdata = [olddata[0], olddata[1], v1, v2, v3, total]
        alltransection[transectionid] = newdata

        UpdateCSV()
        update_table()

        POPUP.destroy() # ปิด POPUP



    B1_img = PhotoImage(file='icons8.png').subsample(2)

    B1 = Button(POPUP, text=f'{"Save": >{5}}', command=Edit, image=B1_img, compound='left')
    B1.pack(ipadx=60, ipady=15, pady=10)

    # get data in select record
    select = resulttable.selection()
    print(select)
    data = resulttable.item(select)
    data = data['values']
    print(data)
    transectionid = str(data[0])

    # ดึงค่าเก่ามาให้ดู
    v_expense.set(data[2])
    v_price.set(data[3])
    v_ea.set(data[4])



    POPUP.mainloop()
    

rightclick = Menu(GUI, tearoff=0)
rightclick.add_command(label='Edit', command=EditRecord)
rightclick.add_command(label='Delete', command=DeleteRecord)


def menupopup(event):
    # print(event.x_root, event.y_root) # แสดงตำแหน่ง click
    rightclick.post(event.x_root, event.y_root) # post คือ เอา menu ไปแปะ ที่ตำแหน่งของ event.x_root, event.y_root
    # event.x_root, event.y_root ใส่ + 1 หรือ ไรเพิ่มเติมได้

resulttable.bind('<Button-2>', menupopup) # <Button-3> คือ click ขวา macOS คือ <Button-2>
# ถ้าใส่ GUI แทนที่ resulttable จะ click ได้ทั่ว GUI
##############################


update_table()
GUI.mainloop()

