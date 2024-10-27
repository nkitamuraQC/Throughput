from bisect import bisect_right
import numpy as np

def max_average_subarray_with_binary_search(A):
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


def read_dos(dosfile):
    ### QE
    return

def det_single_dos(dosfile):
    dos, energy = read_dos(dosfile)
    cdos = cumulative_sum(dos)
    a, b = max_average_subarray_with_binary_search(cdos)
    start = energy[a]
    end = energy[b]
    return start, end
    
    
