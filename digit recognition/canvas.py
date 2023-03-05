import customtkinter
from tkinter import Canvas
from PIL import Image, ImageGrab, ImageTk, ImageOps
import tensorflow as tf
import cv2
#import win32gui
import numpy as np



root = customtkinter.CTk()
root.resizable(False, False)
#root.geometry("1000x800")

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  



frame1 = customtkinter.CTkFrame(master=root)
frame1.pack(padx=20,pady=60, expand=True, fill="both")

canvas_2 = Canvas(frame1, width=500, height=500, bg='white')
canvas_2.pack(padx=60, pady=60,side='right')

canvas = Canvas(frame1, width=500, height=500, bg='white')
canvas.pack(padx=20, pady=60,side='left')

switch_var = customtkinter.StringVar(value="off")



def switch_event():
    #print("switch toggled, current value:", switch_var.get())
    pass

def tobinary(): # turning image to binary from grayscale for our model
    im_gray = cv2.imread('TEMP/temp.png')  #cv2.CV_LOAD_IMAGE_GRAYSCALE
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)
    im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
    thresh = 147
    cv2.imwrite('TEMP/binary_image.png', im_bw)
    plot_image = Image.open('TEMP/binary_image.png').resize((500, 500))
    plot_image.save('TEMP/binary_500.png')
    
    
'''
def getter(widget=canvas):
    x=root.winfo_rootx()+widget.winfo_x()+25 # + calculations are self-made based on the plot size 
    y=root.winfo_rooty()+widget.winfo_y()+75 # + DONT CHANGE
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save("TEMP/temp.png")  
    image = Image.open('TEMP/temp.png').resize((28, 28)) # Saving image in 28 x 28 format 
    image.save("TEMP/temp.png")
    plot_image = image.resize((500, 500)) # Image for the plotting 
    plot_image.save('TEMP/temp_500.png')
'''
    
def getter(): # Collecting the image of number from original canvas

    '''
    coor = canvas.winfo_id()  # get the handle of the canvas
    rect = win32gui.GetWindowRect(coor)  # get the coordinate of the canvas
    im = ImageGrab.grab(rect).resize((28, 28))
    '''
    
    x, y = (canvas.winfo_rootx(),
            canvas.winfo_rooty())
    width, height = (canvas.winfo_width(), 
                     canvas.winfo_height())
    a, b, c, d = (x, y, x+width, y+height)
    im = ImageOps.invert(ImageGrab.grab(bbox=(a,b,c,d)).resize((28,28)))
    im.save("TEMP/temp.png")
    #print(im.size)
    
    plot_image = im.resize((500, 500)) # Image for the plotting 
    plot_image.save('TEMP/temp_500.png')
    
 
 

def nn(): # Loading and using NN model, printing results
    img = tf.image.rgb_to_grayscale(tf.keras.preprocessing.image.load_img('TEMP/binary_image.png')) / 255
    img = tf.reshape(img,(1,28,28,1)) 
    nn = tf.keras.models.load_model('tf-cnn-model.h5') # there are 3 different models to use Two of them called NN are created by me and one is external
    result = nn.predict(img)
    #print(result.argmax())
    #print(result)
    #print(tf.reduce_max(result))
    label_1.configure(text=result.argmax())
    

def plot(switch_val = switch_var): # Plotting the image regarding to the switch position 
    while switch_val.get() == "off":
        img = ImageTk.PhotoImage(Image.open('TEMP/temp_500.png'))
        canvas_2.create_image(0,0, anchor="nw",image=img)
        canvas_2.update()
    while switch_val.get() == "on":
        img = ImageTk.PhotoImage(Image.open('TEMP/binary_500.png'))
        canvas_2.create_image(0,0, anchor="nw",image=img)
        canvas_2.update()
    else:
        plot()
        

    

def scan(): # The function is uniting the function to get and predict the image, additionaly this function will show result on the plot
    getter()
    tobinary()
    nn()
    plot()
    label_1.update()
    

def click(click_event):
    global prev
    prev = click_event
    
def erase(move_event):
    global prev
    canvas.create_line(prev.x, prev.y, move_event.x, move_event.y,width=50, fill='white')
    prev = move_event

def paint(move_event):
    global prev
    canvas.create_line(prev.x, prev.y, move_event.x, move_event.y, width=20)
    prev = move_event  

def clear():
    canvas.delete("all")
    canvas_2.delete('all')
    label_1.text="" 



frame2 = customtkinter.CTkFrame(master=frame1,width=200,height=200,corner_radius=10)
frame2.pack(padx=20, pady=20, side='top')

frame3 = customtkinter.CTkFrame(master=frame1,width=200,height=200,corner_radius=10)
frame3.pack(padx=20, pady=20, side='bottom')

label_1 = customtkinter.CTkLabel(master=frame2, text='',font=('Arial',100))
label_1.place(relx=0.35, rely=0.25)


button_1 = customtkinter.CTkButton(master=frame3, text="Scan", command= scan)
button_1.pack(ipadx=30, ipady=6,side='bottom')


button_2 = customtkinter.CTkButton(master=frame3, text="Clear", command=clear)
button_2.pack(pady=12,padx=10,side='bottom')


switch_1 = customtkinter.CTkSwitch(master=frame3, text="Binary_image", command=switch_event,
                                   variable=switch_var, onvalue="on", offvalue="off")
switch_1.pack(padx=20, pady=10, side="bottom")

 
canvas.bind('<Button-1>', click)
canvas.bind('<B1-Motion>', paint)
canvas.bind('<B3-Motion>', erase)
canvas.bind('<Button-2>', clear)



root.mainloop()

#! In the end use object-oriented programming for a better files organization