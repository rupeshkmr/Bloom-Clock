from multiprocessing import Process,Pipe, Manager
from os import getpid
from datetime import datetime
from hasse import Hasse
#Helper Functions
#Print Local timestamp and actual time on machine executing the processes
def local_time(counter):
    return '(Vector_Time=[{},{},{}], LOCAL_TIME={})'.format(counter[0],counter[1],counter[2],datetime.now())

#Calculate new timestamp when a process receives a msg
def calc_recv_timestamp(recv_time_stamp, counter):
    for i in range(0,len(counter)):
        counter[i] = max(recv_time_stamp[i],counter[i])
    return counter
#Function for every event that ma occur 1: Local event 2: Message send 3: Message Received
#The event function will return updated timestamp

#1 Local event
#Input is local counter and process id
#return local_timestamp +1

def event(pid,counter,eid):
    counter[pid] +=1
    print('Event happened in {} !'.format(pid)+local_time(counter))
    global history
    history[eid] = counter

    return counter

#2 Message send
#Requires pid ,counter and a pipe for two way communication
#pipe creates two objects one for send and one for receive
#it sends down it's updated counter alongwith the message in the pipe
def send_message(pipe,pid,counter,eid):
    counter[pid] += 1
    pipe.send(('Empty shell',counter))
    print('Message sent from ' +str(pid) + local_time(counter))
    global history
    history[eid] = counter
    return counter

#3 Message Receive
#receives message, timestamp by invoking recv function on pipe
#Then it further calculates it's new timestamp depending upon the received timestamp and current timestamp
def recv_message(pipe,pid,counter,eid):
    counter[pid] += 1
    message,timestamp = pipe.recv();
    counter = calc_recv_timestamp(timestamp,counter)
    print('Message received at '+ str(pid) + local_time(counter))
    global history
    history[eid] = counter
    return counter

#Defenitions for three processes
#Each process starts with getting it's process id and sets it's counter to 0

def process_one(pipe12):
    pid = 0
    counter = [0,0,0]
    counter = event(pid,counter,'b')
    counter = send_message(pipe12, pid,counter,'c')
    counter = event(pid, counter,'d')
    counter = recv_message(pipe12,pid,counter,'e')
    counter = event(pid,counter,'f')

def process_two(pipe21,pipe23):
    pid = 1
    counter = [0,0,0]
    counter = recv_message(pipe21,pid,counter,'g')
    counter = send_message(pipe21,pid,counter,'h')
    counter = send_message(pipe23,pid,counter,'i')
    counter = recv_message(pipe23,pid,counter,'j')

def process_three(pipe32):
    pid = 2
    counter = [0,0,0]
    counter = recv_message(pipe32,pid,counter,'k')
    counter = send_message(pipe32,pid,counter,'l')

def get_ordering(poset):

    print(poset)
    # poset = list(return_dict.values())
    hasse = Hasse(poset)
    hasse.print_table()
    print(hasse.hasse)

if __name__ == '__main__':
    #History dictionary to store each process's counter value
    global history
    history = {}
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()
    # return_dict = Manager().dict()
    process1 = Process(target=process_one,args=(oneandtwo,))
    process2 = Process(target=process_two,args=(twoandone,twoandthree))
    process3 = Process(target=process_three,args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
    # for i in return_dict.keys():
    #     print(i,return_dict[i])
    # poset = return_dict
    # get_ordering(poset)
    print(history)
