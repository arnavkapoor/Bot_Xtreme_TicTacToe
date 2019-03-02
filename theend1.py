import copy
import time
# f = 0
class Team164:
    def __init__(self):
        pass

    def minimax(self,board,old_move,flag,depth,p_win, poss_boards):
        # global f
        # f+=1
        if flag == 'o':
           best = [-1,-1,-1, -10000000000000000]
        else:
           best = [-1,-1,-1, +10000000000000000]

        if depth == 0:      
            value = self.calculate_heuristic(board,flag,poss_boards, p_win);
            return [-2, -1 , -1, value];

        cells = board.find_valid_move_cells(old_move)
        # if len(cells) == 0:
        #     print(old_move)
        #     print(depth)
        #     print "chutiye"
        #     ch = raw_input()
        #     # time.sleep(10)
        for cell in cells:
            x,y,z = cell[0],cell[1],cell[2]
            poss_boards.append(cell)

            board.big_boards_status[x][y][z] = flag

            if(self.mywin([x,y,z],board,flag) == 1 and p_win == 0):
                bmove = self.minimax(board,[x,y,z],flag,depth-1,1,poss_boards)

            else:
                if flag == 'x':
                    bmove = self.minimax(board,[x,y,z],'o',depth-1,0,poss_boards)
                if flag == 'o':
                    bmove = self.minimax(board,[x,y,z],'x',depth-1,0,poss_boards)

                    
            board.big_boards_status[x][y][z] = '-'
            if(y%3==1 and z%3==1):
                if flag=='o':
                    bmove[3]+=1;
                elif flag=='x':
                    bmove[3]-=1;


            poss_boards.pop()
            bmove[0],bmove[1],bmove[2] = x,y,z;
            if x == -1:
                print bmove
                print "noo"
                time.sleep(10)
            if flag == 'o':
                if bmove[3] > best[3]:
                    best = bmove  # max value        
            else:
                if bmove[3] <= best[3]:
                    best = bmove  # min value
        # print "arnav"
        # print best
        # time.sleep(10);
        return best

    def mywin(self,mymove,board_state, ch):
      
        x = mymove[1]/3
        y = mymove[2]/3
        z = mymove[0]
        
        haswon = 0;
        
        bs = board_state.big_boards_status[z]
        for i in range(3):
            #checking for horizontal pattern(i'th row)
            if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == ch):
                haswon = 1
            #checking for vertical pattern(i'th column)
            if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == ch):
                haswon = 1
            
            if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == ch):
                haswon = 1
            
            if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == ch):
                haswon = 1
            
        return haswon



    def calculate_heuristic(self,bs,ch,poss_boards,p_win):
        if ch == 'x':
            op_ch = 'o'
        if ch == 'o':
            op_ch = 'x'

        bs2 = bs
        scoremf = 0
        factor = 600  # Winning triplets in Small Boards
        factor6 = 600 # Blocking on small boards
        # if p_win == 0:
        #     factor +=5  
        factor2 = 2000 # Winning Triplets in Big Board(Entire Game)
        factor3 = 0 # xx* type in small boards
        factor4 = 0 # xx* type in Big Board
        factor5 = 1000 # Blocking on big boards
        if p_win == 0:
            factor4 += 0  # Winning triplets in Small Boards
        
        ssmall_boards_status = copy.deepcopy(bs2.small_boards_status)
        poss_boards.reverse()
        for mv in poss_boards:
            x = mv[1]/3
            y = mv[2]/3
            z = mv[0]
            factor *= 4 
            factor2 *= 5
            factor3 *= 3
            factor4 *= 3
            factor5 *= 3
            factor6 *= 3

            bs = copy.deepcopy(bs2.big_boards_status[z])
            for i in range(3):
                    #checking for horizontal pattern(i'th row)
                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == 'o'):
                    ssmall_boards_status[z][x][y] = 'o'
                    scoremf += factor
                    # if self.count(ssmall_boards_status[z], x, y, 'x') * factor5 >= 500:
                        # print("Huan")
                        # time.sleep(10)
                    scoremf += self.count(ssmall_boards_status[z], x, y, 'x') * factor5 
                #checking for vertical pattern(i'th column)
                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == 'o'):
                    ssmall_boards_status[z][x][y] = 'o'
                    scoremf += factor
                    # if self.count(ssmall_boards_status[z], x, y, 'x') * factor5 >= 500:
                        # print("Huan")
                        # time.sleep(10)
                    scoremf += self.count(ssmall_boards_status[z], x, y, 'x') * factor5 
            

                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == 'x'):
                    scoremf-=factor
                    ssmall_boards_status[z][x][y] = 'x'
                    # if self.count(ssmall_boards_status[z], x, y, 'o') * factor5 >= 500:
                        # print("Huan")
                        # time.sleep(10)
                    scoremf -= self.count(ssmall_boards_status[z], x, y, 'o') * factor5

                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == 'x'):
                    scoremf-=factor
                    ssmall_boards_status[z][x][y] = 'x'
                    # if self.count(ssmall_boards_status[z], x, y, 'o') * factor5 >= 500:
                        # print("Huan")
                        # time.sleep(10)
                    scoremf -= self.count(ssmall_boards_status[z], x, y, 'o') * factor5 

                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] and bs[3*x+i][3*y+2]=='-'):
                    if bs[3*x+i][3*y] == 'o':
                        scoremf += factor3
                    elif bs[3*x+i][3*y] =='x':
                        scoremf -= factor3
                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+2] and bs[3*x+i][3*y+1]=='-'):
                    if bs[3*x+i][3*y] == 'o':
                        scoremf += factor3
                    elif bs[3*x+i][3*y] =='x':
                        scoremf -= factor3
                if (bs[3*x+i][3*y+2] == bs[3*x+i][3*y+1] and bs[3*x+i][3*y]=='-'):
                    if bs[3*x+i][3*y+1] == 'o':
                        scoremf += factor3
                    elif bs[3*x+i][3*y+1] =='x':
                        scoremf -= factor3
                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] and bs[3*x+2][3*y+i] == '-'):
                    if bs[3*x][3*y+i] == 'o':
                        scoremf += factor3
                    elif bs[3*x][3*y+i] == 'x':
                        scoremf -= factor3
                if (bs[3*x][3*y+i] == bs[3*x+2][3*y+i] and bs[3*x+1][3*y+i] == '-'):
                    if bs[3*x][3*y+i] == 'o':
                        scoremf += factor3
                    elif bs[3*x][3*y+i] == 'x':
                        scoremf -= factor3
                if (bs[3*x+2][3*y+i] == bs[3*x+1][3*y+i] and bs[3*x][3*y+i] == '-'):
                    if bs[3*x+1][3*y+i] == 'o':
                        scoremf += factor3
                    elif bs[3*x+1][3*y+i] == 'x':
                        scoremf -= factor3

            # Diagonals of Triplets
            
            if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == 'o'):
                ssmall_boards_status[z][x][y] = 'o'
                scoremf += factor
                # if self.count(ssmall_boards_status[z], x, y, 'x') * factor5 >= 500:
                    # print("Huan")
                    # time.sleep(10)
                scoremf += self.count(ssmall_boards_status[z], x, y, 'x') * factor5 

            if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == 'o'):
                ssmall_boards_status[z][x][y] = 'o'
                scoremf += factor
                # if self.count(ssmall_boards_status[z], x, y, 'x') * factor5 >= 500:
                    # print("Huan")
                    # time.sleep(10)
                scoremf += self.count(ssmall_boards_status[z], x, y, 'x') * factor5 


            if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == 'x'):
                ssmall_boards_status[z][x][y] = 'x'
                scoremf -= factor
                # if self.count(ssmall_boards_status[z], x, y, 'o') * factor5 >= 500:
                    # print("Huan")
                    # time.sleep(10)
                scoremf -= self.count(ssmall_boards_status[z], x, y, 'o') * factor5

            if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == 'x'):
                scoremf -= factor
                ssmall_boards_status[z][x][y] = 'x'
                # if self.count(ssmall_boards_status[z], x, y, 'o') * factor5 >= 500:
                    # print("Huan")
                    # time.sleep(10)
                scoremf -= self.count(ssmall_boards_status[z], x, y, 'o') * factor5


            # Diagonals
            # Top Left to Bottom Right
            
            # if(bs[3*x][3*y] == bs[3*x+1][3*y+1] and bs[3*x+2][3*y+2] == '-'):
            #     if (bs[3*x][3*y] == 'x'):
            #         scoremf -= (factor3-1)
            #     elif (bs[3*x][3*y] == 'o'):
            #         scoremf += (factor3-1)
            # if(bs[3*x][3*y] == bs[3*x+2][3*y+2] and bs[3*x+1][3*y+1] == '-'):
            #     if (bs[3*x][3*y] == 'x'):
            #         scoremf -= (factor3-1)
            #     elif (bs[3*x][3*y] == 'o'):
            #         scoremf += (factor3-1)
            # if(bs[3*x+2][3*y+2] == bs[3*x+1][3*y+1] and bs[3*x][3*y] == '-'):
            #     if (bs[3*x+1][3*y+1] == 'x'):
            #         scoremf -= (factor3-1)
            #     elif (bs[3*x+1][3*y+1] == 'o'):
            #         scoremf += (factor3-1)
            
            # # Top right to Bottom Left
            
            # if(bs[3*x+1][3*y+1] == bs[3*x][3*y+2] and bs[3*x+2][3*y] == '-'):
            #     if (bs[3*x+1][3*y+1] == 'x'):
            #         scoremf -= (factor3-1)
            #     elif (bs[3*x+1][3*y+1] == 'o'):
            #         scoremf += (factor3-1)
            # if(bs[3*x+1][3*y+1] == bs[3*x+2][3*y] and bs[3*x][3*y+2] == '-'):
            #     if (bs[3*x+1][3*y+1] == 'x'):
            #         scoremf -= (factor3-1)
            #     elif (bs[3*x+1][3*y+1] == 'o'):
            #         scoremf += (factor3-1)
            # if(bs[3*x][3*y+2] == bs[3*x+2][3*y] and bs[3*x+1][3*y+1] == '-'):
            #     if (bs[3*x][3*y+2] == 'x'):
            #         scoremf -= (factor3-1)
            #     elif (bs[3*x][3*y+2] == 'o'):
            #         scoremf += (factor3-1)
            # count_small(self,)
            if bs[mv[1]][mv[2]] == 'o':
                val = self.count_small(bs, mv[1], mv[2], 'x') * factor6
                # if val > 0:
                    # print("yeh karke aaya")
                    # time.sleep(2)
                scoremf += val

            elif bs[mv[1]][mv[2]] == 'x':
                val = self.count_small(bs, mv[1], mv[2], 'o') * factor6
                scoremf -= val
                # if val > 0:
                    # print("yeh karke aaya")
                    # time.sleep(2)

            bs[mv[1]][mv[2]] = '-'

            # Small Boards Region

            bs = ssmall_boards_status[z]
            for i in range(3):
            # Rows and columns triplets 
                if (bs[i][0] == bs[i][1] and bs[i][1] == bs[i][2]):
                    if (bs[i][0] == 'o'):
                        scoremf += factor2
                    elif (bs[i][0] == 'x'):
                        scoremf -= factor2
                if (bs[0][i] == bs[1][i] and bs[2][i] == bs[1][i]):
                    if (bs[0][i] == 'o'):
                        scoremf += factor2
                    elif (bs[0][i] == 'x'):
                        scoremf -= factor2


            # Rows and Columns duets

            # Rows
            # xx*
                if (bs[0][i] == bs[1][i] and bs[2][i] == '-'): 
                    if (bs[0][i] == 'x'):
                        scoremf -= factor4
                    elif (bs[0][i] == 'o'):
                        scoremf += factor4
            # *xx
                if (bs[2][i] == bs[1][i] and bs[0][i] == '-'):
                    if (bs[1][i] == 'x'):
                        scoremf -= factor4
                    elif (bs[1][i] == 'o'):
                        scoremf += factor4
            # x*x
                if (bs[0][i] == bs[2][i] and bs[1][i] == '-'):
                    if (bs[0][i] == 'x'):
                        scoremf -= factor4
                    elif (bs[0][i] == 'o'):
                        scoremf += factor4
            #  Columns
                if (bs[i][0] == bs[i][1] and bs[i][2] == '-'):
                    if (bs[i][0] == 'x'):
                        scoremf -= factor4
                    elif (bs[i][0] == 'o'):
                        scoremf += factor4
                if (bs[i][2] == bs[i][1] and bs[i][0] == '-'):
                    if (bs[i][1] == 'x'):
                        scoremf -= factor4
                    elif (bs[i][1] == 'o'):
                        scoremf += factor4
                if (bs[i][0] == bs[i][2] and bs[i][1] == '-'):
                    if (bs[i][0] == 'x'):
                        scoremf -= factor4
                    elif (bs[i][0] == 'o'):
                        scoremf += factor4



           # Diagonals of triplets

            if bs[0][0] == bs[1][1] and bs[1][1] == bs[2][2]:
                if bs[0][0] == 'x':
                    scoremf -= factor2
                elif bs[0][0] == 'o':
                    scoremf += factor2
            if bs[2][0] == bs[1][1] and bs[1][1] == bs[0][2]:
                if bs[1][1] == 'x':
                    scoremf -= factor2
                elif bs[1][1] == 'o':
                    scoremf += factor2 

            # Diagonals of duets

            # Top Left to Bottom Right
            # xx*
            if bs[0][0] == bs[1][1] and bs[2][2] == '-':
                if bs[0][0] == 'x':
                    scoremf -= factor4
                elif bs[0][0] == 'o':
                    scoremf += factor4
            # x*x
            if bs[0][0] == bs[2][2] and bs[1][1] == '-':
                if bs[0][0] == 'x':
                    scoremf -= factor4
                elif bs[0][0] == 'o':
                    scoremf += factor4
            # *xx
            if bs[2][2] == bs[1][1] and bs[0][0] == '-':
                if bs[1][1] == 'x':
                    scoremf -= factor4
                elif bs[1][1] == 'o':
                    scoremf += factor4

            # Bottom Left to Top Right
            if bs[2][0] == bs[1][1] and bs[0][2] == '-':
                if bs[1][1] == 'x':
                    scoremf -= factor4
                elif bs[1][1] == 'o':
                    scoremf += factor4
            if bs[0][2] == bs[1][1] and bs[2][0] == '-':
                if bs[1][1] == 'x':
                    scoremf -= factor4
                elif bs[1][1] == 'o':
                    scoremf += factor4
            if bs[2][0] == bs[0][2] and bs[1][1] == '-':
                if bs[2][0] == 'x':
                    scoremf -= factor4
                elif bs[2][0] == 'o':
                    scoremf += factor4


        poss_boards.reverse()
        return scoremf
        
        
    def move(self, board, old_move, flag):
       
        print 'Enter your move: <format:board row column> (you\'re playing with', flag + ")"    
        # if(flag == 'x')
        global f
        f = 0
        mvp = self.minimax(board,old_move,flag,3,0,[])
        # print(f)
        print(mvp)
        # time.sleep(7);
        # ch = raw_input();

        return (int(mvp[0]), int(mvp[1]), int(mvp[2]))

    def count(self, bs, x, y, ch):
        cnt = 0
        if x == 0:
            if y == 0:
                if bs[x][y+1] == ch and bs[x][y+2] == ch:
                    cnt+=1;
                if bs[x+1][y] == ch and bs[x+2][y] == ch:
                    cnt+=1
                if bs[x+1][y+1] == ch and bs[x+2][y+2] == ch:
                    cnt+=1
            if y == 1:
                if bs[x][y-1] == ch and bs[x][y+1] == ch:
                    cnt+=1
                if bs[x+1][y] == ch and bs[x+2][y] == ch:
                    cnt+=1
            if y == 2:
                if bs[x+1][y] == ch and bs[x+2][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch:
                    cnt+=1
                if bs[x+1][y-1] == ch and bs[x+2][y-2] == ch:
                    cnt+=1
        if x == 1:
            if y == 0:
                if bs[x-1][y] == ch and bs[x+1][y] == ch:
                    cnt+=1
                if bs[x][y+1] == ch and bs[x][y+2] == ch:
                    cnt+=1;
            if y == 1:
                if bs[x-1][y] == ch and bs[x+1][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y+1] == ch:
                    cnt+=1
                if bs[x-1][y+1] == ch and bs[x+1][y-1] == ch:
                    cnt+=1
                if bs[x+1][y+1] == ch and bs[x-1][y-1] == ch:
                    cnt+=1
            if y == 2:
                if bs[x-1][y] == ch and bs[x+1][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch:
                    cnt+=1
        if x == 2:
            if y == 0:
                if bs[x-1][y] == ch and bs[x-2][y] == ch:
                    cnt+=1
                if bs[x][y+1] == ch and bs[x][y+2] == ch:
                    cnt+=1
                if bs[x-1][y+1] == ch and bs[x-2][y+2] == ch:
                    cnt+=1
            if y == 1:
                if bs[x-1][y] == ch and bs[x-2][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y+1] == ch:
                    cnt+=1
            if y == 2:
                if bs[x-1][y] == ch and bs[x-2][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch:
                    cnt+=1
                if bs[x-1][y-1] == ch and bs[x-2][y-2] == ch:
                    cnt+=1
        return cnt

    def count_small(self, bs, x, y, ch):

        cnt = 0
        if x%3 == 0:
            if y%3 == 0:
                if bs[x][y+1] == ch and bs[x][y+2] == ch:
                    cnt+=1;
                if bs[x+1][y] == ch and bs[x+2][y] == ch:
                    cnt+=1
                if bs[x+1][y+1] == ch and bs[x+2][y+2] == ch:
                    cnt+=1
            if y%3 == 1:
                if bs[x][y-1] == ch and bs[x][y+1] == ch:
                    cnt+=1
                if bs[x+1][y] == ch and bs[x+2][y] == ch:
                    cnt+=1
            if y%3 == 2:
                if bs[x+1][y] == ch and bs[x+2][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch:
                    cnt+=1
                if bs[x+1][y-1] == ch and bs[x+2][y-2] == ch:
                    cnt+=1
        if x%3 == 1:
            if y%3 == 0:
                if bs[x-1][y] == ch and bs[x+1][y] == ch:
                    cnt+=1
                if bs[x][y+1] == ch and bs[x][y+2] == ch:
                    cnt+=1;
            if y%3 == 1:
                if bs[x-1][y] == ch and bs[x+1][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y+1] == ch:
                    cnt+=1
                if bs[x-1][y+1] == ch and bs[x+1][y-1] == ch:
                    cnt+=1
                if bs[x+1][y+1] == ch and bs[x-1][y-1] == ch:
                    cnt+=1
            if y%3 == 2:
                if bs[x-1][y] == ch and bs[x+1][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch:
                    cnt+=1
        if x%3 == 2:
            if y%3 == 0:
                if bs[x-1][y] == ch and bs[x-2][y] == ch:
                    cnt+=1
                if bs[x][y+1] == ch and bs[x][y+2] == ch:
                    cnt+=1
                if bs[x-1][y+1] == ch and bs[x-2][y+2] == ch:
                    cnt+=1
            if y%3 == 1:
                if bs[x-1][y] == ch and bs[x-2][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y+1] == ch:
                    cnt+=1
            if y%3 == 2:
                if bs[x-1][y] == ch and bs[x-2][y] == ch:
                    cnt+=1
                if bs[x][y-1] == ch and bs[x][y-2] == ch:
                    cnt+=1
                if bs[x-1][y-1] == ch and bs[x-2][y-2] == ch:
                    cnt+=1
        return cnt




