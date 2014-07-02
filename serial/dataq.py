

from singleton import Singleton

class WeldingData(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        self.line1 = ""
        self.data = []
        
    
    def set_data(self, val):
        
        val = val.strip();
        
        if val == "":
            pass
        elif val.count("M:")>0:
            self.line1 = val
        else:
            self.line1 = self.line1 + val
            
        if len(self.line1)>69:
            self.data.append(self.line1)
            self.line1 = ""
            if len(self.data)>0:
                return self.data.pop(0)
            else:
                return 0
        else:
            return 0
                
                
if __name__ == "__main__":
    
    
    lines = ["M:W1,10,1.15,1.15,1.96,1.96,02.3,1.70,W2,2.36,2.34,3",".33,3.14,07.3,1.34","M:W1,12,0.96,0.96,1.72,1.72,01.7,1.79,W2,2.46,2.43,3.34,3.18,07.7,1.31","M:W1,10,1.17,1.17,1.96,1.96,02.3,1.68,W2,2.36,2.34,3.32",",3.17,07.4,1.35"]
    
    for line in lines:
        
        wd = WeldingData()
        
        t = wd.set_data(line)
        if t == 0:
            pass
            
            
        else:
            print t
            print len(t)