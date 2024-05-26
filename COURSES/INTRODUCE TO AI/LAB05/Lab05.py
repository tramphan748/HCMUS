from treelib import Node, Tree
import sys


# Cấu trúc để đại diện các nút trên cây trong
# sự mở rộng A*
class TreeNode(object):
    def __init__(self, c_no, c_id, f_value, h_value, parent_id):
        self.c_no = c_no
        self.c_id = c_id
        self.f_value = f_value
        self.h_value = h_value
        self.parent_id = parent_id


# Cấu trúc đại diện các nút đã được ghé qua trong list A*
class FringeNode(object):
    def __init__(self, c_no, f_value):
        self.f_value = f_value
        self.c_no = c_no


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    # Hàm tiện ích để in MST cấu trúc được lưu trữ trong hàm dict parent[]
    def printMST(self, parent, d_temp, t):
        # Xuất ("Edge\ tWeight")
        sum_weight = 0
        min1 = 10000
        min2 = 10000
        r_temp = {}
        for k in d_temp:
            r_temp[d_temp[k]] = k

        for i in range(1, self.V):
            # Xuất ra (parent[i], "-",i, self.graph[i][parent[i])
            sum_weight = sum_weight + self.graph[i][parent[i]]
            if graph[0][r_temp[i]] < min1:
                min1 = graph[0][r_temp[i]]
            if graph[0][r_temp[parent[i]]] < min1:
                min1 = graph[0][r_temp[parent[i]]]
            if graph[t][r_temp[i]] < min2:
                min2 = graph[t][r_temp[i]]
            if graph[t][r_temp[parent[i]]] < min2:
                min2 = graph[t][r_temp[parent[i]]]

        return (sum_weight + min1 + min2) % 10000


     # Hàm tiện ích để tìm vertex (đỉnh)
     # với giá trị khoảng cách nhỏ nhất từ bộ các đỉnh
     # chưa bao gồm trong đồ thị cây đường đi ngắn nhất
    def minKey(self, key, mstSet):
        #Intialize min value
        min = sys.maxsize

        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v
        return min_index

# Hàm để xây dựng và in MST cho đồ thị graph
# Đại diện sử dụng ma trận
    def primMST(self, d_temp, t):
        # Giá trị khóa để chọn cạnh có khoảng cách nhỏ nhất
        key = [sys.maxsize] * self.V
        parent = [None] * self.V  # Array to store constructed MST
        # Tạo key 0 để đỉnh đc chọn như là đỉnh đầu tiên
        key[0] = 0
        mstSet = [False] * self.V
        sum_weight = 10000
        parent[0] = -1  # Nút đầu tiên luôn là rễ

        for c in range(self.V):
            # Chọn đỉnh có khoảng cách nho nhất của bộ các đỉnh chưa đc ghé đến
            # u is always equa; to src in first iteration
            u = self.minKey(key, mstSet)

            #Put the minimum distance vertex in the shortest path tree
            mstSet[u] = True

            #Update dist value of the adjacent vertices of m
            #current distance is greater than new distance and
            #the vertex in not in the shotest path tree

            for v in range(self.V):
                #graph[u][v] is non zero only for adjacent vertices of m
                #mstSet is false for vertices not yet included in MST graph
                #Update the key only if graph[u][v] is smaller than key[v]
                if 0 < self.graph[u][v] < key[v] and mstSet[v] == False:
                    key[v] = self.graph[u][v]
                    parent[v] = u
        return self.printMST(parent, d_temp, t)

#idea here is to form a graph of all unvisited nodes and make MST from that
#Determine weight of that mst and connect it with the visited node and the 0th node
def heuristic(tree, p_id, t, V, graph):
    visited = set() #Set to store visited nodes
    visited.add(0)
    visited.add(t)
    if p_id != -1:
        tnode = tree.get_node(str(p_id))
        # Find all visited nodes and add them to the set
        while tnode.data.c_id != 1:
            visited.add(tnode.data.c_no)
            tnode = tree.get_node(str(tnode.data.parent_id))
    l = len(visited)
    num = V - l #no of unvisited nodes
    if num != 0:
        g = Graph(num)
        d_temp = {}
        key = 0
        # d_temp dictionary stores mapping of original city no as key and
        # new sequential no as value for MST to work
        for i in range(V):
            if i not in visited:
                d_temp[i] = key
                key = key + 1

        i = 0
        for i in range(V):
            for j in range(V):
                if (i not in visited) and (j not in visited):
                    g.graph[d_temp[i]][d_temp[j]] = graph[i][j]
        # print(g.graph)
        mst_weight = g.primMST(d_temp, t)
        return mst_weight
    else:
        return graph[t][0]


