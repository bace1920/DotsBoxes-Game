# events­example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import time

#宏定义
playerA = 3#玩家A 占领区域 红色
playerB = 4#玩家B 占领区域 蓝色
none = 5#未占领区域

dot = 2#点
DrawedLine = 1#已放置的线
unDrawedLine = 0#未放置的线
#直线方向
Lateral = 1001#横向
Portrait = 1002#纵向

#全局变量
logicBoard = [[] for i in range(9)]
player = playerA
turn = 1#1为换手，得分则不换手，即当前玩家连手
time = 10
scoreA = 0
scoreB = 0

def init(data):
    global player, turn, logicBoard
    # load​ ​data.xyz​ as appropriate
    for i in range(0, 9, 2):
        logicBoard[i]=[dot, unDrawedLine, dot, unDrawedLine, dot, unDrawedLine, dot, unDrawedLine, dot]
    for i in range(1, 9, 2):
        logicBoard[i]=[unDrawedLine, none, unDrawedLine, none, unDrawedLine, none, unDrawedLine, none, unDrawedLine]

    for i in range(0, 9):
        print(logicBoard[i])

def gameOver(canvas):
    global scoreA, scoreB
    if scoreA > scoreB:
        canvas.create_text(450, 325, text="Red Win!", font=(u'微软雅黑',20,'bold'), fill = 'red')
    elif scoreA < scoreB:
        canvas.create_text(450, 325, text="Blue Win!", font=(u'微软雅黑',20,'bold'), fill = 'blue')
    elif scoreA == scoreB:
        canvas.create_text(450, 325, text="DRAW~", font=(u'微软雅黑',20,'bold'), fill = 'gray')

#判断鼠标点击的线条
def pointCheck(event):
    global player, turn, logicBoard, turn, time
    for i in range(0,5):
        if event.y>10+80*i and event.y<20+80*i:
            #print("Y:",i,event.y)
            for q in range(0,4):
                if event.x>10+80*q and event.x<90+80*q:
                    #print("X:",q,event.x)
                    #print(event.x,event.y,i,2*q+1)
                    logicBoard[i*2][2*q+1] = DrawedLine
                    turn = 1
                    time = 10
                    return
    for i in range(0,5):
        if event.x>10+80*i and event.x<20+80*i:
            for q in range(0,4):
                if event.y>10+80*q and event.y<90+80*q:
                    #print("X:",q,"Y:",i,event.x,event.y)
                    logicBoard[2*q+1][i*2] = DrawedLine
                    turn = 1
                    time = 10
                    return

#检测某点周围的四个封闭方块
def occupiedCheck(x, y):
    global player, turn, logicBoard, scoreA, scoreB
    score = 0
    if logicBoard[y][x-1] == DrawedLine and logicBoard[y-1][x-2] == DrawedLine and logicBoard[y-1][x] == DrawedLine and logicBoard[y-2][x-1] == DrawedLine and logicBoard[y-1][x-1] == none:
        logicBoard[y-1][x-1] = player
        turn = 0
        score += 1
    if logicBoard[y][x+1] == DrawedLine and logicBoard[y-1][x+2] == DrawedLine and logicBoard[y-2][x+1] == DrawedLine and logicBoard[y-1][x] == DrawedLine and logicBoard[y-1][x+1] == none:
        logicBoard[y-1][x+1] = player
        turn = 0
        score += 1
    if logicBoard[y][x-1] == DrawedLine and logicBoard[y+1][x-2] == DrawedLine and logicBoard[y+2][x-1] == DrawedLine and logicBoard[y+1][x] == DrawedLine and logicBoard[y+1][x-1] == none:
        logicBoard[y+1][x-1] = player
        turn = 0
        score += 1
    if logicBoard[y][x+1] == DrawedLine and logicBoard[y+1][x+2] == DrawedLine and logicBoard[y+2][x+1] == DrawedLine and logicBoard[y+1][x] == DrawedLine and logicBoard[y+1][x+1] == none:
        logicBoard[y+1][x+1] = player
        turn = 0
        score += 1
    if player == playerA:
        scoreA +=score
    else:
        scoreB +=score
    return

