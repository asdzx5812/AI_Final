import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
from scipy import misc
from Time import Time
from Student import Student, Schedule
import mapmodule
import cv2
import argparse

Health_state = ["SUSCEPTIBLE", "EXPOSED", "INFECTIOUS", "RECOVERED", "DEAD"]
CLASS_END_TIME = ['09:00', '10:00', '11:10', '12:10', '13:10', '14:10', '15:10', '16:20', '17:20', '18:20', '19:15']

def my_color(s):
    if s.healthState.state == Health_state[0]:
        return [0,0,1]
    elif s.healthState.state == Health_state[1]:
        return [1, 0.5, 0.5]
    elif s.healthState.state == Health_state[2]:
        return [1, 0, 0]
    else: return [0, 1, 0]
    
def update(num):
    global Combined_times
    global Students
    global State_count
    global dots
    global txt
    

    pos = []
    day = Combined_times[num][1] % 5
    for student in Students:
        if num != 0 and Combined_times[num][1] != Combined_times[num-1][1]:
            student.newDayInit(day)
        student.Action(Combined_times[num][0], day)
        if student.scheduleState != "NULL" and student.healthState.state != Health_state[4]:
            pos.append(student.currentPosition)
    cur = []
    for i in range(len(Health_state)):
        cur.append( np.sum([student.healthState.state == Health_state[i] for student in Students]) )
        try:
            State_count[i][num] = cur[i]
        except:
            State_count[i].append(cur[i])
    cur=np.array(cur).astype(str)

    if Combined_times[num][0] in CLASS_END_TIME:
        print(num)
        print(Combined_times[num][0], Combined_times[num][1], np.sum([student.healthState.state == "INFECTED"for student in Students]))
        print(cur)
        
    txt.set_text('Time={}, Days={}\nsusceptible={}, exposed={}, infectious={} \n recovered={}, dead={}'.format(Combined_times[num][0], Combined_times[num][1], cur[0], cur[1], cur[2], cur[3], cur[4])) # for debug purposes
    #print(new_x.shape)
    #print(new_y.shape)A[:, None]
    #print(pos)
    dots.set_offsets(pos)
    c = []
    for student in Students:
        if student.scheduleState != "NULL" and student.healthState.state != Health_state[4]:
            c.append(my_color(student))
        else:
            pass
    #print(c)
    dots.set_color(c)

    return txt   

def Def_Times(start_time, end_time, Day):
    Times = []
    days = [i for i in range(Day)]
    
    current_time = start_time
    while Time.compare(current_time, "<=", end_time):
        Times.append(current_time)
        current_time = Time.addMinutes(current_time, 1)
    Combined_times = []
    for day in days:
        for time in Times:
            Combined_times.append([time, day])
    return Combined_times
    
def Create_Students(Healthy_num, Infected_num):
    students = []
    for i in range(Healthy_num):
        students.append(Student())
    for i in range(Infected_num):
        students.append(Student(Health_state[2]))
    a = Student()
    a.healthState.state = "EXPOSED"
    #b = Student()
    ##b.healthState.state = "RECOVERED"
    #students.append(a)
    #students.append(b)
    return students

def main(parser):
    global Combined_times
    global Students
    global State_count
    start_time = "07:30"
    end_time = "20:00"
    days = parser.d
    Healthy_num = parser.n - parser.i

    Infected_num = parser.i
    
    Combined_times = Def_Times(start_time, end_time, days)    
    Students = Create_Students(Healthy_num, Infected_num)

    State_count = []

    for i in range(len(Health_state)):
        State_count.append([])
        #State_count[i].append(np.sum([student.healthState.state == Health_state[i] for student in Students] ))
    fig = plt.figure(figsize=(7, 6), dpi=100)

    blue_patch = mpatches.Patch(color='blue', label='suspectible')
    pink_patch = mpatches.Patch(color='pink', label='exposed')
    red_patch = mpatches.Patch(color='red', label='infectious')
    green_patch = mpatches.Patch(color='green', label='recovered')
    patches = [red_patch, blue_patch, pink_patch, green_patch]
    plt.legend(handles=patches)
    plt.axis('off')
    plt.xlim((0, 16000))
    plt.ylim((0, 16000))
    ax = fig.gca()

    s = []
    x = []
    y = []
    c = []
    for student in Students:
        if student.scheduleState != "NULL" and student.healthState.state != "DEAD":
            x.append(student.currentPosition[0])
            y.append(student.currentPosition[0])
            c.append(my_color(student))
            s.append(15)
    global txt, dots
    dots= ax.scatter(x, y, color=c, s=s)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    cur = []
    for i in range(len(Health_state)):
        cur.append( np.sum([student.healthState.state == Health_state[i] for student in Students]) )
    txt = fig.suptitle('Time={}, Days={}\nsusceptible={}, exposed={}, infectious={} \n recovered={}, dead={}'.format(Combined_times[0][0], Combined_times[0][1], cur[0], cur[1], cur[2], cur[3], cur[4])) # for debug purposes

    #print(x)
    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(Combined_times), interval=0.1)
    img = cv2.imread("map.png")
    plt.imshow(img, extent=[0, 16000, 0, 16000])
    ani.save(parser.f + '.mp4', writer="ffmpeg", fps=5)
    plt.show()
    #print(np.array(Combined_times))
    #print(Combined_times)
    #print(State_count)
    CSV_STACK = np.column_stack((np.array(Combined_times).astype(str), np.array(State_count).astype(str).T))
    #print(CSV_STACK)
    np.savetxt(parser.f + ".csv", np.array(CSV_STACK), fmt="%s" , delimiter=",")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="num of students", default=3000)
    parser.add_argument("-i", type=int, help="num of infectious students", default = 1)
    parser.add_argument("-d", type=int, help="num of days", required=True)
    parser.add_argument("-f", type=str, help="filename", required=True)
    main(parser.parse_args())
