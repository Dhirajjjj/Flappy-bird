
import tkinter
from tkinter import PhotoImage, Text
from tkinter import *
from PIL import ImageTk, Image
from functools import partial
import random
import sqlite3

root = tkinter.Tk()
root.maxsize(600, 0)



#player
x = 300 
y = 500

#wall
wall_var1 = 0
wall_var2 = 0

#commands
i = 0        #stops the spacebar event to repeat itself also does other stuff
clock = 0    #global time counter

#images
background_img = ImageTk.PhotoImage(Image.open("assets/flappy_sky_bgv2.png"))
cloud_img = ImageTk.PhotoImage(Image.open("assets/flappy_cloud.png"))
flappy_img = ImageTk.PhotoImage(Image.open("assets/flappy_birdv3.png"))
start_img = ImageTk.PhotoImage(Image.open("assets/start_textv22.png"))
wall_img = ImageTk.PhotoImage(Image.open("assets/wall_imgv3.png"))
# ded_txt_img = ImageTk.PhotoImage(Image.open("ded_txtv1.png"))
ded_txt_img = ImageTk.PhotoImage(Image.open("assets/start_textv22.png"))
score_txt_img = ImageTk.PhotoImage(Image.open("assets/score_txtv1.png"))
login_bg_img = ImageTk.PhotoImage(Image.open("assets/login_bgv2.png"))
login_btn_img = ImageTk.PhotoImage(Image.open("assets/login_btn_img.png"))
score_btn_img = ImageTk.PhotoImage(Image.open("assets/score_btn_img.png"))
enter_btn_img = ImageTk.PhotoImage(Image.open("assets/enter_btn_img.png"))
back_btn_img = ImageTk.PhotoImage(Image.open("assets/back_btn_img.png"))

canvas = tkinter.Canvas(master = root, bg="grey", width=400, height=500)
canvas.pack(fill = "both", expand = True)
canvas.create_image(0, 0, image=background_img, anchor="nw")

root.title("flappy")


#top cloud border
cloud1 = canvas.create_image(0, 0, image=cloud_img, anchor="nw")
cloud2 = canvas.create_image(700, 0, image=cloud_img, anchor="nw")
cloud3 = canvas.create_image(1400, 0, image=cloud_img, anchor="nw")
#bottom cloud border
cloud4 = canvas.create_image(0, 850, image=cloud_img, anchor="nw")
cloud5 = canvas.create_image(700, 850, image=cloud_img, anchor="nw")
cloud6 = canvas.create_image(1400, 850, image=cloud_img, anchor="nw")

start_player = canvas.create_image(x, y, image=flappy_img)
start_text = canvas.create_image(300, 700, image=start_img)

def time():
    global clock, watch
    
    clock += 1
    watch = root.after(1000, time)
    
def starting_img():
    global start_player, start_text, log_btn, highscore_btn
    
    start_player = canvas.create_image(x, y, image=flappy_img)
    start_text = canvas.create_image(300, 700, image=start_img)

    log_btn = tkinter.Button(root, image=login_btn_img, command=login_screen, bd=0, bg="#00e5ff")
    log_btn.place(x=50, y=150)

    highscore_btn = tkinter.Button(root, image=score_btn_img, command=highscore_screen, bd=0, bg="#00e5ff")
    highscore_btn.place(x=50, y=250)

def delete_everything():
    canvas.delete("all")

#Starting images
def game_reset():
    global start_player, start_text, i, cloud1, cloud2, cloud3, cloud4, cloud5, cloud6
    
    i = 0
    
    canvas.create_image(0, 0, image=background_img, anchor="nw")
    
    #top cloud border
    cloud1 = canvas.create_image(0, 0, image=cloud_img, anchor="nw")
    cloud2 = canvas.create_image(700, 0, image=cloud_img, anchor="nw")
    cloud3 = canvas.create_image(1400, 0, image=cloud_img, anchor="nw")
    #bottom cloud border
    cloud4 = canvas.create_image(0, 850, image=cloud_img, anchor="nw")
    cloud5 = canvas.create_image(700, 850, image=cloud_img, anchor="nw")
    cloud6 = canvas.create_image(1400, 850, image=cloud_img, anchor="nw")
    
