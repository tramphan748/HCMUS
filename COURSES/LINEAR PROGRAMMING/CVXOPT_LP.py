from cvxopt import matrix, solvers
import numpy as np

def input_matrix():
  # input matrix c: hàm mục tiêu
  print("Input matrix c (Nhập ma trận/vector hệ số hàm mục tiêu): ")
  row_c = int(input("Enter the number of rows of matrix/vector c (Nhập số lượng hệ số trên hàm mục tiêu):"))
  print("Enter the entries in a single column (separated by space) (Nhập ma trận/vector theo cột): ")
  c = list(map(float, input().split()))
  matrix_c = matrix(c, (row_c, 1)) # Directly create cvxopt matrix
  print(f'matrix c_T is:\n{matrix_c}\n')

  # input matrix G
  print("Input matrix G (Nhập ma trận hệ số BĐT ràng buộc): ")
  row_G = int(input("Enter the number of rows of matrix G (Nhập số hàng của ma trận G (Số lượng constraints)):"))
  col_G = int(input("Enter the number of columns of matrix G (Nhập số cột của ma trận G (Số lượng biến)):"))
  print("Enter the entries in a single column (separated by space) (Nhập ma trận theo từng cột): ")
  G = list(map(float, input().split()))
  matrix_G = matrix(G, (row_G, col_G)) # Directly create cvxopt matrix
  print(f'matrix G is:\n{matrix_G}\n')

  # input matrix h
  print("Input matrix h (Nhập mma trận/vector giá trị vế phải BĐT ràng buộc): ")
  row_h = int(input("Enter the number of rows of matrix h (Nhập số hàng của ma trận h (Số lượng constraints)):"))
  print("Enter the entries in a single column (separated by space) (Nhập ma trận/vector theo cột): ")
  h = list(map(float, input().split()))
  matrix_h = matrix(h, (row_h, 1)) # Directly create cvxopt matrix
  print(f'matrix b is:\n{matrix_h}\n')
  return matrix_c, matrix_G, matrix_h

matrix_c, matrix_G, matrix_h = input_matrix()

def solver():
  show_progress = input("Do you want to show process? [Y/N] ")
  if show_progress == 'Y' or show_progress == "Yes" or show_progress == "YES" or show_progress == "yes" or show_progress == "y":
    solvers.options['show_progress'] = True
    solution = solvers.lp(matrix_c, matrix_G, matrix_h)
    print('Optimal solution:\n', solution['x'].T)
    print('Optimal value:\n',solution['primal objective'])
    print('Number of iterations:\n', solution['iterations'])
  else:
    solvers.options['show_progress'] = False
    solution = solvers.lp(matrix_c, matrix_G, matrix_h)
    print('Optimal solution:\n', solution['x'].T)
    print('Optimal value:\n', solution['primal objective'])
    print('Number of iterations:\n', solution['iterations'])
  return solution

result = solver()
print(result)
