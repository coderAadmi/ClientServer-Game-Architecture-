import socket
import time
import threading
import pygame as pg
pg.init()
run=True
x_x=0
screen=pg.display.set_mode((500,500))
pg.display.set_caption('Server')

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((socket.gethostname(),12345))

server.listen(5)
c,addr=server.accept()
print('connected to ',addr)

c.setblocking(0)
def recv(x):
    global run
    global x_x
    while run:
        try:
            msg=c.recv(1024)
            if 'QUIT'.encode('utf-8') in msg:
                c.close()
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
        
def send(x):
    global msg
    global run
    while run:
        try:
            if msg:
                c.send(msg.encode('utf-8'))
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
        screen.fill((0,100,250))
        pg.draw.rect(screen,(0,0,0),(40+x_x,40,100,100))
        pg.draw.rect(screen,(100,0,100),(40+x,300,100,100))
        pg.display.flip()
    pg.quit()
    print('game closed')
    msg=''
    
t1=threading.Thread(target=recv,args=('x',))
t2=threading.Thread(target=send,args=('x',))
t1.start()
t2.start()
game('k')

