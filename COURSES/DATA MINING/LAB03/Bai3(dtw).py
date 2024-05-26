import numpy as np

def dtw(x, y):

    m, n = len(x), len(y)
    dtw = np.zeros((m + 1, n + 1)) # Khởi tạo ma trận chi phí rỗng

    # Tính chi phí: sử dụng công thức
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = abs(x[i-1] - y[j-1])
            dtw[i, j] = cost + min(dtw[i-1, j], dtw[i, j-1], dtw[i-1, j-1])

    
    path = []
    i, j = m, n

    while i > 0 or j > 0:
        path.append(dtw[i, j])
        if i == 1 and j == 1:
            break
        elif i == 1:
            j -= 1
        elif j == 1:
            i -= 1
        else:
            if dtw[i-1, j] == min(dtw[i-1, j-1], dtw[i-1, j], dtw[i, j-1]):
                i -= 1
            elif dtw[i, j-1] == min(dtw[i-1, j-1], dtw[i-1, j], dtw[i, j-1]):
                j -= 1
            else:
                i -= 1
                j -= 1

    # Tạo chuỗi đường đi wrapping
    path_str = ""

    for p in path:
        path_str += f"{p} -> "
    path_str = path_str[:-4]
    print("Warping Path:", path_str)
    return dtw[m, n]

if __name__ == "__main__" :

    # Nhập vào hai chuỗi thời gian x và y
    x = input("Input the time series x: ").split()
    x = [float(i) for i in x]
    y = input("Input the time series y: ").split()
    y = [float(i) for i in y]

    # Tính và in ra khoảng cách DTW giữa hai chuỗi thời gian x và y
    distance = dtw(x, y)
    print("Dynamic Time Warping- DTW is:", distance)
