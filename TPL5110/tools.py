
class Table:
    def __init__(self,headers):
        self.headers = headers
        self.content = []
        
    def add_row(self,row : list):
        if (len(row) != len(self.headers)):
            raise Exception("you have to supply as many values as there are columns")
        else:
            self.content.append(row)
            
    def set_content(self, contents : list[list]):
        for r in range(len(contents)):
            #print("cont:",len(contents[r]),"head:",len(self.headers))
            if (len(contents[r]) != len(self.headers)):
                raise Exception("you have to supply as many values as there are columns")
            else:
                self.content.append(contents[r])
                
