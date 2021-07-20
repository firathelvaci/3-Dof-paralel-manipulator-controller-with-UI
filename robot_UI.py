import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import serial
import numpy as np
import math
import time
import threading
from threading import Timer
import math

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        #self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
UI=tkinter.Tk()
UI.title("3RRR User Interface")
#UI.geometry("1366x768")
X=np.array([])
Y=np.array([])
phi=np.array([])
n=0
k=0  
cap = cv2.VideoCapture(0)
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM7'
ser.writeTimeout=0
ser.open()

def printit():
    global n
    global k
    global X
    global Y
    angles=inverse_paralel(1,5,3,X[k],Y[k],phi[k],80,285)
    k=k+1
    print(angles)
    ser.write(str(int(angles[0,0])).encode('ascii'))
    ser.write(b'a')
    ser.write(b'\n')
   # time.sleep(0.05)
    ser.write(str(int(angles[0,1])).encode('ascii'))
    ser.write(b'b')
    ser.write(b'\n')
    #time.sleep(0.05)
    ser.write(str(int(angles[1,0])).encode('ascii'))
    ser.write(b'c')
    #ser.write(b'\n')
    #time.sleep(0.05)
    ser.write(str(int(angles[1,1])).encode('ascii'))
    ser.write(b'd')
    #ser.write(b'\n')
   # time.sleep(0.05)
    ser.write(str(int(angles[2,0])).encode('ascii'))
    ser.write(b'e')
    #ser.write(b'\n')
   # time.sleep(0.05)
    ser.write(str(int(angles[2,1])).encode('ascii'))
    ser.write(b'f')
    #ser.write(b'\n')
   # time.sleep(0.05)
    if n==k:
       print(k)
       rt.stop()
       n=0
       k=0
rt= RepeatedTimer(0.5, printit)

def man_a():
    ser.write(txt_a.get().encode('ascii'))
    ser.write(b'a')
def man_b():
    ser.write(txt_b.get().encode('ascii'))
    ser.write(b'b')
def man_c():
    ser.write(txt_c.get().encode('ascii'))
    ser.write(b'c')
def man_d():
    ser.write(txt_d.get().encode('ascii'))
    ser.write(b'd')
def man_e():
    ser.write(txt_e.get().encode('ascii'))
    ser.write(b'e')
def man_f():
    ser.write(txt_f.get().encode('ascii'))
    ser.write(b'f')

def rotz(tz):
    tz=np.deg2rad(tz)
    return np.array([[np.cos(tz), -1*np.sin(tz), 0], [np.sin(tz), np.cos(tz), 0], [0,0,1]])

def inverse_serial(x_loc,y_loc,a12,a23,manx,many,rot,mod):
    x_loc,y_loc,_=np.dot([x_loc,y_loc,1],rotz(rot));
    manx,many,_=np.dot([manx,many,1],rotz(rot));
    #print(x_loc,y_loc)
    x_loc=x_loc-manx;
    y_loc=y_loc-many;
    #x_loc,y_loc,z_loc =np.dot(rotz(120),[x_loc,y_loc,1])
    e=(x_loc**2+y_loc**2 - a12**2 - a23**2)/(2*a12*a23)
    if mod==0:
       global theta2
       theta2=np.arctan2(1*np.sqrt(1-e**2),e)
    if mod==1:
       theta2=np.arctan2(-1*np.sqrt(1-e**2),e)

    k1=a12+a23*np.cos(theta2)
    k2=a23*np.sin(theta2);

    theta1=np.arctan2(y_loc,x_loc)-np.arctan2(k2,k1)
    a=[theta1 ,theta2]
    
    return np.rad2deg(a)


