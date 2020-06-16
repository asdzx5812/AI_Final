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

def my_blue_and_red(a):
    #return [,0,1]
    #print(a)
    if a == 1 or a == True:
        return [1, 0, 0]
    else: return [0, 0, 1]
    
def update(num):
    global Combined_Times
    global Students
    global total_infected
    global dots
    global txt
    
    print(num)
    txt.set_text('Time={}, Days={}'.format(Combined_Times[num][0], Combined_Times[num][1])) # for debug purposes
    pos = []
    print(Combined_Times[num][0], Combined_Times[num][1], np.sum([student.healthState == "INFECTED"for student in Students]))
    day = Combined_Times[num][1] % 5
    for student in Students:
        if num != 0 and Combined_Times[num][1] != Combined_Times[num-1][1]:
            student.newDayInit(day)
        student.Action(Combined_Times[num][0], day)
        if student.scheduleState != "NULL":
            pos.append(student.currentPosition)
    total_infected.append(np.sum([student.healthState == "INFECTED"for student in Students]))
    #print(new_x.shape)
    #print(new_y.shape)A[:, None]
    #print(pos)
    dots.set_offsets(pos)
    c = []
    for student in Students:
        if student.scheduleState != "NULL":
            c.append(my_blue_and_red(student.healthState == "INFECTED"))
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
    Combined_Times = []
    for day in days:
        for time in Times:
            Combined_Times.append([time, day])
    return Combined_Times
    
def Create_Students(Healthy_num, Infected_num):
    students = []
    for i in range(Healthy_num):
        students.append(Student())
    for i in range(Infected_num):
        students.append(Student("INFECTED"))
    return students

def main():
    global Combined_Times
    global Students
    global total_infected
    total_infected = []
    start_time = "07:30"
    end_time = "20:00"
    days = 20
    Healthy_num = 2999
    Infected_num = 1

    Combined_Times = Def_Times(start_time, end_time, days)    
    Students = Create_Students(Healthy_num, Infected_num)
    total_infected.append(np.sum([student.healthState == "INFECTED" for student in Students]))
    fig = plt.figure(figsize=(7, 6), dpi=100)

    red_patch = mpatches.Patch(color='red', label='infected')
    blue_patch = mpatches.Patch(color='blue', label='healthy')

    plt.legend(handles=[red_patch, blue_patch])
    plt.axis('off')
    plt.xlim((0, 16000))
    plt.ylim((0, 16000))
    ax = fig.gca()


    x = np.array([student.currentPosition[0] for student in Students])
    y = np.array([student.currentPosition[1] for student in Students])
    #x=np.array([pos[i][0] for i in range(len(pos))])
    #y=np.array([pos[i][1] for i in range(len(pos))])
    #print([ student.healthState == "INFECTED" for student in Students])
    c=np.array([my_blue_and_red(student.healthState == "INFECTED") for student in Students])
    global txt, dots
    dots= ax.scatter(x, y, color=c, cmap="bwr")
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    
    txt = fig.suptitle('Time={}, Days={}'.format(Combined_Times[0][0], Combined_Times[0][1]))

    #print(x)
    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(Combined_Times), interval=0.1)
    img = cv2.imread("Test_map.png")
    plt.imshow(img, extent=[0, 16000, 0, 16000])
    ani.save('Testoutput.mp4', writer="ffmpeg", fps=24)
    plt.show()

if __name__ == "__main__":
    main()