def checkPath(tree, toExpand, V):
    tnode = tree.get_node(str(toExpand.c_id))
    # Lấy nuts để mở rộng từ đồ thị cây
    list1 = list()
    # List để lưu trữ đường đi
    # Cho nút đầu tiên:
    if tnode.data.c_id == 1:
        # print("In if")
        return 0
    else:
        # print("In else")
        depth = tree.depth(tnode)  # Kiểm tra độ sâu của cây
        s = set()
        # Đi lên cây sử dụng con trỏ cha và thêm tất cả các nút trên đường đi đến set và list
        while tnode.data.c_id != 1:
            s.add(tnode.data.c_no)
            list1.append(tnode.data.c_no)
            tnode = tree.get_node(str(tnode.data.parent_id))
        list1.append(0)
        if depth == V and len(s) == V and list1[0] == 0:
            print("Path complete")
            list1.reverse()
            print(list1)
            return 1
        else:
            return 0


def startTSP(graph, tree, V):
    goalState = 0
    times = 0
    toExpand = TreeNode(0, 0, 0, 0, 0)  # Nút để mở rộng
    key = 1  # Định danh duy nhất cho nút trên cây
    heu = heuristic(tree, -1, 0, V, graph)
    tree.create_node("1", "1",
                     data=TreeNode(0, 1, heu, heu, -1))  # Tạo nút đầu tiên trên cây nghĩa là  thành phố gốc 0th
    fringe_list = {}
    fringe_list[key] = FringeNode(0, heu)
    key = key + 1
    while goalState == 0:
        minf = sys.maxsize
        # Chọn nút có f_value nhỏ nhất từ fringe_list
        for i in fringe_list.keys():
            if fringe_list[i].f_value < minf:
                toExpand.f_value = fringe_list[i].f_value
                toExpand.c_no = fringe_list[i].c_no
                toExpand.c_id = i
                minf = fringe_list[i].f_value

        h = tree.get_node(str(toExpand.c_id)).data.h_value
        val = toExpand.f_value - h  # giá trị g của nút đc chọn
        path = checkPath(tree, toExpand, V)  # Kiểm tra đường của nút đc chọn nếu nó hoàn thành hay không
        # Nếu nút mở rộng là 0 và path đã hoàn thành thì ngừng bài toán
        # Ta kiểm tra nút ở thời điểm mở rộng và không ở thời điểm của thể hệ
        if toExpand.c_no == 0 and path == 1:
            goalState = 1;
            cost = toExpand.f_value  # Tổng giá trị thật sự
        else:
            del fringe_list[toExpand.c_id]  # Loại bỏ nút từ FL
            j = 0
            # Đánh giá f_values và h_value của các nút liền kề của nút để mở rôngk
            while j < V:
                if j != toExpand.c_no:
                    h = heuristic(tree, toExpand.c_id, j, V, graph) #Heuristric calc
                    f_val = val + graph[j][toExpand.c_no] + h  # g(parent) + g(parent -> child) + h(child)
                    fringe_list[key] = FringeNode(j, f_val)
                    tree.create_node(str(toExpand.c_no), str(key), parent=str(toExpand.c_id), \
                                     data=TreeNode(j, key, f_val, h, toExpand.c_id))
                    key = key + 1
                j = j + 1
    return cost


if __name__ == '__main__':
    # # Trường hợp 1:
    # V = 4
    # graph = [[0, 5, 2, 3],[5, 0, 6, 3], [2, 6, 0, 4], [3, 3, 4, 0]]

    # # Trường hợp 2:
    # V = 2
    # graph = [[0,300],[300,0]]

    # # Trường hợp 3:
    # V = 3
    # graph = [[0,300,200],[300,0,500],[200,500,0]]

    # Trường hợp 4:
    V = 4
    graph=[[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]


    tree = Tree()
    ans = startTSP(graph, tree, V)
    print("Ans is " + str(ans))


