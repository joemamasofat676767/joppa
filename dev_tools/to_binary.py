import ctypes
import sys

with open("knowledge.bin", "r") as file:
    ToBin = file.read().replace("\n", " 0 ")
nums = ToBin.split()
nums_bin = [bytes(ctypes.c_uint16(int(num))) for num in nums]

with open("knowledge.bin", "wb") as file:
    for num in nums_bin:
        file.write(num)
