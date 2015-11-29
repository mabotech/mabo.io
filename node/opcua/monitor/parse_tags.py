


filename = "cool_system.csv"

import json

import csv
with open(filename, 'rb') as f:
    reader = csv.reader(f)
    i = 0
    y = []
    z = []
    for row in reader:
        i = i +1
        if i != 1:
            x = "ns=2;s=CP_OP10C_D.cool_system.%s" % (row[0])
            y.append(x)
            z.append(row[0].split(".")[-1])
            

print y

#print json.dumps(z)


v = ['ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrA', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrB', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrC', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_Vibr', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Filter_DiffPress', 'ns=2;s=CP_OP10C_D.cool_system.Cool_GearBox_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Motor1_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Motor1_Vibr', 'ns=2;s=CP_OP10C_D.cool_system.Cool_System_Flow', 'ns=2;s=CP_OP10C_D.cool_system.Cool_System_Press','ns=2;s=CP_OP10C_D.hyd_system.Hyd_FrDoorCls_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_FrDoorOpen_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_IndexUclamp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampDep_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrA', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrB', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrC', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_Temp', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotSlidMag_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotSlidSpdl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SideClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SideUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SpToolClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_System_Flow', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_System_Oiltemp']

n = []

for i in v:
    z = i.replace("ns=2;s=CP_OP10C_D.","")
    
    n.append(z)
    
    
print json.dumps(n)