#returns hasse diagram of a given poset for <= relation
class Hasse(object):
    def __init__(self,poset):
        self.poset = poset
        print("poset = ",self.poset)
        self.table=self.init_table(self.poset)
        self.table = self.build_table(self.poset,self.table)
        self.hasse = self.get_hasse(self.poset,self.table)

    @classmethod
    def init_table(self,poset):
        table = [[0 for i in range(len(poset))] for j in range(len(poset))]
        return table

    def print_table(self):
        for i in range(len(self.table[0])):
            for j in range(len(self.poset)):
                if(self.table[i][j] == -1):
                    print(self.table[i][j],end=" | ")
                else:
                    print(self.table[i][j],end="  | ")
            print()
            print('_'*10*len(self.poset))
    @classmethod
    def fit_table(self,table):
        table.reverse()
        return table
    @classmethod
    def compare(self,i,j,poset):
        t = 0
        # print("comparing posets")
        # print(poset[i])
        # print(poset[j])
        for a in range(len(poset[i])):
            if(poset[i][a]<=poset[j][a]):
                t += 1
        if(t == len(poset[i])):
            # print("Returning True")
            return True
        else:
            # print("Returning False t= {} len = {}".format(t,len(poset[i])))
            return False
    @classmethod
    def remove_transitivity(self,table,i,j,poset):
        for k in range(len(poset)):
            if(table[len(poset)-j-1][k] == 1):
                table[i][k] = -1
        return table
    @classmethod
    def build_table(self,poset,table):
        for i in range(len(poset)-1,-1,-1):
            for j in range(len(poset)):
                if(poset[i] != poset[j] and self.compare(i,j,poset) ):
                    if(table[len(poset)-i-1][j]!=-1):
                        table[len(poset)-i-1][j] = 1
                    table = self.remove_transitivity(table,len(poset)-i-1,j,poset)
        return table
    @classmethod
    def get_hasse(self,poset,table):
        links = ""
        for i in range(len(poset)-1,-1,-1):
            for j in range(len(poset)):
                    if(table[i][j] == 1):
                        link = " "+str(poset[len(poset)-1-i])+'-->'+str(poset[j])+"|\n"
                        links += link
        return links
# [[0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]
#
# obj = Hasse([[0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]
# )
# obj.print_table()
# print(obj.hasse)
