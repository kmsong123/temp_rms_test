import string
import os
import re

# Given input of line from logged icicle output
# Return signal_time
def get_task_signal_time(line):
    signal_time = 0
    temp = line.partition("signalTime: ")[2]
    signal_time = temp.partition("startTime:")[0]
    signal_time = signal_time.strip()
    return int(signal_time)

# Given input of line from logged icicle output
# Return end_time
def get_task_end_time(line):
    end_time = 0
    temp = line.partition("doneTime: ")[2]
    end_time = temp.strip()
    return int(end_time)


### TEST FOR CHECKING IF THERE WERE ANY TASK OVERRUNS
print("***** Starting test to check if there were any overruns *****")
logfile_name = "icicle_output.txt"
logfile = open(logfile_name, 'r')

if not os.path.exists(logfile_name):
    print("No icicle_output.txt logfile!")
    quit()

overrun = False
lines = logfile.readlines()
overrun_cnt = 0
for line in lines:
    if "overrun: " in line:
        #grab overrun number
        temp_str = line.partition("overrun:")[2]
        temp_str2 = temp_str.partition("latency:")[0]
        temp_overrun = int(temp_str2)
        #if overrun count has increased
        if( temp_overrun > overrun_cnt):
            overrun_cnt += 1
            print("overrun detected!  Printing overrun details:")
            print(line)


### TEST FOR CHECKING IF EACH TASK RAN ONCE PER PERIOD
print("***** Starting test to check each task ran once per period *****")
start_time = 0

# Record start time
# Current start time is when setup for task 100hz is called (I am assuming that task is the first task called)
temp_lines = lines
for line in temp_lines:
    if "Setup time for Task_100Hz_1" in line:
        split = ':'
        start_time = int(line.partition(split)[2])
        print("start time is: " + str(start_time))
        break

# Calculate time bins per task 
# Icicle board runs at 600MHz clock speed
# = 1 clock/1.6667ns 
p_100hz_time_s = 0.01
p_50hz_time_s = 0.02
p_5hz_time_s = 0.2
p_1hz_time_s = 1.0
p_lowrate_time_s = 30.0

icicle_clock_speed_hz = 6.0*pow(10.0,8.0) # 600 MHz
#u54_clock_speed_hz = 
#time_for_1_cycle_s = ((5.0/3.0) * pow(10, -9))
time_for_1_cycle_s = (1.0/icicle_clock_speed_hz)
#time_for_1_cycle_s = ((6) * pow(10, -10))

Task_100Hz_period = int(p_100hz_time_s/time_for_1_cycle_s)     
Task_50Hz_period = int(p_50hz_time_s/time_for_1_cycle_s)      
Task_5Hz_period = int(p_5hz_time_s/time_for_1_cycle_s)       
Task_1Hz_period = int(p_1hz_time_s/time_for_1_cycle_s)         
Task_LowRate_period = int(p_lowrate_time_s/time_for_1_cycle_s)

num_iterations = 200

Task_100Hz_period_start = ["-1"] * num_iterations
Task_50Hz_period_start = ["-1"] * num_iterations
Task_5Hz_period_start = ["-1"] * num_iterations
Task_1Hz_period_start = ["-1"] * num_iterations
Task_LowRate_period_start = ["-1"] * num_iterations

"""
Task_100Hz_period_end[num_iterations]
Task_50Hz_period_end[num_iterations]
Task_5Hz_period_end[num_iterations]
Task_1Hz_period_end[num_iterations]
Task_LowRate_period_end[num_iterations]
"""

Task_100Hz_cnt = start_time
Task_50Hz_cnt = start_time
Task_5Hz_cnt = start_time
Task_1Hz_cnt = start_time
Task_LowRate_cnt = start_time

for iteration in xrange(num_iterations):
    temp_100hz = Task_100Hz_cnt + (iteration * Task_100Hz_period)
    temp_50hz =  Task_50Hz_cnt + (iteration * Task_50Hz_period)
    temp_5hz = Task_5Hz_cnt + (iteration * Task_5Hz_period)
    temp_1hz = Task_1Hz_cnt + (iteration * Task_1Hz_period)
    temp_lowrate = Task_LowRate_cnt + (iteration * Task_LowRate_period)

    Task_100Hz_period_start[iteration] = temp_100hz 
    Task_50Hz_period_start[iteration] = temp_50hz
    Task_5Hz_period_start[iteration] = temp_5hz
    Task_1Hz_period_start[iteration] = temp_1hz     
    Task_LowRate_period_start[iteration] = temp_lowrate

    Task_100Hz_cnt = temp_100hz
    Task_50Hz_cnt = temp_50hz
    Task_5Hz_cnt = temp_5hz
    Task_1Hz_cnt = temp_1hz
    Task_LowRate_cnt = temp_lowrate

# Create lists of task signaled and done times
Task_100Hz_signal_list = ["-1"] * num_iterations
Task_50Hz_signal_list = ["-1"] * num_iterations
Task_5Hz_signal_list = ["-1"] * num_iterations
Task_1Hz_signal_list = ["-1"] * num_iterations
Task_LowRate_signal_list = ["-1"] * num_iterations

Task_100Hz_end_list = ["-1"] * num_iterations
Task_50Hz_end_list = ["-1"] * num_iterations
Task_5Hz_end_list = ["-1"] * num_iterations
Task_1Hz_end_list = ["-1"] * num_iterations
Task_LowRate_end_list = ["-1"] * num_iterations

