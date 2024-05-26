# Author: Bishal Sarang
""" 
    Main solver program that implements bfs, dfs and drawing utilities to draw graphs.
"""

import os
import emoji
import pydot
import random
from collections import deque

# Set it to bin folder of graphviz
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

# Dictionaries to backtrack solution nodes
# Parent stores parent of (m , c, s)
# Move stores (x, y, side) i.e number of missionaries,
#cannibals to be moved from left to right or right to left for particular state
# node_list stores pydot.Node object for particular state (m, c, s) so that we can color the solution nodes
Parent, Move, node_list = dict(), dict(), dict()

class Solution():

    def __init__(self):
        # Start state (3M, 3C, Left)
        # Goal State (0M, 0C, Right)
        # Each state gives the number of missionaries and cannibals on the left side

        self.start_state = (3, 3, 1)
        self.goal_state = (0, 0, 0)
        self.options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]

        self.boat_side = ["right", "left"]

        self.graph = pydot.Dot(graph_type='graph', bgcolor="#fff3af",
                               label="fig: Missionaries and Cannibal State Space Tree",fontcolor="red", fontsize="24")      
        self.visited = {}
        self.solved = False

    def is_valid_move(self, number_missionaries, number_cannnibals): # Hàm check xem có tồn tại đường đi không
        """
        Checks if number constraints are satisfied
        """
        return (0 <= number_missionaries <= 3) and (0 <= number_cannnibals <= 3) # Số truyền giáo và con quỷ >=0 và <=3 thì trả về True, 
                                                                                 # ngược lại trả False.

    def is_goal_state(self, number_missionaries, number_cannnibals, side):
        return (number_missionaries, number_cannnibals, side) == self.goal_state # So sánh trạng thái truyền vào với trạng thái mục tiêu, 
                                                                                 # Nếu bằng trả về True, ngược lại False

    def is_start_state(self, number_missionaries, number_cannnibals, side):
        return (number_missionaries, number_cannnibals, side) == self.start_state # So sánh trạng thái truyền vào với trạng thái ban đầu,
                                                                                  # Nếu bằng trả về True, ngược lại False

    def number_of_cannibals_exceeds(self, number_missionaries, number_cannnibals):
        number_missionaries_right = 3 - number_missionaries # Tạo biến number_missionaries_right để tính số lượng người ăn thịt còn lại bên phải
        number_cannnibals_right = 3 - number_cannnibals
        return (number_missionaries > 0 and number_cannnibals > number_missionaries) \
               or (number_missionaries_right > 0 and number_cannnibals_right > number_missionaries_right)
               '''Hàm này trả về kết quả của việc kiểm tra xem có vi phạm ràng buộc về số lượng người ăn thịt hay không. Có hai điều kiện
               để kiểm tra: Một là bờ mà thuyền đang đậu (bờ hiện tại) có nhiều quỷ hơn số lượng nhà truyền giáo không,
               hai là bờ bên phải (nếu thuyền đậu bên trái) có nhiều quỷ hơn số lượng nhà truyền giáo không. 
               Trả về True nếu 1 trong 2 thỏa còn cả 2 không thỏa trả về False'''

    def write_image(self, file_name="state_space.png"):
        try: # sử dụng try-except để xử lý lỗi.
            self.graph.write_png(file_name) # Ghi biểu đồ của không gian trạng thái vào một tệp hình ảnh với tên là file_name. 
                                            # Phương thức write_png được gọi từ đối tượng self.graph
        except Exception as e: 
        '''Bắt đầu khối except để xử lý các ngoại lệ hoặc lỗi xảy ra trong khối try. Bất kỳ ngoại lệ nào cũng được bắt,
        (thể hiện bằng Exception as e), và ngoại lệ này được gán vào biến e'''

            print("Error while writing file", e) # In ra thông báo lỗi và hiển thị thông tin về ngoại lệ 'e' để mô tả lỗi xảy ra.
        print(f"File {file_name} successfully written.") 
        ''' Nếu không có lỗi, in ra thông báo tập hình ảnh đã được ghi thành công. Giá trị {file_name} được thay thế bằng tên thực tế
        của tệp tin mà bạn truyền vào.'''

    def solve(self, solve_method="dfs"): # Hàm này nhận một tham số solve_method, cho biết phương pháp giải quyết bạn muốn sử dụng
        self.visited = dict() # Tạo một dict rỗng visited trong đối tượng self để theo dõi trạng thái đã được thăm hay chưa.
        Parent[self.start_state] = None # Gán giá trị None cho trạng thái ban đầu (nút gốc) trong dict Parent
        Move[self.start_state] = None # Gán giá trị None cho trạng thái ban đầu (nút gốc) trong dict Move
        node_list[self.start_state] = None # Gán giá trị None cho trạng thái ban đầu (nút gốc) trong danh sách node_list

        return self.dfs(*self.start_state, 0) if solve_method == "dfs" else self.bfs() 
        '''Dựa vào giá trị solve_method, hàm solve sẽ gọi entweder self.dfs (tìm kiếm theo chiều sâu) hoặc self.bfs (tìm kiếm theo chiều rộng)'''

    def draw_legend(self):
        """
            Utility method to draw legend on graph if  legend flag is ON 
        """
        graphlegend = pydot.Cluster(graph_name="legend", label="Legend", fontsize="20", color="gold",
                                    fontcolor="blue", style="filled", fillcolor="#f4f4f4")


        node1 = pydot.Node("1", style="filled", fillcolor="blue", label="Start Node", fontcolor="white", width="2", fixedsize="true")
        graphlegend.add_node(node1)

        node2 = pydot.Node("2", style="filled", fillcolor="red", label="Killed Node", fontcolor="black", width="2", fixedsize="true")
        graphlegend.add_node(node2)

        node3 = pydot.Node("3", style="filled", fillcolor="yellow", label="Solution nodes", width="2", fixedsize="true")
        graphlegend.add_node(node3)
        
        node4 = pydot.Node("4", style="filled", fillcolor="gray", label="Can't be expanded",  width="2", fixedsize="true")
        graphlegend.add_node(node4)

        node5 = pydot.Node("5", style="filled", fillcolor="green", label="Goal node", width="2", fixedsize="true")
        graphlegend.add_node(node5)

        node7 = pydot.Node("7", style="filled", fillcolor="gold", label="Node with child", width="2", fixedsize="true")

        graphlegend.add_node(node7)


        description = "Each node (m, c, s) represents a \nstate where 'm' is the number of\n missionaries,\'n' the cannibals \
             and \n's' the side of the boat\n"
        " where  '1' represents the left \nside and '0' the right side \n\nOur objective is to reach goal state (0, 0, 0)\
        \nfrom start state (3, 3, 1) by some \noperators = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 0),]\n"\
                "each tuples (x, y) inside operators \nrepresents the number of missionaries and\
        \ncannibals to be moved from left to right \nif c == 1 and viceversa" 
        
        node6 = pydot.Node("6", style="filled", fillcolor="gold", label= description, shape="plaintext", fontsize="20", fontcolor="red")
        graphlegend.add_node(node6)

        self.graph.add_subgraph(graphlegend)

        self.graph.add_edge(pydot.Edge(node1, node2, style="invis"))
        self.graph.add_edge(pydot.Edge(node2, node3, style="invis"))
        self.graph.add_edge(pydot.Edge(node3, node4, style="invis"))
        self.graph.add_edge(pydot.Edge(node4, node5, style="invis"))
        self.graph.add_edge(pydot.Edge(node5, node7, style="invis"))
        self.graph.add_edge(pydot.Edge(node7, node6, style="invis"))

    def draw(self, *, number_missionaries_left, number_cannnibals_left, number_missionaries_right, number_cannnibals_right):
        """
            Draw state on console using emojis
        """
        
        left_m = emoji.emojize(f":old_man: " * number_missionaries_left)
        ''' Dòng này sử dụng thư viện emoji để tạo biểu tượng người đàn ông (:old_man:) nhiều lần tương ứng với number_missionaries_left,
        sau đó gán kết quả cho biến left_m. Nhằm hiển thị số lượng nhà truyền giáo trên bờ bên trái. '''
        left_c = emoji.emojize(f":ogre: " * number_cannnibals_left)
        ''' Tương tự như dòng trước, nhưng ở đây ta dùng biểu tượng người khổng lồ (:ogre:) để biểu diễn số lượng quỷ bên bờ trái'''
        right_m = emoji.emojize(f":old_man: " * number_missionaries_right)
        ''' Tương tự như left_m, nhưng áp dụng cho bờ phải'''
        right_c = emoji.emojize(f":ogre: " * number_cannnibals_right)
        ''' Tương tự như left_c, nhưng áp dụng cho bờ phải'''
        print('{}{}{}{}{}'.format(left_m, left_c + " " * (14 - len(left_m) - len(left_c)), "_" * 40, " " * (12 - len(right_m) - len(right_c)) + right_m, right_c))
        ''' Dòng này in biểu đồ của trạng thái bờ sông lên màn hình. Biểu đồ bao gồm hai bờ sông với số lượng nhà truyền giáo (old man) và số quỷ (ogre) tương ứng.
        Các dấu gạch ngang tạo sự phân tách giữa 2 bờ. Sự điều chỉnh dựa vào số lượng kí tự để đảm bảo biểu đồ hiển thị đúng vị trí.'''
        print("") # Dòng này in một dòng trống để tạo khoảng cách giữa các biểu đồ trạng thái liên tiếp.

    def show_solution(self):
        # Recursively start from Goal State
        # And find parent until start state is reached

        state = self.goal_state
        path, steps, nodes = [] ,[], []

        while state is not None:
            path.append(state)
            steps.append(Move[state])
            nodes.append(node_list[state])
        
            state = Parent[state]
        
        steps, nodes = steps[::-1], nodes[::-1]

        number_missionaries_left, number_cannnibals_left = 3, 3
        number_missionaries_right, number_cannnibals_right = 0, 0
    
        print("*" * 60)
        self.draw(number_missionaries_left=number_missionaries_left, number_cannnibals_left=number_cannnibals_left,
                  number_missionaries_right=number_missionaries_right, number_cannnibals_right=number_cannnibals_right)
        
        for i, ((number_missionaries, number_cannnibals, side), node) in enumerate(zip(steps[1:], nodes[1:])):
            
            if node.get_label() != str(self.start_state):
                node.set_style("filled")
                node.set_fillcolor("yellow")
        
            print(f"Step {i + 1}: Move {number_missionaries} missionaries  and {number_cannnibals} \
                     cannibals from {self.boat_side[side]} to {self.boat_side[int(not side)]}.")

            op = -1 if side == 1 else 1
            
            number_missionaries_left = number_missionaries_left + op * number_missionaries
            number_cannnibals_left = number_cannnibals_left + op * number_cannnibals

            number_missionaries_right = number_missionaries_right - op * number_missionaries
            number_cannnibals_right = number_cannnibals_right - op * number_cannnibals
            
            self.draw(number_missionaries_left=number_missionaries_left, number_cannnibals_left=number_cannnibals_left,
                      number_missionaries_right=number_missionaries_right, number_cannnibals_right=number_cannnibals_right)
        
        print("Congratulations!!! you have solved the problem")
        print("*" * 60)

    def draw_edge(self, number_missionaries, number_cannnibals, side, depth_level):
        u, v = None, None # Khởi tạo 2 biến u, v với giá trị là None
        if Parent[(number_missionaries, number_cannnibals, side)] is not None: # Kiểm tra xem đỉnh cha của trạng thái hiện tại có tồn tại không
            u = pydot.Node(str(Parent[(number_missionaries, number_cannnibals, side)] + (depth_level - 1, )),
                           label=str(Parent[((number_missionaries, number_cannnibals, side))]))
            '''Tạo đỉnh u trong biểu đồ với nhãn là trạng thái của đỉnh cha. Nhãn này giúp đại diện cho trạng thái của đỉnh cha và sẽ được hiển thị trong biểu đồ'''

            self.graph.add_node(u) # Thêm đỉnh u vào biểu đồ

            v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level)),
                           label=str((number_missionaries, number_cannnibals, side)))

            edge = pydot.Edge(str(Parent[(number_missionaries, number_cannnibals, side)] + (depth_level - 1, )),
                              str((number_missionaries, number_cannnibals, side, depth_level) ), dir='forward')
            ''' Tạo một cạnh từ đỉnh cha u đến đỉnh hiện tại v, thuộc tính dir='forward xác định hướng của cạnh '''
            self.graph.add_edge(edge) # Thêm cạnh vào biểu đồ
        else: # Nếu đỉnh cha không tồn tại  
            # For start node
            v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level)),
                           label=str((number_missionaries, number_cannnibals, side)))
            '''Tạo đỉnh v với nhãn là trạng thái ban đầu'''
            self.graph.add_node(v) # Thêm đỉnh v vào biểu đồ
        return u, v # Trả về các đỉnh u (cha) và v (hiện tại) để sử dụng trong việc vẽ biểu đồ

    def bfs(self):
        q = deque() # Tạo 1 hàng đợi rỗng để lưu trữ các trạng thái trong quá trình duyệt BFS
        q.append(self.start_state + (0, )) # Thêm trạng thái ban đầu vào hàng đợi, kèm theo mức độ sâu bằng 0
        self.visited[self.start_state] = True # Đánh dấu trạng thái ban đầu là đã được thăm

        while q: # Bắt đầu vòng lặp, lặp đến khi hàng đợi rỗng
            number_missionaries, number_cannnibals, side, depth_level = q.popleft() # lấy trạng thái tiếp theo từ hàng đợi và gán giá trị tương ứng cho các biến
            # Draw Edge from u -> v
            # Where u = Parent[v]
            # and v = (number_missionaries, number_cannnibals, side, depth_level)
            u, v = self.draw_edge(number_missionaries, number_cannnibals, side, depth_level)
            '''Vẽ cạnh từ trạng thái cha (u) đến trạng thái hiện tại (v) và lưu trả về 2 đỉnh  '''   

            
            if self.is_start_state(number_missionaries, number_cannnibals, side): # Kiểm tra trạng thái hiện tại có phải trạng thái ban đầu không
                v.set_style("filled") # Đặt kiểu cho đỉnh v thành "filled" để màu nền có thể được đặt
                v.set_fillcolor("blue") # Đặt màu nền của đỉnh v thành xanh để biểu thị trạng thái ban đầu
                v.set_fontcolor("white") # Đặt font chữ của đỉnh v thành trắng để văn bản trên đỉnh dễ đọc
            elif self.is_goal_state(number_missionaries, number_cannnibals, side): # Kiểm tra trạng thái hiện tại có phải trạng thái mục tiêu không
                v.set_style("filled") # Đặt kiểu cho đỉnh v thành "filled"
                v.set_fillcolor("green") # Đặt màu nền cho đỉnh v thành xanh lá cây để biểu diễn trạng thái mục tiêu
                return True # Trả về True
            elif self.number_of_cannibals_exceeds(number_missionaries, number_cannnibals): # Kiểm tra có vi phạm ràng buộc về số quỷ không
                v.set_style("filled") # Đặt kiểu cho đỉnh v thành "filled"
                v.set_fillcolor("red") # Đặt màu nền của đỉnh v thành đỏ để biểu thị trạng thái vi phạm
                continue # tiếp tục vòng lặp và không xem xét trạng thái này nữa
            else: # Trường hợp không thuộc trường hợp nào ở trên
                v.set_style("filled") # Đặt kiểu cho đỉnh v thành "filled"
                v.set_fillcolor("orange")  # Đặt màu nền cho đỉnh v thành cam để biểu thị trạng thái bình thường

            op = -1 if side == 1 else 1 # Xác định phía bên kia của sông

            can_be_expanded = False # Khởi tạo biến can_be_expanded là False để kiểm tra xem trạng thái hiện tại có thể mở rộng hay không

            for x, y in self.options: # Duyệt qua tất cả các tùy chọn di chuyển từ trạng thái hiện tại
                next_m, next_c, next_s = number_missionaries + op * x, number_cannnibals + op * y, int(not side) 
                #Tính toán trạng thái mới dựa trên dựa trên di chuyển và trạng thái hiện tại

                if (next_m, next_c, next_s) not in self.visited: # Kiểm tra trạng thái mới đã thăm chưa
                    if self.is_valid_move(next_m, next_c): # Kiểm tra di chuyển này có hợp lệ không 
                        can_be_expanded = True # Đánh dấu can_be_expanded là True để biểu thị rằng trạng thái mới có thể mở rộng
                        self.visited[(next_m, next_c, next_s)] = True # Đánh dấu trạng thái mới đã được thăm
                        q.append((next_m, next_c, next_s, depth_level + 1)) # Thêm trạng thái mới vào hàng đợi với độ sâu tăng thêm 1
                        
                        # Keep track of parent and corresponding move
                        Parent[(next_m, next_c, next_s)] = (number_missionaries, number_cannnibals, side) # Ghi lại đỉnh cha của trạng thái mới 
                        Move[(next_m, next_c, next_s)] = (x, y, side) # Ghi lại đường đi để đến trạng thái mới 
                        node_list[(next_m, next_c, next_s)] = v # Lưu trạng thái hiện tại vào danh sách các trạng thái
                
            if not can_be_expanded: # Nếu không có trạng thái nào có thể được mở rộng
                v.set_style("filled") # Đặt kiểu cho đỉnh v thành "filled"
                v.set_fillcolor("gray") # Đặt màu nền cho đỉnh v thành xám để biểu thị trạng thái không thể được mở rộng
        return False # Trả về false để kết thúc trạng thái tìm kiếm BFS nếu không có trạng thái nào thỏa mãn.
        

    def dfs(self, number_missionaries, number_cannnibals, side, depth_level):
        self.visited[(number_missionaries, number_cannnibals, side)] = True # Đánh dấu trạng thái hiện tại là đã được thăm.

        # Draw Edge from u -> v
        # Where u = Parent[v]
        u, v = self.draw_edge(number_missionaries, number_cannnibals, side, depth_level) #Vẽ cạnh từ trạng thái cha đến trạng thái hiện tại và lưu trả về hai đỉnh.

        
        if self.is_start_state(number_missionaries, number_cannnibals, side): # Kiểm tra xem trạng thái hiện tại có phải trạng thái ban đầu không.
            v.set_style("filled") # Đặt kiểu cho đỉnh v thành “filled” để màu nền có thể được đặt.
            v.set_fillcolor("blue") # Đặt màu nền của đỉnh v thành màu xanh để biểu thị trạng thái ban đầu.
        elif self.is_goal_state(number_missionaries, number_cannnibals, side): # Kiểm tra xem trạng thái hiện tại có phải là trạng thái mục tiêu không.
            v.set_style("filled") # Đặt kiểu cho đỉnh v thành “filled”.
            v.set_fillcolor("green") # Đặt màu nền của đỉnh v thành xanh lá cây để biểu thị trạng thái mục tiêu.
            return True # Trả về True để kết thúc tìm kiếm vì đã tìm thấy lời giải.
        elif self.number_of_cannibals_exceeds(number_missionaries, number_cannnibals): # Kiểm tra xem có vi phạm ràng buộc về số lượng người ăn thịt không.
            v.set_style("filled") # Đặt kiểu cho đỉnh v thành “filled”.
            v.set_fillcolor("red") # Đặt màu nền của đỉnh v thành đỏ để biểu thị trạng thái vi phạm
            return False # Trả về False để kết thúc tìm kiếm vì trạng thái hiện tại không thỏa mãn.
        else: # Trường hợp không thuộc trường hợp nào ở trên
            v.set_style("filled") # Đặt kiểu cho đỉnh v thành “filled”.
            v.set_fillcolor("orange") # Đặt màu nền của đỉnh v thành màu cam để biểu thị trạng thái bình thường.

        solution_found = False # Khởi tạo biến solution_found với giá trị False để theo dõi xem có lời giải nào được tìm thấy hay không.
        operation = -1 if side == 1 else 1 # Xác định phía bên kia của sông.
        
        can_be_expanded = False # Khởi tạo biến can_be_expanded với giá trị False để kiểm tra xem trạng thái hiện tại có thể mở rộng hay không.

        for x, y in self.options: # Duyệt qua tất cả các tùy chọn di chuyển từ trạng thái hiện tại.
            next_m, next_c, next_s = number_missionaries + operation * x, number_cannnibals + operation * y, int(not side)
            # Tính toán trạng thái mới dựa trên di chuyển và trạng thái hiện tại.

            if (next_m, next_c, next_s) not in self.visited: # Kiểm tra xem trạng thái mới đã được thăm chưa.
                if self.is_valid_move(next_m, next_c): # Kiểm tra xem di chuyển đến trạng thái mới có hợp lệ không.
                    can_be_expanded = True # Đánh dấu can_be_expanded là True (trạng thái hiện tại có thể được mở rộng)
                    # Keep track of Parent state and corresponding move
                    Parent[(next_m, next_c, next_s)] = (number_missionaries, number_cannnibals, side) # Ghi lại đỉnh cha của trạng thái mới.
                    Move[(next_m, next_c, next_s)] = (x, y, side)  # Ghi lại di chuyển để đến trạng thái mới.
                    node_list[(next_m, next_c, next_s)] = v # Lưu trạng thái hiện tại vào danh sách các trạng thái.

                    solution_found = (solution_found or self.dfs(next_m, next_c, next_s, depth_level + 1))  
                    # Gọi đệ quy hàm dfs để tìm kiếm từ trạng thái mới, và cập nhật biến solution_found nếu tìm thấy lời giải.
                
                    if solution_found: # Nếu kiếm được lời giải
                        return True # Trả về True

        if not can_be_expanded: 
            '''Nếu không có trạng thái nào có thể được mở rộng 
            (điều này có nghĩa rằng chúng ta đã kiểm tra tất cả các tùy chọn di chuyển và không có trạng thái mới nào hợp lệ để mở rộng).'''
            v.set_style("filled") # Đặt kiểu của đỉnh v thành “filled”.
            v.set_fillcolor("gray")  # Đặt màu nền của đỉnh v thành màu xám để biểu thị rằng trạng thái này không thể được mở rộng.

        self.solved = solution_found # Cập nhật biến solved với giá trị của solution_found.
        return solution_found # Trả về solution_found để kết thúc tìm kiếm và thông báo kết quả.
