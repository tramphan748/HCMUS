# Author: Bishal Sarang
""" 
    Program to genrate complete state space tree upto certain depth level
"""

from collections import deque
import pydot
import argparse
import os

# Set it to bin folder of graphviz
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]
Parent = dict()
graph = pydot.Dot(graph_type='graph',strict=False, bgcolor="#fff3af",
                  label="fig: Missionaries and Cannibal State Space Tree",
                  fontcolor="red", fontsize="24", overlap="true")
# To track node
i = 0

arg = argparse.ArgumentParser()
arg.add_argument("-d", "--depth", required=False,
                 help="MAximum depth upto which you want to generate Space State Tree")

args = vars(arg.parse_args())

max_depth = int(args.get("depth", 20))

def is_valid_move(number_missionaries, number_cannnibals):
        """
        Checks if number constraints are satisfied
        """
        return (0 <= number_missionaries <= 3) and (0 <= number_cannnibals <= 3)
        # Kiểm tra số lượng của Missionaries (number_missionaries) và số lượng Cannibals (number_cannnibals) có nằm trong khoảng từ 0 đến 3 không

def write_image(file_name="state_space"):
        try:
            graph.write_png(f"{file_name}_{max_depth}.png") #Thử ghi đồ thị đã vẽ thành một file ảnh với tên "{file_name}_{max_depth}.png"
            # Sử dụng write_png cho đối tượng graph, nếu không lỗi thì chương trình sẽ nhảy vào except để xét ngoại lệ 
        except Exception as e:
            print("Error while writing file", e)
        print(f"File {file_name}_{max_depth}.png successfully written.") # Sau khi ghi file thành công, chương trình in ra thông báo

def draw_edge(number_missionaries, number_cannnibals, side, depth_level, node_num):
        u, v = None, None
        if Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)] is not None:
            u = pydot.Node(str(Parent[(number_missionaries, number_cannnibals,side,depth_level, node_num)]),
                           label=str(Parent[(number_missionaries,number_cannnibals, side, depth_level, node_num)][:3]))
            graph.add_node(u)

            v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level, node_num)),
                           label=str((number_missionaries, number_cannnibals, side)))
            graph.add_node(v)

            edge = pydot.Edge(str(Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)]),
                              str((number_missionaries, number_cannnibals, side, depth_level, node_num) ), dir='forward')
            graph.add_edge(edge)
        else:
            # For start node
            v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level, node_num)),
                           label=str((number_missionaries, number_cannnibals, side)))
            graph.add_node(v)        
        return u, v

def is_start_state(number_missionaries, number_cannnibals, side):
    return (number_missionaries, number_cannnibals, side) == (3, 3, 1) # Nếu trạng thái ban đầu = (3,3,1) return true, nếu không return false

def is_goal_state(number_missionaries, number_cannnibals, side):
    return (number_missionaries, number_cannnibals, side) == (0, 0, 0) # Nếu trạng thái kết thúc = (0, 0, 0) return true, nếu không return false

def number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
    number_missionaries_right = 3 - number_missionaries # Số người truyền giáo bên bờ phải bằng 3 trừ số người truyền giáo bên bờ trái
    number_cannnibals_right = 3 - number_cannnibals # Số con quỷ bờ phải bằng 3 trừ số con quỷ bờ trái
    return (number_missionaries > 0 and number_cannnibals > number_missionaries) 
 or (number_missionaries_right > 0 and number_cannnibals_right > number_missionaries_right)
 # Nếu số quỷ nhiều hơn số người truyền giáo thì hàm trả về True, ngược lại là False

