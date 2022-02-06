# 主程式(GUI模式)。

from DES_Func import *

from tkinter import *
from tkinter import filedialog

from os import startfile

root = Tk()
# 設置視窗標題為 DES
root.title('DES')
# 設置視窗大小為 800x600
root.geometry('800x600')
# 固定視窗大小為 800x600
root.resizable(0, 0)
# 設置視窗背景色為 白色
root.configure(background='white')


# 獲取 明文文件路徑
def get_plain_filePath():
    filename = filedialog.askopenfilename()
    plain_file_label.configure(text=filename)
    return filename


# 獲取 金鑰文件路徑
def get_key_filePath():
    filename = filedialog.askopenfilename()
    key_file_label.configure(text=filename)
    return filename


# 獲取 向量文件路徑
def get_IV_filePath():
    filename = filedialog.askopenfilename()
    IV_file_label.configure(text=filename)
    return filename


# 獲取 密文文件路徑
def get_cipher_filePath():
    filename = filedialog.askopenfilename()
    cipher_file_label.configure(text=filename)
    return filename


# 打開 明文
def open_plain_file():
    filePath = plain_file_label['text']
    startfile(filePath)


# 打開 金鑰
def open_key_file():
    filePath = key_file_label['text']
    startfile(filePath)


# 打開 向量
def open_IV_file():
    filePath = IV_file_label['text']
    startfile(filePath)


# 打開 密文
def open_cipher_file():
    filePath = cipher_file_label['text']
    startfile(filePath)


# 按下加密按鈕後，執行此函式
def des_encrypt():
    # 讀取DES模式
    mode_sel = modes[var.get()]
    # 讀取編碼模式
    encode_sel = encode[var2.get()]
    # 讀取 明文路徑
    plain = plain_file_label['text']
    # 讀取 金鑰路徑
    key = key_file_label['text']
    # 讀取 密文路徑
    cipher = cipher_file_label['text']

    # 讀取 向量路徑
    # 若DES模式為ECB，則向量路徑設置為空
    if mode_sel == 'ECB':
        IV = None
    else:
        IV = IV_file_label['text']

    # 執行DES加密
    Encrypt(mode_sel, encode_sel, plain, key, cipher, IV)
    # 設置state標籤為'加密成功'
    state_label.configure(text='加密成功')


# 按下解密按鈕後，執行此函式
def des_decrypt():
    # 讀取DES模式
    mode_sel = modes[var.get()]
    # 讀取編碼模式
    encode_sel = encode[var2.get()]
    # 讀取 明文路徑
    plain = plain_file_label['text']
    # 讀取 金鑰路徑
    key = key_file_label['text']
    # 讀取 密文路徑
    cipher = cipher_file_label['text']

    # 讀取 向量路徑
    # 若DES模式為ECB，則向量路徑設置為空
    if mode_sel == 'ECB':
        IV = None
    else:
        IV = IV_file_label['text']

    # 執行DES解密
    Decrypt(mode_sel, encode_sel, plain, key, cipher, IV)
    # 設置state標籤為'解密成功'
    state_label.configure(text='解密成功')


plain_label = Label(root, text='DES 明文', fg='black', bg='white', height=1, width=8, anchor='center', font='Helvetica 18')
plain_file_label = Label(root, text='', font='Helvetica 12', height=1, width=36, bg='white', anchor='center')
plain_file_btn = Button(root, text='瀏覽檔案', bg='white', command=get_plain_filePath)
open_plain_file_btn = Button(root, text='開啟檔案', bg='white', command=open_plain_file)

key_label = Label(root, text='DES 金鑰', fg='black', bg='white', height=1, width=8, anchor='center', font='Helvetica 18')
key_file_label = Label(root, text='', font='Helvetica 12', height=1, width=36, bg='white', anchor='center')
key_file_btn = Button(root, text='瀏覽檔案', bg='white', command=get_key_filePath)
open_key_file_btn = Button(root, text='開啟檔案', bg='white', command=open_key_file)

IV_label = Label(root, text='DES 向量', fg='black', bg='white', height=1, width=8, anchor='center', font='Helvetica 18')
IV_file_label = Label(root, text='', font='Helvetica 12', height=1, width=36, bg='white', anchor='center')
IV_file_btn = Button(root, text='瀏覽檔案', bg='white', command=get_IV_filePath)
open_IV_file_btn = Button(root, text='開啟檔案', bg='white', command=open_IV_file)

cipher_label = Label(root, text='DES 密文', fg='black', bg='white', height=1, width=8, anchor='center', font='Helvetica 18')
cipher_file_label = Label(root, text='', font='Helvetica 12', height=1, width=36, bg='white', anchor='center')
cipher_file_btn = Button(root, text='瀏覽檔案', bg='white', command=get_cipher_filePath)
open_cipher_file_btn = Button(root, text='開啟檔案', bg='white', command=open_cipher_file)

plain_label.place(x=320, y=0)
plain_file_label.place(x=200, y=40)
plain_file_btn.place(x=550, y=40)
open_plain_file_btn.place(x=620, y=40)

key_label.place(x=320, y=80)
key_file_label.place(x=200, y=120)
key_file_btn.place(x=550, y=120)
open_key_file_btn.place(x=620, y=120)

IV_label.place(x=320, y=160)
IV_file_label.place(x=200, y=200)
IV_file_btn.place(x=550, y=200)
open_IV_file_btn.place(x=620, y=200)

cipher_label.place(x=320, y=240)
cipher_file_label.place(x=200, y=280)
cipher_file_btn.place(x=550, y=280)
open_cipher_file_btn.place(x=620, y=280)

# 設置DES模式選項按鈕
modes = {0: 'ECB', 1: 'CBC', 2: 'CFB', 3: 'OFB', 4: 'CTR'}
var = IntVar()
var.set(0)

x, y = 240, 320
for val, mode in modes.items():
    Radiobutton(root, text=mode, variable=var, value=val, bg='white').place(x=x, y=y)
    x += 75

# 設置編碼模式選項按鈕
encode = {0: 'ASCII', 1: 'Hex', 2: 'Base64'}
var2 = IntVar()
var2.set(0)

x, y = 240, 360
for val, mode in encode.items():
    Radiobutton(root, text=mode, variable=var2, value=val, bg='white').place(x=x, y=y)
    x += 75

mode_label = Label(root, text='加密模式：', fg='black', bg='white', height=1, width=8, anchor='center', font='Helvetica 12')
encode_label = Label(root, text='編碼模式：', fg='black', bg='white', height=1, width=8, anchor='center', font='Helvetica 12')
mode_label.place(x=150, y=320)
encode_label.place(x=150, y=360)

encrypt_btn = Button(root, text='加密', command=des_encrypt)
encrypt_btn.place(x=275, y=400)

decrypt_btn = Button(root, text='解密', command=des_decrypt)
decrypt_btn.place(x=450, y=400)

state_label = Label(root, text='', bg='white', font='Helvetica 12')
state_label.place(x=350, y=440)

root.mainloop()
