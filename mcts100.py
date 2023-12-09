#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import random
from game import State

def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0,len(legal_actions)-1)]
# In[2]:


# プレイアウト 今の局面からゲーム終了まで戦うシミュレーションするやつ
def playout(state):
    # 負けは状態価値 -1
    if state.is_lose():
        return -1
  
  # 引き分けは状態価値 0
    if state.is_draw():
        return 0

  # 次の状態の状態価値
    return -playout(state.next(random_action(state)))


# In[3]:


# モンテカルロ木探索で手を選ぶ
def mcts100_action(state):
    
  # モンテカルロ木探索
    class Node:
        
        # 初期化
        def __init__(self,state):
            self.state = state # 状態
            self.w = 0 # 累計価値
            self.n = 0 # 試行回数
            self.child_nodes = None # 子ノード群

        def evaluate(self):
            # ゲーム終了
            if self.state.is_done():
                # 勝敗結果で価値を取得
                value = -1 if self.state.is_lose() else 0 # 負けは -1、引き分けは 0

            # 累計価値を試行回数の更新
                self.w += value
                self.n += 1
                return value
          #子ノードが存在しないとき
            if not self.child_nodes:
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
                ucb1_values.append(-child_node.w/child_node.n+(2*math.log(t)/child_node.n)**0.5)

          # UCB1が最大の子ノードを返す
            return self.child_nodes[argmax(ucb1_values)]


        # 現在の局面のノードの作成
    root_node = Node(state)
    root_node.expand()

      # 100回のシミュレーションを実行　この数によって強さが変動する
    for _ in range(100):
        root_node.evaluate()

      # 試行回数の最大値を持つ行動を返す
    legal_actions = state.legal_actions()
    n_list = []
    for c in root_node.child_nodes:
        n_list.append(c.n)
    return legal_actions[argmax(n_list)]


# In[4]:


def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0,len(legal_actions)-1)]


# In[5]:


# 最大値のインデックスを返す
def argmax(collection,key=None):
    return collection.index(max(collection))



# 最大値のインデックスを返す
def argmax(collection,key=None):
    return collection.index(max(collection))


