# ---- CS325 - Fall 2020 - Portfolio Project
# ---- Minesweeper
# ---- Frannie Richert

"""
Puzzle Information from Source:
file:///C:/Users/frann/Downloads/A_Survey_of_NP-Complete_puzzles%20(1).pdf

Problem # 11 Minesweeper is a popular computer puzzle game
that comes with some MicrosoftTM operating systems.
It is played on an m × n grid of cells, all of which are initially hidden.
k mines are randomly distributed over the grid.
Clicking on a cell reveals its contents.
If the cell contains a mine then the game ends and the player loses.
If there is not a mine in the cell, a number is revealed (1..8
that corresponds to the number of adjacent
(horizontally, vertically or diagonally) cells that contain a mine.
If a cell does not contain a mine, and is not next to a mine,
a blank cell is displayed and other adjacent blank cells are also revealed.
The game ends when, either a mine is uncovered (a loss) or
all cells are revealed that do not contain a mine (a win).

The goal is to reveal all of the cells that do not contain a mine,
leaving the k cells that do contain a mine still hidden.
Deciding the solvability of Minesweeper has been shown
to be NP-Complete by Kaye (2000).
We can define l as the maximum number of mines that surround any cell,
and then general Minesweeper has l = 8.
DECISION QUESTION (Kaye, 2000):
Given an arbitrary set of mines and numbers on a rectangular grid, can
mines be placed consistently, following the usual minesweeper rules?
"""

import random


class MINESWEEPER:

    # --- Initializer function
    def __init__(self, rows=0, cols=0, numMines=0, hardcodedBoard=False):

        self.rows = rows
        self.cols = cols
        self.numMines = numMines
        self.isBoardHardcoded = hardcodedBoard
        self.mineList = []
        self.minesFoundList = []
        self.visibleBoard = []  # holds what USER CAN CURRENTLY SEE
        self.invisibleBoard = []  # holds ALL NUMBERS AND MINES
        self.currUserChoiceRowCol = [0, 0]
        self.historicalUserChoices = []
        self.correctChoices = 0
        self.iteration = 0
        self.quitChoice = 0
        self.status = ""

    """
    # source: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
    """  # noqa

    def representsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    # --- Ask user for board specifications
    def getUserBoardInfo(self):

        # -- assuming that if user inputs 1 arg, they will input all args
        if self.rows > 0 and self.cols > 0 and self.numMines > 0:
            return 1   # all is good

        # -- if user did not enter all 3 args
        elif self.rows > 0 or self.cols > 0 or self.numMines > 0:
            print("\n -!- ERROR. All THREE input values required in object class variable, ")  # noqa
            print("if you choose to setup the game that way, as opposed to picking")  # noqa
            print("the board characteristics (row, col, numMines) while running the program.\n")  # noqa
            print("Please restart the game and adjust your object declaration accordingly.\n")  # noqa
            return 0   # error

        # -- Ask if user wants to use hardcoded board
        hcboard = input("Do you want to use the hardcoded example board? Y/N --> ")  # noqa
        if hcboard == "Y":
            self.createHardcodedBoard()
            return 2

        # -- num rows
        while True:
            rows = input("Enter number of board rows (4<=rows<=100): ")
            if not self.representsInt(rows):
                continue
            elif int(rows) >= 4 and int(rows) <= 100:
                self.rows = int(rows)
                break
            else:
                continue
        # -- num cols
        while True:
            cols = input("Enter number of board columns (4<=cols<=100): ")
            if not self.representsInt(cols):
                continue
            elif int(cols) >= 4 and int(cols) <= 100:
                self.cols = int(cols)
                break
            else:
                continue
        # -- num mines
        while True:
            mineMin = 1
            mineMax = (self.rows * self.cols) * .2  # max is 20% of cells
            mines = input("Enter number of mines on board (%i<=mines<=%.0f): " %  # noqa
                          (mineMin, mineMax))
            if not self.representsInt(mines):
                continue
            elif int(mines) >= mineMin and int(mines) <= mineMax:
                self.numMines = int(mines)
                break
            else:
                continue

        return 1  # all is good

    # --- Create minesweeper board, a list of lists:
    #     each internal list represents a row of data
    #    NOTE ITEMS IN BOARD ARE 0-INDEXED
    def createBoard(self):

        visibleBoard = []
        invisibleBoard = []
        # create empty board first, '-' represents hidden cell
        for i in range(self.rows):
            visibleBoard.append([])
            invisibleBoard.append([])
            currlist = []
            for j in range(self.cols):
                visibleBoard[i].append('-')
                invisibleBoard[i].append('-')

        # randomly place mines on INVISIBLE BOARD
        i = 0
        mineListStr = []
        while i < self.numMines:

            currrow = random.randint(0, self.rows - 1)
            currcol = random.randint(0, self.cols - 1)
            currstr = str(currrow) + '-' + str(currcol)

            # if mine list is not empty, need to check we haven't already
            # picked this cell
            if not mineListStr:
                while currstr in mineListStr:
                    currrow = random.randint(0, self.rows - 1)
                    currcol = random.randint(0, self.cols - 1)
                    currstr = str(currrow) + '-' + str(currcol)

            # Update board value for this cell
            # board iz 1-indexed
            currlist = [currrow+1, currcol+1]
            self.mineList.append(currlist)
            mineListStr.append(currstr)
            invisibleBoard[currrow][currcol] = '*'  # using star for a mine!

            i += 1

        self.visibleBoard = visibleBoard
        self.invisibleBoard = invisibleBoard

        # self.saveBoardToFile()

    # -- Used for grabbing a sample board for hardcoding
    def saveBoardToFile(self):
        f = open("minesweeper_game_board.txt", "w")
        for row in self.invisibleBoard:
            f.writelines(row)
            f.writelines("\n")
        f.close()

    def createHardcodedBoard(self):
        self.rows = 10
        self.cols = 10
        self.numMines = 15
        hb = ["-----*---*",
              "----------",
              "--------*-",
              "-*-**-----",
              "----------",
              "-*--*-**--",
              "-------*--",
              "-------*--",
              "----**----",
              "--*-------"]

        invisarr = []
        visarr = []
        for i in range(len(hb)):
            invisarr.append([])
            visarr.append([])
            currrow = hb[i]
            for j in range(len(currrow)):
                invisarr[i].append(currrow[j])
                visarr[i].append('-')
                if currrow[j] == '*':
                    self.mineList.append([i+1, j+1])
        self.invisibleBoard = invisarr
        self.visibleBoard = visarr

    # --- Print minesweeper board
    def printBoard(self, type="visible"):

        # Print header and separator line
        print("\nCurrent Minesweeper Board:")
        seprow = ['-' for i in range(self.cols*5+5)]
        seprow = ''.join([str(elem) for elem in seprow])
        print(seprow)

        # Print col #s
        print("   ", end='')
        for j in range(self.cols):
            if (j+1) <= 9:
                print("   C" + str(j+1), end='')
            elif (j+1) <= 99:
                print("  C" + str(j+1), end='')
        print("\n")

        # Loop through each row,  print data for each cell
        # NOT doing any calculations in this function, just printing the board
        # as it is
        for i in range(self.rows):
            print("R%i:" % (i+1), end='')

            # assuming max board is 100x100, so only need to consider
            # col size numbers up to 3
            if (i+1) <= 9:
                print("    ", end='')
            elif (i+1) <= 99:
                print("   ", end='')
            else:
                print("  ", end='')

            if type == "invisible":
                rowlist = self.invisibleBoard[i]
            else:
                rowlist = self.visibleBoard[i]
            rowlist = '    '.join([str(elem) for elem in rowlist])
            print(rowlist)
        print(seprow)
        print("\n")

    # -- Checking user input!
    def getUserInput(self):
        i = 0
        countCommas = 0
        countFirstHalfDigits = 0
        firstHalfDigits = []
        foundFirstNum = False
        countSecondHalfDigits = 0
        secondHalfDigits = []
        foundSecondNum = False
        countTimesAsked = 0

        while True:

            # first time around, ask for user input
            if i == 0 and countTimesAsked == 0:
                # Initial ask for user input
                userinput = input("Please enter your row,column choice here: ")
                if userinput == "quit":
                    self.quitChoice = 1
                    return
                inputlen = len(userinput)

            # if we have reached the end of our current string
            elif i == (inputlen):
                # if we have a full set of data now, and
                # user has already chosen this value
                if foundFirstNum and foundSecondNum:
                    if [firstNum, secondNum] in self.historicalUserChoices:
                        foundFirstNum = False
                        foundSecondNum = False
                        firstNum = 0
                        secondNum = 0
                        i = 0
                        print("User has already chosen this pair.")
                        countTimesAsked += 1
                    else:
                        self.currUserChoiceRowCol[0] = firstNum
                        self.currUserChoiceRowCol[1] = secondNum
                        break

            if countTimesAsked > 0 and i == 0:
                countCommas = 0
                countFirstHalfDigits = 0
                firstHalfDigits = []
                countSecondHalfDigits = 0
                secondHalfDigits = []
                userinput = input("ERROR! Please enter A VALID CHOICE: ")
                inputlen = len(userinput)

            # Grabbing current character of user input
            currchar = userinput[i]

            # UPDATE COUNTS
            if currchar == ',':
                countCommas += 1
            elif countCommas == 0 and currchar.isdigit():
                countFirstHalfDigits += 1
                firstHalfDigits.append(currchar)
            elif countCommas > 0 and currchar.isdigit():
                countSecondHalfDigits += 1
                secondHalfDigits.append(currchar)

            # if firt character is not a digit
            if i == 0 and not currchar.isdigit():
                i = 0
                print("First char is not digit.")
                countTimesAsked += 1
                continue

            # if get to last digit and haven't encountered a comma or too many
            elif i == (inputlen-1) and (countCommas == 0):
                i = 0
                print("No commas by end of string.")
                countTimesAsked += 1
                continue

            # if user has input too many commas
            elif countCommas > 1:
                i = 0
                print("More than 1 comma.")
                countTimesAsked += 1
                continue

            # if we get to last digit and haven't encountered second digits yet
            elif i == (len(userinput)-1) and countSecondHalfDigits == 0:
                i = 0
                print("No digits after comma.")
                countTimesAsked += 1
                continue

            # if any character is anything other than a comma or digit
            elif not currchar.isdigit() and currchar != ',':
                i = 0
                print("Current char isn't a comma or digit.")
                countTimesAsked += 1
                continue

            # checking if we have safely found the first number
            elif countCommas > 0 and not foundFirstNum:
                firstNum = ""
                firstNum = int(firstNum.join(firstHalfDigits))
                # CHECK IF IT IS <= num rows
                if firstNum > self.rows or firstNum == 0:
                    i = 0
                    print("First number is > # rows or is 0.")
                    countTimesAsked += 1
                    continue
                else:
                    foundFirstNum = True

            # checking if we have safely found the second number
            elif countCommas > 0 and not foundSecondNum and i == (inputlen - 1):  # noqa
                secondNum = ""
                secondNum = int(secondNum.join(secondHalfDigits))
                # CHECK IF IT IS <= num cols
                if secondNum > self.cols or secondNum == 0:
                    i = 0
                    print("Second number is > # cols or is 0.")
                    countTimesAsked += 1
                    continue
                else:
                    foundSecondNum = True

            # Increment i
            i += 1

        # keeping track of historical user choices
        self.historicalUserChoices.append([firstNum, secondNum])

    def updateCellMineCount(self, currrow, currcol, adjList):

        # --- If user did not hit a mine,
        # update numbers in visible board in all adjacent cells around curr cell  # noqa
        # need to look in all 8 directions from cell to see if there are mines
        # directions below are as if i am facing the board

        countMines = 0

        for l in adjList:
            # mineList is 1-indexed, need to add 1 to indices
            if [l[0]+1, l[1]+1] in self.mineList:
                countMines += 1

        # setting the number on the visible board if applicable
        if countMines > 0:
            self.visibleBoard[currrow][currcol] = countMines
            self.historicalUserChoices.append([currrow+1, currcol+1])
            return countMines
        else:
            self.visibleBoard[currrow][currcol] = ' '
            self.historicalUserChoices.append([currrow+1, currcol+1])
            return 0

    def topLeftCell(self, currrow, currcol):
        if currrow >= 1 and currcol >= 1:
            cell = [currrow - 1, currcol - 1]
            # print("Top Left: ", end='')
            # print(cell)
            # if this cell hasn't been "turned over yet", return
            if self.visibleBoard[cell[0]][cell[1]] == '-':
                return cell
        else:
            return []

    def topMiddleCell(self, currrow, currcol):
        if currrow >= 1:
            cell = [currrow - 1, currcol]
            # print("Top Middle: ", end='')
            # print(cell)
            # if this cell hasn't been "turned over yet", return
            if self.visibleBoard[cell[0]][cell[1]] == '-':
                return cell
        else:
            return []

    def topRightCell(self, currrow, currcol):
        if currrow >= 1 and currcol <= (self.cols - 2):
            cell = [currrow - 1, currcol + 1]
            # print("Top Right: ", end='')
            # print(cell)
            # if this cell hasn't been "turned over yet", return
            if self.visibleBoard[cell[0]][cell[1]] == '-':
                return cell
        else:
            return []

    def leftCell(self, currrow, currcol):
        if currcol >= 1:
            cell = [currrow, currcol - 1]
            # print("Left: ", end='')
            # print(cell)
            # if this cell hasn't been "turned over yet", return
            if self.visibleBoard[cell[0]][cell[1]] == '-':
                return cell
        else:
            return []

    def rightCell(self, currrow, currcol):
        if currcol <= (self.cols - 2):
            cell = [currrow, currcol + 1]
            # print("Right: ", end='')
            # print(cell)
            # if this cell hasn't been "turned over yet", return
            if self.visibleBoard[cell[0]][cell[1]] == '-':
                return cell
        else:
            return []

    def bottomLeftCell(self, currrow, currcol):
        if currrow <= (self.rows - 2) and currcol >= 1:
            cell = [currrow + 1, currcol - 1]
            # print("Bottom Left: ", end='')
            # print(cell)
            # if this cell hasn't been "turned over yet", return
            if self.visibleBoard[cell[0]][cell[1]] == '-':
                return cell
        else:
            return []

    def bottomMiddleCell(self, currrow, currcol):
        if currrow <= (self.rows - 2):
            cell = [currrow + 1, currcol]
            # print("Bottom Middle: ", end='')
            # print(cell)
            # if this cell hasn't been "turned over yet", return
            if self.visibleBoard[cell[0]][cell[1]] == '-':
                return cell
            else:
                return
        else:
            return []

    def bottomRightCell(self, currrow, currcol):
        if currrow <= (self.rows - 2) and currcol <= (self.cols - 2):
            cell = [currrow + 1, currcol + 1]
            # print("Bottom Right: ", end='')
            # print(cell)
            # if this cell hasn't been "turned over yet", return
            if self.visibleBoard[cell[0]][cell[1]] == '-':
                return cell
        else:
            return []

    def createAdjacentCellList(self, currrow, currcol):
        adjList = []

        tl = self.topLeftCell(currrow, currcol)
        if tl:
            adjList.append(tl)

        tm = self.topMiddleCell(currrow, currcol)
        if tm:
            adjList.append(tm)

        tr = self.topRightCell(currrow, currcol)
        if tr:
            adjList.append(tr)

        l = self.leftCell(currrow, currcol)
        if l:
            adjList.append(l)

        r = self.rightCell(currrow, currcol)
        if r:
            adjList.append(r)

        bl = self.bottomLeftCell(currrow, currcol)
        if bl:
            adjList.append(bl)

        bm = self.bottomMiddleCell(currrow, currcol)
        if bm:
            adjList.append(bm)

        br = self.bottomRightCell(currrow, currcol)
        if br:
            adjList.append(br)

        return adjList

    """ --------------------------------------------------------------
    This is the meat of the game, and the impoprtant part of updating
    the adjacent cell values as appropriate based on the chosen input cell.
    The algorithm I used here is similar to the bipartite wrestler problem
    approach I used. Grab a list of immediately adjacent items, 
    go through those, adding their adjacent items, etc. etc. as appropriate
    until the list of adjacent items is empty and we have processed 
    all we can. 
    -----------------------------------------------------------------"""

    def updateBoardValues(self, currrow, currcol):

        # -- Initial list of adjacent cells
        adjList = self.createAdjacentCellList(currrow, currcol)
        # print(adjList)

        # -- Calculate Value of Current Cell
        currCellCount = self.updateCellMineCount(currrow, currcol, adjList)

        # -- If current cell has count mines > 0, return
        if currCellCount > 0:
            return

        # If current cell has no mines, keep adding adjacent items of
        # adjacent items to list and checking them for mines around them
        while len(adjList) > 0:

            # -- get first item in list
            cell = adjList.pop(0)
            row = cell[0]
            col = cell[1]

            # -- if this cell value is already blank or equal to a number
            # do not do anything with it, just continue
            if self.visibleBoard[row][col] == ' ' or \
               isinstance(self.visibleBoard[row][col], int):
                continue

            # -- if value of cell is a mine, don't do anything with it and
            # remove this cell from the adjacency list
            if self.invisibleBoard[row][col] == '*':
                continue

            # -- create new adj list
            newAdjList = self.createAdjacentCellList(row, col)

            # -- get current mine count
            mineCount = self.updateCellMineCount(row, col, newAdjList)

            # -- if mine count == 0, add adj list to current adj list
            if mineCount == 0:
                for i in newAdjList:
                    if i not in adjList:
                        adjList.append(i)

            # -- if mine count > 0, continue
            else:
                continue

    def showAllMinesOnVisibleBoard(self):

        for mine in self.mineList:
            row = mine[0]-1
            col = mine[1]-1
            self.visibleBoard[row][col] = '*'

    def countDashesOnBoard(self):
        countDashes = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.visibleBoard[i][j] == '-':  # noqa
                    countDashes += 1
        return countDashes


    def updateGameStatus(self):
        if self.currUserChoiceRowCol in self.mineList:
            self.status = "GAME_OVER"
            self.showAllMinesOnVisibleBoard()
        elif self.countDashesOnBoard() == self.numMines:
            self.status = "GAME_WON"
        else:
            self.status = "CONTINUE"

    def gameIntro(self):
        # -- Welcome message!
        print("\n------------------------ WELCOME TO MINESWEEPER ------------------------")  # noqa
        print("The game will be played on a board size of your choice, selected shortly.")  # noqa
        print("The limit for # of rows and columns is 100 each.")
        print("You will also be asked to enter # of mines. The limit is 20% * # cells in board.")  # noqa
        print("You will be asked to enter a cell at each iteration of the game: row,column .")  # noqa
        print("The board will update, and if you picked a valid cell, the game will continue.")  # noqa
        print("If you entered a cell which contains a mine, the game is over!")
        print("If at any point you want to quit, just type quit when asked for input.")  # noqa
        print("Good luck!")

        # -- Ask user to input board information
        print("\n\n-------------------- CREATE BOARD --------------------")

        if self.isBoardHardcoded:
            self.createHardcodedBoard()
        else:
            userInfoStatus = self.getUserBoardInfo()
            if userInfoStatus == 0:  # if error
                return 0
            elif userInfoStatus != 2:  # using hardcoded board
                self.createBoard()

        print("\n*************** BOARD SHOWING MINES ***************** ")
        print("Used to validate input and results below. In a real game situation,")  # noqa
        print("this would be hidden.")
        self.printBoard(type="invisible")

        # -- Stating Board Characteristics to User
        print("---------------------- BOARD INFO ----------------------")
        print("There are %i rows, %i columns, %i total squares, and\n%i mines on this game board.\n" %  # noqa
              (self.rows, self.cols, self.rows*self.cols, self.numMines))

        # -- Ask user to input board information and create board
        print("\n------------------ NOTE ABOUT INPUT -------------------")
        print("This Message Only Displays at the Beginning of the Game:")
        print("Pick a square in the format #1,#2, ", end='')
        print("where #1 is the row and #2 is the column.")
        print("Example input: 1,4 --> which indicates row 1 and column 4.\n")

        return 1

    def gamePlay(self):
        while True:

            # -- Print Iteration Information
            self.iteration += 1
            print("\n-----> Current Iteration: %i" % self.iteration)

            # -- Get user input and verify is correct,
            # current choice stored in self.currUserChoiceRowCol
            # and historical choices stored in self.historicalUserChoices
            userInputCheck = self.getUserInput()

            # -- Check to see if user wants to quit the program
            if self.quitChoice == 1:
                print("\nEnding the program now. Thank you for playing!\n")
                return

            # -- Check if user hit a mine
            self.updateGameStatus()
            if self.status == "GAME_OVER":
                self.printBoard()
                print("You have hit a mine, and the game is over.")
                print("All mines are now visible on the board.")
                print("Nice try! Play again soon.\n")
                break

            # If the user did not hit a mine, update cell(s) values
            # subtracting 1 as the board itself is 0-indexed
            currRow = self.currUserChoiceRowCol[0]-1
            currCol = self.currUserChoiceRowCol[1]-1
            self.updateBoardValues(currRow, currCol)
            self.printBoard()

            # If user has found ALL NON-MINE CELLS, they have won!
            self.updateGameStatus()
            if self.status == "GAME_WON":
                print("YOU HAVE WON THE GAME!! Congrats!!")
                break

        return 1

    # --- Play Minesweeper Game
    def play(self):
        # ------------- Game intro message + user choices
        gameIntroCheck = self.gameIntro()
        if gameIntroCheck == 0:
            return 0
        # ------------- Game intro message + user choices
        gamePlayCheck = self.gamePlay()
        return 1


# ---- Create Minesweeper class object
# optional args = rows,cols,numMines
# if these aren't input to the initilization here, user is asked later
# mw = MINESWEEPER(hardcodedBoard = True)
mw = MINESWEEPER()
# ---- Play minesweeper
mw.play()
