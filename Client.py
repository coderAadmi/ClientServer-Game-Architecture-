import threading
import pygame as pg
import socket
run=True
x_x=0

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),12345))
print('connected')
pg.init()

screen=pg.display.set_mode((500,500))

msg=''
s.setblocking(0)
import time
def fun(x):
    global msg
    global run
    while run:
        if msg:
            s.send(msg.encode('utf-8'))
        time.sleep(1/40)

def recv(x):
    global run
    global x_x
    while run:
        try:
            msg=s.recv(1024)
            if 'QUIT'.encode('utf-8') in msg:
                s.close()
                print('closed')
                run=false
                break
                
            if msg:
                if 'LEFT'.encode('utf-8') in msg:
                    x_x-=5
                if 'RIGHT'.encode('utf-8') in msg:
                    x_x+=5
            time.sleep(1/40)
        except:
            pass
        
def game(x):
    global run
    x=0
    global msg
    clock=pg.time.Clock()
    while run:
        clock.tick(40)
        msg=''
        for event in pg.event.get():
            if event.type==pg.QUIT:
                msg+=' QUIT'
                run=False
        keys=pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            x-=5
            msg+=' LEFT'
        if keys[pg.K_RIGHT]:
            x+=5
            msg+=' RIGHT'
        screen.fill((255,100,0))
        pg.draw.rect(screen,(0,0,0),(40+x,40,100,100))
        pg.draw.rect(screen,(100,0,100),(40+x_x,300,100,100))
        pg.display.flip()
    pg.quit()
    print('game closed')
    msg=''
    
t1=threading.Thread(target=fun,args=('polo',))
t2=threading.Thread(target=recv,args=('habibi',))
t1.start()
t2.start()
game('kk')
s.close()