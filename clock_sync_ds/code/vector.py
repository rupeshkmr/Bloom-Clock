from multiprocessing import Process,Pipe, Manager
from os import getpid
from datetime import datetime
from hasse import Hasse
import csv
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

def event(pid,counter,eid,history):
    counter[pid] +=1
    print('Event happened in {} !'.format(pid)+local_time(counter))
    history[eid] = counter

    return counter,history

#2 Message send
#Requires pid ,counter and a pipe for two way communication
#pipe creates two objects one for send and one for receive
#it sends down it's updated counter alongwith the message in the pipe
def send_message(pipe,pid,counter,eid,history):
    counter[pid] += 1
    pipe.send(('Empty shell',counter))
    print('Message sent from ' +str(pid) + local_time(counter))
    history[eid] = counter
    # print(eid,"\t",history[eid])
    return counter,history

#3 Message Receive
#receives message, timestamp by invoking recv function on pipe
#Then it further calculates it's new timestamp depending upon the received timestamp and current timestamp
def recv_message(pipe,pid,counter,eid,history):
    counter[pid] += 1

    message,timestamp = pipe.recv();
    counter = calc_recv_timestamp(timestamp,counter)
    print('Message received at '+ str(pid) + local_time(counter))
    history[eid] = counter
    return counter,history

#Defenitions for three processes
#Each process starts with getting it's process id and sets it's counter to 0

def process_one(pipe12,return_dict):
    pid = 0
    history={}
    counter = [0,0,0]
    counter,history = event(pid,counter,'b',history)
    return_dict['b'] = history['b']
    counter,history = send_message(pipe12, pid,counter,'c',history)
    return_dict['c'] = history['c']
    counter,history = event(pid, counter,'d',history)
    return_dict['d'] = history['d']
    counter,history = recv_message(pipe12,pid,counter,'e',history)
    return_dict['e'] = history['e']
    counter,history = event(pid,counter,'f',history)
    return_dict['f'] = history['f']
def process_two(pipe21,pipe23,return_dict):
    pid = 1
    history={}
    counter = [0,0,0]
    counter,history = recv_message(pipe21,pid,counter,'g',history)
    return_dict['g'] = history['g']
    counter,history = send_message(pipe21,pid,counter,'h',history)
    return_dict['h'] = history['h']
    counter,history = send_message(pipe23,pid,counter,'i',history)
    return_dict['i'] = history['i']
    counter,history = recv_message(pipe23,pid,counter,'j',history)
    return_dict['j'] = history['j']
def process_three(pipe32,return_dict):
    pid = 2
    counter = [0,0,0]
    history={}
    counter,history = recv_message(pipe32,pid,counter,'k',history)
    return_dict['k'] = history['k']
    counter,history = send_message(pipe32,pid,counter,'l',history)
    return_dict['l'] = history['l']
def get_ordering(poset):

    print(poset)
    # poset = list(return_dict.values())
    hasse = Hasse(poset)
    hasse.print_table()
    print(hasse.hasse)
    with open('vector_poset.csv','a') as openfile:
        csvwriter = csv.writer(openfile,delimiter=',')
        for i in hasse.table:
            csvwriter.writerow(i)
if __name__ == '__main__':
    #History dictionary to store each process's counter value
    global history
    history = {}
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()
    return_dict = Manager().dict()
    process1 = Process(target=process_one,args=(oneandtwo,return_dict))
    process2 = Process(target=process_two,args=(twoandone,twoandthree,return_dict))
    process3 = Process(target=process_three,args=(threeandtwo,return_dict))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
    for i in return_dict.keys():
        print(i,return_dict[i])
    poset = return_dict
    get_ordering(poset)
