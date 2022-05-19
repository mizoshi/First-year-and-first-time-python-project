from tkinter import *
import os, sqlite3, tkinter.messagebox, re, yagmail, random

def get_username_f_db(usernametext):
    #Recive username from username textbox.
    username = usernametext.get()
    if username == None:
        username = '0'
    
    #connect to DB and pull data from DB to check if there are duplicates.
    conn = sqlite3.connect(r"D:/Visual Basic/Python/Project_Python/DB/userdata.db")
    c    = conn.cursor()
    c.execute("SELECT * FROM userdata WHERE USERNAME=?", (username,))
    checkuser = c.fetchone()
    conn.close()
    return username,checkuser

def confirmpassword(passtxt, cpasstxt):
    password = passtxt.get()
    c_pass   = cpasstxt.get()
    #Check password are not empty.
    if password == None:
        tkinter.messagebox.showwarning('Warning!', 'Your password is empty.')
        checkpassword = False
    elif len(password) < 8 or len(password) > 30:
        checkpassword = False
        tkinter.messagebox.showwarning('Warning!', 'Your password must have 8 - 30 charecters.')
    elif len(password) >= 8 or len(password) <= 30:
        checkpassword = True
    else:
        tkinter.messagebox.showwarning('Warning!', 'Wrong input!.')
        checkpassword = False

    #Check passwords are match.
    if c_pass   != password:
        tkinter.messagebox.showwarning('Warning!', 'Your passwords not match.')
        checkc_pass = False
    elif c_pass == password:
        checkc_pass = True
    else:
        tkinter.messagebox.showwarning('Warning!', 'Your passwords not match.')
        checkc_pass = False

    if checkc_pass == True and checkpassword == True:
        return True
    else: return False

def random_code():
    #chenge format (List to String)
    def ltos_():
            x = []
            ltos = map(str, number)
            x = list(ltos)
            txt1 = []
            for i in range(len(x)):
                    txt1.append(x[i])
            txt2 = ' '.join([str(elem) for elem in txt1])
            return txt2

    number = []
    for i in range(6):
            n = random.randint(0,9)
            number.append(n)
    #Final code
    code = ltos_()
    return code

def recovery_email(useremail,recov_code, username):
    email = useremail
    user_email = "prejpbypandp@gmail.com"
    user_password = "P123456789p"
    yag = yagmail.SMTP(user_email,user_password,)
    recipients = email
    subject = 'Pre-Japan Store Recovery password'
    body = ["Dear",username,'\n',
            "The code to recovery your password is :",recov_code,'\n',
            "Do not copy and paste the code in the code box. Only allowed to type code in the code box.",'\n\n',
            'Thank you for using Pre-Japan Store.']

    yag.useralias = 'PRE-JAPAN Store'
    yag.send(to=recipients,subject=subject,contents=body)
                            
#Add product to cart
def pdtidotlist(count):
    if len(listid) < 14:
        showtextadded = Label(root, text="Added", font=("Coves", "11"),bg = 'White')
        showtextadded.place(x=1025, y=595)
        root.after(1000, showtextadded.destroy)
        listid.append(count)
    elif len(listid) >= 14:
        tkinter.messagebox.showerror('Cart is full!', 'There are 14 products in your cart, Your cart.')