def inverse_paralel(man1_joint,man2_joint,man3_joint,Px,Py,phi,r,r_outer):
    manx_1=r_outer*np.cos(np.deg2rad(270));
    many_1=r_outer*np.sin(np.deg2rad(270));

    manx_3=r_outer*np.cos(np.deg2rad(30));
    many_3=r_outer*np.sin(np.deg2rad(30));

    manx_2=r_outer*np.cos(np.deg2rad(150));
    many_2=r_outer*np.sin(np.deg2rad(150));
    
    man1_jointx=Px-r*np.cos(np.deg2rad(60+phi));
    man1_jointy=Py-r*np.sin(np.deg2rad(60+phi));
    r1=0
    r2=0
    r3=0
    r1_theta=0
    r2_theta=0
    r3_theta=0

    i=0
    check1=0
    check=man1_joint
    check2=0
 
    while True:
     i=i-1
     check=check-1
     if(check==0):
         check=6
     if(check==7):
         check=1
     if(check==man2_joint):
         check2=i
         break
    while True:
     i=i+1
     check=check+1
     if(check==0):
        check=6
     if(check==7):
        check=1
     if(check==man3_joint):
        check1=i
        break


    if(check1==1):
     r1=r
     r1_theta=0+phi
    if(check1==2):
     r1=r*math.sqrt(3)
     r1_theta=30+phi
    if(check1==3):
     r1=r*2
     r1_theta=60+phi
    if(check1==4):
     r1=r*2
     r1_theta=90+phi

    if(check2==-1):
     r2=r
     r2_theta=120+phi
    if(check2==-2):
     r2=r*math.sqrt(3)
     r2_theta=90+phi
    if(check2==-3):
     r2=r*2
     r2_theta=60+phi
    if(check2==-4):
     r2=r*2
     r2_theta=30+phi

    man3_jointx=math.cos(math.radians(r1_theta))*r1+man1_jointx
    man3_jointy=math.sin(math.radians(r1_theta))*r1+man1_jointy

    man2_jointx=math.cos(math.radians(r2_theta))*r2+man1_jointx
    man2_jointy=math.sin(math.radians(r2_theta))*r2+man1_jointy
   # print(Px,Py)
    p=[inverse_serial(man1_jointx,man1_jointy,335,(315+144-115),manx_1,many_1,0,0),
       inverse_serial(man2_jointx,man2_jointy,335,(315+144-115),manx_2,many_2,-120,0),
       inverse_serial(man3_jointx,man3_jointy,335,(315+144-115),manx_3,many_3,120,0)]
    #-115
    return np.array(p)



    
def path_tracing():
    global n
    for t in np.arange(0,5,0.1):
        X.resize(n+1)
        Y.resize(n+1)
        phi.resize(n+1)
        X[n]=0
        Y[n]=50*t
        phi[n]=64.58
        n=n+1
    rt.start()
path_tracing()    
label_1=tkinter.Label(UI,text="Theta_1",font=('Helvetica',8))
label_1.grid(row=0, column=2,padx=5, pady=5)
label_2=tkinter.Label(UI,text="Real Position",font=('Helvetica',8))
label_2.grid(row=0, column=3,padx=5, pady=5)
label_3=tkinter.Label(UI,text="Theta_2",font=('Helvetica',8))
label_3.grid(row=0, column=5,padx=5, pady=5)
label_4=tkinter.Label(UI,text="Real Position",font=('Helvetica',8))
label_4.grid(row=0, column=6,padx=5, pady=5)
label_5=tkinter.Label(UI,text="Connection",font=('Helvetica',8))
label_5.grid(row=0, column=8,padx=5, pady=5)
label_6=tkinter.Label(UI,text="Servos",font=('Helvetica',8))
label_6.grid(row=0, column=9,padx=5, pady=5)
label_6=tkinter.Label(UI,text="Lock Mechanism",font=('Helvetica',8))
label_6.grid(row=0, column=10,padx=5, pady=5)



label_a=tkinter.Label(UI,text="Manipulator 1",font=('Helvetica',8))
label_a.grid(row=1, column=0,padx=5, pady=5)
btn_a=tkinter.Button(UI,text="GO",command=man_a)
btn_a.grid(row=1, column=1,padx=5, pady=5)
txt_a=tkinter.Entry(UI,width="20")
txt_a.grid(row=1, column=2,padx=5, pady=5)
label_a_pos=tkinter.Label(UI,text="no information",font=('Helvetica',8))
label_a_pos.grid(row=1, column=3,padx=5, pady=5)
btn_b=tkinter.Button(UI,text="GO",command=man_b)
btn_b.grid(row=1, column=4,padx=5, pady=5)
txt_b=tkinter.Entry(UI,width="20")
txt_b.grid(row=1, column=5,padx=5, pady=5)
label_b_pos=tkinter.Label(UI,text="no information",font=('Helvetica',8))
label_b_pos.grid(row=1, column=6,padx=5, pady=5)
ma1_con=tkinter.Label(UI,text="connection testing",font=('Helvetica',8))
ma1_con.grid(row=1, column=8,padx=5, pady=5)
btn_1_servo=tkinter.Button(UI,text="Opened",command=man_b)
btn_1_servo.grid(row=1, column=9,padx=5, pady=5)
btn_1_servo=tkinter.Button(UI,text="Opened",command=man_b)
btn_1_servo.grid(row=1, column=9,padx=5, pady=5)
btn_1_lock=tkinter.Button(UI,text="Not Locked",command=man_b)
btn_1_lock.grid(row=1, column=10,padx=5, pady=5)

