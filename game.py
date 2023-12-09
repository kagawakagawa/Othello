#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random 
import math

class State: 
    #最初に設定するやつ
    def __init__(self,pieces = None,enemy_pieces = None,depth = 0): 
        
        #次の行ける宝庫を示すからdxy
        self.dxy = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))

        #連続パスは負け
        self.pass_end = False

        #自分と相手の石のリスト
        self.pieces = pieces
        self.enemy_pieces = enemy_pieces
        self.depth = depth

        #初期配置
        if pieces == None or enemy_pieces == None:
            self.pieces = [0]*64
            self.pieces[27] = self.pieces[36] = 1
            self.enemy_pieces = [0]*64
            self.enemy_pieces[28] = self.enemy_pieces[35] = 1
            #真ん中四つは最初から石が置かれている
            #リストは一次元で最後に区切って表示する
            
    #石の数の取得
    def piece_count(self,pieces):
        count = 0
        for i in pieces:
            if i == 1:
                count += 1
        return count
    
#     #勝ちかどうか
#     def is_win(self):
#         if slef.piece_count(self.pieces) > self.piece_count(self.enemy_pieces):
#             print("oの勝ち")
#         return self.is_done() and self.piece_count(self.pieces) > self.piece_count(self.enemy_pieces) and print("oの勝ち")

    #負けかどうか
    def is_lose(self):
        return self.is_done() and self.piece_count(self.pieces) < self.piece_count(self.enemy_pieces) 

    #引き分けかどうか
    def is_draw(self):
        return self.is_done() and self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces) 
    
    #ゲーム終了かどうか
    def is_done(self):
        return self.piece_count(self.pieces)+self.piece_count(self.enemy_pieces) == 64 or self.pass_end
    
    # ゲームが半分進んでいないとき
    def is_half(self):
        return self.piece_count(self.pieces)+self.piece_count(self.enemy_pieces) < 32
    
    #ゲーム結果、どれだけ引き分けに近いか
    
     #引き分けかどうか
    def is_draw(self):
        return self.is_done() and self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces) 
     
    def is_draw2(self):
        return self.is_done() and self.piece_count(self.pieces) - self.piece_count(self.enemy_pieces) <= 3
     
    def is_draw3(self):
        return self.is_done() and self.piece_count(self.pieces) - self.piece_count(self.enemy_pieces) <= 5
     
    def is_draw4(self):
        return self.is_done() and self.piece_count(self.pieces) - self.piece_count(self.enemy_pieces) <= 10
     
    def is_draw5(self):
        return self.is_done() and self.piece_count(self.pieces) - self.piece_count(self.enemy_pieces) <= 15
    
    def is_draw6(self):
        return self.is_done() and self.piece_count(self.pieces) - self.piece_count(self.enemy_pieces) > 15
    

     #試合週終了後差を出す
    def gap(self):
        if self.is_done():
            gap = self.piece_count(self.pieces) - self.piece_count(self.enemy_pieces) 
        return gap
            
        
        
    
   
    

        

    #次の状態
    def next(self,action):
        state = State(self.pieces.copy(),self.enemy_pieces.copy(),self.depth+1)# 相手と自分を交代して相手のターンにする
        if action != 64:
            state.is_legal_action_xy(action%8,int(action/8),True)
        w = state.pieces
        state.pieces = state.enemy_pieces
        state.enemy_pieces = w
        
        #二回連続パス判定
        if action == 64 and state.legal_actions() == [64]:
            ##print("２連続パスにより強制終了")
            state.pass_end = True
        return state
    
    
    #合法手のリストの取得
    def legal_actions(self):
        actions = []
        for j in range(0,8):
            for i in range(0,8):
                if self.is_legal_action_xy(i,j):
                    actions.append(i+j*8)
        if len(actions) == 0:
            actions.append(64)
        return actions
    
    #任意のマスが合法手かどうか
    def is_legal_action_xy(self,x,y,flip=False):
        gaplist = []
        #任意のマスの任意の方向で敵の石を挟むことができるか
        #そのとき挟んだ石を自分のものにする
        def is_legal_action_xy_dxy(x,y,dx,dy):
            #一つ目　相手の石
            x,y = x+dx,y+dy
            
            if y<0 or 7<y or x<0 or 7<x or self.enemy_pieces[x+y*8]!=1:#x+y*8は自分の座標
                return False
            #二つ目以降
            for j in range(8):
                #空
                if y<0 or 7<y or x<0 or 7<x or (self.enemy_pieces[x+y*8] == 0 and self.pieces[x+y*8] == 0):
                    return False
            
                #自分の石
                if self.pieces[x+y*8] == 1:
                    #反転
                    if flip:
                        for i in range(8):
                            x,y = x-dx,y-dy
                            if self.pieces[x+y*8]  == 1:
                                #print(self.pieces.count(1))
                                return True
                            self.pieces[x+y*8]  =1
                            self.enemy_pieces[x+y*8] = 0