def stop_process():
    global wall_proc, generate_proc, gravity_proc
    root.after_cancel(wall_proc)
    root.after_cancel(generate_proc)
    root.after_cancel(gravity_proc)
    root.after_cancel(watch)
    
def highscore():
    canvas.delete("all")
    game_reset()
    canvas.create_text(100, 50, fill="black", text="score:", font="200")

def scoreboard(time):
    global i
    i = 1

    print("score:",time)
    var = IntVar()
    var.set(time)
    
    ded_txt = canvas.create_image(250, 200, image=ded_txt_img)
    score_txt = canvas.create_image(250, 300, image=score_txt_img)
    ded_time = canvas.create_text(250, 400, fill="purple", text=var.get(), font=("Helvetica",50, "bold"))

    root.after(5000, delete_everything)
    root.after(5000, game_reset)
    root.after(5000, starting_img)


def delete_starting_img():
    canvas.delete(start_player, start_text)
    log_btn.destroy()
    highscore_btn.destroy()

def check_collision():
    global clock
    time = clock
             
    result = len(canvas.find_overlapping(canvas.coords(player)[0], canvas.coords(player)[1],
                              canvas.coords(player)[0]+30, canvas.coords(player)[1]+30))
    
    collision_repeater = root.after(10, check_collision)
    
    if result>2:
        print("DED")
        print("Time: ", clock, "sec")
        clock = 0
        root.after_cancel(collision_repeater)
        stop_process()
        canvas.delete("all")
        game_reset()
        scoreboard(time)

        #database part--
        conn = sqlite3.connect('flappy_test.db')
        db = conn.cursor()

        db.execute("SELECT * FROM user ORDER BY user_name DESC LIMIT 1")
        records = db.fetchone()
        result = str(records[0])

        print(time, result)

        db.execute("INSERT INTO highscore VALUES (:user_name, :score)",
            {
                "user_name" : result,
                "score" : time
            })

        conn.commit()
        conn.close()

def random_number():
    random_no = random.randint(50, 600)
    return random_no

def move_wall(wallAbv, wallBlw):
    global wall_proc
    
    canvas.move(wallAbv, -1, 0)
    canvas.move(wallBlw, -1, 0)
    wall_proc = root.after(30, move_wall, wallAbv, wallBlw) 
    
def delete_wall(wallAbv, wallBlw):
    canvas.delete(wallAbv, wallBlw)

def generate_walls():
    global generate_proc
    
    val = random_number()
    wallAbv = canvas.create_image(800, val-325, image=wall_img)
    wallBlw = canvas.create_image(800, 550 + val, image=wall_img)
    move_wall(wallAbv, wallBlw)
    root.after(40000, delete_wall, wallAbv, wallBlw)
    generate_proc = root.after(8000, generate_walls)
    
#Ingame gravity
def gravity():
    global gravity_proc
    
    x = 0
    y = 1
    canvas.move(player, x, y)
    gravity_proc = root.after(5, gravity)
    
#jump action
def jump():
    jump_no = random.randint(4, 10)
    for val in range(10):
        canvas.move(player, 0, -jump_no)
 
def spacebar(event):
    global i

    if event.char == "x":
        highscore()

    if event.char == " ":
        
        if i<1:
           global player
           i += 1
           player = canvas.create_image(x, y, image=flappy_img, anchor="nw")
           delete_starting_img()
           time()
           gravity()
           generate_walls()
           check_collision()
           
        jump()
        
        
#Keybinds
root.bind("<Key>", spacebar)

