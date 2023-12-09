#!/usr/bin/env python
# coding: utf-8

# In[11]:


import math
import random
from game import State


# In[20]:


# プレイアウト 今の局面からゲーム終了まで戦うシミュレーションするやつ
def draw_playout(state):
    if state.is_draw():
         return 1
    if state.is_draw2():
         return 0.9
    if state.is_draw3():
         return 0.8
    if state.is_draw4():
         return 0.3
    if state.is_draw5():
         return 0.1
    if state.is_draw6():
         return 0
    

  # 次の状態の状態価値
    return draw_playout(state.next(random_action(state)))


# In[21]:


# モンテカルロ木探索で手を選ぶ
# 手の選び方、毎回選ぶときに引き分けを狙いに行く、ちょっとだけ勝ちも狙った方が引き分けしやすい？？
def draw_mcts_action(state):
    
  # モンテカルロ木探索
    class Node:
        
        # 初期化
        def __init__(self,state):
            self.state = state # 状態
            self.w = 0 # 累計価値
            self.n = 0 # 試行回数
            self.child_nodes = None # 子ノード群　ｂ

        def evaluate(self):
            # ゲーム終了
            if self.state.is_done():
                # 勝敗結果で価値を取得、引き分けに近いほど価値が高い、これにより作られる木が引き分けを狙う木になる、はず、、、
                
                if state.is_draw():
                    value = 1
                if state.is_draw2():
                    value = 0.7
                if state.is_draw3():
                    value = 0.5
                if state.is_draw4():
                    value = 0.3
                if state.is_draw5():
                    value = 0.1
                else:
                    value = 0
#                 if state.is_draw6():
                    
#                     value = 0
                #value = -1 if self.state.is_lose() else 1 # 負けは -1、引き分けは 0

            # 累計価値を試行回数の更新
                self.w += value
                self.n += 1
                return value
          #子ノードが存在しないとき
            if not self.child_nodes:
                value = draw_playout(self.state)

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
                value = self.next_child_node().evaluate()
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
                ucb1_values.append(child_node.w/child_node.n+(2*math.log(t)/child_node.n)**0.5)

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


# In[22]:


#ランダムに手を打つやつ
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0,len(legal_actions)-1)]


# In[23]:


# # 最大値のインデックスを返す
def argmax(collection,key=None):
    return collection.index(max(collection))


# # In[16]:


# # def selct0(collection,key=None):
    
# #     return collection.index()


# # In[17]:


# # 動作確認
# #mcts VS ランダム
# EP_GAME_COUNT = 10

#    # 1評価当たりのゲーム数

# # 先手プレイヤーのポイント
# def first_player_point(ended_state):
#   # 1:先手勝利、0:先手敗北、0.5:引き分け
#     if ended_state.is_lose():
#         return 0 if ended_state.is_first_player() else 1
#     return 0.5

# # 1ゲームの実行
# def play(next_actions):
#   # 状態の生成
#     state = State()

#   # ゲーム終了までループ
#     while True:
#     # ゲーム終了時
#         if state.is_done():
#             break

#     # 行動の取得
#         next_action = next_actions[0] if state.is_first_player() else next_actions[1]
#         action = next_action(state)

#     # 次の状態の取得
#         state = state.next(action)

#   # 先手プレイヤーのポイントを返す
#     return 

# # 任意のアルゴリズムの評価
# def evaluate_algorithm_of(label,next_actions):
    
#   # 複数回の対戦を繰り返す
#     total_point = 0
#     for i in range(EP_GAME_COUNT):
        
#     # 1ゲームの実行
#         if i%2 == 0:
            
#             total_point += play(next_actions)
#         else:
#             total_point += 1 - play(list(reversed(next_actions)))
    
#     # 出力
#         print('\nEvaluate {}/{}'.format(i+1,EP_GAME_COUNT),end='')
#     print()

#   # 平均ポイントの計算
#     average_point = total_point/EP_GAME_COUNT
#     print(label.format(average_point))


# # In[18]:


# #VSランダム
# next_actions = (random_action,random_action)
# evaluate_algorithm_of('VS_Random {:.3f}',next_actions)
# # print(state)
# # print()


# # In[25]:


# # program VS program
# #動作確認
# if __name__ == '__main__':
#     #状態の生成
#     state = State()
    
#     #ゲーム終了までのループ
#     while True:
#         #ゲーム終了時
#         if state.is_done():
#             break 
        
#         #先行後攻で交互に使うプログラムを入れ替える
#         next_actions = (random_action,draw_mcts_action)
#         next_action = next_actions[0] if state.is_first_player() else next_actions[1]
        
#         action = next_action(state)
        
#         #次の状態の取得
#         state = state.next(action)
        
#         #文字列表示
#         #print(str("座標(")+x,y+str(") に石を置いたよ"))
#         print(state)
#         print()  


# In[ ]:




