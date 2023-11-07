# determine the number of distict paths from warehours[0][0] to warehouse[n-1][m-1]
# 1's are open,  0's are close
# example:  
# (1) warehouse = [[1,1,0,1],[1,1,1,1]]
# 1    1(1) 0(0) 1(0)
# 1(1) 1(2) 1(2) 1(2)
# (2) epected output : 10
# 1 1    1    1
# 1 1(2) 1(3) 1(4)
# 1 1(3) 1(6) 1(10)
import numpy as np

def num(warehouse):
    n, m = len(warehouse), len(warehouse[0])

    mem = [[0] * m] * n
    mem = np.array(mem)

    if warehouse[0][0] == 0:
        return 0
    else:
        mem[0, 0] = 1

    print(mem)
    print("now start:")
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if i==0 and j==0:
                continue
            elif warehouse[i][j] == 0:
                continue
            elif i == 0:
                mem[i, j] = mem[i, j-1]
            elif j == 0:
                mem[i, j] = mem[i-1, j]
            else:
                mem[i, j] = mem[i-1, j] + mem[i, j-1]
            print(i, j)
            print(mem)
            print()

    return mem[n-1, m-1]


if __name__ == "__main__":
    warehouse1 = [[1,1,1,1],[1,1,1,1],[1,1,1,1]]
    warehouse2 = [[1,1,0,1],[1,1,1,1]]
    result = num(warehouse2)
    print(result)



