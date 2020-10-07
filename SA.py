
# coding: utf-8

# In[1]:


import sys
import time
import math
import random
import itertools
import pandas as pd
import statistics


# <img src = 'https://www.researchgate.net/profile/Ellips_Masehian/publication/257549155/figure/fig3/AS:667780986728453@1536222802314/General-template-of-the-SA-algorithm.png' >
# <img src = 'https://image.slidesharecdn.com/simulatedannealing-130723035358-phpapp01/95/simulated-annealing-18-638.jpg?cb=1374552539'>
# ## 建立讀檔用 Function

# In[2]:


def readfile(dic):
    with open('C:/Users/qscf6/Desktop/eil51.tsp') as f:
        r = f.read()
        read_line = r.split('\n')               
        for i in range(len(read_line)):         
            read_element = read_line[i].split()
            dic[int(read_element[0])] = [int(read_element[1])]
            dic[int(read_element[0])].append(int(read_element[2]))
        f.close()


# ## 宣告所需 Function

# In[3]:


#產生隨機順序的初始 sequence
def initial_sequence(num):
    seq = [n for n in range(1,num + 1)]
    random.shuffle(seq)
    
    return seq

#依照搜尋半徑,隨機產生 swap case
#Main idea:利用 shuffle 達到隨機與省略"重複判斷"
def random_swap_case(domain,neighbors_size,number_of_case):
    case = []
    #產生 1~domain 的 list
    temp = [n for n in range(1,domain+1)]
    
    for i in range(number_of_case):
        random.shuffle(temp)
        case.append([temp[j] for j in range(neighbors_size)])
   
    return case

#依照 Case 取得原 sequence 內 Index
def get_position(seq,case):
    position = []
    
    for i in range(len(case)):
        position.append(seq.index(case[i]))
        
    return position

#依照該次的 case 交換
def swap_by_case(seq,case,position):
    temp = seq[:]
    
    for i in range(len(case)):
        temp[position[i]] = case[i]
        
    return temp

#因是Symmetic，所以先把各城鎮距離算出來，省下每次重新計算的時間
def calculate_distance_table(dic):
    dx = 0
    dy = 0
    distance_table = []
    for i in range(1,len(dic) + 1):
        temp = [0] * 51
        for j in range(i,len(dic) + 1):
            dx = dic[i][0] - dic[j][0]
            dy = dic[i][1] - dic[j][1]
            temp[j - 1] = math.sqrt(dx**2 + dy**2)
            
        distance_table.append(temp)
        
    return distance_table
            

#計算該 seqence 總路徑長(利用查表)
def sequence_total_distance(seq,distance_table):
    dist = 0
    index1 = 0
    index2 = 0
    for i in range(len(seq)):
        if seq[i] > seq[(i + 1) % len(seq)]:
            index1 = seq[(i + 1) % len(seq)] - 1
            index2 = seq[i] - 1
        else:
            index1 = seq[i] - 1
            index2 = seq[(i + 1) % len(seq)] - 1
        
        dist += distance_table[index1][index2]
        #dist += distance_table[seq[i] - 1][seq[(i + 1) % len(seq)] - 1]
        
    return dist

# def determine_for_HC():
    
def determine_for_SA(neighbors,current_sequence,shortest_sequence,current_temperature,distance_table):
    index = random.randint(0,len(neighbors) - 1)
    position = get_position(current_sequence,neighbors[index])
    random.shuffle(neighbors[index])
    temp = swap_by_case(current_sequence,neighbors[index],position)
    
    value = sequence_total_distance(temp,distance_table) - sequence_total_distance(current_sequence,distance_table)
    
    if value <= 0:
        current_sequence = temp
        shortest_sequence = current_sequence[:]
        
    else:
        r = random.random()
        if math.exp((-10) * value / current_temperature) >= r:
            current_sequence = temp
    
    return current_sequence,shortest_sequence

#判斷誰大誰小
def determine(temp,min_seq,distance_table):
    global flag
    if sequence_total_distance(temp,distance_table) < sequence_total_distance(min_seq,distance_table):
        min_seq = temp[:]
        flag = True
#         print(min_seq, evalu(min_seq,dic))
  
#     return min_seq,sequence_total_distance(min_seq,distance_table)
    return min_seq

def determine2(temp,min_seq,distance_table):
    if sequence_total_distance(temp,distance_table) < sequence_total_distance(min_seq,distance_table):
        min_seq = temp[:]
#         print(min_seq, evalu(min_seq,dic))
  
#     return min_seq,sequence_total_distance(min_seq,distance_table)
    return min_seq


# # Simulated Annealin
# ## 變形:可抽 n 個 Node(n<= City數)

# In[4]:


def Simulated_Annealing(number_of_iteration,start_temperature,end_temperature,size_of_neighbor,decrease_ratio,distance_table):    
    result = []
    
    for current_iteration in range(number_of_iteration):
        current_sequence = initial_sequence(51)
        neighbors = []
        
        current_temperature = start_temperature
        
        shortest_sequence = []
        
        count = 0
        
        while current_temperature > end_temperature:
            best_value = sequence_total_distance(shortest_sequence,distance_table)
            neighbors = random_swap_case(len(distance_table),size_of_neighbor,10)
            
            current_sequence,shortest_sequence = determine_for_SA(neighbors,current_sequence,shortest_sequence,current_temperature,distance_table)
            
            if sequence_total_distance(current_sequence,distance_table) >= best_value:
                count += 1
            
            else:
                count = 0
                
            if count == 10:
                current_temperature *= decrease_ratio
                count = 0
                
        result.append(sequence_total_distance(current_sequence,distance_table))
                
    return result       


# In[5]:


random_swap_case(51,3,2)


# In[6]:


dic = {}
readfile(dic)

distance_table = []
distance_table = calculate_distance_table(dic)

test = Simulated_Annealing(100,100,10,3,0.99,distance_table)


# In[7]:


test_average = statistics.mean(test)
test_stdev = statistics.stdev(test)


# In[8]:


import numpy as np
import scipy.stats as stats


# In[10]:


testDis = stats.norm(test_average,test_stdev)
pd.Series(test).plot(kind = 'kde')

