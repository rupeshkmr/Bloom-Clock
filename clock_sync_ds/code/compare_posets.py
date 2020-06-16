import csv
def compare(poset1,poset2):
    print("Poset 1:\t")
    for i in poset1:
        print(i)
    print("poset 2:\t")
    for i in poset2:
        print(i)
    differences = []
    for i in range(len(poset1)):
        for j in range(len(poset2)):
            if(poset1[i][j] == '1'):
                if(poset2[i][j]!='1'):
                    temp = ['Diff 1->2: (',i,',',j,")",'Poset1(',poset1[i][j],')','Poset2(',poset2[i][j],')']
                    differences.append(temp)
            if(poset2[i][j] == '1'):
                if(poset1[i][j]!='1'):
                    temp = ['Diff 2->1: (',i,',',j,")",'Poset2(',poset2[i][j],')','Poset1(',poset1[i][j],')']
                    differences.append(temp)

    return differences
def truncate_ipstring(poset):
    for i in poset:
        print(i)
if __name__=='__main__':
    with open('vector_poset.csv','r') as openfile:
        csvreader = csv.reader(openfile,delimiter=',')
        poset2 = []
        for i in csvreader:
            poset2.append(list(i))

    with open('bloom_poset.csv','r') as openfile:
        csvreader = csv.reader(openfile,delimiter=',')
        poset1 = []
        for i in csvreader:
            poset1.append(list(i))
    result = compare(poset1,poset2)
    print("differences:")
    for i in result:
        print(i)