def generate():
        global i # Đánh dấu i là biến toàn cục.
        q = deque() # Tạo một hàng đợi (queue) bằng deque để lưu trữ các trạng thái của cây tìm kiếm.
        node_num = 0 # Khởi tạo biến node_num với giá trị 0 để đánh dấu các nút trong cây.
        q.append((3, 3, 1, 0, node_num)) # Thêm trạng thái ban đầu vào hàng đợi. Trạng thái ban đầu bao gồm 3 nhà truyền giáo và 3 người ăn thịt
                                         # trên bờ một, chiều sâu bằng 0 và đánh dấu node số 0

        Parent[(3, 3, 1, 0, node_num)] = None # Gán giá trị Node cho nút ban đầu (node gốc) trong dict Parent.

        while q: # Bắt đầu vòng lặp, lặp cho đến khi hàng đợi rỗng

            number_missionaries, number_cannnibals, side, depth_level, node_num = q.popleft() '''Lấy trạng thái tiếp theo từ hàng đợi và gán 
            các giá trị tương ứng cho các biến. Nếu không có trạng thái nào trong hàng đợi, vòng lặp kết thúc'''

            # print(number_missionaries, number_cannnibals)
            # Draw Edge from u -> v
            # Where u = Parent[v]
            # and v = (number_missionaries, number_cannnibals, side, depth_level)

            u, v = draw_edge(number_missionaries, number_cannnibals, side, depth_level, node_num) '''Gọi hàm draw_edge để vẽ cạnh từ đỉnh cha (u)
            đến đỉnh hiện tại (v) và lưu trả về 2 đỉnh này. Hàm draw_edge được gọi là hàm tạo biểu đồ cây tìm kiếm'''

            # Kiểm tra trạng thái hiện tại và thực hiện thay đổi màu sắc cho đỉnh
            if is_start_state(number_missionaries, number_cannnibals, side): # Nếu là trạng thái ban đầu, đánh dấu màu xanh dương
                v.set_style("filled")
                v.set_fillcolor("blue")
                v.set_fontcolor("white")
            elif is_goal_state(number_missionaries, number_cannnibals, side): # Nếu là trạng thái kết thúc, đánh dấu màu xanh lá cây và kết thúc loop
                v.set_style("filled")
                v.set_fillcolor("green")
                continue
                # return True
            elif number_of_cannibals_exceeds(number_missionaries, number_cannnibals): ''' Nếu trạng thái vi phạm ràng buộc (số người ăn thịt lớn hơn
            số nhà truyền giáo trên bất kì bờ nào), đánh dấu màu đỏ và tiếp tục vòng lặp'''
                v.set_style("filled")
                v.set_fillcolor("red")
                continue
            else: # Nếu không thuộc trường hợp nào ở trên, đánh dấu màu cam
                v.set_style("filled")
                v.set_fillcolor("orange")

            if depth_level == max_depth: # Nếu độ sâu của cây tìm kiếm bằng max_depth, kết thúc vòng lặp và trả về True
                return True

            op = -1 if side == 1 else 1 # Xác định phía bờ sông đối diện

            can_be_expanded = False # Khởi tạo biến can_be_expanded là False để kiểm tra xem trạng thái hiện tại có được mở rộng hay không

            # i = node_num
            for x, y in options: # Duyệt qua tất cả các tùy chọn di chuyển từ trạng thái hiện tại và kiểm tra tính hợp lệ của các di chuyển
                next_m, next_c, next_s = number_missionaries + op * x, number_cannnibals + op * y, int(not side) # Lấy giá trị mới dựa trên di chuyển 
                                                                                                                 # và trạng thái hiện tại
               
                if Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)] is None or(next_m, next_c, next_s)\
				!= Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)][:3]:
                    if is_valid_move(next_m, next_c):
                        can_be_expanded = True
                        i += 1
                        q.append((next_m, next_c, next_s, depth_level + 1, i))
                        # Keep track of parent
                        Parent[(next_m, next_c, next_s, depth_level + 1, i)] =\
                        (number_missionaries, number_cannnibals, side, depth_level, node_num) 
                        ''' Kiểm tra xem trạng thái cha (đỉnh cha) có giá trị None và trạng thái mới khác với trạng thái cha không. 
                        Nếu có và di chuyển là hợp lệ, đánh dấu  can_be_expanded = True (trạng thái có thể được mở rộng), 
                        tăng giá trị của i lên và thêm trạng thái mới vào hàng đợi '''

            if not can_be_expanded: # nếu không có trạng thái nào có thể được mở rộng (can_be_expanded vẫn là False), đánh dấu màu xám cho đỉnh.
                v.set_style("filled")
                v.set_fillcolor("gray")
        return False # Trả về False để kết thúc hàm sau khi duyệt hết toàn bộ cây tìm kiếm.

if __name__ == "__main__":
    if generate():
        write_image()


