
import pygame, time
from pygame.locals import *
import socket
import threading
import pyaudio

# Define width and height of img
IMG_WIDTH = 48
IMG_HEIGHT = 48

# Define window size
WIN_WIDTH = 780
WIN_HEIGHT = 1024
#WIN_SIZE = (WIN_WIDTH,WIN_HEIGHT)

# Define offset for score display
OFFSET = 80

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 255)
black = (0,0,0)
white = (255,255,255)
BLUE=(176,224,230)
red = (200,0,0)
green = (0,200,0)
WIN_SIZE = (WIN_WIDTH,WIN_HEIGHT)

pygame.init()
screen = pygame.display.set_mode(WIN_SIZE)

pygame.display.set_caption('Pygame Keyboard Test')
pygame.mouse.set_visible(1)
def text_objects(text, font):
    textSurface = font.render(text, True,BLACK)
    return textSurface, textSurface.get_rect()
def display(msg,height=200):
    smallText = pygame.font.Font('fonts/AvenirMedium.ttf', 36)# pygame.font.SysFont("comicsansms",40)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (410,height)
    screen.blit(textSurf, textRect)

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while 1:
            try:
                self.target_ip = input('Enter IP address of server --> ')#ip address
                self.target_port = int(input('Enter target port of server --> '))#port

                self.s.connect((self.target_ip, self.target_port))

                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 2#stereo audio
        rate = 44100

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Connected to Server")
        """receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()"""

    def receive_server_data(self):
        while True:
            data = self.s.recv(1024)
            if(mute==0):
                self.playing_stream.write(data)


    def send_data_to_server(self):
        data = self.recording_stream.read(1024)
        self.s.sendall(data)
bg_surface=pygame.image.load('background.jpg').convert_alpha()
bg_surface = pygame.transform.scale(bg_surface, (WIN_WIDTH,WIN_HEIGHT))
screen.blit(bg_surface,(0,0))
display("ENTER THE PORT NUMBER",200)
pygame.display.update()

mic=0
mute=0
client = Client()


t = threading.Thread(target=client.receive_server_data).start()
while True:
    bg_surface=pygame.image.load('in_call.png').convert_alpha()
    bg_surface = pygame.transform.scale(bg_surface, (WIN_WIDTH,WIN_HEIGHT))
    screen.blit(bg_surface,(0,0))

    op3surface = pygame.image.load('mic_mute.png').convert_alpha()
    op3surface = pygame.transform.scale(op3surface, (70,70))
    op3_box = op3surface.get_rect(center = ((WIN_WIDTH/2-170,WIN_HEIGHT/2+400)))

    op4surface = pygame.image.load('mic_on.png').convert_alpha()
    op4surface = pygame.transform.scale(op4surface, (70,70))
    op4_box = op4surface.get_rect(center = ((WIN_WIDTH/2-170,WIN_HEIGHT/2+400)))

    op5surface = pygame.image.load('mute_speaker.jpeg').convert_alpha()
    op5surface = pygame.transform.scale(op5surface, (70,70))
    op5_box = op3surface.get_rect(center = ((WIN_WIDTH/2+170,WIN_HEIGHT/2+400)))

    op6surface = pygame.image.load('speaker_on.png').convert_alpha()
    op6surface = pygame.transform.scale(op6surface, (70,70))
    op6_box = op6surface.get_rect(center = ((WIN_WIDTH/2+170,WIN_HEIGHT/2+400)))

    quitsurface = pygame.image.load('quit.png').convert_alpha()
    quitsurface = pygame.transform.scale(quitsurface, (110,80))
    quit_box= quitsurface.get_rect(center = ((WIN_WIDTH/2,WIN_HEIGHT/2+400)))
    
    #screen.blit(op3surface,op3_box)
    screen.blit(op4surface,op4_box)
    #screen.blit(op5surface,op5_box)
    screen.blit(op6surface,op6_box)
    screen.blit(quitsurface,quit_box)
    display("I N  C A L L .........",WIN_HEIGHT/2)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if (event.type == KEYUP) or (event.type == KEYDOWN):
        if (event.key==pygame.K_m):            
            print ("muted")
            mute=1
            display("muted")
        if(event.key==pygame.K_u):
            print("unmuted")
            display("unmuted")
            mute=0
        if(event.key==pygame.K_l):
            print("microphone is off")
            mic=1
            display("microphone is off")
        if(event.key==pygame.K_p):
            mic=0
            print("microphone is on")
            display("microphone is on")
      if event.type == pygame.MOUSEBUTTONUP:
        if(quit_box.collidepoint(pygame.mouse.get_pos())):
            pygame.quit()
            quit()
        if mute==1:
            if(op6_box.collidepoint(pygame.mouse.get_pos())):
                display("unmuted")
                mute=0
        else:
            if(op5_box.collidepoint(pygame.mouse.get_pos())):
                display("muted")
                mute=1
        if mic==1:
            if(op3_box.collidepoint(pygame.mouse.get_pos())):
                display("mic_off")
                mic=0     
        else:
            if(op4_box.collidepoint(pygame.mouse.get_pos())):
                display("mic_on")
                mic=1
    if(mic==0):
        client.send_data_to_server()
        screen.blit(op4surface,op4_box)
    else:
        screen.blit(op3surface,op3_box)
    if(mute==0):
        screen.blit(op6surface,op6_box)
    else:
        screen.blit(op5surface,op5_box)
    pygame.display.update()    

