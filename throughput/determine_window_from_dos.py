from bisect import bisect_right
import numpy as np

def search_window(A):
    n = len(A)
    
    # 累積和の計算
    S = [0] * (n + 1)
    for i in range(n):
        S[i + 1] = S[i] + A[i]
    
    # 最大値とその区間の上限を保存するリスト
    max_averages = []
    max_j_list = []
    
    # 下限 i を固定しながら上限 j を探索
    for i in range(n):
        left, right = i + 1, n  # 上限の候補は i+1 から n-1
        best_j = i
        best_avg = float('-inf')
        
        # 二分探索で最適な j を見つける
        while left < right:
            mid = (left + right) // 2
            # 区間平均を計算
            current_avg = (S[mid] - S[i]) / (mid - i)
            
            # 平均が最大化される方向に j を調整
            if current_avg > best_avg:
                best_avg = current_avg
                best_j = mid
                left = mid + 1  # より大きな区間での最大化を目指す
            else:
                right = mid
        
        # 各下限 i に対する最大平均と上限を保存
        max_averages.append(best_avg)
        max_j_list.append(best_j)
    
    # 全体の最大値を求める
    idx = np.argmax(max_averages)
    overall_max_j = max_j_list[idx]
    
    return idx, overall_max_j


def read_dos(dosfile, target):
    rf = open(dosfile, "r")
    lines = rf.readlines()
    e_ret = []
    dos_ret = []
    integral = 0.0
    for i in range(1,len(lines)):
        e = float(lines[i].split()[0])
        _ = lines[i].split()[1]
        dos = float(lines[i].split()[target])
        e_ret.append(e)
        dos_ret.append(dos)
    integral += sum(dos_ret)
    return e_ret, dos_ret, integral

def for_single_dos(dosfile, target_start=2, target_end=7, offset=3):
    sta = []
    end = []
    for t in range(target_start, target_end):
        energy, dos, _ = read_dos(dosfile, t)
        e = energy[np.argmax(dos)]
        # a, b = search_window(dos)
        sta.append(e-offset)
        end.append(e+offset)
    a = min(sta)
    b = max(end)
    start = energy[a] - offset
    end = energy[b] + offset
    print("start:", convert_to_fortran_notation(start))
    print("end:", convert_to_fortran_notation(end))
    return start, end

def convert_to_fortran_notation(num):
    # 数値を浮動小数点での指数表現文字列に変換
    sci_notation = f"{num:.1e}"
    
    # 'e'を'd'に置き換えたFortran形式に変換
    fortran_notation = sci_notation.replace('e', 'd')
    
    # 指数部が0の場合にd0を付加する
    if 'd0' in fortran_notation:
        return fortran_notation  # 既に d0 形式ならそのまま返す
    elif 'd+0' in fortran_notation or 'd-0' in fortran_notation:
        fortran_notation = fortran_notation.replace('d+0', 'd0').replace('d-0', 'd0')
    
    return fortran_notation

if __name__ == "__main__":
    fdos = "throughput/calculation.pdos_atm#1(Fe)_wfc#4(d)"

    start, end = for_single_dos(fdos)
    print(start, end)
