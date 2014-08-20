# -*- coding: utf-8 -*-


import  os

import xlrd
import sys

#import  images
import  encodings.mbcs
import  codecs
from encodings import gbk


import traceback

class excel:
  
  def __init__(self, filename, sheet = 0):
    self.filename = filename
    self.data = ()
    self.collabel = ()
    self.rowlabel = ()
    self.partdata = ()
    self.book = xlrd.open_workbook(filename)
    self.datemode = self.book.datemode
    self.sheets = self.book.sheets()
    self.currentsheet = self.sheets[sheet]
    self.colLabelRange = ((3,1),(3,20))
    self.rowLabelRange = range(4,41)
    self.rowLabelSeg1 = range(4,8)
    self.rowLabelSeg2 = range(36,41)
    
  
  def getColLabel(self):
    start, end = self.colLabelRange
    print start[0], start[1]
    print end[0], end[1]
    
  def getRowLabel(self):
    #for x in self.rowLabelRange:
    for x in self.rowLabelSeg1:
      print x,
    print
    
  def getLabelSeg(self):
    print self.rowLabelSeg1
    print "..."
    print self.rowLabelSeg2
  
  def getRowLabel(self):
    return self.onelinelabel
    
  def getAllData(self):
    return self.alldata
  
  def getData(self):
    sheet = self.currentsheet
    cols =  sheet.ncols
    rows =  sheet.nrows
    print cols, rows
    data = tuple()
    all = []
    onerowlabel =[]
    for i in xrange(0,15):
      val =  sheet.cell_value(2,i)
      item = self.getValue(val,2,i)
      onerowlabel.append(item)
    self.onelinelabel = tuple(onerowlabel)
    #print self.onelinelabel
      
    for r in xrange(0,rows):
      
      #print tuple(onerow)
      """
      for x in onerow:
          print type(x),
      print
      """
      #print type(onerow)
      oneline = []
      
      for c in xrange(0,15):
        val = sheet.cell_value(r,c)
        #print ("(%s,%s) :") %(r,c),
        item = self.getValue(val,r,c)
        oneline.append(item)
        #print item,
        #print
      all.append(tuple(oneline))
    data = tuple(oneline)
    self.alldata = tuple(all)
    
    #print self.alldata
    
    #return self.alldata
    
    for x in self.alldata:
      for y in x:
        #if  type(y) == unicode:
        #    print y.encode("gbk"),
        #else:
        print y,
        print "|",
            
      print
    #all.append(data)
    
    #print all

  def getValue(self, val, r, c):
      
    
    #x = self.currentsheet.cell_type(r,c)
    
    #return val
    
     
    if  type(val) == unicode:
      item = val.encode("gbk")
    elif self.currentsheet.cell_type(r,c) == xlrd.XL_CELL_DATE:
      thisdate = xlrd.xldate_as_tuple(val, self.datemode)
      item = "%s-%s-%s" %(thisdate[0],thisdate[1], thisdate[2])
    else:
      item =  val
    return item
      
def test():    
    
    xls = excel("·ç1.xlsx")     
    
    xls.getData()
    #xls.getColLabel()
    #xls.getRowLabel()
    #xls.getLabelSeg()

if __name__ == "__main__":
    test()
