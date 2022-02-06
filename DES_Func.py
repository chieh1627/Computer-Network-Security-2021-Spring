# DES加解密函式

from math import ceil

from subKey import *
from Feistel import *
from fileProcess import *


def Encrypt(mode, encode, plainTxt, keyTxt, cipherTxt, IVTxt=None):
    # 讀取明文(字元)
    plainText = inputTxt(plainTxt)
    # 宣告暫存密文
    temp = ''

    # 讀取金鑰
    k = convert_in('ASCII', inputTxt(keyTxt))
    # 生成16組子金鑰
    key_16 = generateKeys(k)

    # 計算總共需要跑幾次
    # math.ceil()：無條件進位
    count = ceil(len(plainText) / 8)

    # 若有設定向量檔案的話，則讀取其值。
    if IVTxt is not None:
        # 讀取初始向量(字元)
        IVText = inputTxt(IVTxt)
        # 讀取初始向量(64bits)，若初始向量長度不足64bits，則padding 0至64bits
        IV = padding_64(convert_in('ASCII', IVText))

    # 宣告向量(儲存上一輪數據(64bits))
    vector = []

    for i in range(count):
        # 讀取明文(64bits)，若明文長度不足64bits，則padding 0至64bits
        P = padding_64(convert_in('ASCII', plainText[i * 8:i * 8 + 8]))

        # DES_ECB 加密
        # Ci = Ek(Pi)
        if mode == 'ECB':
            # 使用Feistel，生成密文(64bits)
            L, R = IP(P)
            result = listToString(IIP(F_16(L, R, key_16)))

        # DES_CBC 加密
        # Ci = Ek(Ci-1 ⊕ Pi), C0 = IV
        if mode == 'CBC':
            # 將明文與向量進行 XOR 處理
            if i == 0:
                new_M = xor(P, IV)
            else:
                new_M = xor(P, vector[i - 1])

            # 使用Feistel，生成密文(64bits)
            L, R = IP(new_M)
            result = listToString(IIP(F_16(L, R, key_16)))

            # 將密文存入vector中，以便下一輪的調用
            vector.append(result)

        # DES_CFB 加密
        # Ci = Ek(Ci-1) ⊕ Pi, C0 = IV
        if mode == 'CFB':
            if i == 0:
                L, R = IP(IV)
            else:
                L, R = IP(vector[i - 1])

            Key_IV_xor = listToString(IIP(F_16(L, R, key_16)))

            # 將金鑰與向量加密結果與明文做XOR
            result = listToString(xor(P, Key_IV_xor))

            # 將密文存入vector中，以便下一輪的調用
            vector.append(result)

        # DES_OFB 加密
        # Ci = Pi ⊕ Ek(Oi-1), O0 = IV
        if mode == 'OFB':
            if i == 0:
                L, R = IP(IV)
            else:
                L, R = IP(vector[i - 1])

            tmp = listToString(IIP(F_16(L, R, key_16)))

            # 將密文存入vector中，以便下一輪的調用
            vector.append(tmp)

            # 將金鑰與向量加密結果與明文做XOR
            result = listToString(xor(P, tmp))

        # DES_CTR 加密
        # Ci = Pi ⊕ Ek(counter)
        if mode == 'CTR':
            L, R = IP(IV)
            tmp = listToString(IIP(F_16(L, R, key_16)))

            IV = bin(int(IV, 2) + 1).replace('0b', '').zfill(64)
            # 將金鑰與向量加密結果與明文做XOR
            result = listToString(xor(P, tmp))

        temp += result

    C = convert_out(encode, temp)
    # 將密文寫入.txt文件中
    outputTxt(cipherTxt, C)


