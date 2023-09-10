from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
import cv2
import numpy as np
from kivy.clock import Clock
from datetime import datetime

class CamWid(Camera):
    def __init__(self,capture,**kwargs):
        super().__init__(**kwargs)
        self.capture=capture
    def update(self,dt):
        ret,frm=self.capture.read()
        if ret:
            frm=cv2.flip(frm,0)#frm.shape[1],frm.shape[0]
            texture=Texture.create(size=(frm.shape[1],frm.shape[0]),colorfmt='bgr')
            texture.blit_buffer(frm.tobytes(),colorfmt='bgr',bufferfmt='ubyte')
            self.texture=texture
            
class CamApp(App):
    def build(self):
        flay=FloatLayout()
        self.capture=cv2.VideoCapture(0)
        self.camera_wid=CamWid(capture=self.capture)
        Clock.schedule_interval(self.camera_wid.update,1.0/30.0)

        flay.add_widget(self.camera_wid)
        button=Button(text="Take",size_hint=(None,None),pos_hint={'x':0.5,'y':0.0},on_release=self.capturesave)
        flay.add_widget(button)
        return flay
    #save the image...
    def capturesave(self,instance):
        ret,frm=self.capture.read()
            
        if ret:
            targetsize=25
            frm=self.resize_image(frm,targetsize)
            #file name attached date and time...
            current_datetime=datetime.now()
            current_datetime=current_datetime.strftime("%H%M%S")
            current=str(current_datetime)
            #save the image
            cv2.imwrite('image_{}.jpg'.format(current),frm)
            print("Image Savef",current)
    #resize the image
    def resize_image(self,image,targetsize):
        while True:
            _,buffer=cv2.imencode(".jpg",image)
            sizekb=len(buffer)/1024
            if (sizekb<=targetsize):
                return image
            scale=np.sqrt(targetsize/sizekb)
            targetw=150
            targeth=175
            width=int(image.shape[1]*scale)
            height=int(image.shape[0]*scale)
            image=cv2.resize(image,(targetw,targeth))
            
if __name__=='__main__':
    CamApp().run()
