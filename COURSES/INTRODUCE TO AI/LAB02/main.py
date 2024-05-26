# Author: Bishal Sarang
""" 
    Driver Program to handle command line arguments and  create Solution object
"""
from solve import Solution
import argparse
import itertools

arg = argparse.ArgumentParser() # Tạo một đối tượng arg của lớp ArgumentParser để quản lý các dòng lệnh.
arg.add_argument("-m", "--method", required=False, help="Specify which method to use")
''' Thêm một đối số -m hoặc -method cho chương trình. Đối số này cho phép người dùng chọn phương thức giải quyết bằng cách 
chỉ định tên phương thức sau khi sử dụng -m hoặc --method trên dòng lệnh. Đối số không bắt buộc (required=False) và có mô tả ("help") 
giúp người dùng hiểu cách sử dụng.'''
arg.add_argument("-l", "--legend", required=False, help="Specify if you want to display legend on graph")
'''Tương tự như đối số phương thức, đối số -1 hoặc --legend cho phép người dùng chỉ định xem có muốn hiển thị chú thích (legend) trên biểu đồ hay không. 
Đối số không bắt buộc (required=False) và có mô tả ("help") giúp người dùng hiểu cách sử dụng.'''
args = vars(arg.parse_args())
'''Sử dụng parge_args() để phân tích các đối số trên dòng lệnh và lưu chúng vào biến args. Hàm này trả về một dict chứa các đối số và giá
trị tương ứng của chúng'''

solve_method = args.get("method", "bfs")
# Sử dụng arg.get("method","bfs") để lấy giá trị đối số "method" từ biến args. Nếu đối số "method" không được cung cấp, giá trị mặc định là "bfs". 
legend_flag = args.get("legend", False)
# Tương tự như trên, lấy giá trị của đối số "legend" từ biến args. Nếu không có đối số "legend", giá trị mặc định là False.

def main():
    s = Solution()  # Tạo một đối tượng của lớp Solution gọi là s, để sử dụng các phương thức và thuộc tính của lớp này để giải bài toán.

    if(s.solve(solve_method)): 
    #Gọi phương thức solve() của đối tượng s với đối số solve_method. Nếu phương thức solve() trả về True, tức là đã tìm thấy lời giải, thực hiện các bước sau:
        
        
        s.show_solution() # Hiển thị lời giải trên màn hình

        output_file_name = f"{solve_method}" #Xây dựng tập đầu ra (output_file_name) dựa trên phương thức giải (solve_method) đã chọn.
        # Draw legend if legend_flag is set
        if legend_flag:  # Kiểm tra biến legend_flag
            if legend_flag[0].upper() == 'T' : # Nếu legend_flag được đặt và có giá trị bắt đầu bằng "T" (hoặc "t")
                output_file_name += "_legend.png"  # Chú thích legend vào tệp đầu ra
                s.draw_legend() # Vẽ chú thích
            else:
                output_file_name += ".png" # Sử dụng tên tệp mặc định (output_file_name += ".png").
        else:
             output_file_name += ".png"

        # Write State space tree
        s.write_image(output_file_name) # Ghi biểu đồ cây trạng thái vào tập đầu ra.
    else: # Nếu không tìm thấy lời giải (kết quả trả về từ solve() là False)
        raise Exception("No solution found") # Ném một ngoại lệ với thông báo "No solution found".


if __name__ == "__main__":
    main()


	
	
	