def start():

    def home():

        def login():
            #Login part
            def checkuser():
                username  = usernametext.get()
                password  = newpasstext.get()
                usertuple = get_username_f_db(usernametext)
                checkuser  = usertuple[1]
                if checkuser == None:
                    tkinter.messagebox.showerror('Something wrong!','Username or password is incorrect.')
                elif checkuser[1] == username and checkuser[2] == password:
                    tkinter.messagebox.showinfo('SUCCESS!','Login complete.')
                    menu()
                elif checkuser[1] != username and checkuser[2] == password:
                    tkinter.messagebox.showerror('Something wrong!','Username or password is incorrect.')
                elif checkuser[1] == username and checkuser[2] != password:
                    tkinter.messagebox.showerror('Something wrong!','Username or password is incorrect.')
                elif checkuser[1] != username and checkuser[2] != password:
                    tkinter.messagebox.showerror('Something wrong!','Username or password is incorrect.')
                else:
                    tkinter.messagebox.showerror('Something wrong!','Username or password is incorrect.')
            #End login part 

            #Recovery part
            def forgotpass():
                def check_and_confirm():
                    input_code = codetext.get()
                    input_code = str(input_code)

                    #covert code from user to recovery code format
                    n1 = map(str, input_code)
                    x = list(n1)
                    txt1 = []
                    for i in range(len(x)):
                        txt1.append(x[i])
                    usercode = ' '.join([str(elem) for elem in txt1])

                    #check recovery code.
                    if usercode == recov_code:
                        #check password.
                        checkpass = confirmpassword(newpasstext, connewpasstext)

                        if checkpass == True:
                            username = usernametext.get()
                            newpassword = newpasstext.get()
                                    
                            conn = sqlite3.connect(r"D:/Visual Basic/Python/Project_Python/DB/userdata.db")
                            c    = conn.cursor()
                            data = (newpassword, username)
                            c.execute('''UPDATE userdata SET PASSWORD =? WHERE USERNAME =?''', data,)
                            conn.commit()
                            c.close()

                            tkinter.messagebox.showinfo('Completed','Recovery completed!')
                            login()
                        else:...

                    elif usercode != recov_code:
                            tkinter.messagebox.showerror('Error', 'Your recovery code is incorrect please try again.')
                            forgotpass()
                    else:
                            tkinter.messagebox.showerror('Error', 'Your recovery code or password is incorrect please try again.')
                            forgotpass()
                def send_code():
                    username = usernametext.get()
                    x = get_username_f_db(usernametext)
                    userinfo = x[1]
                    if userinfo == None:
                        tkinter.messagebox.showerror('Error', 'This username does not exist in the our store.')
                    else:
                        useremail = userinfo[5]
                        recovery_email(useremail, recov_code, username)
                
                
                recov_code = str(random_code())
                #BG
                rbg = Label(root, image = recovebg)
                rbg.place(x = 0,y = 0)

                rtxt = Label(root, text = 'Recovery Password', font= ('Coves Bold', 22), bg = 'White')
                rtxt.place(x = 700, y = 150)

                #text : username
                usernametxt = Label(root, text = 'Username',font = ('Coves Bold',15), bg = 'White')
                usernametxt.place(x = 543, y = 210)

                #textbox to input username.
                usernametext = StringVar()
                tbcode  = Entry(root, font=('Coves',20), textvariable = usernametext, width = 25, bd = 0)
                tbcode.config({'background':'#d4e4f9'})
                tbcode.place(x = 543, y = 240)
                
                #send email button.
                checkbtn = Button(root, text = "Send recovery code", font = ('Coves', 13), bd = 1, command = send_code)
                checkbtn.place(x = 960, y = 205)

                #text : code
                codetxt = Label(root, text = 'Recovery code (6 digits)',font = ('Coves Bold',15), bg = 'White')
                codetxt.place(x = 543, y = 290)

                #textbox to input username.
                codetext = StringVar()
                tbcode  = Entry(root, font=('Coves',20), textvariable = codetext, width = 25, bd = 0)
                tbcode.config({'background':'#d4e4f9'})
                tbcode.place(x = 543, y = 320)

                #text : New Password
                npasstxt = Label(root, text = 'New Password',font = ('Coves Bold',15), bg = 'White')
                npasstxt.place(x = 543, y = 380)
                
                #textbox to input password.
                newpasstext = StringVar()
                tbnpass  = Entry(root, font=('Coves',20), textvariable = newpasstext, width = 25, bd = 0)
                tbnpass.config({'background':'#d4e4f9'})
                tbnpass.place(x = 543, y = 410)

                 #text : New Password
                cnpasstxt = Label(root, text = 'Confirm New Password',font = ('Coves Bold',15), bg = 'White')
                cnpasstxt.place(x = 543, y = 460)
                
                #textbox to input password.
                connewpasstext = StringVar()
                tbcnpass  = Entry(root, font=('Coves',20), textvariable = connewpasstext, width = 25, bd = 0)
                tbcnpass.config({'background':'#d4e4f9'})
                tbcnpass.place(x = 543, y = 490)

                #confirm pass button
                cf = Button(root, text = 'Confirm', font=('Coves Bold', 13), width= 14, bd = 0, command=check_and_confirm)
                cf.place(x = 750, y = 585)

                #back button
                br2 = Button(root, image = btbk, bd=0, command = login)
                br2.place(x = 1030, y = 620)
            #End recovery part

            #Menu page
            def menu():

                def addtocart():
                    def addtocart2():
                        def preview(count):
                            if count == 1:
                                pre = Label(root, image= hinablue1_7, bd = 0)
                                pre.place(x = 880, y = 100)
                                #Text Price
                                price = Label(root, text= '8010 BAHT',font = ('Coves Bold', 13), width = 12, bd = 0,bg = 'White')
                                price.place(x = 1000, y =  620)
                                #Button buy.
                                addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(9))
                                addbtn.place(x = 1010, y = 650)
                            elif count == 2:
                                pre = Label(root, image= tsubakiblue1_7, bd = 0)
                                pre.place(x = 880, y = 100)
                                #Text Price
                                price = Label(root, text= '7700 BAHT',font = ('Coves Bold', 13), width = 12, bd = 0,bg = 'White')
                                price.place(x = 1000, y =  620)
                                #Button buy.
                                addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(10))
                                addbtn.place(x = 1010, y = 650)
                            elif count == 3:
                                pre = Label(root, image= altriacas1_7, bd = 0)
                                pre.place(x = 880, y = 100)
                                #Text Price
                                price = Label(root, text= '12500 BAHT',font = ('Coves Bold', 13), width = 12, bd = 0,bg = 'White')
                                price.place(x = 1000, y =  620)
                                #Button buy.
                                addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(11))
                                addbtn.place(x = 1010, y = 650)
                            elif count == 4:
                                pre = Label(root, image= yae1_8, bd = 0)
                                pre.place(x = 880, y = 100)
                                #Text Price
                                price = Label(root, text= '9900 BAHT',font = ('Coves Bold', 13), width = 12, bd = 0,bg = 'White')
                                price.place(x = 1000, y =  620)
                                #Button buy.
                                addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(12))
                                addbtn.place(x = 1010, y = 650)
                            elif count == 5:
                                pre = Label(root, image= eugenazl1_7, bd = 0)
                                pre.place(x = 880, y = 100)
                                #Text Price
                                price = Label(root, text= '13000 BAHT',font = ('Coves Bold', 13), width = 12, bd = 0,bg = 'White')
                                price.place(x = 1000, y =  620)
                                #Button buy.
                                addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(13))
                                addbtn.place(x = 1010, y = 650)
                            elif count == 6:
                                pre = Label(root, image= gbfartbook, bd = 0)
                                pre.place(x = 880, y = 100)
                                #Text Price
                                price = Label(root, text= '1390 BAHT',font = ('Coves Bold', 13), width = 12, bd = 0,bg = 'White')
                                price.place(x = 1000, y =  620)
                                #Button buy.
                                addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(14))
                                addbtn.place(x = 1010, y = 650)

                        #BG
                        addbg = Label(root, image=bgproduct)
                        addbg.place(x = 0, y = 0)

                        pdtnum = Label(root, text="Product 9 - 14", font=('Coves', 20), bg='White')
                        pdtnum.place(x = 580, y =70)

                        #Buntton : Hina.BlueArchive (1/7)
                        p1 = Button(root, text = 'Hina.BlueArchive (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(1))
                        p1.place(x = 500, y = 120)

                        #Buntton : Tsubaki.BlueArchive (1/7)
                        p2 = Button(root, text = 'Tsubaki.BlueArchive (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(2))
                        p2.place(x = 500, y = 180)

                        #Buntton : Altria Caster.FGO (1/7)
                        p3 = Button(root, text = 'Altria Caster.FGO (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(3))
                        p3.place(x = 500, y = 240)

                        #Buntton : Yae.HK3rd (1/8)
                        p4 = Button(root, text = 'Yae.HK3rd (1/8)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(4))
                        p4.place(x = 500, y = 300)
                        
                        #Buntton : Prinz Eugen.Azurlane (1/7)
                        p5 = Button(root, text = 'Prinz Eugen.Azurlane (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(5))
                        p5.place(x = 500, y = 360)

                        #Buntton : GBF Graphic Archive V
                        p6 = Button(root, text = 'GBF Graphic Archive V', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(6))
                        p6.place(x = 500, y = 420)

                        #Button : Previous.
                        nextbtn = Button(root,text=('Previous page'),font=('Coves', 13)    , bd=0, width= 20, command = addtocart)
                        nextbtn.place(x = 500, y = 620)

                        #back button
                        back2 = Button(root, image = btbk, bd=0, command = menu)
                        back2.place(x = 30, y = 620)
                        
                    #Products preview with price
                    def preview(count):
                        if count == 1:
                            #Preview
                            pre = Label(root, image= yaeA4, bd = 0)
                            pre.place(x = 880, y = 100)
                            #Text Price
                            price = Label(root, text= '1590 BAHT',font = ('Coves Bold', 13), width = 10, bd = 0,bg = 'White')
                            price.place(x = 1010, y =  620)
                            #Button buy.
                            addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(1))
                            addbtn.place(x = 1010, y = 650)
                        elif count == 2:
                            pre = Label(root, image= yaeA2, bd = 0)
                            pre.place(x = 880, y = 100)
                            #Text Price
                            price = Label(root, text= '1900 BAHT',font = ('Coves Bold', 13), width = 10, bd = 0,bg = 'White')
                            price.place(x = 1010, y =  620)
                            #Button buy.
                            addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(2))
                            addbtn.place(x = 1010, y = 650)
                        elif count == 3:
                            pre = Label(root, image= mikusdy, bd = 0)
                            pre.place(x = 880, y = 100)
                            #Text Price
                            price = Label(root, text= '2400 BAHT',font = ('Coves Bold', 13), width = 10, bd = 0,bg = 'White')
                            price.place(x = 1010, y =  620)
                            #Button buy.
                            addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(3))
                            addbtn.place(x = 1010, y = 650)
                        elif count == 4:
                            pre = Label(root, image= genshinV_1, bd = 0)
                            pre.place(x = 880, y = 100)
                            #Text Price
                            price = Label(root, text= '1700 BAHT',font = ('Coves Bold', 13), width = 10, bd = 0,bg = 'White')
                            price.place(x = 1010, y =  620)
                            #Button buy.
                            addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(4))
                            addbtn.place(x = 1010, y = 650)
                        elif count == 5:
                            pre = Label(root, image= mizukiAK_pillow, bd = 0)
                            pre.place(x = 880, y = 100)
                            #Text Price
                            price = Label(root, text= '3000 BAHT',font = ('Coves Bold', 13), width = 10, bd = 0,bg = 'White')
                            price.place(x = 1010, y =  620)
                            #Button buy.
                            addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(5))
                            addbtn.place(x = 1010, y = 650)
                        elif count == 6:
                            pre = Label(root, image= lamy_cup, bd = 0)
                            pre.place(x = 880, y = 100)
                            #Text Price
                            price = Label(root, text= '1200 BAHT',font = ('Coves Bold', 13), width = 10, bd = 0,bg = 'White')
                            price.place(x = 1010, y =  620)
                            #Button buy.
                            addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(6))
                            addbtn.place(x = 1010, y = 650)
                        elif count == 7:
                            pre = Label(root, image= aquaBirthday2021, bd = 0)
                            pre.place(x = 880, y = 100)
                            #Text Price
                            price = Label(root, text= '6300 BAHT',font = ('Coves Bold', 13), width = 10, bd = 0,bg = 'White')
                            price.place(x = 1010, y =  620)
                            #Button buy.
                            addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(7))
                            addbtn.place(x = 1010, y = 650)
                        elif count == 8:
                            pre = Label(root, image= abigalFgo1_7, bd = 0)
                            pre.place(x = 880, y = 100)
                            #Text Price
                            price = Label(root, text= '6200 BAHT',font = ('Coves Bold', 13), width = 10, bd = 0,bg = 'White')
                            price.place(x = 1010, y =  620)
                            #Button buy.
                            addbtn = Button(root, text='Add to cart', font= ('Coves',13),width = 10, bd = 0, command = lambda:pdtidotlist(8))
                            addbtn.place(x = 1010, y = 650)

                    #Preview page 
                    def previewpage1():
                        def previewpage2():
                            #BG
                            pdtguestbg = Label(root, image = bgproduct)
                            pdtguestbg.place(x = 0,y = 0)

                            #Text : Product list 9-14
                            pdtnum = Label(root, text="Product 9 - 14", font=('Coves', 20), bg='White')
                            pdtnum.place(x = 580, y =70)

                            #Buntton : Hina.BlueArchive (1/7)
                            p1 = Button(root, text = 'Hina.BlueArchive (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(9))
                            p1.place(x = 500, y = 120)

                            #Buntton : Tsubaki.BlueArchive (1/7)
                            p2 = Button(root, text = 'Tsubaki.BlueArchive (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(10))
                            p2.place(x = 500, y = 180)

                            #Buntton : Altria Caster.FGO (1/7)
                            p3 = Button(root, text = 'Altria Caster.FGO (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(11))
                            p3.place(x = 500, y = 240)

                            #Buntton : Yae.HK3rd (1/8)
                            p4 = Button(root, text = 'Yae.HK3rd (1/8)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(12))
                            p4.place(x = 500, y = 300)
                            
                            #Buntton : Prinz Eugen.Azurlane (1/7)
                            p5 = Button(root, text = 'Prinz Eugen.Azurlane (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(13))
                            p5.place(x = 500, y = 360)

                            #Buntton : GBF Graphic Archive V
                            p6 = Button(root, text = 'GBF Graphic Archive V', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(14))
                            p6.place(x = 500, y = 420)

                            #Button : Previous.
                            prevbtn = Button(root,text=('Previous page'),font=('Coves', 13), bd=0, width= 20, command = lambda : addtocart())
                            prevbtn.place(x = 500, y = 620)

                            #back button
                            blkguest = Button(root, image = btbk, bd=0, command = menu)
                            blkguest.place(x = 30, y = 620)
                        #Text : Product list 1-8
                        pdtnum = Label(root, text="Product 1 - 8", font=('Coves', 20), bg='White')
                        pdtnum.place(x = 580, y =70)
                        #Buntton : Yae (A4)
                        p1 = Button(root, text = 'Yae (A4)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(1))
                        p1.place(x = 500, y = 120)

                        #Buntton : Yae (A2)
                        p2 = Button(root, text = 'Yae (A2)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(2))
                        p2.place(x = 500, y = 180)

                        #Buntton : Hatsune Miku(Standy)
                        p3 = Button(root, text = 'Hatsune Miku(Standy)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(3))
                        p3.place(x = 500, y = 240)

                        #Buntton : Genshin Photobook Vol.1
                        p4 = Button(root, text = 'Genshin Photobook Vol.1', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(4))
                        p4.place(x = 500, y = 300)
                        
                        #Buntton : Mizuki.Arknights (Pillowcase)
                        p5 = Button(root, text = 'Mizuki.Arknights (Pillowcase)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(5))
                        p5.place(x = 500, y = 360)

                        #Buntton : Lamy.Hololive (Glass)
                        p6 = Button(root, text = 'Lamy.Hololive (Glass)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(6))
                        p6.place(x = 500, y = 420)

                        #Buntton : Aqua.Hololive (Calendars)
                        p7 = Button(root, text = 'Aqua Minato Birthday 2021', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(7))
                        p7.place(x = 500, y = 480)

                        #Buntton : Fou.FGO (Plush)
                        p8 = Button(root, text = 'Abigail Williams.F/GO (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(8))
                        p8.place(x = 500, y = 540)

                        #Button : Next.
                        nextbtn = Button(root,text=('Next page'),font=('Coves', 13)    , bd=0, width= 20, command = lambda : addtocart2())
                        nextbtn.place(x = 700, y = 620)

                        #back button
                        blkguest = Button(root, image = btbk, bd=0, command = menu)
                        blkguest.place(x = 30, y = 620)
                    #Romove menu.
                    menubg.destroy()
                    user.destroy()
                    bitem.destroy()
                    cartx.destroy()
                    blogout.destroy()

                    #BG
                    pdtguestbg = Label(root, image = bgproduct)
                    pdtguestbg.place(x = 0,y = 0)

                    previewpage1()

                #cart
                #refresh : for refresh cart when use remove() or removeall() funtion because they can't call cart() funtion.
                def refresh():
                    #link listid to photo preview.
                    def link():
                        #show product preview.
                        def showitem(list1, x, y, a, b, c, d):
                            #remove item id from list id.
                            def remove(count3):
                                listid.remove(count3)
                                refresh()
                            
                            for i in range(len(list1)):
                                if list1[i] == 1:
                                    pre1 = Label(root, image=syaeA4)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Yae A4', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='1590 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(1))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 2:
                                    pre1 = Label(root, image=syaeA2)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Yae A2', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='1900 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(2))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 3:
                                    pre1 = Label(root, image=smikusdy)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Hatsune Miku(Standy)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='2400 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command=lambda : remove(3))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 4:
                                    pre1 = Label(root, image=sgenshinV_1)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Genshin Artwork Vol.1', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='1700 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(4))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 5:
                                    pre1 = Label(root, image=smizukiAK_pillow)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Mizuki.Arkinghts (Pillow)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='3000 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(5))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 6:
                                    pre1 = Label(root, image=slamy_cup)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Lamy.Hololive (Cup)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='1200 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(6))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 7:
                                    pre1 = Label(root, image=saquaBirthday2021)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Aqua Birthday Memorial 2021', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='6300 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(7))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 8:
                                    pre1 = Label(root, image=sabigalFgo1_7)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Abigal William.FGO (1/7)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='6200 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(8))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 9:
                                    pre1 = Label(root, image=shinablue1_7)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Hina.BlueArchive (1/7)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='8010 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(9))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 10:
                                    pre1 = Label(root, image=stsubakiblue1_7)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Tsubaki.BlueArchive (1/7)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='7700 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(10))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 11:
                                    pre11 = Label(root, image=saltriacas1_7)
                                    pre11.place(x = x, y =y)
                                    txt1 = Label(root, text='Altria Caster.FGO (1/7)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='12500 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(11))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 12:
                                    pre1 = Label(root, image=syae1_8)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Yae Honkai 3rd (1/8)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='9900 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(12))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 13:
                                    pre1 = Label(root, image=seugenazl1_7)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='Prinz Eugen.Azurlane (1/7)', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='13000 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(13))
                                    removebtn.place(x = c, y =d)
                                elif list1[i] == 14:
                                    pre1 = Label(root, image=sgbfartbook)
                                    pre1.place(x = x, y =y)
                                    txt1 = Label(root, text='GBF Graphic Archive V', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 25)
                                    txt1.place(x = a, y = b)
                                    txt2 = Label(root, text='1390 BATH', font=('Coves Bold',13),fg = 'white',bg= '#484a51', width= 15)
                                    txt2.place(x = a, y = d)
                                    removebtn = Button(root, text = 'Remove', font=('Coves',12),bd = 0,command= lambda : remove(14))
                                    removebtn.place(x = c, y =d)
                                y = y + 80
                                b += 80
                                d += 80
                            
                        #When there are more than 7 items in cart.
                        if len(listid) > 7:

                            #create listidclone : listidclone will delete second half id in it and use for crate second column.
                            listidclone = []

                            #copy listid  to listidclone
                            for i in range(len(listid)):
                                listidclone.append(listid[i])

                            #create listx for first half of preview column   
                            listx = []

                            #Split listid first half in listx, second half in listidclone.
                            for i in range(0,7):
                                listx.append(listid[i])
                            for i in range(0,7):
                                listidclone.remove(listx[i])
                            #show first column(listx = list item, x and y = first product preview position, a and b = first product name position, c and d = Remove button position) 
                            showitem(listx, x=460, y=120, a=545, b=130, c = 692, d = 160)
                            #show second column
                            showitem(listidclone, x=860, y=120, a=945, b=130, c = 1092, d = 160)
                        
                        #if no item in listid
                        elif len(listid) == 0:
                            nothing = Label(root, text = 'Nothing in your cart!',font = ('Coves',50), bg= 'White', fg = '#94dbf9')
                            nothing.place(x = 560, y = 470)
                            sticker = Label(root, image=cartsticker, bd =0)
                            sticker.place(x = 670, y = 140)

                        #When there are less than 8 items in the cart.
                        elif len(listid) <= 7:
                            showitem(listid, x=460, y=120, a=545, b=130, c = 692, d = 160)

                    #remove all item.
                    def removeall():
                        listid.clear()
                        refresh()

                    #Total product price.
                    def calc_():
                        conn =sqlite3.connect(r"D:\Visual Basic\Python\Project_Python\DB\itemlist.db")
                        c    = conn.cursor()
                        sum = 0
                        for i in range(len(listid)):
                            idx = listid[i]
                            c.execute("SELECT * FROM itemlist WHERE ID=?",(idx,))
                            iteminfo = c.fetchone()
                            sum = sum + int(iteminfo[2])
                        conn.close()
                        return sum

                    #Check listid if = 0 show warning.
                    def checklistid():
                        if len(listid) == 0:
                            tkinter.messagebox.showwarning('Warning','Cart is empty.')
                        else:
                            purchase_()
                    
                    #time to Purchase.
                    def purchase_():
                            def autoemail():
                                #connect to user infomation DB.
                                conn = sqlite3.connect(r"D:\Visual Basic\Python\Project_Python\DB\userdata.db")
                                c = conn.cursor()
                                c.execute("SELECT * FROM userdata WHERE USERNAME=?", (username,))
                                nameDB   = c.fetchone()
                                email    = nameDB[5]
                                user_email = "prejpbypandp@gmail.com"
                                user_password = "P123456789p"
                                yag = yagmail.SMTP(user_email,user_password)
                                recipients = email
                                subject = 'Your order receipt'
                                body = ["Dear",username,'\n',
                                    "Thank you for your pre-order.\n\n",
                                    "- Pre-order products will take about 2-3 weeks to arrive at our store (schedules for sale are subject to change).\n",
                                    "- Please pay via QR code according to the amount of the product and send proof of transfer to this email.\n",
                                    "- The shop will pack the product as best as possible. But we can't guarantee that every box is 100 percent good. There may be dents from transportation.\n",
                                    "- Sold items are considered final. The shop will not accept return or cancel the product in any case.\n",
                                    "- When the product arrives, the shop will contact via email. As the customer has provided information to the shop. (If you do not receive the email Please try checking in Junk)\n\n",
                                    "ありがとうございます\n"
                                    "Thank you\n",
                                    "Pre-Japan Store"]

                                email_attachment = (r"D:/Edit picture/python/pay.png")
                                yag.useralias = 'PRE-JAPAN Store'
                                yag.send(to=recipients,subject=subject,contents=body,attachments=email_attachment)
                            
                            #list to string.
                            def ltos_():
                                x     = []
                                sstr  = map(str, listid) #use map to change list to string.
                                x     = list(sstr)       #covert back to list but in list is string.
                                text1 = []
                                for i in range(len(x)):  #insert ',' between numbers in list.
                                    text1.append(x[i])
                                    text1.append(',')
                                n = i * 2 + 1
                                text1.pop(n)             #remove last ','.
                                text2 = ' '.join([str(elem) for elem in text1]) #covert list to string before put it into DB.
                                return text2

                            def transactionlog():
                                #connect to user infomation DB.
                                conn = sqlite3.connect(r"D:\Visual Basic\Python\Project_Python\DB\userdata.db")
                                c = conn.cursor()
                                c.execute("SELECT * FROM userdata WHERE USERNAME=?", (username,))
                                nameDB   = c.fetchone()
                                name     = nameDB[3]
                                lastname = nameDB[4]
                                email    = nameDB[5]
                                conn.close

                                #recive address
                                address = addressreciver.get()

                                #recive phone number
                                phonenum = phonerecive.get()

                                #recive zipcode
                                zipcode = zipcodereciver.get()

                                #convert listid to string before put ot to DB.
                                listItem = ltos_()

                                #recive total price:
                                summ = calc_()
                                #connect to transaction log DB.
                                conn = sqlite3.connect(r"D:\Visual Basic\Python\Project_Python\DB\tranclog.db")
                                c = conn.cursor()
                                sql  = '''INSERT INTO TransactionLog (Username,Name,Last_Name,Email,Address,ZipCode,Phone,ProductID,TotalPrice) VALUES (?,?,?,?,?,?,?,?,?)'''
                                data = (username, name, lastname, email, address, zipcode, phonenum, listItem, summ)
                                c.execute(sql, data)
                                conn.commit()
                                c.close()

                                listid.clear()
                                menu()

                            def check_everything():
                                checkerpn = False
                                checkeradd = False
                                checkerzip = False
                                #recive phone number.
                                phonenum = phonerecive.get()
                                if phonenum.isnumeric() == True:
                                    if len(phonenum) == 10:
                                        checkerpn = True 
                                    else:
                                        tkinter.messagebox.showwarning('Waring' ,'Phone number must have 10 numbers.\n\nPhone number must be numbers.')
                                else: tkinter.messagebox.showwarning('Waring' ,'Phone number must have 10 numbers.\n\nPhone number must be numbers.')

                                #recive address.
                                address = addressreciver.get()
                                if address == '':
                                    tkinter.messagebox.showwarning('Waring' ,'Address is empty.')        
                                else: 
                                    checkeradd = True

                                #recive zip code.
                                zipcode = zipcodereciver.get()
                                if zipcode.isnumeric() == True:
                                    if len(zipcode) == 5:
                                        checkerzip = True
                                    else:
                                        tkinter.messagebox.showwarning('Warning','Zip code must be numbers\n\nZip code must have 5 numbers')
                                else: 
                                    tkinter.messagebox.showwarning('Warning','Zip code must be numbers\n\nZip code must have 5 numbers')

                                #Checker works the way it's supposed to do.
                                if checkerpn == True and checkeradd == True and checkerzip == True:
                                    askbox = tkinter.messagebox.askquestion('PRE-JAPAN STORE','Is your contact correct?')
                                    if askbox == 'yes':
                                        tkinter.messagebox.showinfo('PRE-JAPAN STORE', 'Please wait for the confirmation email from the shop within 24 hours before transferring money. (must transfer and notify the transfer within 3 days otherwise the purchase order will expire)')
                                        transactionlog()
                                        autoemail()

                            #remove cart.
                            cartbg.destroy()
                            remvall_btn.destroy()
                            purchase_btn.destroy()
                            backbtn.destroy()
                            #BG
                            paybg = Label(root, image= bgpay)
                            paybg.place(x = 0, y = 0)

                            #text : Enter your contact.
                            contecttxt = Label(root, text = 'Enter your contact.', font = ('Coves Bold',22),bg = 'White')
                            contecttxt.place(x = 710, y = 125)

                            #Text : Phone number.
                            phonetxt = Label(root, text = 'Phone number', font = ('Coves Bold',15), bg = 'White')
                            phonetxt.place(x = 543, y = 190)

                            #textbox to input phone number.
                            phonerecive = StringVar()
                            txtboxphone  = Entry(root, font=('Coves',15), textvariable = phonerecive, width = 23, bd = 0)
                            txtboxphone.config({'background':'#d4e4f9'})
                            txtboxphone.place(x = 680 , y = 190)

                            #Text : Address.
                            addresstxt = Label(root, text = 'Address', font = ('Coves Bold',15), bg = 'White')
                            addresstxt.place(x = 543, y = 250)

                            #textbox to input Address.
                            addressreciver = StringVar()
                            txtaddress  = Entry(root, font=('Coves',15), textvariable = addressreciver, width = 23, bd = 0)
                            txtaddress.config({'background':'#d4e4f9'})
                            txtaddress.place(x = 680 , y = 250)

                            #Text : Zip Code.
                            ziptxt = Label(root, text = 'Zip Code', font = ('Coves Bold',15), bg = 'White')
                            ziptxt.place(x = 543, y = 310)

                            #textbox to input zip code.
                            zipcodereciver = StringVar()
                            txtzipcode  = Entry(root, font=('Coves',15), textvariable = zipcodereciver, width = 23, bd = 0)
                            txtzipcode.config({'background':'#d4e4f9'})
                            txtzipcode.place(x = 680 , y = 310)

                            #Button : Complete
                            completebtn = Button(root, text='Complete', font=('Coves',13), bd = 0, width= 10, command=check_everything)
                            completebtn.place(x =770, y = 590)

                            backbtn1 = Button(root, image= btbk, bd = 0, command= menu)
                            backbtn1.place(x = 1030, y = 620)

                    #remove menu.
                    menubg.destroy()
                    user.destroy()
                    bitem.destroy()
                    cartx.destroy()
                    blogout.destroy()
                    
                    #BG
                    cartbg = Label(root, image=bgcart)
                    cartbg.place(x = 0, y = 0)

                    summary = calc_()
                    totalpricetxt = Label(root, text=(summary," BAHT"), font = ('Coves', 13), bg = "White", width= 14)
                    totalpricetxt.place(x =1165, y = 560)

                    remvall_btn = Button(root, text = 'Remove all', font=('Coves',13), width= 10, bd = 0, command=removeall)
                    remvall_btn.place(x = 1190, y = 610)

                    purchase_btn = Button(root, text = 'Purchase', font=('Coves', 13), width= 10, bd = 0, command=checklistid)
                    purchase_btn.place(x = 1190, y = 660)

                    backbtn = Button(root, image= btbk, bd = 0, command= menu)
                    backbtn.place(x = 30, y = 620)

                    link()
                #Recive username.
                username = usernametext.get()
                #remove login
                lbg.destroy()
                ltxt.destroy()
                usernametxt.destroy()
                tblogin.destroy()
                tbpass.destroy()
                bl1.destroy()
                bl2.destroy()
                forgot.destroy()

                #BG
                menubg = Label(root, image=bgm)
                menubg.place(x = 0, y = 0)

                #Show username
                user = Label(root, text = username, font = ('Coves Bold',35), fg = 'White', bg = "#94dbf9")
                user.place(x = 390, y = 670)

                #Button : Add to cart.
                bitem = Button(root, image = btadd, bd=0, command = addtocart)
                bitem.place(x = 910, y = 200)

                #Show cart, remove item and purchase.
                cartx = Button(root, image=btcart, bd= 0, command = refresh)
                cartx.place(x = 910, y = 300)

                #Button : Logout.
                blogout = Button(root, image = btout, bd=0, command = home)
                blogout.place(x = 910, y = 600)

            #remove home
            hbg.destroy()
            bh2.destroy()
            bh1.destroy()
            bh3.destroy()
            bh4.destroy()
            
            recov_code = str(random_code())

            #BG
            lbg = Label(root, image = bgl)
            lbg.place(x = 0,y = 0)

            ltxt = Label(root, text = 'Login', font= ('Coves Bold', 22), bg = 'White')
            ltxt.place(x = 700, y = 200)

            #text : Username
            usernametxt = Label(root, text = 'Username',font = ('Coves Bold',15), bg = 'White')
            usernametxt.place(x = 543, y = 250)

            #textbox to input username.
            usernametext = StringVar()
            tblogin  = Entry(root, font=('Coves',20), textvariable = usernametext, width = 17, bd = 0)
            tblogin.config({'background':'#d4e4f9'})
            tblogin.place(x = 543, y = 280)

            #text : Password
            passtxt = Label(root, text = 'Password',font = ('Coves Bold',15), bg = 'White')
            passtxt.place(x = 543, y = 350)
            
            #textbox to input password.
            newpasstext = StringVar()
            tbpass  = Entry(root, font=('Coves',20), textvariable = newpasstext, width = 17, bd = 0)
            tbpass.config({'background':'#d4e4f9'})
            tbpass.place(x = 543, y = 380)
            
            #login button
            bl1 = Button(root, image = sblogin, bd=0, command = checkuser)
            bl1.place(x = 670, y = 480)

            #forgot pass button
            forgot = Button(root, text = 'Forgot Password', font=('Coves Bold', 13), width= 14, bd = 0, command=forgotpass)
            forgot.place(x = 786, y = 425)

            #back button
            bl2 = Button(root, image = btbk, bd=0, command = home)
            bl2.place(x = 1030, y = 620)

        def reg():
            #remove home
            hbg.destroy()
            bh2.destroy()
            bh1.destroy()
            bh3.destroy()
            bh4.destroy()

            def check_username_regis():
                usernamechecker = False
                username_tuple = get_username_f_db(usernametext)
                username       = username_tuple[0]
                checkuser      = username_tuple[1]

                if len(username)   < 5:
                    tkinter.messagebox.showwarning('Warning!', 'Username must have 5 or more charecters.')
                    return usernamechecker
                elif len(username) > 30:
                    tkinter.messagebox.showwarning('Warning!', 'Username must less than 31 charecters.')
                    return usernamechecker
                elif checkuser    == None:
                    tkinter.messagebox.showinfo('Nice username!', 'You can use this username.')
                    usernamechecker = True
                    return usernamechecker
                elif checkuser[1] == username:
                    tkinter.messagebox.showwarning('Warning!', 'Username already exists.')
                    return usernamechecker
                else:
                    tkinter.messagebox.showwarning('Warning!', 'Wrong input!.')
                    return usernamechecker
            
            def reg_process():
                usernamechecker = check_username_regis()
                username = usernametext.get()
                if usernamechecker == True:
                    checkpass = confirmpassword(passtxt, cpasstxt)
                
                #recive e-mail.
                    regex = r"\b[A-Za-z0-9._-]+@([gmail]|[hotmail]|[kkumail]|[yahoo]|[outlook])+\.([com]|[net])\b"
                    email = emailreciver.get()
                    if email == '':
                        tkinter.messagebox.showwarning('Waring' ,'E-mail is empty.')
                        checkerem = False
                    else:
                        if(re.search(regex,email)):   
                            checkerem = True
                        else: 
                            tkinter.messagebox.showwarning('Waring' ,'E-mail is invalid.')
                            checkerem = False

                #Recive name and last name from textbox and check it.
                    name   = fname.get()
                    laname = lname.get()

                    if name == None or laname == None:
                        tkinter.messagebox.showwarning('Warning!', 'Your first name or last name is empty.')
                        checkname = False
                    elif name.isalpha() == True and laname.isalpha() == True:
                        checkname = True
                    else:
                        tkinter.messagebox.showwarning('Warning!', 'Your first name and last name must not be numbers, empty or special charecters.')
                        checkname = False

                #check result before put info into DB.
                    if checkname == True and checkpass == True and  checkerem == True:
                        conn = sqlite3.connect(r"D:\Visual Basic\Python\Project_Python\DB\userdata.db")
                        c = conn.cursor()
                        sql = '''INSERT INTO userdata (USERNAME,PASSWORD,NAME,LAST_NAME,Email) VALUES (?,?,?,?,?)'''
                        data = (username, password, name, laname, email)
                        c.execute(sql, data)
                        conn.commit()
                        conn.close()
                        tkinter.messagebox.showinfo('SUCCESS!', 'You have successfully created an account.')
                        home()
                else:
                    tkinter.messagebox.showwarning('Warning','Please check your username first')
            
            #BG
            rbg = Label(root, image = bgr)
            rbg.place(x = 0,y = 0)

            createtxt = Label(root, text = 'Create an account.', font= ('Coves Bold', 22), bg = 'White')
            createtxt.place(x = 620, y = 110)

            #text : Username
            usernametxt = Label(root, text = 'Username (5 - 30 charecters)',font = ('Coves Bold',15), bg = 'White')
            usernametxt.place(x = 543, y = 150)

            #textbox to input username.
            usernametext = StringVar()
            tbregis  = Entry(root, font=('Coves',20), textvariable = usernametext, width = 17, bd = 0)
            tbregis.config({'background':'#d4e4f9'})
            tbregis.place(x = 543, y = 180)

            #check user button.
            checkbtn = Button(root, text = "Check", font = ('Coves Bold', 13), bd = 1, command = check_username_regis)
            checkbtn.place(x = 865, y = 145)

            #text : Password
            ptxt = Label(root, text = 'Password (8 - 30 charecters)',font = ('Coves Bold',15), bg = 'White')
            ptxt.place(x = 543, y = 220)

            #textbox to input password.
            passtxt = StringVar()
            tbpass  = Entry(root, font=('Coves',20), textvariable = passtxt, width = 17, bd = 0)
            tbpass.config({'background':'#d4e4f9'})
            tbpass.place(x = 543, y = 250)

            #text : Confirm password
            cpasstxt = Label(root, text = 'Confirm password',font = ('Coves Bold',15), bg = 'White')
            cpasstxt.place(x = 543, y = 290)

            #textbox to input password.
            cpasstxt = StringVar()
            tbcp = Entry(root, font=('Coves',20), textvariable = cpasstxt, width = 17, bd = 0)
            tbcp.config({'background':'#d4e4f9'})
            tbcp.place(x = 543, y = 320)

            #text : Email
            emailtxt = Label(root, text = 'E-mail',font = ('Coves Bold',15), bg = 'White')
            emailtxt.place(x = 543, y = 360)

            #textbox to input email.
            emailreciver = StringVar()
            tbemail = Entry(root, font=('Coves',20), textvariable = emailreciver, width = 17, bd = 0)
            tbemail.config({'background':'#d4e4f9'})
            tbemail.place(x = 543, y = 390)

            #text : First name
            fntxt = Label(root, text = 'First Name (English)',font = ('Coves Bold',15), bg = 'White')
            fntxt.place(x = 543, y = 430)

            #textbox to input name.
            fname = StringVar()
            tbfn = Entry(root, font=('Coves',20), textvariable = fname, width = 17, bd = 0)
            tbfn.config({'background':'#d4e4f9'})
            tbfn.place(x = 543, y = 460)

            #text : Last name
            lntxt = Label(root, text = 'Last Name (English)',font = ('Coves Bold',15), bg = 'White')
            lntxt.place(x = 543, y = 510)

            #textbox to input lastname.
            lname = StringVar()
            tbln  = Entry(root, font=('Coves',20), textvariable = lname, width = 17, bd = 0)
            tbln.config({'background':'#d4e4f9'})
            tbln.place(x = 543, y = 540)

            #regis button
            br1 = Button(root, image = sbre, bd=0, command = reg_process)
            br1.place(x = 670, y = 593)

            #back button
            br2 = Button(root, image = btbk, bd=0, command = home)
            br2.place(x = 1030, y = 620)

        def menu_guest():
            #show all product.
            def productlist():
                #Products preview 
                def preview(count):
                    if count == 1:
                        pre = Label(root, image= yaeA4, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 2:
                        pre = Label(root, image= yaeA2, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 3:
                        pre = Label(root, image= mikusdy, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 4:
                        pre = Label(root, image= genshinV_1, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 5:
                        pre = Label(root, image= mizukiAK_pillow, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 6:
                        pre = Label(root, image= lamy_cup, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 7:
                        pre = Label(root, image= aquaBirthday2021, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 8:
                        pre = Label(root, image= abigalFgo1_7, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 9:
                        pre = Label(root, image= hinablue1_7, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 10:
                        pre = Label(root, image= tsubakiblue1_7, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 11:
                        pre = Label(root, image= altriacas1_7, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 12:
                        pre = Label(root, image= yae1_8, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 13:
                        pre = Label(root, image= eugenazl1_7, bd = 0)
                        pre.place(x = 880, y = 100)
                    elif count == 14:
                        pre = Label(root, image= gbfartbook, bd = 0)
                        pre.place(x = 880, y = 100)
                #Preview page 
                def previewpage1():
                    def previewpage2():
                        #BG
                        pdtguestbg = Label(root, image = bgproduct)
                        pdtguestbg.place(x = 0,y = 0)

                        #Text : Product list 9-14
                        pdtnum = Label(root, text="Product 9 - 14", font=('Coves', 20), bg='White')
                        pdtnum.place(x = 580, y =70)

                        #Buntton : Hina.BlueArchive (1/7)
                        p1 = Button(root, text = 'Hina.BlueArchive (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(9))
                        p1.place(x = 500, y = 120)

                        #Buntton : Tsubaki.BlueArchive (1/7)
                        p2 = Button(root, text = 'Tsubaki.BlueArchive (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(10))
                        p2.place(x = 500, y = 180)

                        #Buntton : Altria Caster.FGO (1/7)
                        p3 = Button(root, text = 'Altria Caster.FGO (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(11))
                        p3.place(x = 500, y = 240)

                        #Buntton : Yae.HK3rd (1/8)
                        p4 = Button(root, text = 'Yae.HK3rd (1/8)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(12))
                        p4.place(x = 500, y = 300)
                        
                        #Buntton : Prinz Eugen.Azurlane (1/7)
                        p5 = Button(root, text = 'Prinz Eugen.Azurlane (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(13))
                        p5.place(x = 500, y = 360)

                        #Buntton : GBF Graphic Archive V
                        p6 = Button(root, text = 'GBF Graphic Archive V', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(14))
                        p6.place(x = 500, y = 420)

                        #Button : Previous.
                        prevbtn = Button(root,text=('Previous page'),font=('Coves', 13), bd=0, width= 20, command = lambda : previewpage1())
                        prevbtn.place(x = 500, y = 620)

                        #back button
                        blkguest = Button(root, image = btbk, bd=0, command = menu_guest)
                        blkguest.place(x = 30, y = 620)
                    #Text : Product list 1-8
                    pdtnum = Label(root, text="Product 1 - 8", font=('Coves', 20), bg='White')
                    pdtnum.place(x = 580, y =70)
                    #Buntton : Yae (A4)
                    p1 = Button(root, text = 'Yae (A4)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(1))
                    p1.place(x = 500, y = 120)

                    #Buntton : Yae (A2)
                    p2 = Button(root, text = 'Yae (A2)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(2))
                    p2.place(x = 500, y = 180)

                    #Buntton : Hatsune Miku(Standy)
                    p3 = Button(root, text = 'Hatsune Miku(Standy)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(3))
                    p3.place(x = 500, y = 240)

                    #Buntton : Genshin Photobook Vol.1
                    p4 = Button(root, text = 'Genshin Photobook Vol.1', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(4))
                    p4.place(x = 500, y = 300)
                    
                    #Buntton : Mizuki.Arknights (Pillowcase)
                    p5 = Button(root, text = 'Mizuki.Arknights (Pillowcase)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(5))
                    p5.place(x = 500, y = 360)

                    #Buntton : Lamy.Hololive (Glass)
                    p6 = Button(root, text = 'Lamy.Hololive (Glass)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(6))
                    p6.place(x = 500, y = 420)

                    #Buntton : Aqua.Hololive (Calendars)
                    p7 = Button(root, text = 'Aqua Minato Birthday 2021', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(7))
                    p7.place(x = 500, y = 480)

                    #Buntton : Fou.FGO (Plush)
                    p8 = Button(root, text = 'Abigail Williams.F/GO (1/7)', font =  ("Coves Bold", 15), fg = '#94dbf9', bd = 0, width = 25, bg = '#2d2f30', command = lambda : preview(8))
                    p8.place(x = 500, y = 540)

                    #Button : Next.
                    nextbtn = Button(root,text=('Next page'),font=('Coves', 13)    , bd=0, width= 20, command = lambda : previewpage2())
                    nextbtn.place(x = 700, y = 620)

                    #back button
                    blkguest = Button(root, image = btbk, bd=0, command = menu_guest)
                    blkguest.place(x = 30, y = 620)
                
                def create_preview_button():
                    #Romove menu.
                    mgbg.destroy()
                    user.destroy()
                    bitem.destroy()
                    baddlock.destroy()
                    blk.destroy()

                    previewpage1()

                #BG
                pdtguestbg = Label(root, image = bgproduct)
                pdtguestbg.place(x = 0,y = 0)

                create_preview_button()
                
            def lockmenu():
                tkinter.messagebox.showwarning('Warning','Please login first.')

            #romve home
            hbg.destroy()
            bh2.destroy()
            bh1.destroy()
            bh3.destroy()
            bh4.destroy()

            #BG
            mgbg = Label(root, image = bgm)
            mgbg.place(x = 0,y = 0)

            #show username
            user = Label(root, text = "Guest", font = ('Coves Bold',35), fg = 'White', bg = "#94dbf9")
            user.place(x = 390, y = 670)

            #Button : Product
            bitem = Button(root, image = btitem, bd=0, command = productlist)
            bitem.place(x = 910, y = 200)

            #Button : Add cart.
            baddlock = Button(root, image = btaddlock, bd=0, command = lockmenu)
            baddlock.place(x = 910, y = 320)

            #back button
            blk = Button(root, image = btbk, bd=0, command = home)
            blk.place(x = 1030, y = 620)

        #destroy start
        stbg.destroy()
        wlc.destroy()
        b1.destroy()

        #BG
        hbg = Label(root, image = bgh)
        hbg.place(x = 0,y = 0)

        bh1 = Button(root, image = btlogin, bd=0, command = login)
        bh1.place(x = 910, y = 200)

        bh2 = Button(root, image = btreg, bd=0, command = reg)
        bh2.place(x = 910, y = 330)

        bh3 = Button(root, image = btguest, bd=0, command = menu_guest)
        bh3.place(x = 910, y = 460)

        bh4 = Button(root, image = sqbt, bd=0, command = exit)
        bh4.place(x = 960, y = 600)

    listid.clear()

    stbg = Label(root, image = bgst)
    stbg.place(x = 0,y = 0)

    wlc = Label(root, text = 'WELCOME\nPRE-JAPAN', font = ('Pomeranian',40),fg = '#82cefe')
    wlc.place(x = 425, y = 320)

    b1 = Button(root, image = btst, command = home, bd = 0)
    b1.place(x = 510, y = 500)

email = ''
listid = []
#Creat window
root = Tk()
root.geometry('1280x720')
root.title('PRE-JAPAN STORE')
root.iconbitmap("D:\Edit picture\icon.ico")
root.resizable(0,0)

#BG
bgst       = PhotoImage(file="D:/Edit picture/python/bnt/bgst.png")
bgh        = PhotoImage(file="D:/Edit picture/python/bnt/bg1.png")
bgl        = PhotoImage(file="D:/Edit picture/python/bnt/bgloginpage.png")
bgr        = PhotoImage(file="D:/Edit picture/python/bnt/bgreg.png")
bgm        = PhotoImage(file="D:/Edit picture/python/bnt/bg2.png")
bgproduct  = PhotoImage(file="D:/Edit picture/python/bnt/productbg.png")
bgcart     = PhotoImage(file="D:/Edit picture/python/bnt/Cart.png")
bgpay      = PhotoImage(file="D:/Edit picture/python/bnt/paybg.png")
recovebg   = PhotoImage(file="D:/Edit picture/python/bnt/recov.png")

#Sticker
cartsticker = PhotoImage(file="D:/Edit picture/ganyu2.png")

#Button
btst    = PhotoImage(file="D:/Edit picture/python/bnt/start1.png")
btlogin = PhotoImage(file="D:/Edit picture/python/bnt/login.png")
btreg   = PhotoImage(file="D:/Edit picture/python/bnt/re1.png")
btguest = PhotoImage(file="D:/Edit picture/python/bnt/guest1.png")
btbk    = PhotoImage(file="D:/Edit picture/python/bnt/back1.png")
btitem  = PhotoImage(file="D:/Edit picture/python/bnt/pdt1.png")
btaddlock  = PhotoImage(file="D:/Edit picture/python/bnt/addlock.png")
btadd   = PhotoImage(file="D:/Edit picture/python/bnt/add1.png")
btout   = PhotoImage(file="D:/Edit picture/python/bnt/logout1.png")
btcart  = PhotoImage(file="D:/Edit picture/python/bnt/cart1.png")

#Small button
sqbt    = PhotoImage(file="D:/Edit picture/python/bnt/quit1.png")
sblogin = PhotoImage(file="D:/Edit picture/python/bnt/vslogin1.png")
sbre    = PhotoImage(file="D:/Edit picture/python/bnt/vsregis1.png")

#Preview page 1.
yaeA4            = PhotoImage(file="D:/Edit picture/python/Previews/pre1.png")
yaeA2            = PhotoImage(file="D:/Edit picture/python/Previews/pre2.png")
mikusdy          = PhotoImage(file="D:/Edit picture/python/Previews/pre3.png")
genshinV_1       = PhotoImage(file="D:/Edit picture/python/Previews/pre4.png")
mizukiAK_pillow  = PhotoImage(file="D:/Edit picture/python/Previews/pre5.png")
lamy_cup         = PhotoImage(file="D:/Edit picture/python/Previews/pre6.png")
aquaBirthday2021 = PhotoImage(file="D:/Edit picture/python/Previews/pre7.png")
abigalFgo1_7     = PhotoImage(file="D:/Edit picture/python/Previews/pre8.png")
#Preview page 2
hinablue1_7      = PhotoImage(file="D:/Edit picture/python/Previews/pre9.png")
tsubakiblue1_7   = PhotoImage(file="D:/Edit picture/python/Previews/pre10.png")
altriacas1_7     = PhotoImage(file="D:/Edit picture/python/Previews/pre11.png")
yae1_8           = PhotoImage(file="D:/Edit picture/python/Previews/pre12.png")
eugenazl1_7      = PhotoImage(file="D:/Edit picture/python/Previews/pre13.png")
gbfartbook       = PhotoImage(file="D:/Edit picture/python/Previews/pre14.png")

#Cart previewpic
syaeA4            = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s1.png")
syaeA2            = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s2.png")
smikusdy          = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s3.png")
sgenshinV_1       = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s4.png")
smizukiAK_pillow  = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s5.png")
slamy_cup         = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s6.png")
saquaBirthday2021 = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s7.png")
sabigalFgo1_7     = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s8.png")
shinablue1_7      = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s9.png")
stsubakiblue1_7   = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s10.png")
saltriacas1_7     = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s11.png")
syae1_8           = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s12.png")
seugenazl1_7      = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s13.png")
sgbfartbook       = PhotoImage(file="D:/Edit picture/python/Previews/smolpreview/s14.png")
start()

root.mainloop()