def mousePressed(event, data, canvas):
    # use event.x and event.y
    #棋盘外的click不响应
    global player, turn, logicBoard, time
    turn = 0
    if (scoreA + scoreB) == 16 :
        exit(0)
    if event.x > 340 or event.y > 340 or event.x < 10 or event.y < 10:
        return
    else:
        pointCheck(event)
        #检测点(3,3) (7,3) (3,7) (7,7)四个点周围的4各方块即可
        occupiedCheck(3-1, 3-1)
        occupiedCheck(7-1, 3-1)
        occupiedCheck(3-1, 7-1)
        occupiedCheck(7-1, 7-1)
        #print(turn)
        if turn == 1:
            if player == playerA:
                player = playerB
            else:
                player = playerA
    return

def timerFired(canvas):
    global player, turn, logicBoard, time
    time = 10
    if player == playerA:
        player = playerB
    else:
        player = playerA
    return

def drawBoard(canvas):
    global player, turn, logicBoard, time, scoreA, scoreB
    #基础图形为点，蓝色玩家占领区域，红色玩家占领区域，未放置的线，已放置的线
    def UndrawLine(canvas, x, y, direct):
        if direct == Lateral:
            canvas.create_line(x-40,y-4,x+40,y-4,width=2)
            canvas.create_line(x-40,y+4,x+40,y+3,width=2)
        elif direct == Portrait:
            canvas.create_line(x-4,y-40,x-4,y+40,width=2)
            canvas.create_line(x+4,y-40,x+4,y+40,width=2)

    def drawedLine(canvas, x, y, direct):
        if direct == Lateral:
            #print("drawedLine Lateral")
            canvas.create_line(x-40,y,x+40,y,width=8,fill = 'black')
        elif direct == Portrait:
            canvas.create_line(x,y-40,x,y+40,width=8,fill = 'black')

    def drawDot(canvas,x,y):
        canvas.create_oval(x-8,  y-8, x+8, y+8, fill = 'black')

    def drawRectangle(canvas, x, y, q, i):
        if logicBoard[q][i] == playerA:
            color = "red"
        else:
            color = "blue"
        canvas.create_rectangle(x - 38,y - 38,x + 38,y + 38,fill = color)

    #绘制游戏信息
    canvas.create_text(450, 20, text="Timer:"+str(round(time,1)), font=(u'微软雅黑',20,'bold'), fill = 'green')
    canvas.create_text(450, 80, text="：", font=(u'微软雅黑',20,'bold'), fill = 'gray')
    canvas.create_text(432, 80, text=scoreA, font=(u'微软雅黑',20,'bold'), fill = 'red')
    canvas.create_text(468, 80, text=scoreB, font=(u'微软雅黑',20,'bold'), fill = 'blue')
    if player == playerA:
        canvas.create_text(450, 50, text="Red's Turn", font=(u'微软雅黑',20,'bold'), fill = 'red')
    else:
        canvas.create_text(450, 50, text="Blue's Turn", font=(u'微软雅黑',20,'bold'), fill = 'blue')
    #绘制棋盘
    for i in range(0, 9):
        for q in range(0, 9):
            if logicBoard[q][i] == dot:
                #print("Draw dots at",15+i*40,15+q*40)
                drawDot(canvas, 15+i*40, 15+q*40)
            elif logicBoard[q][i] == unDrawedLine:
                if q%2 == 0:
                    UndrawLine(canvas, 15+i*40, 15+q*40, Lateral)
                else:
                    UndrawLine(canvas, 15+i*40, 15+q*40, Portrait)
            elif logicBoard[q][i] == DrawedLine:
                if q%2 == 0:
                    drawedLine(canvas, 15+i*40, 15+q*40, Lateral)
                else:
                    drawedLine(canvas, 15+i*40, 15+q*40, Portrait)
            elif logicBoard[q][i] == playerA or logicBoard[q][i] == playerB:
                drawRectangle(canvas ,15+i*40, 15+q*40, q, i)
    if (scoreA + scoreB) == 16:
        gameOver(canvas)
    canvas.update()

def redrawAll(canvas, data):
    # draw in canvas
    drawBoard(canvas)
    return

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data, canvas)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        global time, scoreA, scoreB
        if (scoreA + scoreB) != 16:
            time -= 0.1
        if time == 0:
            pass
        if time <= 0:
            timerFired(canvas)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object):
        pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    #data.
    init(data)
    # create the root and the canvas
    root = Tk()
    root.title("Dots And Boxes")
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))

    timerFiredWrapper(canvas, data)
    canvas.update()
    # and launch the app
    #drawBoard(canvas)
    root.mainloop()  # blocks until window is closed
run(550, 350)
