import math
import mmh3
from bitarray import bitarray
#Referenced from https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/

class BloomFilter(object):
    #CLass for Bloom FIlter ,murmur3 hash function
    def __init__(self,items_count,fp_prob,timestamp):
        #items_count: no of expected items to be stored in the bloom FIlter
        #fp_prob false positive probability
        self.fp_prob = fp_prob
        #size of bit array to use
        self.size = self.get_size(items_count,fp_prob)
        #no of hash functions to be used
        self.hash_count = self.get_hash_count(self.size,items_count)
        #bit array of given size
        self.bit_array = bitarray(self.size)
        #init all bits as 0
        self.bit_array.setall(0)
        #to save timestamp histories
        self.history = {}# it saves a list containing previous bit arrays as timestamps
        self.timestamp = timestamp#to store the current global timestamp

    def add(self,item,timestamp):
        #To add an item to the filter
        digests = []
        self.timestamp = timestamp
        for i in range(self.hash_count):
            #create digest for given items
            #i work as seed to mmh3 hash function
            #with different seed , digest created is different
            digest = mmh3.hash(item,i)%self.size
            digests.append(digest)
            #set the bit True in bit array
            self.bit_array[digest] += 1
        self.history[str(self.timestamp)] = self.bit_array

    def update_filter(self,filter1,timestamp):
        #To add an item to the filter
        digests = []
        old_ts = self.timestamp
        self.timestamp = timestamp
        #updating the current timestamp
        for i in range(self.size):
            self.bit_array[i] = max(self.bit_array[i],filter1.bit_array[i])
        #saving the current bit array for history of the timestamps
        self.history[str(old_ts)] = self.bit_array

    def check(self,item):
        #check for existence of an item in filter
        for i in range(self.hash_count):
            digest = mmh3.hash(item,i)%self.size
            if(self.bit_array[digest]>=1):
                #if any of the bit is Falsr then it's not present
                #in filter else there is probability that it exist
                return False
            return True s

    @classmethod
    def get_size(self,n,p):
        #return the size of bit aarray(m) to used using formula
        '''
        m = -(n*lg(p))/(lg(2)^2)
        n:int no of items expected to be stored in filter
        p:float False positive probability
        '''
        m = -(n*math.log(p))/(math.log(2)**2)
        return int(m)
    @classmethod
    def get_hash_count(self,m,n):
        #return the hash function(k) to be used
        k = (m/n)*math.log(2)
        return int(k)
