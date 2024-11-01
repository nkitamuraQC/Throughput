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


def cumulative_sum(A):
    # 配列 A の長さを取得
    n = len(A)
    
    # 累積和のリスト S を作成。S[0] は 0 とし、S[i] は A[0] から A[i-1] までの合計。
    S = [0] * (n + 1)
    
    # 累積和の計算
    for i in range(n):
        S[i + 1] = S[i] + A[i]
    
    return S


def read_dos(dosfile, choice1=2, choice2=5):
    rf = open(dosfile, "r")
    lines = rf.readlines()
    e_ret = []
    dos_ret = []
    integral = 0.0
    for i in range(1,len(lines)):
        e = float(lines[i].split()[0]) - fermi
        _ = lines[i].split()[1]
        dos_ = lines[i].split()[choice1:choice2]
        val = 0.0
        for i in range(len(dos_)):
            val += float(dos_[i])
        tmp = []
        if e > range_[0] and e < range_[1]:
            e_ret.append(e)
            dos_ret.append(val)
    integral += sum(dos_ret)
    return e_ret, dos_ret, integral

def det_single_dos(dosfile):
    energy, dos, _ = read_dos(dosfile)
    a, b = search_window(dos)
    start = energy[a]
    end = energy[b]
    start = convert_to_fortran_notation(start)
    end = convert_to_fortran_notation(end)
    return start, end

def convert_to_fortran_notation(num):
    # 数値を浮動小数点での指数表現文字列に変換
    sci_notation = f"{num:.1e}"
    
    # 'e'を'd'に置き換えたFortran形式に変換
    fortran_notation = sci_notation.replace('e', 'd')
    
    return fortran_notation
    
