import pandas as pd
from sklearn.externals import joblib
import turtle
import graphics
NUM_FRUIT = 1
DIM = 8
X = [1, -1, 0, 0];
Y = [0, 0, 1, -1];

def move(l, wh):
    posx = 0
    posy = 0
    S = []
    for i in range(DIM):
        S += [[0] * DIM]
    
    for i in range(0, DIM):
        for j in range(0, DIM):
            now = l[i * DIM + j]
            S[i][j] = now
            if(now == 2 or now == 6):
                posx = i
                posy = j

    i = posx
    j = posy
    i += X[wh]
    j += Y[wh]
    while(i >= 0 and i < DIM and j >= 0 and j < DIM and (S[i][j] == 3 or S[i][j] == 5)):
        i += X[wh]
        j += Y[wh]

    if(i < 0 or i >= DIM or j < 0 or j >= DIM):
        return l

    while(i != posx or j != posy):
        agex = i - X[wh]
        agey = j - Y[wh]

        if(S[i][j] == 1):
            if(S[agex][agey] == 2):
                S[i][j] = 2
                S[agex][agey] = 1
                
            if(S[agex][agey] == 6):
                S[i][j] = 2
                S[agex][agey] = 4
                
            if(S[agex][agey] == 3):
                S[i][j] = 3
                S[agex][agey] = 1
                
            if(S[agex][agey] == 5):
                S[i][j] = 3
                S[agex][agey] = 4
                
        else:
            if(S[agex][agey] == 2):
                S[i][j] = 6
                S[agex][agey] = 1
                
            if(S[agex][agey] == 6):
                S[i][j] = 6
                S[agex][agey] = 4
            
            if(S[agex][agey] == 3):
                S[i][j] = 5
                S[agex][agey] = 1
            
            if(S[agex][agey] == 5):
                S[i][j] = 5
                S[agex][agey] = 4
            
        i = agex;
        j = agey;
        
    ret = []
    for i in range(0, DIM):
        for j in range(0, DIM):
            ret.append(S[i][j])

    
    return ret

def check_finished(l):
    cnt = 0
    for i in l:
        if(i == 5):
            cnt += 1
    return cnt == NUM_FRUIT
    
def print_grid(l, win):

    rect = graphics.Rectangle(graphics.Point(0, 0), graphics.Point(600, 600))
    rect.setFill("cyan")
    rect.draw(win)
    
    diff = 600//DIM

    for i in range(0, DIM):
        line = graphics.Line(graphics.Point(i * diff, 0), graphics.Point(i * diff, 600))
        line.draw(win)

        line = graphics.Line(graphics.Point(0, i * diff), graphics.Point(600, i * diff))
        line.draw(win)

    for i in range(0, DIM):
        for j in range(0, DIM):
            now = l[j * DIM + i]
            if(now > 3):
                rect = graphics.Rectangle(graphics.Point(i * diff, j * diff), graphics.Point(i * diff + diff, j * diff + diff))
                rect.setFill("yellow")
                rect.draw(win)

            if(now == 2 or now == 6):
                x = i * diff + diff // 2;
                y = j * diff + diff // 2;
                cir = graphics.Circle(graphics.Point(x, y), 25)
                cir.setFill("red")
                cir.draw(win)

            if(now == 3 or now == 5):
                x = i * diff + diff // 2;
                y = j * diff + diff // 2;
                cir = graphics.Circle(graphics.Point(x, y), 25)
                cir.setFill("green")
                cir.draw(win)
            
    direction = win.getKey()
    return direction

def give_me_grid():
    l = [1] * (DIM * DIM)

    l[42] = 3
    l[11] = 4
    l[27] = 2
    
    return l

def list_to_dataframe(l):
    p = {}
    for i in range(len(l)):
        p[i] = [l[i]]
    return pd.DataFrame.from_dict(p)

def main():
    model = joblib.load('svm.pkl')
    data = pd.read_csv('data.csv')

    data = data.iloc[0:1000]
    
    X = data.iloc[:, 0:64]
    Y = data.iloc[:, 64]

    pr = model.predict(X)
    print(pr)
    return

    grid = give_me_grid()

    win = graphics.GraphWin('Game', 600, 600)

    while not check_finished(grid):
        print_grid(grid, win)
        wh = model.predict(list_to_dataframe(grid))[0]
        print(model.predict(list_to_dataframe(grid)))
        grid = move(grid, wh)

    print_grid(grid, win)
    win.close()

if __name__ == "__main__":
    main()
"""
    l = [1] * 64
    l[6] = 6
    l[20] = 3

    win = graphics.GraphWin('Game', 600, 600)
    
    while True:
        direction = print_grid(l, win)
        if direction == 'Down':
            l = move(l, 0)
        elif direction == 'Up':
            l = move(l, 1)
        elif direction == 'Right':
            l = move(l, 2)
        elif direction == 'Left':
            l = move(l, 3)
        else:
            break
    win.close()
"""
