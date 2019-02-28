import copy
import time

class Team16:
    def __init__(self):
        pass

    def minimax(self,board,old_old_move,old_move,flag,depth):
        if flag == 'o':
           best = [-1,-1,-1, -1000]
        else:
           best = [-1,-1,-1, +1000]

        if depth == 0:      
            value = self.calculate_heuristic(board,flag,old_move,old_old_move);
            return [-1 , -1 , -1, value];

        cells = board.find_valid_move_cells(old_move)
        
        for cell in cells:
            x, y, z = cell[0],cell[1],cell[2]
           
            board.big_boards_status[x][y][z] = flag
            
            if flag == 'x':
                bmove = self.minimax(board,old_move,[x,y,z],'o',depth-1)
            if flag == 'o':
                bmove = self.minimax(board,old_move,[x,y,z],'x',depth-1)

            # if(y%3 == 1 and z%3 == 1):
            #     if flag == 'x':
            #         bmove[3] -= 1
            #     else:
            #         bmove[3] += 1
            board.big_boards_status[x][y][z] = '-'
            bmove[0],bmove[1],bmove[2] = x,y,z;
            
            if flag == 'o':
                if bmove[3] >= best[3]:
                    best = bmove  # max value        
            else:
                if bmove[3] < best[3]:
                    best = bmove  # min value

        
        return best

    def calculate_heuristic(self,bs,ch,old_move,old_old_move):
        
        if ch == 'x':
            op_ch = 'o'
        if ch == 'o':
            op_ch = 'x'

        bs2 = bs
        scoremf = 0
        ssmall_boards_status = copy.deepcopy(bs2.small_boards_status)


        x = old_move[1]/3
        y = old_move[2]/3
        for k in range(2):
            bs = bs2.big_boards_status[k]
            cntx = 0
            cnto = 0
            for i in range(3):
                    #checking for horizontal pattern(i'th row)
                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == 'o'):
                    ssmall_boards_status[k][x][y] = 'o'
                    scoremf+=10
                #checking for vertical pattern(i'th column)
                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == 'o'):
                    ssmall_boards_status[k][x][y] = 'o'
                    scoremf+=10
                if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == 'o'):
                    ssmall_boards_status[k][x][y] = 'o'
                    scoremf+=10
                if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == 'o'):
                    ssmall_boards_status[k][x][y] = 'o'
                    scoremf+=10
                

                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] and bs[3*x+i][3*y+2]=='-'):
                    if bs[3*x+i][3*y] == 'o':
                        cnto+=1
                    elif bs[3*x+i][3*y] =='x':
                        cntx+=1
                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+2] and bs[3*x+i][3*y+1]=='-'):
                    if bs[3*x+i][3*y] == 'o':
                        cnto+=1
                    elif bs[3*x+i][3*y] =='x':
                        cntx+=1
                if (bs[3*x+i][3*y+2] == bs[3*x+i][3*y+1] and bs[3*x+i][3*y]=='-'):
                    if bs[3*x+i][3*y+1] == 'o':
                        cnto+=1
                    elif bs[3*x+i][3*y+1] =='x':
                        cntx+=1


                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == 'x'):
                    scoremf-=10
                    ssmall_boards_status[k][x][y] = 'x'
                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == 'x'):
                    scoremf-=10
                    ssmall_boards_status[k][x][y] = 'x'
                if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == 'x'):
                    scoremf-=10
                    ssmall_boards_status[k][x][y] = 'x'
                if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == 'x'):
                    scoremf-=10
                    ssmall_boards_status[k][x][y] = 'x'

                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] and bs[3*x+2][3*y+i] == '-'):
                    if bs[3*x][3*y+i] == 'o':
                        cnto+=1
                    elif bs[3*x][3*y+i] == 'x':
                        cntx+=1
                if (bs[3*x][3*y+i] == bs[3*x+2][3*y+i] and bs[3*x+1][3*y+i] == '-'):
                    if bs[3*x][3*y+i] == 'o':
                        cnto+=1
                    elif bs[3*x][3*y+i] == 'x':
                        cntx+=1
                if (bs[3*x+2][3*y+i] == bs[3*x+1][3*y+i] and bs[3*x][3*y+i] == '-'):
                    if bs[3*x+1][3*y+i] == 'o':
                        cnto+=1
                    elif bs[3*x+1][3*y+i] == 'x':
                        cntx+=1
            scoremf += (cnto-cntx) * 5


        x = old_old_move[1]/3
        y = old_old_move[2]/3
        for k in range(2):
            bs = bs2.big_boards_status[k]
            for i in range(3):
                    #checking for horizontal pattern(i'th row)
                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == 'o'):
                    ssmall_boards_status[k][x][y] = 'o'
                    scoremf+=10
                #checking for vertical pattern(i'th column)
                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == 'o'):
                    ssmall_boards_status[k][x][y] = 'o'
                    scoremf+=10
                if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == 'o'):
                    ssmall_boards_status[k][x][y] = 'o'
                    scoremf+=10
                if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == 'o'):
                    ssmall_boards_status[k][x][y] = 'o'
                    scoremf+=10

                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] and bs[3*x+i][3*y+2]=='-'):
                    if bs[3*x+i][3*y] == 'o':
                        cnto+=1
                    elif bs[3*x+i][3*y] =='x':
                        cntx+=1
                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+2] and bs[3*x+i][3*y+1]=='-'):
                    if bs[3*x+i][3*y] == 'o':
                        cnto+=1
                    elif bs[3*x+i][3*y] =='x':
                        cntx+=1
                if (bs[3*x+i][3*y+2] == bs[3*x+i][3*y+1] and bs[3*x+i][3*y]=='-'):
                    if bs[3*x+i][3*y+1] == 'o':
                        cnto+=1
                    elif bs[3*x+i][3*y+1] =='x':
                        cntx+=1


                if (bs[3*x+i][3*y] == bs[3*x+i][3*y+1] == bs[3*x+i][3*y+2]) and (bs[3*x+i][3*y] == 'x'):
                    scoremf-=10
                    ssmall_boards_status[k][x][y] = 'x'
                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] == bs[3*x+2][3*y+i]) and (bs[3*x][3*y+i] == 'x'):
                    scoremf-=10
                    ssmall_boards_status[k][x][y] = 'x'
                if (bs[3*x][3*y] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y+2]) and (bs[3*x][3*y] == 'x'):
                    scoremf-=10
                    ssmall_boards_status[k][x][y] = 'x'
                if (bs[3*x][3*y+2] == bs[3*x+1][3*y+1] == bs[3*x+2][3*y]) and (bs[3*x][3*y+2] == 'x'):
                    scoremf-=10
                    ssmall_boards_status[k][x][y] = 'x'

                if (bs[3*x][3*y+i] == bs[3*x+1][3*y+i] and bs[3*x+2][3*y+i] == '-'):
                    if bs[3*x][3*y+i] == 'o':
                        cnto+=1
                    elif bs[3*x][3*y+i] == 'x':
                        cntx+=1
                if (bs[3*x][3*y+i] == bs[3*x+2][3*y+i] and bs[3*x+1][3*y+i] == '-'):
                    if bs[3*x][3*y+i] == 'o':
                        cnto+=1
                    elif bs[3*x][3*y+i] == 'x':
                        cntx+=1
                if (bs[3*x+2][3*y+i] == bs[3*x+1][3*y+i] and bs[3*x][3*y+i] == '-'):
                    if bs[3*x+1][3*y+i] == 'o':
                        cnto+=1
                    elif bs[3*x+1][3*y+i] == 'x':
                        cntx+=1
            scoremf += (cnto-cntx) * 5

        
        for k in range(2):
            bs = ssmall_boards_status[k]
            for i in range(3):
                if (bs[i][0] == bs[i][1] and bs[i][1] == bs[i][2]):
                    if (bs[i][0] == 'o'):
                        scoremf += 100
                    elif (bs[i][0] == 'x'):
                        scoremf -= 100
                if (bs[0][i] == bs[1][i] and bs[2][i] == bs[1][i]):
                    if (bs[0][i] == 'o'):
                        scoremf += 100
                    elif (bs[0][i] == 'x'):
                        scoremf -= 100
            if bs[0][0] == bs[1][1] and bs[1][1] == bs[2][2]:
                if bs[0][0] == 'x':
                    scoremf -= 100
                elif bs[0][0] == 'o':
                    scoremf += 100
            if bs[2][0] == bs[1][1] and bs[1][1] == bs[0][2]:
                if bs[1][1] == 'x':
                    scoremf -= 100
                elif bs[1][1] == 'o':
                    scoremf += 100  

        return scoremf
        
        # f_ans = 0;
        # for k in range(0,2):
        #     ans=0
        #     for h in range(0,3):
        #         mdh = (h+1)*3;
        #         mdh_ = h*3;
        #         for v in range(0,3):
        #             mdv = (v+1)*3;
        #             mdv_ = v*3;
        #             can_win = 0
        #             can_lose = 0
        #             if h == 1 and v == 1:
        #                 score = 3
        #             elif (h+v)%2 == 0:
        #                 score = 4
        #             else:
        #                 score = 6   
        #             for i in range(0,3):
        #                 for j in range(0,3):
        #                     if (v*3+j+1)%mdv == 0:
        #                         rr = mdv_
        #                     else:
        #                         rr = v*3+j+1
        #                     if (h*3+j+1)%mdh == 0:
        #                         rh = mdh_
        #                     else:
        #                         rh = h*3+j+1
        #                     if game_board.big_boards_status[k][h*3+i][v*3+j] == ch and game_board.big_boards_status[k][h*3+i][rr] == ch:
        #                         can_win = 1
        #                     if game_board.big_boards_status[k][h*3+i][v*3+j] == op_ch and game_board.big_boards_status[k][h*3+i][rr] == op_ch:
        #                         can_lose = 1
        #                     if game_board.big_boards_status[k][h*3+j][v*3+i] == ch and game_board.big_boards_status[k][rh][v*3+i] == ch:
        #                         can_win = 1
        #                     if game_board.big_boards_status[k][h*3+j][v*3+i] == op_ch and game_board.big_boards_status[k][rh][v*3+i] == op_ch:
        #                         can_lose = 1
                    
        #             # Diagonals
                    
        #             if game_board.big_boards_status[k][h*3][v*3] == ch and game_board.big_boards_status[k][h*3+1][v*3+1] == ch:
        #                 can_win = 1
        #             if game_board.big_boards_status[k][h*3+1][v*3+1] == ch and game_board.big_boards_status[k][h*3+2][v*3+2] == ch:
        #                 can_win = 1
        #             if game_board.big_boards_status[k][h*3+2][v*3+2] == ch and game_board.big_boards_status[k][h*3][v*3] == ch:
        #                 can_win = 1
        #             if game_board.big_boards_status[k][h*3][v*3] == op_ch and game_board.big_boards_status[k][h*3+1][v*3+1] == op_ch:
        #                 can_lose = 1
        #             if game_board.big_boards_status[k][h*3+1][v*3+1] == op_ch and game_board.big_boards_status[k][h*3+2][v*3+2] == op_ch:
        #                 can_lose = 1
        #             if game_board.big_boards_status[k][h*3+2][v*3+2] == op_ch and game_board.big_boards_status[k][h*3][v*3] == op_ch:
        #                 can_lose = 1
        #             if game_board.big_boards_status[k][h*3][v*3+2] == ch and game_board.big_boards_status[k][h*3+1][v*3+1] == ch:
        #                 can_win = 1
        #             if game_board.big_boards_status[k][h*3+1][v*3+1] == ch and game_board.big_boards_status[k][h*3+2][v*3] == ch:
        #                 can_win = 1
        #             if game_board.big_boards_status[k][h*3+2][v*3] == ch and game_board.big_boards_status[k][h*3][v*3+2] == ch:
        #                 can_win = 1
        #             if game_board.big_boards_status[k][h*3][v*3+2] == op_ch and game_board.big_boards_status[k][h*3+1][v*3+1] == op_ch:
        #                 can_lose = 1
        #             if game_board.big_boards_status[k][h*3+1][v*3+1] == op_ch and game_board.big_boards_status[k][h*3+2][v*3] == op_ch:
        #                 can_lose = 1
        #             if game_board.big_boards_status[k][h*3+2][v*3] == op_ch and game_board.big_boards_status[k][h*3][v*3+2] == op_ch:
        #                 can_lose = 1

        #             if can_win == 1 and can_lose == 1:
        #                 ans += 0;
        #             elif can_lose == 1:
        #                 ans -= score
        #             elif can_win == 1:
        #                 ans += score
        #             else:
        #                 pass
        #     f_ans += ans
        # if f_ans != 0:
        # game_board.print_board()
       
        # return f_ans


    def move(self, board, old_move, flag):
       
        print 'Enter your move: <format:board row column> (you\'re playing with', flag + ")"    
        # if(flag == 'x')
        mvp = self.minimax(board,old_move,old_move,flag,2)
        print(mvp)
        time.sleep(7);
        
        return (int(mvp[0]), int(mvp[1]), int(mvp[2]))
