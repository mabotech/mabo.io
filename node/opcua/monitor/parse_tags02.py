




import json

import csv

def get_a(channel, device):

    filename = "channels/%s/%s.csv" % (channel, device)

    y = []
    
    with open(filename, 'rb') as f:
        
        reader = csv.reader(f)
        
        #channel = "CP_OP10C_D"
        
        i = 0
        
        z = []
        for row in reader:
            i = i +1
            if i != 1:
                x = "%s.%s.%s" % (channel, device, row[0])
                y.append(x)
                z.append(row[0].split(".")[-1])
                
    return y


def ch_tags(channel, devices):

    tags = []
    
    for device in devices:
        v =get_a(channel, device)
        tags.extend(v)       
        
    return tags
    #print json.dumps(tags)    

def main():
    
    channels = ["CP_OP10C_D","CP_OP20C_D"] 
    
    channels = ["Digi"]
    
    devices = ["cool_system"]#,"hyd_system", "power_system","screw_system","sp_system","TEST" ]
    
    all = []
    
    for channel in channels:
        
        rtn = ch_tags(channel, devices)
        
        all.extend(rtn)
        
    print(len(all))
    print(json.dumps(all))
    
if __name__ == "__main__":
    main()