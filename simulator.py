'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Author: Minh Ho
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt

Apr 10th Revision 1:
    Update FCFS implementation, fixed the bug when there are idle time slices between processes
    Thanks Huang Lung-Chen for pointing out
Revision 2:
    Change requirement for future_prediction SRTF => future_prediction shortest job first(SJF), the simpler non-preemptive version.
    Let initial guess = 5 time units.
    Thanks Lee Wei Ping for trying and pointing out the difficulty & ambiguity with future_prediction SRTF.
'''
import sys
import copy

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum):
    temp_list = copy.deepcopy(process_list)
    schedule = []
    current_time = 0
    waiting_time = 0
    index = 0
    while index < len(temp_list):
        process = temp_list[index]
        step = time_quantum
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        if (process.burst_time < time_quantum):
            step = process.burst_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + step
        if (process.burst_time > step):
            process.burst_time -= step
            process.arrive_time = current_time
            new_index = 0
            if (temp_list[-1].arrive_time < current_time):
                temp_list.pop(index)
                temp_list.append(process)
                index -= 1
            else:
                for temp_process in temp_list:
                    if (temp_process.arrive_time > current_time):
                        temp_list.pop(index)
                        if (index < new_index):
                            new_index -= 1
                            index -= 1
                        temp_list.insert(new_index, process)
                        break
                    new_index += 1
        index += 1
    average_waiting_time = waiting_time/float(len(temp_list))
    return schedule, average_waiting_time
    #return (["to be completed, scheduling process_list on round robin policy with time_quantum"], 0.0)

def SRTF_scheduling(process_list):
    temp_list = copy.deepcopy(process_list)
    schedule = []
    waiting_time = 0
    current_time = 0
    count = 0
    n = len(temp_list)
    temp_list.append(Process(9999,9999,9999))
    while (count != n):
        smallest = n
        i = 0
        for process in temp_list:
            if (process.arrive_time > current_time):
                break;
            if (process.arrive_time <= current_time and process.burst_time < temp_list[smallest].burst_time and process.burst_time > 0):
                smallest = i
            i += 1
        if smallest != n:
            temp_list[smallest].burst_time -= 1
        if (temp_list[smallest].burst_time == 0):
            count += 1
            end = current_time + 1
            waiting_time = waiting_time + end - temp_list[smallest].arrive_time - process_list[smallest].burst_time
        if smallest != n:
            schedule.append((current_time, temp_list[smallest].id))
        current_time += 1
    average_waiting_time = waiting_time / float(len(temp_list))
    return schedule, average_waiting_time
    #return (["to be completed, scheduling process_list on SRTF, using process.burst_time to calculate the remaining time of the current process "], 0.0)

def SJF_scheduling(process_list, alpha):
    temp_list = copy.deepcopy(process_list)
    predicted_time = {}
    schedule = []
    waiting_time = 0
    current_time = 0
    count = 0
    n = len(temp_list)
    temp_list.append(Process(9999, 9999, 9999))
    while (count != n):
        smallest = len(temp_list) - 1
        i = 0
        if (current_time < temp_list[0].arrive_time):
            current_time = temp_list[0].arrive_time
        for process in temp_list:
            if (process.arrive_time > current_time):
                break;
            burst_time = 5
            if process.id in predicted_time:
                burst_time = predicted_time[process.id]
            if (process.arrive_time <= current_time and burst_time < temp_list[smallest].burst_time and process.burst_time > 0):
                smallest = i
            i += 1
        burst_time = alpha * temp_list[smallest].burst_time + (1 - alpha) * burst_time
        predicted_time[temp_list[smallest].id] = burst_time
        current_time += temp_list[smallest].burst_time
        schedule.append((current_time, temp_list[smallest].id))
        count += 1
        waiting_time = waiting_time + current_time - temp_list[smallest].arrive_time - temp_list[smallest].burst_time
        temp_list.pop(smallest)
    average_waiting_time = waiting_time / float(len(process_list))
    return schedule, average_waiting_time
    #return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])
