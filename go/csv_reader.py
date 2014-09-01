

import csv




class CsvReader(object):
    
    def __init__(self):
        pass
        
        self.header = {}
        
        self.data = []
        
    def get_header(self, row):
        for i in xrange(0, len(row)):
            self.header[row[i]] = i
        
        
        #print self.header
        
    def get_data(self, row):
        self.data.append(row)

    def read(self, fn):
        
        with open(fn, 'rb') as f:
            
            reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
            
            i = 0
            
            for row in reader:
                
                #print row
                
                if i == 0:
                    self.get_header(row)
                else:
                    self.get_data(row)
                i = i + 1
    
    def process(self):
        
        for item in self.data:
            i = self.header["Sequence number"]
            i = self.header["Production number"]
            print item[i]
        
        
def main():
    
    fn = 'C41295-100_20140220_135315.CSV'
    
    reader = CsvReader()
    
    reader.read(fn)
    
    reader.process()
    
    

if __name__ == "__main__":
    main()
    
    