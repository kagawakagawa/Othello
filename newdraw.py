#!/usr/bin/env python
# coding: utf-8

# In[7]:


import math
import random
from game import State


# In[8]:


from mcts100 import mcts100_action 
from game import random_action


# In[9]:


# プレイアウト 今の局面からゲーム終了まで戦うシミュレーションするやつ
def draw_playout(state):
    if state.is_draw():
         return 1
    if state.is_draw2():
         return 0.9
    if state.is_draw3():
         return 0.7
    if state.is_draw4():
         return 0.5
    if state.is_draw5():
         return 0.3
    if state.is_draw6():
         return 0
    

  # 次の状態の状態価値
    return draw_playout(state.next(random_action(state)))

def playout(state):
    if state.is_lose() :
        return -1
    if state.is_draw():
        return 0
        # 負けは -1、引き分けは 0
    return -playout(state.next(random_action(state)))


# In[10]:


# モンテカルロ木探索で手を選ぶ
# 手の選び方、毎回選ぶときに引き分けを狙いに行く、ちょっとだけ勝ちも狙った方が引き分けしやすい？？
def draw_mcts_newaction(state):
    
  # モンテカルロ木探索
    class Node:
        
        # 初期化
        def __init__(self,state):
            self.state = state # 状態
            self.draw_w = 0 #提案累計価値#累計価値のみ変更、試行回数はそのままにしておこう
            self.w = 0 # 累計価値
            self.n = 0 # 試行回数
            self.child_nodes = None # 子ノード群

        def evaluate(self):
            
            # ゲーム終了
            if self.state.is_done():
                if state.is_first_player():
                    
                    # 勝敗結果で価値を取得、引き分けに近いほど価値が高い、
                    # これにより作られる木が引き分けを狙う木になる、はず、、、

#                     if state.is_draw():
#                         value = 1
                    if state.is_draw2():
                        value = 0.9
                    if state.is_draw3():
                        value = 0.7
                    if state.is_draw4():
                        value = 0.5
                    if state.is_draw5():
                        value = 0.3
                    else:
                        value = 0
                    
                    self.draw_w += value
                # 後攻は普通に勝ったらポイントゲットとなる
                else:
                    # 勝敗結果で価値を取得
                    value = -1 if self.state.is_lose() else 0 # 負けは -1、引き分けは 0

            # 累計価値を試行回数の更新
                    self.w += value
                self.n += 1
                return value
          #子ノードが存在しないとき
            if not self.child_nodes:
                if state.is_first_player():
                    value = draw_playout(self.state)
                    self.draw_w += value
                else:
                    value = playout(self.state)

            # 累計価値と試行回数の更新
                    self.w += value
                self.n += 1

                # 子ノードの展開
                if self.n == 10:

                    self.expand()
                return value

          # 子ノードが存在するとき
            else:
                # UCB1が最大の子ノードの評価で価値を取得
                if state.is_first_player():  
                    value = self.next_child_node().evaluate()
                    self.draw_w += value
                else:
                    value = -self.next_child_node().evaluate()
                    self.w += value
                self.n += 1
                return value
            
        # 子ノードの展開
        def expand(self):
            legal_actions = self.state.legal_actions()
            self.child_nodes = []
            for action in legal_actions:
                self.child_nodes.append(Node(self.state.next(action)))

        # UCB1が最大の子ノードの取得
        # ここでの最大値を持つノードが次の手に選ばれる、今回はそうではなく引き分けを狙えそうな
        # 物を選ぶためargmaxにはならない
        # どうにかしてここが平均くらいの手を選ぶようにして展開するノードが引き分けを狙えるノードにしたい
        
        def next_child_node(self):
            for child_node in self.child_nodes:
                if child_node.n == 0:
                    return child_node

          # UCB1の計算
            t = 0
            for c in self.child_nodes:
                t += c.n
            ucb1_values = []
            for child_node in self.child_nodes:
                
                if state.is_first_player():
                    ucb1_values.append(child_node.draw_w/child_node.n+(2*math.log(t)/child_node.n)**0.5)
                else:
                    ucb1_values.append(-child_node.w/child_node.n+(2*math.log(t)/child_node.n)**0.5)

          # UCB1が最大の子ノードを返す
            return self.child_nodes[argmax(ucb1_values)] 
        
          # そうではなく最も0に近いノードを選べばいいのではないだろうか
            #return self.child_nodes[select0(ucb1_values)]


        # 現在の局面のノードの作成
    root_node = Node(state)
    root_node.expand()

      # n回のシミュレーションを実行　この数によって強さが変動する
    for _ in range(1000):
        root_node.evaluate()

      # 試行回数の最大値を持つ行動を返す
    legal_actions = state.legal_actions()
    n_list = []
    for c in root_node.child_nodes:
        n_list.append(c.n)
    return legal_actions[argmax(n_list)]
#########うまくいかなかったら返り値とかの符号を全部変えよう


# In[15]:


#ランダムに手を打つやつ
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0,len(legal_actions)-1)]

# 最大値のインデックスを返す
def argmax(collection,key=None):
    return collection.index(max(collection))


import matplotlib.pyplot as plt
import random 
import numpy as np


# tatakaimasu


# パラメータ
EP_GAME_COUNT = 100  # 1評価当たりのゲーム数

# 先手プレイヤーのポイント
def first_player_point(ended_state):
  # 1:先手勝利、0:先手敗北または引分け
    if ended_state.is_lose():
        return 0 if ended_state.is_first_player() else 1
    return 0

# 1ゲームの実行
def play(next_actions):
  # 状態の生成
    state = State()

  # ゲーム終了までループ
    while True:
    # ゲーム終了時
        if state.is_done():
            break

    # 行動の取得
        next_action = next_actions[0] if state.is_first_player() else next_actions[1]
        action = next_action(state)

    # 次の状態の取得
        state = state.next(action)

  # 先手プレイヤーのポイントを返す
    return first_player_point(state)#数字はそのまま勝った回数となっている

# 任意のアルゴリズムの評価
def evaluate_algorithm_of(label,next_actions):
  # 複数回の対戦を繰り返す
    total_point = 0
    wp_list = []
    for i in range(EP_GAME_COUNT):
    # 1ゲームの実行
    # 先攻後攻毎回プログラムを切り替える
    # 
        if i%2 == 0:
            total_point += play(next_actions)
            # 現時点での勝率の計算
            now_average_point = total_point/(i+1)
            # 配列には毎回現時点での勝率を追加する
            wp_list.append(now_average_point*100)
            # 先攻が負けた場合相手が勝ったということで１－１で０点が加算される
        else:
            total_point += 1-play(list(reversed(next_actions)))
            now_average_point = total_point/(i+1)
            wp_list.append(now_average_point*100)
# reversed はリストを逆にするやつ、先攻後攻入れ替えたってこと
    
    # 出力、グラフの表示
    # 最後まで毎回計算し最後にグラフの出力
        print('\nEvaluate {}/{}'.format(i+1,EP_GAME_COUNT),end='')
#         print(self.pieces.count(1),end="")
#         print("対",end="")
#         print(self.enemy_pieces.count(1))
    print('')

  # 平均ポイントの計算
    average_point = total_point/EP_GAME_COUNT
    print(label.format(average_point))
    x = list(range(1,1+EP_GAME_COUNT))
    y = wp_list
    plt.title('result')
    plt.xlabel('winning parcentage')
    plt.ylabel('times')
    plt.plot(x,y,color = "red",marker = "",label = "changes")
    plt.legend()
    plt.show


# In[16]:



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




