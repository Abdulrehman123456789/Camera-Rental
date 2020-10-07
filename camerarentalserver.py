import asyncio
import websockets
import pymysql
import base64 
from PIL import Image
import numpy as np  
import random
import requests

class img():
 def covertfiletostring(img):
  imgs=str(img)
  arr=imgs.split("'")
  return (arr[1])


 def RASdecrp(edata):
  privatekey=2011
  n=3127
  #d=c^d mod n
  earr=edata.split("*")
  data=""
  for i in range(0,len(earr)-1):
   a=pow(int(earr[i]),privatekey)
   b=a%n
   data=data+chr(b)
  return(data)
   


class owner():
 def ownersignin(tdata):
  try:
   print(tdata) 
   sp=tdata.split("$")
   decryptpass=img.RASdecrp(sp[3]) 
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="camerarental")
   c=db.cursor()
   c.execute("INSERT INTO ownerdetails values (%s,%s,%s,%s,%s,%s,%s)",(sp[0],int(sp[1]),sp[2],decryptpass,sp[4],sp[5],sp[6]))
   db.commit()
   db.close()
   return(1)
  except:
   return(0)
    


 def login(tdata):
  try:
   sp=tdata.split("$")
   decryptpass=img.RASdecrp(sp[1])  
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="camerarental")
   c=db.cursor()
   c.execute("select o.phone,o.password from ownerdetails o where o.phone=%s",int(sp[0]))
   result=c.fetchall()
   print("userphoneno")
   print(result[0][0]) #don't delete is print statment
   db.commit()
   db.close()
   if result[0][1]==decryptpass:
     return(1)
   else:
     return(2)
  except:
   return(0)
     
 
 

 def dslrsaved(tdata): 
  try:
   sp=tdata.split("$")
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="camerarental")
   c=db.cursor()
   c.execute("INSERT INTO cameradetails values (%s,%s,%s,%s,%s,%s,%s,%s)",(sp[0],sp[1],sp[2],int(sp[3]),sp[4],sp[5],int(sp[6]),sp[7]))
   db.commit()
   db.close()
   return("1")
  except:
   return("0")
  

 



 def getownerdetails(tdata):
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="camerarental")
   c=db.cursor()
   c.execute("select o.name,o.phone,o.email,o.cityname,o.fulladd,o.image FROM ownerdetails o where o.phone=%s",tdata)
   result=c.fetchall()
   fulldata=result[0][0]+"$"+str(result[0][1])+"$"+result[0][2]+"$"+result[0][3]+"$"+result[0][4]+"$"+img.covertfiletostring(result[0][5])
   return(fulldata)






 def getownercamera(tdata):
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="camerarental")
   c=db.cursor()
   c.execute("select c.cameraname,c.companyname,c.modelno,c.lences,c.fulldec,c.price,c.cimage FROM cameradetails c where c.ophone=%s",tdata)
   result=c.fetchall()
   fulldata=""
   for row in result:
    fulldata=fulldata+row[0]+"$"+row[1]+"$"+row[2]+"$"+row[3]+"$"+row[4]+"$"+str(row[5])+"$"+img.covertfiletostring(row[6])+"%"
   return(fulldata)
   db.commit()
   db.close()


 def cameradetails(tdata):
   db=pymysql.connect(host="localhost",user="root",passwd="root",db="camerarental")
   c=db.cursor()
   c.execute("select c.cameraname,c.companyname,c.modelno,c.lences,c.fulldec,c.price,c.cimage,c.ophone FROM cameradetails c where c.ophone in (select o.phone from ownerdetails o where o.cityname=%s)",tdata)
   result=c.fetchall()
   fulldata=""
   for row in result:
    fulldata=fulldata+row[0]+"$"+row[1]+"$"+row[2]+"$"+row[3]+"$"+row[4]+"$"+str(row[5])+"$"+img.covertfiletostring(row[6])+"$"+str(row[7])+"%"
   return(fulldata)
   db.commit()
   db.close()

 
 



async def time(websocket, path):
 print(websocket)
 data= await websocket.recv()
 tdata=data.split('%')



 if tdata[0]=="1":
  r=owner.ownersignin(tdata[1])
  if r==1:
   await websocket.send("1")
   print("docter profile details saved")
  else:
   await websocket.send("0") 
   print("unable to save the docter profile")    
   



 if tdata[0]=="2":
   status=owner.dslrsaved(tdata[1])
   if status=="0":
   	await websocket.send("0")
   else:	
    await websocket.send("1")



   


 

 
 if tdata[0]=="5":
   ownerdata=owner.getownerdetails(tdata[1])
   #print(ownerdata)
   await websocket.send(ownerdata)


   data=owner.getownercamera(tdata[1])
   data1=data.split("%")
   #print(data1)
   l=len(data1)
   
   for i in range(l-1): 
    await websocket.send(data1[i]) 
   await websocket.send("ok") 
   
  
 if tdata[0]=="55":
    
   data=owner.cameradetails(tdata[1])
   data1=data.split("%")
   #print(data1)
   l=len(data1)
   
   for i in range(l-1): 
    await websocket.send(data1[i]) 
   await websocket.send("ok") 
   


 if tdata[0]=="8":
   ownerdata=owner.getownerdetails(tdata[1])
   await websocket.send(ownerdata)

    
 
   
 
 if tdata[0]=="6":
   data=owner.login(tdata[1])
   sdata=str(data)
   print(sdata)
   await websocket.send(sdata) 




     
print("server is online")
start_server = websockets.serve(time, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

