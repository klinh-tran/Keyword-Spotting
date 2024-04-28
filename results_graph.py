import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

def error_range_of_a_point(points):
    ''' Calculate the range to true mean - error bar at each point'''
    return np.std(points) / (sqrt(len(points)))   # standard deviation / root square(number of points)


SNRs = np.array([-3, -1.5, 0, 1.5, 3])
default_SNRs = range(len(SNRs)) # only specific values are displayed on axis

# data of new approach - Keyword Spotting
new_0_5 = np.array([6,8,7,7,8,8,8,7,8,8])/8*100 # scores for each sentence using new approach at SNR=3.0 (gain=0.5), total of each = 8 (8 participants)
                                                # % intelligibility = scores /8(max score) *100(%) /10(number of sentences per SNR)(avg)
new_0_7 = np.array([7,1,8,7,8,8,8,7,8,8])/8*100 # new approach, SNR=1.5 (gain=0.7)
new_1_0 = np.array([7,8,7,8,5,8,7,2,8,8])/8*100 # new approach, SNR=0 (gain=1.0)
new_1_4 = np.array([4,3,8,7,7,5,5,8,7,7])/8*100 # new approach, SNR=-1.5 (gain=1.4)
new_2_0 = np.array([2,7,5,3,7,6,5,3,8,6])/8*100 # new approach, SNR=-3.0 (gain=2.0)
new_approach_points = np.array([np.mean(new_2_0),
                                np.mean(new_1_4),
                                np.mean(new_1_0),
                                np.mean(new_0_7),
                                np.mean(new_0_5)]) # new approach points
print(new_approach_points)


# Error bar value
error_new_0_5 = error_range_of_a_point(new_0_5)
error_new_0_7 = error_range_of_a_point(new_0_7)
error_new_1_0 = error_range_of_a_point(new_1_0)
error_new_1_4 = error_range_of_a_point(new_1_4)
error_new_2_0 = error_range_of_a_point(new_2_0)

error_new_approach = [error_new_0_5, 
                      error_new_0_7,
                      error_new_1_0, 
                      error_new_1_4, 
                      error_new_2_0]
print(error_new_approach)

# data of naive baseline - Random Words
random_0_5 = np.array([8,8,8,8,2,8,8,6,8,7])/8*100 # scores for each sentence using random approach at SNR=3.0 (gain=0.5), total of each = 8 (8 participants),
                                                   # % intelligibility = scores /8(max score) *100(%)
random_0_7 = np.array([7,7,8,8,8,7,7,8,8,8])/8*100 # random approach, SNR=1.5 (gain=0.7)
random_1_0 = np.array([8,8,6,8,5,8,7,8,8,8])/8*100 # random approach, SNR=0 (gain=1.0)
random_1_4 = np.array([7,7,8,8,5,3,3,5,7,5])/8*100 # random approach, SNR=-1.5 (gain=1.4)
random_2_0 = np.array([6,3,6,7,5,7,4,5,3,4])/8*100 # random approach, SNR=-3.0 (gain=2.0)
random_approach_points = np.array([np.mean(random_2_0),
                                   np.mean(random_1_4),
                                   np.mean(random_1_0),
                                   np.mean(random_0_7),
                                   np.mean(random_0_5)]) # random approach

# Error bar value
error_random_0_5 = error_range_of_a_point(random_0_5)
error_random_0_7 = error_range_of_a_point(random_0_7)
error_random_1_0 = error_range_of_a_point(random_1_0)
error_random_1_4 = error_range_of_a_point(random_1_4)
error_random_2_0 = error_range_of_a_point(random_2_0)

error_random_approach = [error_random_0_5, 
                         error_random_0_7,
                         error_random_1_0, 
                         error_random_1_4, 
                         error_random_2_0]


# Plot graph
plt.grid(True, axis='x')
plt.xlabel('SNR (dB)')
plt.ylabel('Intelligiblity (%)')
plt.errorbar(default_SNRs, new_approach_points, marker='o', color='b', label='Keyword Spotting', yerr=error_new_approach)
plt.errorbar(default_SNRs, random_approach_points, marker='v', color='orange', label='Random Words', yerr = error_random_approach)
plt.xticks(default_SNRs, SNRs)
plt.legend(loc="lower right")
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.show()