def Decrypt(mode, encode, plainTxt, keyTxt, cipherTxt, IVTxt=None):
    # 讀取密文
    ciphertext = inputTxt(cipherTxt)
    # 宣告空明文
    temp = ''

    # 讀取金鑰
    k = convert_in('ASCII', inputTxt(keyTxt))
    # 生成16組子金鑰
    key_16 = generateKeys(k)

    # 計算總共需要跑幾次
    # math.ceil()：無條件進位
    if encode == 'ASCII':
        count = ceil(len(ciphertext) / 8)
    if encode == 'Hex':
        count = ceil(len(ciphertext) / 16)
    if encode == 'Base64':
        ciphertext = convert_in('Base64', ciphertext)
        count = ceil(len(ciphertext) / 64)

    # 若有設定向量檔案的話，則讀取其值。
    if IVTxt is not None:
        # 讀取初始向量(字元)
        IVText = inputTxt(IVTxt)
        # 讀取初始向量(64bits)，若初始向量長度不足64bits，則padding 0至64bits
        IV = padding_64(convert_in('ASCII', IVText))

    # 宣告向量(儲存上一輪密文(64bits))
    vector = []

    for i in range(count):
        # 讀取密文(64Bits)
        if encode == 'ASCII':
            C = convert_in('ASCII', ciphertext[i * 8:i * 8 + 8])
        if encode == 'Hex':
            C = convert_in('Hex', ciphertext[i * 16:i * 16 + 16])
        if encode == 'Base64':
            C = ciphertext[i * 64:i * 64 + 64]

        # DES_ECB 解密
        # Pi = Dk(Ci)
        if mode == 'ECB':
            # 使用Feistel，生成密文(64bits)
            # 使用Feistel，生成明文(64Bin)
            L, R = IP(C)
            result = listToString(IIP(IF_16(L, R, key_16)))

        # DES_CBC 解密
        # Pi = Dk(Ci) ⊕ Ci-1 , C0 = IV
        if mode == 'CBC':
            # 將密文存入vector中，以便下一輪的調用
            vector.append(C)

            # 使用Feistel，生成明文(64Bits)
            L, R = IP(C)
            Ci = listToString(IIP(IF_16(L, R, key_16)))

            # 將明文與向量進行 XOR 處理
            if i == 0:
                result = xor(Ci, IV)
            else:
                result = xor(Ci, vector[i - 1])
            result = listToString(result)

        # DES_CFB 解密
        # Pi = Ek(Ci-1) ⊕ Ci, C0 = IV
        if mode == 'CFB':
            # 將密文存入vector中，以便下一輪的調用
            vector.append(C)

            # 使用Feistel，生成明文(64Bits)
            if i == 0:
                L, R = IP(IV)
            else:
                L, R = IP(list(vector[i - 1]))
            EC = listToString(IIP(F_16(L, R, key_16)))

            # 將明文與向量進行 XOR 處理
            result = listToString(xor(EC, C))

        # DES_OFB 解密
        # Pi = Ci ⊕ Ek(Oi-1), O0 = IV
        if mode == 'OFB':
            # 使用Feistel，生成明文(64Bits)
            if i == 0:
                L, R = IP(IV)
            else:
                L, R = IP(list(vector[i - 1]))
            EO = listToString(IIP(F_16(L, R, key_16)))
            # 將密文存入vector中，以便下一輪的調用
            vector.append(EO)

            # 將明文與向量進行 XOR 處理
            result = listToString(xor(EO, C))

        # DES_CTR 加密
        # Ci = Pi ⊕ Ek(counter)
        if mode == 'CTR':
            # 使用Feistel，生成明文(64Bits)
            L, R = IP(IV)
            EO = listToString(IIP(F_16(L, R, key_16)))

            IV = bin(int(IV, 2) + 1).replace('0b', '').zfill(64)
            # 將明文與向量進行 XOR 處理
            result = listToString(xor(EO, C))

        temp += result

    P = convert_out('ASCII', temp)
    # 將密文寫入.txt文件中
    outputTxt(plainTxt, P)

# Encrypt('ECB', 'Hex', 'p.txt', 'key.txt', 'c.txt', 'IV.txt')
# Decrypt('ECB', 'Hex', 'p.txt', 'key.txt', 'c.txt', 'IV.txt')
