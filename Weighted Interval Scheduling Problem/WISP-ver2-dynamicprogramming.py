from tracemalloc import start
import numpy as np
import math

###################################################################### Improvement1: package the interval as a class 
class Interval(object):
    #initialization
    def __init__(self, interv_number, interv_start, interv_finish, interv_weight):
        self.number = interv_number
        self.start = interv_start
        self.finish = interv_finish 
        self.weight = interv_weight

    #print the information
    def print_info(self):
        print("-------------")
        print("Interval No:", self.number, "\nInterval Time:", self.start, '-', self.finish, "\nInterval weight:", self.weight)
        print("-------------")

    #expose the interfaces 
    def get_para(self, option):
        if option == 1:
            return self.number
        elif option == 2:
            return self.start
        elif option == 3:
            return self.finish
        elif option == 4:
            return self.weight
        else:
            print("Invalid parameters!")
            return 0

#create a list of multiple intervals
def create_interval_list(interv_number, interv_start, interv_finish, interv_weight):
    list = []
    for i in range(interv_number):
        list.append(Interval(i+1, interv_start[i], interv_finish[i], interv_weight[i]))
    return list 

###################################################################### Improvement2: apply a binary search instead of brute search to reduce the complexity from O(n^2) to O(nlogn)
# interv_p:compute the expected index of the former compatible one for each interval with binary search, set as -1 if does not exist
def compute_compatible_interval(list):
    num = len(list)
    for i in range(num):
        max_index = num-1
        min_index = 0
        while(1):
            index = math.floor((max_index+min_index)/2) 
            if list[index].get_para(3) <= list[i].get_para(2):
                min_index = index
                if max_index-min_index == 1: 
                    interv_p[i] = min_index
                    break # find a compatible result
            else:
                max_index = index 
                if max_index == min_index: 
                    break # can not find a compatible result
    return interv_p

###################################################################### Improvement3: use a hashtable(memo) to store the value of each compute_opt(num) to avoid redundant computations
# dynamic programming function: compute the Bellman equation recursively without storage
def compute_opt(num):
    global list_opt
    if num == -1: 
        return 0
    elif list_opt[num] == -1:  
        opt_1 = compute_opt(num-1)
        opt_2 = list[num].get_para(4) + compute_opt(interv_p[num])
        list_opt[num] = max(opt_1, opt_2)
        return list_opt[num]
    else: return list_opt[num]

# according to the opt computation result, find the chosen intervals
def find_optimal_interval(list_opt):
    list_result = []
    i = len(list_opt)-1
    while(1):
        if list_opt[i] == list_opt[i-1]:
            i = i-1
        else:
            list_result.append(i)
            pre_index = np.where(list_opt == (list_opt[i] - list[i].get_para(4)))[0].tolist()
            if pre_index != []:
                i = pre_index[0]
            else: break
    return list_result

""" #functionality test of the Interval class 
inter_1 = Interval(1, 1, 4, 1)
inter_1.print_info()
print(inter_1.get_para(1)) """

#parameter setting
list_opt = np.zeros(8, dtype=np.int32) - np.ones(8, dtype=np.int32)
interv_p = np.zeros(8, dtype=np.int32) - np.ones(8, dtype=np.int32)
interv_num = 8
interv_start = np.array([1,3,0,4,3,5,6,4]) # the start time of each interval
interv_finish = np.array([4,5,6,7,8,9,10,11]) # the finish time of each interval 
interv_weight = np.array([1,2,3,4,5,6,7,8]) # the weight time of each interval

#algorithm execute
list = create_interval_list(interv_num,interv_start,interv_finish,interv_weight)

interv_p = compute_compatible_interval(list)

print("The optimal total weight is:",compute_opt(interv_num-1))

print("The optimal weights for each interval are:",list_opt)

list_result = find_optimal_interval(list_opt)

print("The chosen intervals for the optimal weight are:",list_result)