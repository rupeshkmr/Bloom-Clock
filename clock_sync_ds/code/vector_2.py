from multiprocessing import Process,Pipe, Manager
from os import getpid
from datetime import datetime
from hasse import Hasse
import csv
import json
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
    data = {eid:counter}
    with open('vector_poset_2.txt', 'a') as outfile:
        json.dump(data, outfile)
        outfile.write("\n")
    return counter

#2 Message send
#Requires pid ,counter and a pipe for two way communication
#pipe creates two objects one for send and one for receive
#it sends down it's updated counter alongwith the message in the pipe
def send_message(pipe,pid,counter,eid):
    counter[pid] += 1
    pipe.send(('Empty shell',counter))
    print('Message sent from ' +str(pid) + local_time(counter))
    data = {eid:counter}
    with open('vector_poset_2.txt', 'a') as outfile:
        json.dump(data, outfile)
        outfile.write("\n")
    return counter

#3 Message Receive
#receives message, timestamp by invoking recv function on pipe
#Then it further calculates it's new timestamp depending upon the received timestamp and current timestamp
def recv_message(pipe,pid,counter,eid):
    counter[pid] += 1
  
    message,timestamp = pipe.recv();
    counter = calc_recv_timestamp(timestamp,counter)
    data = {eid:counter}
    with open('vector_poset_2.txt', 'a') as outfile:
        json.dump(data, outfile)
        outfile.write("\n")
    print('Message received at '+ str(pid) + local_time(counter))
    return counter

#Defenitions for three processes
#Each process starts with getting it's process id and sets it's counter to 0

def process_one(pipe12,pipe13):
    pid = 0
    counter = [0,0,0]
    counter = send_message(pipe13,pid,counter,'a')
    counter = recv_message(pipe12,pid,counter,'b')
    counter = send_message(pipe12,pid,counter,'c')
    counter = recv_message(pipe13,pid,counter,'d')
    
def process_two(pipe21,pipe23):
    pid = 1
    counter = [0,0,0]
    counter = send_message(pipe21,pid,counter,'e')    
    counter = event(pid,counter,'f')
    counter = send_message(pipe23,pid,counter,'g')
    counter = recv_message(pipe21,pid,counter,'h')
    counter = event(pid,counter,'i')
    
def process_three(pipe31,pipe32):
    pid = 2
    counter = [0,0,0]
    counter = send_message(pipe31,pid,counter,'j')
    counter = recv_message(pipe31,pid,counter,'k')
    counter = recv_message(pipe32,pid,counter,'l')
    counter = event(pid,counter,'m')
def get_ordering(poset):

    #print(poset)
    
    hasse = Hasse(poset)
    #hasse.print_table()
    print(hasse.hasse)
    with open('vector_poset.csv','a') as openfile:
        csvwriter = csv.writer(openfile,delimiter=',')
        for i in hasse.table:
            csvwriter.writerow(i)
if __name__ == '__main__':

    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()
    oneandthree, threeandone = Pipe()
    process1 = Process(target=process_one,args=(oneandtwo,oneandthree))
    process2 = Process(target=process_two,args=(twoandone,twoandthree))
    process3 = Process(target=process_three,args=(threeandone,threeandtwo))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
    
    poset = {}
    with open('vector_poset_2.txt') as json_file:
        for jsonobj in json_file:
            data = json.loads(jsonobj)#[json.load(line) for line in json_file]
            poset[list(data.keys())[0]] = data[list(data.keys())[0]]
    get_ordering(poset)
 
