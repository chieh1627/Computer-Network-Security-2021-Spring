# Feistel函式

from Table import Table


# IP置換
def IP(key_64):
    # 宣告new_key(list)，用於存放置換結果。
    new_key = [0] * 64
    # 利用IP置換表進行置換。
    for i in range(64):
        new_key[i] = int(key_64[Table.IP[i] - 1])
    # 將置換結果分為左半部及右半部。
    L = new_key[:32]
    R = new_key[32:]
    return L, R


# IIP逆置換
def IIP(key_64):
    # 宣告new_key(list)，用於存放置換結果。
    new_key = [0] * 64
    # 利用IIP置換表進行置換。
    for i in range(64):
        new_key[i] = int(key_64[Table.IIP[i] - 1])
    return new_key


# 將明文R 從 32位 擴展成 48位
def R_expand(R):
    new_R = [0] * 48
    for i in range(48):
        new_R[i] = int(R[Table.E[i] - 1])
    return new_R


# 將兩list 做xor
def xor(list1, list2):
    xor_result = []
    for i in range(len(list1)):
        xor_result.append(int(list1[i]) ^ int(list2[i]))
    return xor_result


# S盒置換
def S_Box(xor_result):
    S_result = ''
    for i in range(8):
        tmp = xor_result[i * 6:i * 6 + 6]
        row = int(tmp[0] * 2 + tmp[5])
        col = int(tmp[1] * 8 + tmp[2] * 4 + tmp[3] * 2 + tmp[4])
        S_result += bin(int(Table.S[i][row][col])).replace('0b', '').zfill(4)
    # 將S_result從str轉型成list。
    S_result = list(S_result)
    S_result = [int(i) for i in S_result]
    return S_result


# P置換
def P_Box(S_result):
    P_result = [0] * 32
    for i in range(32):
        P_result[i] = int(S_result[Table.P[i] - 1])
    return P_result


# feistel函式
def F(R, K):
    new_R = R_expand(R)
    RK_xor = xor(new_R, K)
    s_result = S_Box(RK_xor)
    p_result = P_Box(s_result)
    return p_result


# DES加密用完整feistel函式 (k[1] -> k[16])
def F_16(L, R, K):
    L_16 = [0] * 17
    R_16 = [0] * 17
    L_16[0] = L
    R_16[0] = R
    for i in range(16):
        R_16[i+1] = xor(L_16[i], F(R_16[i], K[i+1]))
        L_16[i+1] = R_16[i]
    result = R_16[16] + L_16[16]
    return result


# DES解密用完整feistel函式 (k[16] -> k[1])
def IF_16(L, R, K):
    L_16 = [0] * 17
    R_16 = [0] * 17
    L_16[0] = L
    R_16[0] = R
    for i in range(16):
        R_16[i+1] = xor(L_16[i], F(R_16[i], K[16 - i]))
        L_16[i+1] = R_16[i]
    result = R_16[16] + L_16[16]
    return result
