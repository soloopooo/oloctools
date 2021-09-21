import os
import psutil
import re
from ctypes import *
from Memory64 import *


def Get_Name_Pid(name):
    for pid in psutil.pids():
        try:
            process = psutil.Process(pid)
            if name in process.name():
                return pid
        except Exception:
            pass


def Search_Memory_Code(name, code):
    Game_Pid = Get_Name_Pid(name)
    Drive = SetupProcess(Game_Pid)

    Dream_dll = CDLL(os.getcwd() + "GameTime.dll")
    ret_number = Dream_dll.Search_Code(code.encode("ISO-8859-1"))  # ISO-8859-1
    Result = string_at(ret_number).decode("ISO-8859-1")  # gbk

    Rule = re.compile(r"\d+")
    Res_data = re.findall(Rule, Result)
    for Final_data in Res_data:
        Ret_Value = Drive.ReadMemory64_Wchar(int(Final_data), 180, 0)
        # print(Ret_Value)
        if "20" in Ret_Value:
            first = re.search('\S+[0-9]', Ret_Value)
            end = re.search('\s\d{1,2}:\d{1,2}:\d\d', Ret_Value)
            return [first.group() + end.group()]
    # print('-------------------------------------------------------------')


def get_played_time():
    result = Search_Memory_Code("osu!.exe", "50 00 6C 00 61 00 79 00 65 00")
    return result
