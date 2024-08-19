# Color Picker for windows
# A program window with a color picker for picking a (pixel) color from screen
# Shows Color values: RGB, Hexa and HSL values of the picked color
# Shows Color values for the Complementary and Triad colors
# Any value can be copied to clipboard by clicking the value


from tkinter import *
import customtkinter as ctk
from PIL import ImageGrab
import time
from threading import Thread
from os import path as ospath

def resource_path(relative_path):
    base_path = ospath.abspath(".")
    return ospath.join(base_path, relative_path)


class ColorPicker:
    def __init__(self) -> None:
        print("\n")
        print(10*"-")
        print("ColorPicker init")
        
        self.hslConverter = HSLConverter()

        self.root = ctk.CTk()
        self.root.geometry("300x400")
        self.root.minsize(200, 300)
        self.root.title('ColorPicker')

        iconPath = resource_path('favicon.ico')
        self.root.iconbitmap(iconPath)

        self.pickerWindow = None
        self.pickerHighlights = []

        # TopBar Title text (StringVar)
        self.svRgb = ctk.StringVar(value="0,0,0")
        self.svHexa = ctk.StringVar(value="#000000")
        self.svHsl = ctk.StringVar(value="0,0,0")
        self.svComplementRgb = ctk.StringVar(value="255,0,0")
        self.svComplementHexa = ctk.StringVar(value="#ffffff")
        self.svComplementHsl = ctk.StringVar(value="0,0,0")
        self.svTriad1Rgb = ctk.StringVar(value="0,0,0")
        self.svTriad1Hexa = ctk.StringVar(value="#000000")
        self.svTriad1Hsl = ctk.StringVar(value="0,0,0")
        self.svTriad2Rgb = ctk.StringVar(value="0,0,0")
        self.svTriad2Hexa = ctk.StringVar(value="#000000")
        self.svTriad2Hsl = ctk.StringVar(value="0,0,0")

        mainFrame = ctk.CTkScrollableFrame(master=self.root)
        mainFrame.pack(padx=20, pady=20, fill='both', expand=True)

        # COLOR PICK

        TopFrame = ctk.CTkFrame(mainFrame,height=30)
        TopFrame.pack(fill='x')

        pickButton = ctk.CTkButton(master=TopFrame,text="Pick",width=16,height=16,command=self.createPickEvent)
        pickButton.pack(side=LEFT,padx=(30,10))
        
        # PICKED COLOR
        pickedBox = self.createColorSection(mainFrame, "Picked Color")
        self.colorFrame = self.createColorValueWidget(pickedBox, self.svRgb, self.svHexa, self.svHsl)
        
        
        # COMPLEMENTARY
        complementBox = self.createColorSection(mainFrame, "Complementary")
        self.complementaryColorFrame = self.createColorValueWidget(complementBox, self.svComplementRgb, self.svComplementHexa, self.svComplementHsl)
        
        # TRIAD COLOR 1
        triadBox1 = self.createColorSection(mainFrame, "Triad 1")
        self.triad1ColorFrame = self.createColorValueWidget(triadBox1, self.svTriad1Rgb, self.svTriad1Hexa, self.svTriad1Hsl)
        
        # TRIAD COLOR 2
        triadBox2 = self.createColorSection(mainFrame, "Triad 2")
        self.triad2ColorFrame = self.createColorValueWidget(triadBox2, self.svTriad2Rgb, self.svTriad2Hexa, self.svTriad2Hsl)
        
        
        # OVERLAY for message: "Copied!"
        self.showingInfo = False
        self.infoOverlay = ctk.CTkFrame(master=self.root)
        self.root.lift(self.infoOverlay)

        self.infoOverlay.place(relx=0.5, rely=0.5, anchor='center')
        infoText = ctk.CTkLabel(self.infoOverlay,  height= 50, width=120, text="Copied!", font=("Courier", 24), fg_color='white', text_color='black', corner_radius=6)
        infoText.pack(padx=5, pady=5)
        self.infoOverlay.place_forget()


    def createColorSection(self, parentFrame : ctk.CTkFrame, labelText : str):
        box = ctk.CTkFrame(parentFrame)
        box.pack(fill='x')
        boxlabel = ctk.CTkLabel(box, text=labelText, fg_color="transparent")
        boxlabel.pack(fill='x')
        return box

    def createColorValueWidget(self, parentBox : ctk.CTkFrame, rgbStringVar : ctk.StringVar, hexaStringVar : ctk.StringVar, hslStringVar : ctk.StringVar):
        # Create widget rows for color values : RGB, Hexa, HSL
        # Return frame that displays the color
        
        rgbBox = ctk.CTkFrame(parentBox,height=30)
        rgbBox.pack(fill='x')
        rgbLabel = ctk.CTkLabel(rgbBox, text="RGB")
        rgbLabel.pack(side=LEFT,padx=(30,10))
        rgbValue = ctk.CTkLabel(rgbBox, textvariable=rgbStringVar, cursor="hand2")
        rgbValue.pack(side=RIGHT,padx=(10,30))
        rgbValue.bind('<Button-1>', lambda _: self.copyToClipBoard(rgbStringVar.get()))

        hexaBox = ctk.CTkFrame(parentBox,height=30)
        hexaBox.pack(fill='x')
        hexaLabel = ctk.CTkLabel(hexaBox, text="Hexa")
        hexaLabel.pack(side=LEFT,padx=(30,10))
        hexaValue = ctk.CTkLabel(hexaBox, textvariable=hexaStringVar, cursor="hand2")
        hexaValue.pack(side=RIGHT,padx=(10,30))
        hexaValue.bind('<Button-1>', lambda _: self.copyToClipBoard(hexaStringVar.get()))
        
        hslBox = ctk.CTkFrame(parentBox,height=30)
        hslBox.pack(fill='x')
        hslLabel = ctk.CTkLabel(hslBox, text="Hsl")
        hslLabel.pack(side=LEFT,padx=(30,10))
        hslValue = ctk.CTkLabel(hslBox, textvariable=hslStringVar, cursor="hand2")
        hslValue.pack(side=RIGHT,padx=(10,30))
        hslValue.bind('<Button-1>', lambda _: self.copyToClipBoard(hslStringVar.get()))

        colorBox = ctk.CTkFrame(parentBox,height=30)
        colorBox.pack(fill='x')
        emptySlot = ctk.CTkLabel(colorBox,height=30,text="")
        emptySlot.pack(side=LEFT,padx=(30,10))
        colorFrame = ctk.CTkFrame(colorBox, height=20, fg_color='black', bg_color="transparent", border_width=3)
        colorFrame.pack(side=RIGHT,padx=(10,30), pady=5)

        return colorFrame


    def run(self) -> None:
        self.root.mainloop()

    def copyToClipBoard(self, text : str):
        # print("copyToClipBoard")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

        # print("self.svComplementHexa.get()::::",self.svComplementHexa.get())
        # print("text --- input gotten::::: ", text)

        if not self.showingInfo:
            # Show info (on thread)
            t1=Thread(target=self.showInfoText) 
            t1.start()
            # self.showInfoText()

    def showInfoText(self):
        print("Show info text")
        self.infoOverlay.place(relx=0.5, rely=0.5, anchor='center')
        # self.infoLabel.configure(font=("Courier", 24))
        self.root.update_idletasks()
        self.showingInfo = True
        time.sleep(0.5)
        self.hideInfoText()

    def hideInfoText(self):
        print("Hide info text")
        # self.infoLabel.configure(font=("Courier", 1))
        # self.infoLabel.update()
        
        self.infoOverlay.place_forget()
        self.root.update_idletasks()
        self.showingInfo = False

    def createPickEvent(self):
        # Top level window that will register click as color pick
        newWindow = Toplevel(self.root)
        self.pickerWindow = newWindow
        newWindow.title("Color Picker top level")
        newWindow.overrideredirect(True)
        
        newWindow.geometry(self.getScreenDimensions(newWindow))
        newWindow.update()

        newWindow.configure(bg='black')
        newWindow.attributes("-alpha", 0.2)

        # Highlighting cursor during color pick
        hl1 = ctk.CTkCanvas(newWindow,width=50, height=1)
        hl1.place()
        hl2 = ctk.CTkCanvas(newWindow,width=50, height=1)
        hl2.place()
        hl3 = ctk.CTkCanvas(newWindow,width=1, height=50)
        hl3.place()
        hl4 = ctk.CTkCanvas(newWindow,width=1, height=50)
        hl4.place()
        self.pickerHighlights = [hl1,hl2,hl3,hl4]

        newWindow.bind("<Motion>", self.moveHighlight)
        newWindow.bind("<Button-1>", self.pickColor)

    def getScreenDimensions(self, win):
        # Pixels / inch
        # dpi = win.winfo_fpixels('1i')
        # w & h
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        print("w & h:" ,screen_width, screen_height)
        wh = str(screen_width) + "x" + str(screen_height)
        return (wh)
    
    def moveHighlight(self, event):
        cx=self.root.winfo_pointerx()
        cy=self.root.winfo_pointery()
        if self.pickerHighlights:
            self.pickerHighlights[0].place(x=cx-25, y=cy-25)
            self.pickerHighlights[1].place(x=cx-25, y=cy+25)
            self.pickerHighlights[2].place(x=cx+25, y=cy-25)
            self.pickerHighlights[3].place(x=cx-25, y=cy-25)

    def pickColor(self, event):
        print("\npickEvent ----------")
        if self.pickerHighlights:
            self.pickerHighlights = []
        if self.pickerWindow:
            self.pickerWindow.destroy()
            self.pickerWindow = None
        # one pixel
        bounds = (event.x, event.y, event.x +1, event.y +1)
        rgb = self.getPixelRGB(bounds)
        hexa = self.rgbToHexa(rgb)
        hsl = self.hslConverter.RGB2HSL(*rgb)
        print("rgb, hexa, hsl:",rgb, hexa, hsl)

        # PICKED COLOR
        self.svRgb.set(rgb)
        self.svHexa.set(hexa)
        self.svHsl.set(hsl)
        self.colorFrame.configure(fg_color=hexa)

        # COMPLEMENTARY
        complementHsl = self.hslConverter.getComplementaryHsl(*hsl)
        complementRgb = self.hslConverter.HSL2RGB(*complementHsl)
        complementHexa = self.rgbToHexa(complementRgb)
        print("complementary:",complementRgb, complementHexa, complementHsl)

        self.svComplementHsl.set(complementHsl)
        self.svComplementRgb.set(complementRgb)
        self.svComplementHexa.set(complementHexa)
        self.complementaryColorFrame.configure(fg_color=complementHexa)

        # TRIAD
        #TODO
        # Make triads with --- getTriadHsl() ---

        triad1Hsl = self.hslConverter.getTriadHsl(*hsl, True)
        triad1Rgb = self.hslConverter.HSL2RGB(*triad1Hsl)
        triad1Hexa = self.rgbToHexa(triad1Rgb)
        self.svTriad1Hsl.set(triad1Hsl)
        self.svTriad1Rgb.set(triad1Rgb)
        self.svTriad1Hexa.set(triad1Hexa)
        self.triad1ColorFrame.configure(fg_color=triad1Hexa)
        
        triad2Hsl = self.hslConverter.getTriadHsl(*hsl, False)
        triad2Rgb = self.hslConverter.HSL2RGB(*triad2Hsl)
        triad2Hexa = self.rgbToHexa(triad2Rgb)
        self.svTriad2Hsl.set(triad2Hsl)
        self.svTriad2Rgb.set(triad2Rgb)
        self.svTriad2Hexa.set(triad2Hexa)
        self.triad2ColorFrame.configure(fg_color=triad2Hexa)

    def getPixelRGB(self, bounds):
        screenimage = ImageGrab.grab(bbox=bounds, include_layered_windows=True, all_screens=True)
        rgb = screenimage.getpixel((0,0))
        print("rgb: ", rgb)
        return rgb

    def rgbToHexa(self, rgb):
        # Change to hexa with format operator %:
        # 02 means at least two digis
        # x means lower-case hexadecimal
        hexa = '#%02x%02x%02x' % rgb
        return hexa

