#

from pymodbus.client.sync import  ModbusSerialClient
import time

def main():

    t=1

    # Linux
    #client = ModbusSerialClient("rtu", port='/dev/ttyS1', baudrate=9600, timeout=t)
    
    # Windows
    client = ModbusSerialClient("rtu", port='COM4', baudrate=9600, timeout=t)
    
    client.connect()
    
    start = time.time()

    #data = client.read_input_registers(0x0000, count=10, unit=0x01)
    data = client.read_holding_registers(0x0002, count=5, unit=0x01)

    #print dir(data)

    print (data.function_code)
    
    print (data.registers)

    stop = time.time()

    if data:
        succ = "was successful"
    else:
        succ = "failed"

    print ("timeout: %ss, read %s, time spent reading: %fs" % (t, succ, stop-start))
    
if __name__ == "__main__":
        
    main()