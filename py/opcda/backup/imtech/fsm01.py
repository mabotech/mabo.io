


from fysom import Fysom

def onarrived(e):
    print '=>arrived'

def onarrive(e):
    print '=>arrive'
   
def onchanged(e):
    print '=>changed'
    
def ondepart(e):
    print '=>depart'
    
def onwaiting(e):
    print '=>on waiting'
    
def error(e):
    print e
    
fsm = Fysom(
            {'initial': 'waiting',
            
             'events': [
                 {'name': 'arrive', 'src': 'waiting', 'dst': 'arrived'},
                 {'name': 'change', 'src': 'arrived', 'dst': 'changed'},
                 {'name': 'depart', 'src': 'changed', 'dst': 'waiting'},
                ],

             'callbacks': {                 
                'onarrive': onarrive,
                'onchanged': onchanged,
                'ondepart':ondepart
                }
            })
                 
                 
print dir(fsm)

import time

p  =  fsm.current

print p

def loop() :
    
    
    while True:
        c =  fsm.current
        
        global p
        
        if c != p:
            p = c
            print  "S:"+c
            print "\n"
        i = int( time.time() )
        
        if i % 4 == 0 and fsm.can('arrive'):
            fsm.arrive()

        elif i %5 == 1 and  fsm.can('change'):
            fsm.change()

        elif i%7 ==2 and fsm.can('depart'):
            fsm.depart()
        else:
            time.sleep(2)        
            #print  "E:"+fsm.current
            print "."
        
        time.sleep(1)
    


if __name__ == '__main__':
    
    loop()