class HSLConverter:
    # https://www.easyrgb.com/en/math.php?MATH=M18
    # Complementary calculations math by EasyRgb ! <3

    def getComplementaryHsl(self, H:float, S:float, L:float):
        complementaryHue = H + 0.5
        if complementaryHue > 1:
            complementaryHue -= 1
        complementaryHue = round(complementaryHue,3)
        return (complementaryHue, S, L)

    def getTriadHsl(self, H:float, S:float, L:float, isFirstTriad:bool):
        if isFirstTriad:
            hue = H + 1/3
        else:
            hue = H - 1/3
        if hue > 1:
            hue -= 1
        elif hue < 0:
            hue += 1
        hue = round(hue,3)
        return (hue, S, L)
    
    def RGB2HSL(self,R,G,B):
        #R, G and B input range = 0 ÷ 255
        #H, S and L output range = 0 ÷ 1.0

        var_R = ( R / 255 )
        var_G = ( G / 255 )
        var_B = ( B / 255 )

        var_Min = min( var_R, var_G, var_B )    #Min. value of RGB
        var_Max = max( var_R, var_G, var_B )    #Max. value of RGB
        del_Max = var_Max - var_Min             #Delta RGB value

        L = ( var_Max + var_Min )/ 2


        #This is a gray, no chroma...
        if ( del_Max == 0 ):
            H = 0
            S = 0

        #Chromatic data...
        else:
            if ( L < 0.5 ): 
                S = del_Max / ( var_Max + var_Min )
            else:
                S = del_Max / ( 2 - var_Max - var_Min )

            del_R = ( ( ( var_Max - var_R ) / 6 ) + ( del_Max / 2 ) ) / del_Max
            del_G = ( ( ( var_Max - var_G ) / 6 ) + ( del_Max / 2 ) ) / del_Max
            del_B = ( ( ( var_Max - var_B ) / 6 ) + ( del_Max / 2 ) ) / del_Max

            if ( var_R == var_Max ):
                H = del_B - del_G
            elif ( var_G == var_Max ):
                H = ( 1 / 3 ) + del_R - del_B
            elif ( var_B == var_Max ):
                H = ( 2 / 3 ) + del_G - del_R

            if ( H < 0 ):
                H += 1
            if ( H > 1 ):
                H -= 1

        H = round(H,3)
        S = round(S,3)
        L = round(L,3)

        return (H,S,L)

    def HSL2RGB(self,H,S,L):
        #H, S and L input range = 0 ÷ 1.0
        #R, G and B output range = 0 ÷ 255

        if ( S == 0 ):
            R = L * 255
            G = L * 255
            B = L * 255
        else:
            if ( L < 0.5 ):
                var_2 = L * ( 1 + S )
            else:
                var_2 = ( L + S ) - ( S * L )

            var_1 = 2 * L - var_2

            R = 255 * self.Hue_2_RGB( var_1, var_2, H + ( 1 / 3 ) )
            G = 255 * self.Hue_2_RGB( var_1, var_2, H )
            B = 255 * self.Hue_2_RGB( var_1, var_2, H - ( 1 / 3 ) )
        return (int(R),int(G),int(B))
    
    # Function Hue_2_RGB
    def Hue_2_RGB( self, v1, v2, vH ):
        if ( vH < 0 ):
            vH += 1
        if( vH > 1 ):
            vH -= 1
        if ( ( 6 * vH ) < 1 ):
            return ( v1 + ( v2 - v1 ) * 6 * vH )
        if ( ( 2 * vH ) < 1 ):
            return ( v2 )
        if ( ( 3 * vH ) < 2 ):
            return ( v1 + ( v2 - v1 ) * ( ( 2 / 3 ) - vH ) * 6 )
        return ( v1 )
        

app = ColorPicker()
app.run()