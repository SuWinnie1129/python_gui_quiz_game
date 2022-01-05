import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as tkmessage
import csv
import random
from PIL import Image, ImageTk

# frame setting
INIT_X = 1366 / 2  # the initial x coordinate of the object
INIT_Y = 768 / 2  # the initial y coordinate of the object

# game info
FILE_PATH = "ref/dataset/"
CURRENT_DATASET = str()  # record of question dataset this time
CURRENT_ODDS = 0    # record of game odds this time
ASSETS_ADD = 0  # record the assets won/lose this time
title_dict = {'賭場貴客': 0, '高淨值人士': 1000000, '百萬富翁': 6500000,
              '千萬富翁': 65000000, '超級億萬富翁': 2100000000}  # user title level
dataset_dict = {'s': '社會時事', 'p': 'PYTHON', 'k': '知識', 'n': '台大校園生活'}
# entrance fee for different level
fee_dict = {'1': 1000000, '2': 5000000, '3': 20000000}
chip_dict = {'1': 1000000, '2': 5000000,
             '3': 10000000}  # chip for every question
ques_list = list()  # record questions, answers, choices from dataset
ques_index = list()  # record index of 5 questions in this time


# user info
USER_NAME = str()
USER_TITLE = '賭場貴客'  # record of user's title
ASSETS = 8000000  # record of user's asset
BANKRUPTCY = False  # record bankruptcy or not
user_finished = []  # record of  challenges that have completed
# record of the finished amount of each level
level_finished = {'1': 0, '2': 0, '3': 0}