#                             print("1P",end="")
#                             print(self.pieces.count('1'))
#                             print("2P",end="")
#                             print(self.enemy_pieces.count('1'))
                    return True
                #相手の石
                x,y = x+dx,y+dy
            return False
    
        #空きなし
        if self.enemy_pieces[x+y*8] == 1 or self.pieces[x+y*8] ==1:
            return False
        
#         playlist = [[]]
#         enemy.playlist = [[]]  
    
        #石を置く
        if flip:
            self.pieces[x+y*8] = 1
            #座標の取得
#             print("座標(",end='')
#             print(x+1,end='')
#             print(",",end='')
#             print(y+1,end='')
#             print(")に打つ")
            gap = self.piece_count(self.pieces) - self.piece_count(self.enemy_pieces)
            gaplist.append(gap)
            #棋譜の保管　奇数は自分、偶数は相手
#             if 
#             playlist.append += playlist.append[x+1,y+1]
#             enemy.playlist += 
            
    
        #任意の位置が合法手かどうか
        flag = False 
        for dx,dy in self.dxy:
            if is_legal_action_xy_dxy(x,y,dx,dy):
                flag = True
        return flag 
    
    #先手かどうか
    def is_first_player(self):
        return self.depth%2 == 0
    
    
    
    
        
        #文字列表示
    def __str__(self):
        ox = ('o','x') if self.is_first_player() else ('x','o')
        attack = ("先攻","後攻")#oを使ったら先攻確定
        
        print()
        str = ''
        for i in range(64):
            if self.pieces[i] == 1:
                str += ox[0]
            elif self.enemy_pieces[i] == 1:
                str += ox[1]
            else:
                str += '_'
            if i%8 == 7:
                str += '\n'
        if self.piece_count(self.pieces)+self.piece_count(self.enemy_pieces) == 64 or self.pass_end:
            print(self.pieces.count(1),end="")
            print("対",end="")
            print(self.enemy_pieces.count(1))
            if self.pieces.count(1) > self.enemy_pieces.count(1):
                print("先攻よお前の勝ちだ")
            elif self.pieces.count(1) == self.pieces.count(0):
                print("引き分けー")
            else:
                print("後攻の勝ち！")
                ##これみたいな感じで差を作ってリストに格納していく
                
                
        
        return str
# if self.piece_count(self.pieces) > self.piece_count(self.enemy_pieces):
#                 print("oの勝ち")
#             elif self.piece_count(self.pieces) < self.piece_count(self.enemy_pieces):
#                 print("oの負け")
#             else:
#                 print("引き分け")


# In[2]:


#ランダムで行動選択
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0,len(legal_actions)-1)]

#動作確認
if __name__ == '__main__':
    #状態の生成
    state = State()
    
    #ゲーム終了までのループ
    while True:
        #ゲーム終了時
        if state.is_done():
            break
        
        #次の状態の取得
        state = state.next(random_action(state))
        
        #文字列表示
        #print(str("座標(")+x,y+str(") に石を置いたよ"))
        print(state)
        print()
        


# In[ ]:





# In[ ]:




