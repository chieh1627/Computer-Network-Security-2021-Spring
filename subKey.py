# 生成16組子金鑰。

from Table import Table


def PC1(key64):
    key56 = []
    for i in Table.PC_1:
        key56.append(int(key64[int(i) - 1]))
    C = key56[:28]
    D = key56[28:]
    return C, D


def PC2(C, D):
    key56 = C + D
    key48 = []
    for i in Table.PC_2:
        key48.append(int((key56[int(i) - 1])))
    return key48


def leftShift(num, C, D):
    Shift = int(Table.shiftBits[num - 1])

    new_C = C[Shift:] + C[:Shift]
    new_D = D[Shift:] + D[:Shift]

    return new_C, new_D


# 生成16組子密鑰
def generateKeys(realKey):
    C = [0] * 17
    D = [0] * 17
    subKey = [0] * 17

    C[0], D[0] = PC1(realKey)
    subKey[0] = PC2(C[0], D[0])

    for i in range(1, 17):
        C[i], D[i] = leftShift(i, C[i - 1], D[i - 1])
        subKey[i] = PC2(C[i], D[i])

    return subKey