class App(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        global WINDOW_W, WINDOW_H, INIT_X, INIT_Y

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.grid()

        # set font style
        self.project_title_font = tkfont.Font(
            family="微軟正黑體", size=35, weight="bold")
        self.title_font = tkfont.Font(family="微軟正黑體", size=25, weight="bold")
        self.label_font = tkfont.Font(family="微軟正黑體", size=18, weight="normal")
        self.button_font = tkfont.Font(
            family="微軟正黑體", size=14, weight="normal")

        # set frame size
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # set layout of frame
        container.grid_rowconfigure(0, weight=1)    # weight=1 代表可以縮放
        container.grid_columnconfigure(0, weight=1)

        # consist all frames
        self.frames = {}
        for F in (StartPage, HomePage, MenuPage, GamePage, ResultPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # set widget style
        self.button_style = {'background': '#354C60',
                             'font': self.button_font}

        self.show_frame("StartPage")

    # to display the current frame
    def show_frame(self, page_name):
        """Display the specific frame"""
        print(page_name)
        frame = self.frames[page_name]
        frame.tkraise()

    def show_message(cls, msg):
        """Display message"""
        tkmessage.showinfo("Notice", msg)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        global INIT_X, INIT_Y

        tk.Frame.__init__(self, parent)
        self.controller = controller

        # background
        background = ImageTk.PhotoImage(Image.open(
            "ref/img/start_page.png").resize((1366, 768)))
        self.background_img = tk.Label(self, image=background)
        self.background_img.image = background
        self.background_img.place(x=0, y=0, relwidth=1, relheight=1)

        # title
        self.title = tk.Label(self, text="Who Wants To Be A Billionaire",
                              font=controller.project_title_font, fg="#354C60", bg="white")
        self.title.grid(
            row=0, padx=INIT_X-600, pady=(100, 14), sticky=tk.NW)

        # username input field
        self.name_label = tk.Label(
            self, text="User Name:", font=controller.label_font, fg="#354C60", bg="white")
        self.name_label.grid(
            row=1, padx=INIT_X-550, pady=(30, 6), sticky=tk.NW)
        self.name = tk.Entry(self)
        self.name.grid(row=1, padx=INIT_X-400, pady=(36, 6), sticky=tk.NW)

        # buttons
        self.next_btn = tk.Button(self, text="Next", font=controller.button_font,
                                  bg='white', fg='#354C60', width=15, height=1, activeforeground='white', activebackground='#354C60',
                                  command=lambda: self.get_username())
        self.next_btn.grid(row=2, padx=INIT_X-450, pady=(30, 6), sticky=tk.NW)

    def get_username(self):
        """ get user name"""
        global USER_NAME
        USER_NAME = self.name.get()
        # check if input is empty
        if USER_NAME == "":
            self.controller.show_message("請輸入玩家名稱")
        else:
            self.controller.show_frame("HomePage")


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        global INIT_X, INIT_Y

        tk.Frame.__init__(self, parent,)
        self.controller = controller

        # variables of user info (for update)
        self.name_var = tk.StringVar()
        self.assets_var = tk.StringVar()

        # background
        background = ImageTk.PhotoImage(Image.open(
            "ref/img/home_page.png").resize((1366, 768)))
        self.background_img = tk.Label(self, image=background)
        self.background_img.image = background
        self.background_img.place(x=0, y=0, relwidth=1, relheight=1)

        # user info
        self.line1_label = tk.Label(
            self, text="Hi~ ", font=controller.title_font, bg="#FFC736", fg="#354C60")
        self.username_label = tk.Label(
            self, textvariable=self.name_var, font=controller.title_font, bg="#FFC736", fg="#354C60")
        self.line1_label.grid(
            row=0, padx=INIT_X-500, pady=(155, 14), sticky=tk.NW)
        self.username_label.grid(
            row=0, padx=INIT_X-400, pady=(155, 14), sticky=tk.NW)

        self.line2_label = tk.Label(
            self, text="你的初始資產為", font=controller.title_font, bg="#FFC736", fg="#354C60")
        self.asset_label = tk.Label(
            self, textvariable=self.assets_var, font=controller.title_font, bg="#FFC736", fg="#354C60")
        self.line2_label.grid(
            row=0, padx=INIT_X-500, pady=(438, 14), sticky=tk.NW)

        self.asset_label.grid(
            row=0, padx=INIT_X-250, pady=(438, 14), sticky=tk.NW)

        # next button
        self.next_btn = tk.Button(self, text="Menu Page →", font=controller.button_font,
                                  bg='white', fg='#354C60', width=20, height=1, activeforeground='white', activebackground="#354C60",
                                  command=lambda: controller.show_frame("MenuPage"))
        self.next_btn.grid(row=3, padx=INIT_X+400,
                           pady=(170, 6), sticky=tk.NW)

        # to update userinfo
        self.update_info()

    def update_info(self):
        """ update user infomation(USER_NAME, USER_TITLE, ASSETS)"""
        global USER_NAME, ASSETS
        self.name_var.set(USER_NAME)
        self.assets_var.set(str(format(ASSETS, ',')))

        self.after(500, self.update_info)


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        global INIT_X, INIT_Y, CURRENT_DATASET

        tk.Frame.__init__(self, parent,)
        self.controller = controller

        # variables of user info (for update)
        self.name_var = tk.StringVar()
        self.usertitle_var = tk.StringVar()
        self.assets_var = tk.StringVar()

        # variables of game info
        self.current_dataset_var = tk.StringVar()
        self.current_odds_var = tk.StringVar()

        # background
        background = ImageTk.PhotoImage(Image.open(
            "ref/img/menu_page.png").resize((1366, 768)))
        self.background_img = tk.Label(self, image=background)
        self.background_img.image = background
        self.background_img.place(x=0, y=0, relwidth=1, relheight=1)

        # title
        tk.Label(self, text="選擇題目和賠率☺︎", font=controller.title_font, bg="#FFC736", fg="black").grid(
            row=0, padx=INIT_X-130, pady=(40, 7), sticky=tk.NW)

        # user info
        self.username_label = tk.Label(
            self, textvariable=self.name_var, font=controller.label_font, bg="#FFC736", fg="black")
        self.username_label.grid(
            row=1, padx=INIT_X-400, pady=4, sticky=tk.NW)

        self.usertitle_label = tk.Label(
            self, textvariable=self.usertitle_var, font=controller.label_font, bg="#FFC736", fg="black")
        self.usertitle_label.grid(row=1, padx=INIT_X-100, pady=4, sticky=tk.NW)

        self.assets_label = tk.Label(
            self, textvariable=self.assets_var, font=controller.label_font, bg="#FFC736", fg="black")
        self.assets_label.grid(row=1, padx=INIT_X+200, pady=7, sticky=tk.NW)

        # show current dataset
        self.current_dataset_label = tk.Label(
            self, textvariable=self.current_dataset_var, font=controller.label_font, bg="#FFC736")
        self.current_dataset_label.grid(
            row=2, padx=INIT_X-450, pady=(30, 6), sticky=tk.NW)

        # question_menu
        self.buttons = {
            's_lv1': tk.Button(self, text="社會時事_1（需$600萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("s_lv1")),
            's_lv2': tk.Button(self, text="社會時事_2（需$3000萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("s_lv2")),
            's_lv3': tk.Button(self, text="社會時事_3（需$7000萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("s_lv3")),
            'p_lv1': tk.Button(self, text="Python_1（需$600萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("p_lv1")),
            'p_lv2': tk.Button(self, text="Python_2（需$3000萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("p_lv2")),
            'p_lv3': tk.Button(self, text="Python_3（需$7000萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("p_lv3")),
            'k_lv1': tk.Button(self, text="知識_1（需$600萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("k_lv1")),
            'k_lv2': tk.Button(self, text="知識_2（需$3000萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("k_lv2")),
            'k_lv3': tk.Button(self, text="知識_3（需$7000萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("k_lv3")),
            'n_lv1': tk.Button(self, text="台大生活_1（需$600萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("n_lv1")),
            'n_lv2': tk.Button(self, text="台大生活_2（需$3000萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("n_lv2")),
            'n_lv3': tk.Button(self, text="台大生活_3（需$7000萬)", font=controller.button_font, fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60", command=lambda: self.get_datasetMenu("n_lv3"))
        }

        self.buttons['s_lv1'].grid(
            row=3, padx=INIT_X-450, pady=(15, 6), sticky=tk.NW)
        self.buttons['s_lv2'].grid(
            row=3, padx=INIT_X-150, pady=(15, 6), sticky=tk.NW)
        self.buttons['s_lv3'].grid(
            row=3, padx=INIT_X+150, pady=(15, 6), sticky=tk.NW)
        self.buttons['p_lv1'].grid(
            row=4, padx=INIT_X-450, pady=(15, 6), sticky=tk.NW)
        self.buttons['p_lv2'].grid(
            row=4, padx=INIT_X-150, pady=(15, 6), sticky=tk.NW)
        self.buttons['p_lv3'].grid(
            row=4, padx=INIT_X+150, pady=(15, 6), sticky=tk.NW)
        self.buttons['k_lv1'].grid(
            row=5, padx=INIT_X-450, pady=(15, 6), sticky=tk.NW)
        self.buttons['k_lv2'].grid(
            row=5, padx=INIT_X-150, pady=(15, 6), sticky=tk.NW)
        self.buttons['k_lv3'].grid(
            row=5, padx=INIT_X+150, pady=(15, 6), sticky=tk.NW)
        self.buttons['n_lv1'].grid(
            row=6, padx=INIT_X-450, pady=(15, 6), sticky=tk.NW)
        self.buttons['n_lv2'].grid(
            row=6, padx=INIT_X-150, pady=(15, 6), sticky=tk.NW)
        self.buttons['n_lv3'].grid(
            row=6, padx=INIT_X+150, pady=(15, 6), sticky=tk.NW)

        # show current odds
        self.current_odds_label = tk.Label(
            self, textvariable=self.current_odds_var, font=controller.label_font, bg="#FFC736")
        self.current_odds_label.grid(
            row=7, padx=INIT_X-450, pady=(45, 6), sticky=tk.NW)

        # odds_menu buttons
        self.odds5X = tk.Button(self, text="5X", font=controller.button_font,
                                fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60",
                                command=lambda: self.get_oddsMenu(5))
        self.odds10X = tk.Button(self, text="10X", font=controller.button_font,
                                 fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60",
                                 command=lambda: self.get_oddsMenu(10))
        self.odds15X = tk.Button(self, text="15X", font=controller.button_font,
                                 fg='#354C60', bg='white', width=25, height=1, activeforeground='white', activebackground="#354C60",
                                 command=lambda: self.get_oddsMenu(15))

        self.odds5X.grid(row=8, padx=INIT_X-450, pady=(20, 6), sticky=tk.NW)
        self.odds10X.grid(row=8, padx=INIT_X-150, pady=(20, 6), sticky=tk.NW)
        self.odds15X.grid(row=8, padx=INIT_X+150, pady=(20, 6), sticky=tk.NW)

        # next btn
        self.next_btn = tk.Button(self, text="NEXT", font=controller.button_font,
                                  bg='#354C60', fg='white', width=25, height=1, activeforeground='white', activebackground="#354C60",
                                  command=lambda: self.check_info())
        self.next_btn.grid(row=9, padx=INIT_X-150,
                           pady=(30, 6), sticky=tk.NW)

        # to update info
        self.update_info()

    def update_info(self):
        """ update user infomation(USER_NAME, USER_TITLE, ASSETS)"""
        global USER_NAME, ASSETS, USER_TITLE, user_finished
        # update user info
        self.name_var.set(USER_NAME)
        self.usertitle_var.set(USER_TITLE)
        self.assets_var.set(str(format(ASSETS, ',')))

        # update btn of playable game
        for i in self.buttons:
            if ASSETS < fee_dict[i[4]] + chip_dict[i[4]] * 5:
                self.buttons[i].configure(state=tk.DISABLED, cursor="x_cursor")
            else:
                self.buttons[i].configure(state=tk.NORMAL, cursor="arrow")
        # update picked game and odds
        if len(CURRENT_DATASET) > 0:
            self.current_dataset_var.set(
                "目前選取的題庫是： " + dataset_dict[CURRENT_DATASET[0]] + CURRENT_DATASET[4])
        else:
            self.current_dataset_var.set(
                "目前選取的題庫是： ")
        self.current_odds_var.set("目前選取的賠率是：" + str(CURRENT_ODDS))

        # update btn of finished game
        for i in user_finished:
            self.buttons[i].configure(
                state=tk.DISABLED, cursor="x_cursor", bg="light grey")

        self.after(100, self.update_info)

    def get_datasetMenu(self, btn):
        """ get the dataset name which is chosen currently"""
        global CURRENT_DATASET
        CURRENT_DATASET = btn

    def get_oddsMenu(self, btn):
        """ get the value of odds which is chosen currently"""
        global CURRENT_ODDS
        CURRENT_ODDS = btn

    def check_info(self):
        """ check game in(CURRENTDATASET, CURRENTODDS) is empty"""
        global CURRENT_DATASET, CURRENT_ODDS
        # check if CURRENT_DATASET is empty
        if CURRENT_DATASET == "":
            self.controller.show_message("請選取題庫")
        # check if CURRENT_ODDS is empty
        elif CURRENT_ODDS == 0:
            self.controller.show_message("請選取賠率")
        else:
            self.doublecheck_window()

    def doublecheck_window(self):
        """ pop up CURRENT_DATASET and CURRENT_ODDS to revise or confirm"""
        global INIT_X, INIT_Y, CURRENT_DATASET, CURRENT_ODDS, dataset_dict
        doublecheck_window = tk.Toplevel(self, width=INIT_X, height=INIT_Y)
        # place toplevel in the center of screen
        x = INIT_X-50  # the position of x
        y = INIT_Y-50  # the position of y
        doublecheck_window.geometry('%dx%d+%d+%d' % (400, 200, x, y))
        doublecheck_window.title("double check")
        # show current dataset & odds
        label_dataset = tk.Label(doublecheck_window,
                                 text="選擇的關卡是: "+dataset_dict[CURRENT_DATASET[0]], font=self.controller.button_font, fg='#354C60')
        label_odds = tk.Label(doublecheck_window,
                              text="選擇的賠率是: "+str(CURRENT_ODDS)+"X", font=self.controller.button_font, fg='#354C60')
        label_dataset.pack(fill='x', padx=30, pady=5)
        label_odds.pack(fill='x', padx=30, pady=5)

        # revise button
        revise_btn = tk.Button(doublecheck_window, text="修改", font=self.controller.button_font,
                               fg='#354C60', bg='white', width=15, height=1, activeforeground='white', activebackground="#354C60",
                               command=lambda: doublecheck_window.withdraw())
        revise_btn.pack(side="left", padx=12, pady=10)
        # confirm button
        confirm_btn = tk.Button(doublecheck_window, text="確認", font=self.controller.button_font,
                                fg="#354C60", bg='white', width=15, height=1, activeforeground='white', activebackground="#354C60",
                                command=lambda: self.onClick_confirm(doublecheck_window))
        confirm_btn.pack(side="left", padx=12, pady=10)

    def onClick_confirm(self, doublecheck_window):
        global ASSETS, CURRENT_DATASET, fee_dict
        # get dataset
        self.get_dataset()

        # calculate assets
        ASSETS -= fee_dict[CURRENT_DATASET[4]]

        # close toplevel & change page
        doublecheck_window.withdraw()
        self.controller.show_frame("GamePage")

    def get_dataset(self):
        """ get data from dataset and get index of question"""
        global FILE_PATH, CURRENT_DATASET, ques_index, ques_list

        filename = FILE_PATH + CURRENT_DATASET + ".csv"
        with open(filename, encoding="utf-8-sig") as f:
            rows = csv.reader(f)
            for row in rows:
                # assign data to ques_list
                ques_list.append(row)

        # random pick 5 numbers as index of question
        ques_index = random.sample(range(0, len(ques_list)), 5)


class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        global INIT_X, INIT_Y

        tk.Frame.__init__(self, parent)
        self.controller = controller

        # variable of assets
        self.assets_var = tk.StringVar()

        # variable of question and choices
        self.question_var = tk.StringVar()
        self.choiceA_var = tk.StringVar()
        self.choiceB_var = tk.StringVar()
        self.choiceC_var = tk.StringVar()
        self.choiceD_var = tk.StringVar()

        # background
        background = ImageTk.PhotoImage(Image.open(
            "ref/img/game_page.png").resize((1366, 768)))
        self.background_img = tk.Label(self, image=background)
        self.background_img.image = background
        self.background_img.place(x=0, y=0, relwidth=1, relheight=1)

        # assets info
        self.assets_label = tk.Label(
            self, textvariable=self.assets_var, font=controller.title_font, bg="white")
        self.assets_label.grid(row=0, padx=INIT_X+450,
                               pady=(30, 6), sticky=tk.NW)

        # question
        self.question_labelframe = tk.LabelFrame(self, text="Question",
                                                 font=controller.title_font, bg="white", width=100)
        self.question_label = tk.Label(
            self.question_labelframe, textvariable=self.question_var, font=controller.label_font, width=60, height=3, wraplength=600, justify='left', bg="white")
        self.question_labelframe.grid(
            row=1, columnspan=3, rowspan=10, padx=INIT_X-400, pady=(100, 14), sticky=tk.NW)
        self.question_label.grid()

        # choice buttons
        self.choice_btn = {
            '1': tk.Button(self, textvariable=self.choiceA_var, font=controller.button_font,
                           bg='white', fg='black', width=35, height=3, activebackground='#32326B', activeforeground="white", command=lambda: self.submit_answer(0)),
            '2': tk.Button(self, textvariable=self.choiceB_var, font=controller.button_font,
                           bg='white', fg='black', width=35, height=3, activebackground='#32326B', activeforeground="white", command=lambda: self.submit_answer(1)),
            '3': tk.Button(self, textvariable=self.choiceC_var, font=controller.button_font,
                           bg='white', fg='black', width=35, height=3, activebackground='#32326B', activeforeground="white", command=lambda: self.submit_answer(2)),
            '4': tk.Button(self, textvariable=self.choiceD_var, font=controller.button_font,
                           bg='white', fg='black', width=35, height=3, activebackground='#32326B', activeforeground="white", command=lambda: self.submit_answer(3))
        }
        self.choice_btn['1'].grid(row=20, padx=INIT_X-400,
                                  pady=(30, 6), sticky=tk.NW)
        self.choice_btn['2'].grid(row=20, padx=INIT_X+50,
                                  pady=(30, 6), sticky=tk.NW)
        self.choice_btn['3'].grid(row=21, padx=INIT_X-400,
                                  pady=(30, 6), sticky=tk.NW)
        self.choice_btn['4'].grid(row=21, padx=INIT_X+50,
                                  pady=(30, 6), sticky=tk.NW)

        self.update_info()

    def update_info(self):
        """ get current question and its choices"""
        global ASSETS, ques_list, ques_index
        if len(ques_index) != 0:
            # set assets
            self.assets_var.set(str(format(ASSETS, ',')))
            # get question
            self.question_var.set(ques_list[ques_index[0]][0])

            # get choiceA~D
            self.choiceA_var.set(ques_list[ques_index[0]][1])
            self.choiceB_var.set(ques_list[ques_index[0]][2])
            self.choiceC_var.set(ques_list[ques_index[0]][3])
            self.choiceD_var.set(ques_list[ques_index[0]][4])

            # reset btn color
            for i in self.choice_btn:
                self.choice_btn[i].configure(bg="white")

        self.after(800, self.update_info)

    def submit_answer(self, ans):
        """ check answer and calculate assets"""
        global ASSETS, ASSETS_ADD, CURRENT_DATASET, CURRENT_ODDS, BANKRUPTCY, ques_list, ques_index, chip_dict
        # correct answer
        if ans == int(ques_list[ques_index[0]][5]):
            # calculate assets
            ASSETS += CURRENT_ODDS * chip_dict[CURRENT_DATASET[4]]
            ASSETS_ADD += CURRENT_ODDS * chip_dict[CURRENT_DATASET[4]]
            # change btn color according to submit answer
            self.choice_btn[str(ans+1)].configure(bg="light green")
        # wrong answer
        else:
            # calculate assets
            ASSETS -= CURRENT_ODDS * chip_dict[CURRENT_DATASET[4]]
            ASSETS_ADD -= CURRENT_ODDS * chip_dict[CURRENT_DATASET[4]]
            # change btn color according to submit answer
            self.choice_btn[str(ans+1)].configure(bg="light coral")
            self.choice_btn[str(int(ques_list[ques_index[0]][5])+1)
                            ].configure(bg="light green")

        # delete completed question in ques_index
        ques_index.pop(0)
        print(ques_index)

        # bankruptcy
        if ASSETS < 0:
            self.controller.show_message("破產!將跳出遊戲")
            BANKRUPTCY = True
            self.controller.show_frame("ResultPage")

        # finish game
        if len(ques_index) == 0:
            level_finished[CURRENT_DATASET[4]] += 1
            # assets not enough for next game
            if ASSETS < 6000000:
                BANKRUPTCY = True
            elif level_finished['1'] == 4 and ASSETS < 30000000:
                BANKRUPTCY = True
            elif level_finished['1'] == 4 and level_finished['2'] == 4 and ASSETS < 60000000:
                BANKRUPTCY = True
        # assets enough for next game
            else:
                # add data
                user_finished.append(CURRENT_DATASET)
                self.usertitle_attain()
                if len(user_finished) == 12:
                    self.controller.show_message("完成所有關卡!")

            if BANKRUPTCY == True:
                self.controller.show_message("剩餘資產不足支付其他關卡入場費，淪為遊民，視為破產!")

            self.after(1000, lambda: self.controller.show_frame("ResultPage"))

    def usertitle_attain(self):
        """judge user title according to assets"""
        global ASSETS, ASSETS_ADD, USER_TITLE, title_dict
        if ASSETS_ADD > 0:
            for i in title_dict:
                if ASSETS >= title_dict[i] and title_dict[i] > title_dict[USER_TITLE]:
                    USER_TITLE = i
        elif ASSETS_ADD < 0:
            for i in title_dict:
                if ASSETS >= title_dict[i] and title_dict[i] < title_dict[USER_TITLE]:
                    USER_TITLE = i


class ResultPage(tk.Frame):

    def __init__(self, parent, controller):
        global INIT_X, INIT_Y

        tk.Frame.__init__(self, parent)
        self.controller = controller

        # variables of user info
        self.username_var = tk.StringVar()
        self.usertitle_var = tk.StringVar()
        self.assets_var = tk.IntVar()
        self.assets_add_var = tk.IntVar()
        self.bankruptcy_var = tk.BooleanVar()

        # background
        self.background = ImageTk.PhotoImage(
            Image.open("ref/img/result_page.png").resize((1366, 768)))
        self.background_img = tk.Label(self, image=self.background)
        self.background_img.image = self.background
        self.background_img.place(x=0, y=0, relwidth=1, relheight=1)

        # title
        self.title_label = tk.Label(
            self, text="遊戲結果: ", font=controller.title_font, bg="#212121", fg="white")
        self.title_label.grid(
            row=4, ipadx=30, ipady=10, padx=INIT_X+80, pady=(50, 6), sticky=tk.NW)
        # user name
        self.username_text_label = tk.Label(
            self, text="玩家名稱: ", font=controller.label_font, bg="#212121", fg="white")
        self.username_label = tk.Label(
            self, textvariable=self.username_var, font=controller.label_font, bg="#212121", fg="white")
        self.username_text_label.grid(
            row=5, ipadx=30, ipady=10, padx=INIT_X+30, pady=(40, 6), sticky=tk.NW)
        self.username_label.grid(
            row=5, ipadx=30, ipady=10, padx=INIT_X+180, pady=(40, 6), sticky=tk.NW)

        # assets
        self.assets_text_label = tk.Label(
            self, text="個人資產: ", font=self.controller.label_font, bg="#212121", fg="white")
        self.assets_label = tk.Label(
            self, textvariable=self.assets_var, font=self.controller.label_font, bg="#212121", fg="white")
        self.assets_text_label.grid(
            row=6, ipadx=30, ipady=10, padx=INIT_X+30, pady=(40, 6), sticky=tk.NW)
        self.assets_label.grid(
            row=6, ipadx=30, ipady=10, padx=INIT_X+180, pady=(40, 6), sticky=tk.NW)

        # assets win / lose in game
        self.assets_add_text_label = tk.Label(
            self, text="賺/賠: ", font=self.controller.label_font, bg="#212121", fg="white")
        self.assets_add_label = tk.Label(
            self, textvariable=self.assets_add_var, font=self.controller.label_font, bg="#212121", fg="white")
        self.assets_add_text_label.grid(
            row=8, ipadx=30, ipady=10, padx=INIT_X+30, pady=(40, 6), sticky=tk.NW)
        self.assets_add_label.grid(
            row=8, ipadx=30, ipady=10, padx=INIT_X+180, pady=(40, 6), sticky=tk.NW)

        # user title
        self.usertitle_text_label = tk.Label(
            self, text="恭喜獲得: ", font=self.controller.label_font, bg="#212121", fg="white")
        self.usertitle_label = tk.Label(
            self, textvariable=self.usertitle_var, font=self.controller.label_font, bg="#212121", fg="white")
        self.usertitle_text_label.grid(
            row=10, ipadx=30, ipady=10, padx=INIT_X+30, pady=(40, 6), sticky=tk.NW)
        self.usertitle_label.grid(
            row=10, ipadx=30, ipady=10, padx=INIT_X+180, pady=(40, 6), sticky=tk.NW)

        # stop button
        self.stop_btn = tk.Button(self, text="✖End Game", font=controller.button_font,
                                  bg="white", fg="#770C20", width=15, height=3, activeforeground='white', activebackground="#770C20",                                 command=lambda: app.destroy())
        self.stop_btn.grid(row=30, padx=INIT_X-200, pady=(30, 6), sticky=tk.NW)
        # menu button
        self.menu_btn = tk.Button(self, text="Play More➡", font=self.controller.button_font,
                                  bg="white", fg="#32326B", width=15, height=3, activeforeground='white', activebackground="#32326B",
                                  command=lambda: self.play_again())
        self.menu_btn.grid(row=30, padx=INIT_X+430,
                           pady=(30, 6), sticky=tk.NW)

        # to update information
        self.update_info()

    def show_bankruptcy(self):
        """delete information for not bankruptcy"""
        self.title_label.destroy()
        self.username_text_label.destroy()
        self.username_label.destroy()
        self.assets_text_label.destroy()
        self.assets_label.destroy()
        self.assets_add_text_label.destroy()
        self.assets_add_label.destroy()
        self.usertitle_text_label.destroy()
        self.usertitle_label.destroy()
        self.menu_btn.destroy()

    def update_info(self):
        """ update information(USERNAME, ASSETS, ASSETS_ADD)"""
        global USER_NAME, USER_TITLE, ASSETS, ASSETS_ADD, BANKRUPTCY

        if USER_NAME != "":
            if BANKRUPTCY == True:
                # update background
                # TODO
                img = ImageTk.PhotoImage(
                    Image.open("ref/img/bankruptcy.png").resize((1366, 768)))
                self.background_img.configure(image=img)
                self.background_img.image = img
                self.show_bankruptcy()
            else:
                # update user info
                self.usertitle_var.set(USER_TITLE)
                self.assets_var.set(str(format(ASSETS, ',')))
                self.assets_add_var.set(str(format(ASSETS_ADD, ',')))

                # if finish all games
                if len(user_finished) == 12:
                    self.menu_btn.destroy()

        self.username_var.set(USER_NAME)
        self.bankruptcy_var.set(BANKRUPTCY)
        self.after(500, self.update_info)

    def play_again(self):
        """ clear data and change page"""
        global CURRENT_DATASET, CURRENT_ODDS, ASSETS_ADD, ques_list

        # clear data
        CURRENT_DATASET = ""
        CURRENT_ODDS = 0
        ASSETS_ADD = 0
        ques_list.clear()

        # change page
        self.controller.show_frame("MenuPage")

    def stop_game(self):
        """shut down game"""
        app.destroy()


# Driver Code
if __name__ == "__main__":
    app = App()
    # place frame in the center of screen
    x = app.winfo_screenwidth()/2 - INIT_X  # the position of x
    y = app.winfo_screenheight()/2 - INIT_Y  # the position of y
    app.geometry('%dx%d+%d+%d' % (1366, 768, x, y))

    app.title("Want to Be a Billionaire")
    app.mainloop()
