
import time

"""
logging simulator
"""

def run():
    
    filename = "Test.log"

    output = "test.log"

    try:
        
        fh_in = open(filename,"r")

        fh_out = open(output,"a")
        
        for line in fh_in:
            print(line),
            fh_out.write(line)
            fh_out.flush()
            time.sleep(2)
            
    except Exception as ex:
        print(ex)   
        
    finally:
        fh_out.close()
        fh_in.close()
        
if __name__ == "__main__":
    run()