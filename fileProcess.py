# 檔案or文字處理

def inputTxt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        return text


def outputTxt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


# 將 list 轉換成 string
def listToString(s):
    str1 = ''
    return str1.join('%s' % ID for ID in s)


def padding_64(s):
    if len(s) % 64 != 0:
        s += '0' * (64 - len(s) % 64)
    return s


def ASCII(mode, string):
    if mode == 'in':
        encode = ''
        for i in range(len(string)):
            encode += bin(ord(string[i])).replace('0b', '').zfill(8)
        return encode
    if mode == 'out':
        decode = ''
        count = int(len(string) / 8)
        for i in range(count):
            decode += chr(int(string[i * 8:i * 8 + 8], 2))
        return decode


def Hex(mode, string):
    if mode == 'in':
        decode = ''
        for i in range(len(string)):
            decode += bin(int(string[i], 16)).replace('0b', '').zfill(4)
        return decode
    if mode == 'out':
        decode = ''
        count = int(len(string) / 4)
        for i in range(count):
            decode += hex(int(string[i * 4:i * 4 + 4], 2)).replace('0x', '')
        return decode


def Base64(mode, string):
    index = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    if mode == 'in':
        decode = ''
        if string[-1] == '=' and string[-2] == '=':
            count = 2
        elif string[-1] == '=':
            count = 4
        else:
            count = 0
        for i in range(len(string)):
            for j in range(len(index)):
                if string[i] == index[j]:
                    decode += bin(j).replace('0b', '').zfill(6)
        decode += '0' * count
        return decode
    if mode == 'out':
        encode = ''

        mod = len(string) % 6
        count = int(len(string) / 6)

        if mod == 2:
            string += '0' * 4
        elif mod == 4:
            string += '0' * 2

        for i in range(count):
            tmp = index[int(string[i * 6:i * 6 + 6], 2)]
            encode += tmp

        if mod == 2:
            encode += '=' * 2
        elif mod == 4:
            encode += '=' * 1
        return encode


def convert_in(mode, string):
    # 編碼模式 to bin
    encode = ''
    if mode == 'ASCII':
        encode = ASCII('in', string)
    if mode == 'Hex':
        encode = Hex('in', string)
    if mode == 'Base64':
        encode = Base64('in', string)
    return encode


def convert_out(mode, string):
    # bin to 編碼模式
    decode = ''
    # 將64bits，每8bits轉換成ASCII
    if mode == 'ASCII':
        decode = ASCII('out', string)
    # 將64bits，每4bits轉換成Hex
    if mode == 'Hex':
        decode = Hex('out', string)
    # 將64bits，每6bits轉換成Base64
    if mode == 'Base64':
        decode = Base64('out', string)
    return decode