def validateLogin(username, password):
    print("username entered :", username.get())
    print("password entered :", password.get())

    conn = sqlite3.connect('flappy_test.db')
    db = conn.cursor()

    db.execute(" INSERT INTO user VALUES (:user_name, :pass_word)",
        {
            "user_name" : username.get(),
            "pass_word" : password.get()
        })
        

    conn.commit()
    conn.close()

    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)

def home_screen():
    global back_btn, i
    
    if i == 2 :
        highscore_label.destroy()

    if i == 1:
        usernameEntry.destroy()
        passwordEntry.destroy()
        final_login_btn.destroy()

    i = 0

    canvas.delete("all")
    back_btn.destroy()
    game_reset()
    starting_img()


def login_screen():
    global cloud1, cloud4, back_btn, passwordLabel, usernameLabel, passwordEntry, usernameEntry, i, validateLogin, final_login_btn
    i = 1

    #background
    canvas.create_image(0, 0, image=background_img, anchor="nw")
    cloud1 = canvas.create_image(0, 0, image=cloud_img, anchor="nw")
    cloud4 = canvas.create_image(0, 850, image=cloud_img, anchor="nw")
    canvas.create_image(75, 200, image=login_bg_img, anchor="nw")

    username_txt = canvas.create_text(225, 340, text="username:", fill="black")
    username = StringVar()
    canvas.create_line(200, 370, 320, 370, fill="black")
    usernameEntry = Entry(root, textvariable=username, bg="#FF9800", bd=0) 
    usernameEntry.place(x=200, y=350)

    password_txt = canvas.create_text(225, 390, text="password:", fill="black") 
    password = StringVar()
    canvas.create_line(200, 420, 320, 420)
    passwordEntry = Entry(root, textvariable=password, show='*', bg="#FF9800", bd=0)  
    passwordEntry.place(x=200, y=400)

    validateLogin = partial(validateLogin, username, password)

    #login button
    final_login_btn = tkinter.Button(root, image=enter_btn_img, command=validateLogin, bd=0, bg="#FF9800")
    final_login_btn.place(x=250, y =450) 

    back_btn = tkinter.Button(root, image=back_btn_img, command=home_screen, bd=0, bg="#84ffff")
    back_btn.place(x=250, y=700)

    log_btn.destroy()
    highscore_btn.destroy()

def highscore_screen():
    global cloud1, cloud4, back_btn, i, clock, highscore_label
    i = 2

    conn = sqlite3.connect('flappy_test.db')
    db = conn.cursor()

    db.execute("SELECT * FROM highscore ORDER BY score DESC")
    records = db.fetchmany(10)

    print_records = " "
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + "\n"

    highscore_label = Label(root, text=print_records, font=("Helvetica",16, "bold"), padx=10, pady=10, bg="#FF9800", bd=0)
    highscore_label.place(x=200, y=250)

    conn.commit()
    conn.close()

    #background
    canvas.create_image(0, 0, image=background_img, anchor="nw")
    cloud1 = canvas.create_image(0, 0, image=cloud_img, anchor="nw")
    cloud4 = canvas.create_image(0, 850, image=cloud_img, anchor="nw")
    canvas.create_image(75, 200, image=login_bg_img, anchor="nw")

    back_btn = tkinter.Button(root, image=back_btn_img, command=home_screen, bd=0, bg="#84ffff")
    back_btn.place(x=250, y=700)

    log_btn.destroy()
    highscore_btn.destroy()



log_btn = tkinter.Button(root, image=login_btn_img, command=login_screen, bd=0, bg="#00e5ff")
log_btn.place(x=50, y=150)

highscore_btn = tkinter.Button(root, image=score_btn_img, command=highscore_screen, bd=0, bg="#00e5ff")
highscore_btn.place(x=50, y=250)

root.mainloop()


# #FF9800 orange (login)
# #FFC107 golden (login) 
# #84fff skyblue (back)