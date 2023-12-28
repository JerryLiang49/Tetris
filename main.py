from cmu_graphics import *
import math
import random

def onAppStart(app):
    newGame(app)
    
def newGame(app):
    app.rows = 15 
    app.cols = 10
    app.boardLeft = 60
    app.boardTop = 40
    app.boardWidth = 280
    app.boardHeight = 350
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.nextPieceIndex = 0
    app.stepsPerSecond = 2
    app.paused = False
    app.score = 0
    app.gameOver = False
    loadTetrisPieces(app)
    loadNextPiece(app)

def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [gradient('red','purple',start='left'), gradient('yellow','green',start='left'), 
                            gradient('lightblue','navy',start='left'), gradient('cyan','tomato',start='left'),
                            gradient('chartreuse','aquamarine',start='left'), gradient('orange','turquoise',start='left') ,
                            gradient('oliveDrab','teal',start='left')]

def loadNextPiece(app):
    loadPiece(app,app.nextPieceIndex)
    if not pieceIsLegal(app): #if piece is immediately not legal, game over
        app.gameOver = True
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces)) #next piece is randomized

def loadPiece(app, pieceIndex):
    app.piece = app.tetrisPieces[pieceIndex] 
    app.pieceColor = app.tetrisPieceColors[pieceIndex] #gets the piece and its color
    app.pieceTopRow = 0
    app.pieceLeftCol = app.cols//2 - len(app.piece[0])//2 #finds the left column of the piece

def drawPiece(app):
    if app.piece != None:
        rows = len(app.piece)
        cols = len(app.piece[0])
        for row in range(rows): #loops through the piece
            for col in range(cols):
                if app.piece[row][col]:
                    #fills the cell if it's True
                    drawCell(app, app.pieceTopRow+row, app.pieceLeftCol+col, app.pieceColor)
                    
def onKeyPress(app, key):
    if '0' <= key <= '6': loadPiece(app, int(key))
    elif key == 'left': movePiece(app,0,-1)
    elif key == 'right': movePiece(app,0,1)
    elif key == 'down': movePiece(app,1,0)
    elif key == 'space': hardDropPiece(app)
    elif key == 'up': rotatePieceClockwise(app)
    elif key == 's': takeStep(app)
    elif key == 'p': app.paused = not app.paused
    elif key == 'r': newGame(app)
    elif key in ['a','b','c','d','e','f','g','h']: loadTestBoard(app, key)

def loadTestBoard(app, key):
    # DO NOT EDIT THIS FUNCTION
    # We are providing you with this function to set up the board
    # with some test cases for clearing the rows.
    # To use this: press 'a', 'b', through 'h' to select a test board.
    # Then press 'space' for a hard drop of the red I,
    # and then press 's' to step, which in most cases will result
    # in some full rows being cleared.

    # 1. Clear the board and load the red I piece 
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.nextPieceIndex = 0
    loadNextPiece(app)
    # 2. Move and rotate the I piece so it is vertical, in the
    #    top-left corner
    for keyName in ['down', 'down', 'up', 'left', 'left', 'left']:
        onKeyPress(app, keyName)
    # 3. Add a column of alternating plum and lavender cells down
    #    the rightmost column
    for row in range(app.rows):
        app.board[row][-1] = 'plum' if (row % 2 == 0) else 'lavender'
    # 4. Now almost fill some of the bottom rows, leaving just the
    #    leftmost column empty
    indexesFromBottom = [ [ ], [0], [0,1], [0,1,2], [0,2],
                          [1,2,3], [1,2,4], [0,2,3,5] ]
    colors = [gradient('pink','purple',start='left'), 'aqua', 'khaki', 'aquamarine',
              'darkKhaki', 'peachPuff']
    for indexFromBottom in indexesFromBottom[ord(key) - ord('a')]:
        row = app.rows - 1 - indexFromBottom
        color = colors[indexFromBottom]
        for col in range(1, app.cols):
            app.board[row][col] = color
            
def rotatePieceClockwise(app):
    oldPiece, oldTopRow, oldLeftCol = app.piece, app.pieceTopRow, app.pieceLeftCol
    oldRows, oldCols = len(oldPiece), len(oldPiece[0])
    centerRow, centerCol = oldTopRow + oldRows//2, oldLeftCol + oldCols//2
    app.piece = rotate2dListClockwise(app.piece)
    newRows, newCols = len(app.piece), len(app.piece[0])
    app.pieceTopRow, app.pieceLeftCol = centerRow - newRows//2, centerCol - newCols//2
    if pieceIsLegal(app) == False:
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol
    
def movePiece(app, drow, dcol):
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if pieceIsLegal(app) == False:
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
    else:
        return True

def pieceIsLegal(app):
    if app.piece != None:
        rows = len(app.piece)
        cols = len(app.piece[0])
        for row in range(rows):
            for col in range(cols):
                if app.piece[row][col]:
                    targetRow = app.pieceTopRow + row
                    targetCol = app.pieceLeftCol + col
                    #returns false if piece goes out of the board or there is already another piece there
                    if ((targetRow < 0 or targetRow >= app.rows) or (targetCol < 0 or targetCol >= app.cols) or
                        (app.board[targetRow][targetCol] != None)):
                            return False
    return True

def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass

def redrawAll(app):
    if app.gameOver:
        drawLabel("Game Over! Press r to start a new game", 200, 200, bold = True, fill = 'red', size = 18)
    if not app.gameOver:
        drawLabel('Tetris!', 200, 23, bold = True, font='cinzel', size=18)
        drawLabel("Score: " + str(app.score), 30, 15, bold = True, size = 12)
        drawBoard(app)
        drawPiece(app)
        drawBoardBorder(app)

def onStep(app):
    if not app.paused:
        takeStep(app)
    
def takeStep(app):
    if not movePiece(app, +1, 0): #We could not move the piece, so place it on the board:
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)

def placePieceOnBoard(app):
    if app.piece != None:
        rows = len(app.piece)
        cols = len(app.piece[0])
        for row in range(rows):
            for col in range(cols):
                if app.piece[row][col]:
                    targetRow = app.pieceTopRow + row
                    targetCol = app.pieceLeftCol + col
                    #change the board to the color of the piece so it's placed there
                    app.board[targetRow][targetCol] = app.pieceColor
                
def removeFullRows(app):
    row = 0
    addRow = 0
    colorCount = 0
    rowsPopped = 0
    while row < len(app.board):
        for cell in app.board[row]:
            if cell != None:
                colorCount += 1
        if colorCount == app.cols: #if the full row is colored, remove the row
            app.board.pop(row)
            rowsPopped += 1
            row -= 1 #subtract row by one because one row was removed
        row += 1
        colorCount = 0 #reset colocount
    #score system
    if rowsPopped == 1: app.score += 100
    elif rowsPopped == 2: app.score += 300
    elif rowsPopped == 3: app.score += 500
    elif rowsPopped == 4: app.score += 800
    if app.score > 1100: app.stepsPerSecond = 4.5
    elif app.score > 800: app.stepsPerSecond = 4
    elif app.score > 500: app.stepsPerSecond = 3
    #add rows back on top
    while addRow < rowsPopped:
        emptyRow = [None] * app.cols
        app.board.insert(0, emptyRow)
        addRow += 1
                
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
             
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def rotate2dListClockwise(L):
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = [[0]*newCols for i in range(newRows)]
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            M[oldCol][oldRows-1-oldRow] = L[oldRow][oldCol]
    return M

def main():
    runApp()

main()