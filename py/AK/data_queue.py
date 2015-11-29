

import Queue


queue = Queue.Queue()


print dir(queue)



for i in xrange(0, 5):
    
    v = (i,i*i,i*2)
    print v
    queue.put(v)
    
    
    
print "==" * 20

for j in xrange(0, 6):
    
    n =  queue.qsize()
    
    if n > 0:
        v = queue.get()
        
        print v