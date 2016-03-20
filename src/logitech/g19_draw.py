

import PIL.Image as Img
import PIL.ImageColor
import os
import ImageFont
import Image, ImageDraw

class G19Draw(object):

    def __init__(self):
        pass
        
    def draw(self, canvas=None):
        return canvas;

        
class G19DrawCanvas(G19Draw):

    def __init__(self, lines, font):
        self.__drawObjects = [];
        self.__drawTextLines = [];
        self.__font = font;
        self.__x = 0;
        self.__y = 0;
        self.__center = False;
        for i in range(0,lines):
            text = G19DrawText(font);
            text.setPos(20, 20+i*30)
            self.__drawObjects.append(text)
            self.__drawTextLines.append(text)
            
    def draw(self, canvas=None, clean = True):
        if clean or canvas==None:
            canvas=Img.new("RGB", (320, 240));
        drawobject = ImageDraw.Draw(canvas)
        for obj in self.__drawObjects:
            obj.draw(drawobject);
        del drawobject;
        return canvas;
        
    def clearText(self):
        for i in self.__drawTextLines:
            i.clear();
        
    def setText(self, text, line=1, clear=False, center=False, color="white"):
        if clear:
            self.clearText()
        self.__drawTextLines[line-1].setText(text)
        self.__drawTextLines[line-1].setCenter(center)
        self.__drawTextLines[line-1].setColor(color)

class G19DrawText(G19Draw):
    
    def __init__(self, font):
        self.__text = "";
        self.__color = PIL.ImageColor.getrgb("rgb(255,255,255)");
        self.__font = font;
        self.__x = 0;
        self.__y = 0;
        self.__center = False;
        
    def draw(self, canvas):
        drawx = self.__x
        if self.__center:
            drawx = ( 320 - canvas.textsize(self.__text, font=self.__font)[0] ) / 2
        canvas.text((drawx, self.__y), self.__text, fill=self.__color, font=self.__font)
        
    def setText(self, text):
        self.__text = text;
        
    def setCenter(self, center):
        self.__center = center;
        
    # Use strings, can use:
    #   "#rgb"
    #   "#rrggbb"
    #   "rgb(red, green, blue)" (x% or 0-256)
    #   "hsl(hue, saturation%, lightness%)"
    #   color names: "red", "Red", "green"
    def setColor(self, color):
        self.__color = PIL.ImageColor.getrgb(color);
        
    def clear(self):
        self.__text = "";
        self.__center = False;
        self.__color = PIL.ImageColor.getrgb("rgb(255,255,255)");
        
    def setPos(self, x, y):
        self.__x = x;
        self.__y = y;
