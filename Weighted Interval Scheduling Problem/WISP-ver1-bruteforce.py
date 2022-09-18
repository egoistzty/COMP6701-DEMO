import numpy as np

###################################################################### Improvement1: package the interval as a class 
interv_num = 8
interv_start = np.array([1,3,0,4,3,5,6,4]) # the start time of each interval
interv_finish = np.array([4,5,6,7,8,9,10,11]) # the finish time of each interval 
interv_weight = np.array([1,2,3,4,5,6,7,8]) # the weight time of each interval
interv_p = np.zeros(8, dtype=np.int32) - np.ones(8, dtype=np.int32)

opt = 0
opt_selected = np.array([], dtype=np.int32)

###################################################################### Improvement2: apply a binary search instead of brute search to reduce the complexity from O(n^2) to O(nlogn)
# interv_p:compute the expected index of the former compatible one for each interval, set as -1 if does not exist
def compute_compatible_interv():
    for i in range(8):
        for j in range(8):
            if interv_finish[i-j] <= interv_start[i]:
                interv_p[i] = i-j
                break # only need to find the closest one  

###################################################################### Improvement3: use a hashtable(memo) to store the value of each compute_opt(num) to avoid redundant computations
# brute force function: compute the Bellman equation recursively without storage
def compute_opt(num):
    global opt_selected
    if num == -1: 
        return 0
    else:
        opt_1 = compute_opt(num-1)
        opt_2 = interv_weight[num] + compute_opt(interv_p[num])
        max_opt = max(opt_1, opt_2)
        ###################################################################### Improvement4: try to apply a more elegant way to record the optimized result in each step
        if opt_1 > opt_2: 
            opt_selected = np.append(opt_selected, num-1)
        else:
            opt_selected = np.append(opt_selected, num)
        print("max",max_opt)
        return max_opt

compute_compatible_interv() 
print("compatible p:",interv_p)
opt = compute_opt(interv_num-1)
print("opt:",opt)
print("opt_selected:",opt_selected)