import numpy as np


def read_dos(dosfile, target):
    rf = open(dosfile, "r")
    lines = rf.readlines()
    e_ret = []
    dos_ret = []
    integral = 0.0
    for i in range(1, len(lines)):
        e = float(lines[i].split()[0])
        _ = lines[i].split()[1]
        dos = float(lines[i].split()[target])
        e_ret.append(e)
        dos_ret.append(dos)
    integral += sum(dos_ret)
    return e_ret, dos_ret, integral


def for_single_dos(dosfile, target_start=2, target_end=7, offset=0.5, thr=0.1):
    sta = []
    end = []
    for t in range(target_start, target_end):
        energy, dos, _ = read_dos(dosfile, t)
        dos = np.array(dos)
        energy = np.array(energy)
        e = energy[np.where(dos > thr)]
        # a, b = search_window(dos)
        sta.append(np.min(e))
        end.append(np.max(e))
    a = min(sta)
    b = max(end)
    start = a - offset
    end = b + offset
    print("start:", convert_to_fortran_notation(start))
    print("end:", convert_to_fortran_notation(end))
    return start, end


def convert_to_fortran_notation(num):
    # 数値を浮動小数点での指数表現文字列に変換
    sci_notation = f"{num:.4e}"

    # 'e'を'd'に置き換えたFortran形式に変換
    fortran_notation = sci_notation.replace("e", "d")

    # 指数部が0の場合にd0を付加する
    if "d0" in fortran_notation:
        return fortran_notation  # 既に d0 形式ならそのまま返す
    elif "d+0" in fortran_notation or "d-0" in fortran_notation:
        fortran_notation = fortran_notation.replace("d+0", "d0").replace("d-0", "d0")

    return fortran_notation


if __name__ == "__main__":
    fdos = "throughput/examples/calculation.pdos_atm#1(Fe)_wfc#4(d)"

    start, end = for_single_dos(fdos)
    print(convert_to_fortran_notation(start), convert_to_fortran_notation(end))