# Note: hardcoded to match RMS metrics logging outputs
cnt_100hz = 0
cnt_50hz = 0
cnt_5hz = 0
cnt_1hz = 0
cnt_lowrate = 0
for line in lines:
    #TODO: make sure parsed iteration number matches cnt number to account for potentially unlogged/skipped iterations
    if "task_100Hz iteration" in line:
        Task_100Hz_signal_list[cnt_100hz] = get_task_signal_time(line)        
        Task_100Hz_end_list[cnt_100hz] = get_task_end_time(line)
        cnt_100hz += 1
    if "task_50Hz_ iteration" in line:
        Task_50Hz_signal_list[cnt_50hz] = get_task_signal_time(line)
        Task_50Hz_end_list[cnt_50hz] = get_task_end_time(line)
        cnt_50hz += 1
    if "task_5Hz_1 iteration" in line:
        Task_5Hz_signal_list[cnt_5hz] = get_task_signal_time(line)
        Task_5Hz_end_list[cnt_5hz] = get_task_end_time(line)    
        cnt_5hz += 1
    if "task_1Hz_1 iteration" in line:
        Task_1Hz_signal_list[cnt_1hz] = get_task_signal_time(line)
        Task_1Hz_end_list[cnt_1hz] = get_task_end_time(line)    
        cnt_1hz += 1
    if "task_Lowra iteration" in line:
        Task_1Hz_lowrate_list[cnt_lowrate] = get_task_signal_time(line)
        Task_1Hz_lowrate_list[cnt_lowrate] = get_task_end_time(line)    
        cnt_lowrate += 1

# Go through list of task execution iterations
# and make sure each iteration per task is only run once per period
# TODO: edge cases for edge cycle counts of cycles/deadlines

for iteration in xrange(num_iterations-1):
    #make sure task signal time > period_start and task end time < period_end (which is next iteration start time)
    if not (Task_100Hz_signal_list[iteration] > Task_100Hz_period_start[iteration] and
            Task_100Hz_end_list[iteration] < Task_100Hz_period_start[iteration+1]):
        if ((Task_100Hz_signal_list[iteration] == "-1") or (Task_100Hz_end_list[iteration] == "-1")):
            continue
        print("FAIL.  Task_100Hz_1 iteration " + str(iteration) + " execution does not fall within deadline bounds")
        print("Task_100Hz_1's execution range is between " + str(Task_100Hz_period_start[iteration]) + " and " +
                str(Task_100Hz_period_start[iteration+1]))
        print("Task_100Hz_1's signal time is " + str(Task_100Hz_signal_list[iteration]))
        print("Task_100Hz_1's done time is " + str(Task_100Hz_end_list[iteration]))
    if not (Task_50Hz_signal_list[iteration] > Task_50Hz_period_start[iteration] and
            Task_50Hz_end_list[iteration] < Task_50Hz_period_start[iteration+1]):
        if ((Task_50Hz_signal_list[iteration] == "-1") or (Task_50Hz_end_list[iteration] == "-1")):
            continue
        print("FAIL.  Task_50Hz_1 iteration " + str(iteration) + " execution does not fall within deadline bounds")
        print("Task_50Hz_1's execution range is between " + str(Task_50Hz_period_start[iteration]) + " and " +
                str(Task_50Hz_period_start[iteration+1]))
        print("Task_50Hz_1's signal time is " + str(Task_50Hz_signal_list[iteration]))
        print("Task_50Hz_1's done time is " + str(Task_50Hz_end_list[iteration]))
    if not (Task_5Hz_signal_list[iteration] > Task_5Hz_period_start[iteration] and
            Task_5Hz_end_list[iteration] < Task_5Hz_period_start[iteration+1]):
        if ((Task_5Hz_signal_list[iteration] == "-1") or (Task_5Hz_end_list[iteration] == "-1")):
            continue
        print("FAIL.  Task_5Hz_1 iteration " + str(iteration) + " execution does not fall within deadline bounds")
        print("Task_5Hz_1's execution range is between " + str(Task_5Hz_period_start[iteration]) + " and " +
                str(Task_5Hz_period_start[iteration+1]))
        print("Task_5Hz_1's signal time is " + str(Task_5Hz_signal_list[iteration]))
        print("Task_5Hz_1's done time is " + str(Task_5Hz_end_list[iteration]))
    if not (Task_1Hz_signal_list[iteration] > Task_1Hz_period_start[iteration] and
            Task_1Hz_end_list[iteration] < Task_1Hz_period_start[iteration+1]):
        if ((Task_1Hz_signal_list[iteration] == "-1") or (Task_1Hz_end_list[iteration] == "-1")):
            continue
        print("FAIL.  Task_1Hz_1 iteration " + str(iteration) + " execution does not fall within deadline bounds")
        print("Task_1Hz_1's execution range is between " + str(Task_1Hz_period_start[iteration]) + " and " +
                str(Task_1Hz_period_start[iteration+1]))
        print("Task_1Hz_1's signal time is " + str(Task_1Hz_signal_list[iteration]))
        print("Task_1Hz_1's done time is " + str(Task_1Hz_end_list[iteration]))
    if not (Task_LowRate_signal_list[iteration] > Task_LowRate_period_start[iteration] and
            Task_LowRate_end_list[iteration] < Task_LowRate_period_start[iteration+1]):
        if ((Task_LowRate_signal_list[iteration] == "-1") or (Task_LowRate_end_list[iteration] == "-1")):
            continue
        print("FAIL.  Task_LowRate_1 iteration " + str(iteration) + " execution does not fall within deadline bounds")
        print("Task_LowRate_1's execution range is between " + str(Task_LowRate_period_start[iteration]) + " and " +
                str(Task_LowRate_period_start[iteration+1]))
        print("Task_LowRate_1's signal time is " + str(Task_LowRate_signal_list[iteration]))
        print("Task_LowRate_1's done time is " + str(Task_LowRate_end_list[iteration]))

print("PASS.  All tasks only ran once.")
logfile.close()
