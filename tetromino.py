def tetromino():
    tetromino = [[[[] for k in range(4)] for j in range(4)] for i in range(7)]
    with open("ars") as f:
        for i in range(7):
            for j in range(4):
                for k in range(4):
                    line = f.readline().rstrip()
                    tetromino[i][j][k] = line
    return tetromino

def colors(): return [(255, 0, 0), (0, 0, 255), (255, 127, 0), (255, 255, 0), (128, 0, 128), (0, 255, 255), (0, 255, 0)]

if __name__ == '__main__':
    s = shapes()
    for j in range(4):
        for k in range(4):
            print(s[1][j][k])
    pass