label_c=tkinter.Label(UI,text="Manipulator 2",font=('Helvetica',8))
label_c.grid(row=2, column=0,padx=5, pady=5)
btn_c=tkinter.Button(UI,text="GO",command=man_c)
btn_c.grid(row=2, column=1,padx=5, pady=5)
txt_c=tkinter.Entry(UI,width="20")
txt_c.grid(row=2, column=2,padx=5, pady=5)
label_c_pos=tkinter.Label(UI,text="no information",font=('Helvetica',8))
label_c_pos.grid(row=2, column=3,padx=5, pady=5)
btn_d=tkinter.Button(UI,text="GO",command=man_d)
btn_d.grid(row=2, column=4,padx=5, pady=5)
txt_d=tkinter.Entry(UI,width="20")
txt_d.grid(row=2, column=5,padx=5, pady=5)
label_d_pos=tkinter.Label(UI,text="no information",font=('Helvetica',8))
label_d_pos.grid(row=2, column=6,padx=5, pady=5)
ma2_con=tkinter.Label(UI,text="connection testing",font=('Helvetica',8))
ma2_con.grid(row=2, column=8,padx=5, pady=5)
btn_2_servo=tkinter.Button(UI,text="Opened",command=man_b)
btn_2_servo.grid(row=2, column=9,padx=5, pady=5)

label_e=tkinter.Label(UI,text="Manipulator 3",font=('Helvetica',8))
label_e.grid(row=3, column=0,padx=5, pady=5)
btn_e=tkinter.Button(UI,text="GO",command=man_e)
btn_e.grid(row=3, column=1,padx=5, pady=5)
txt_e=tkinter.Entry(UI,width="20")
txt_e.grid(row=3, column=2,padx=5, pady=5)
label_e_pos=tkinter.Label(UI,text="no information",font=('Helvetica',8))
label_e_pos.grid(row=3, column=3,padx=5, pady=5)
btn_f=tkinter.Button(UI,text="GO",command=man_f)
btn_f.grid(row=3, column=4,padx=5, pady=5)
txt_f=tkinter.Entry(UI,width="20")
txt_f.grid(row=3, column=5,padx=5, pady=5)
label_f_pos=tkinter.Label(UI,text="no information",font=('Helvetica',8))
label_f_pos.grid(row=3, column=6,padx=5, pady=5)
ma3_con=tkinter.Label(UI,text="connection testing",font=('Helvetica',8))
ma3_con.grid(row=3, column=8,padx=5, pady=5)
btn_3_servo=tkinter.Button(UI,text="Opened",command=man_b)
btn_3_servo.grid(row=3, column=9,padx=5, pady=5)

connect=tkinter.Button(UI,text="Send Values",command=path_tracing)
connect.grid(row=4, column=4,padx=5, pady=5)
connect=tkinter.Button(UI,text="Stop",command=path_tracing)
connect.grid(row=4, column=5,padx=5, pady=5)
#portlabel=tkinter.Label(UI,text="d" ,font=('Helvetica',8))
#portlabel.grid(row=4, column=2,padx=5, pady=5)

angles1=inverse_paralel(1,5,3,0,0,64.97,80,285)
#angles2=inverse_serial(315+215+335,-285,335,(315+215),0,-285,0,0)
print(angles1)
while True:
    try:
       UI.update()
       s = int(ser.read())
       print(s)
       if s==9999:
            ma1_con.config(text='not connected')
       if s==9998:
            ma1_con.config(text='connected')
       if s==8999:
            ma2_con.config(text='not connected')
       if s==8998:
            ma2_con.config(text='connected')
       if s==7999:
            ma3_con.config(text='not connected')
       if s==7998:
            ma3_con.config(text='connected')
            

    
       if s>1000 and s<2000:
            label_a_pos.config(text=(s-1500))
       if s>2000 and s<3000:
            label_b_pos.config(text=(s-2500))
       if s>3000 and s<4000:
            label_c_pos.config(text=(s-3500))
       if s>4000 and s<5000:
            label_d_pos.config(text=(s-4500))
       if s>5000 and s<6000:
            label_e_pos.config(text=(s-5500))
       if s>6000 and s<7000:
            label_f_pos.config(text=(s-6500))
       
       
    except:
      break
        

    
    


