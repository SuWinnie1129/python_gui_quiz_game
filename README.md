# Want to Be a Billionaire -- python GUI game

introduction

## Installation

- Install PIL:

1. for Windows OS:
   ```
   pip install pillow
   ```
2. for Mac OS:
   ```
   python3 -m pip install --upgrade pip
   python3 -m pip install --upgrade Pillow
   ```

## Get Start

```python
  python main.py
```

## Code Structure

```properties
main.py
    |
    |--global variables
    |
    |--class App(tk.Tk) *basic setting*
    |
    |--class StartPage(tk.Frame)  *login page*
    |
    |--class HomePage(tk.Frame) *instruction page*
    |
    |--class MenuPage(tk.Frame) *game menu page*
    |
    |--class GamePage(tk.Frame) *game page*
    |
    |--class ResultPage(tk.Frame) *result page*
```

## Library

```python
import tkinter as tk  #set GUI
import tkinter.font as tkfont # set GUI font
import tkinter.messagebox as tkmessage # set GUI message box
import csv # handle csv file for question dataset
import random # handle questions order
from PIL import Image, ImageTk # handle background image
```

## Interfaces and Functions

There 5 interfaces in this project, including:

- <a href="###StartPage">Start Page</a>
- <a href="###HomePage">Home Page</a>
- <a href="###MenuPage">Menu Page</a>
- <a href="###GamePage">Game Page</a>
- <a href="###ResultPage">Result Page</a>

### StartPage

1. **Input user name**
   ```python=
   self.name_label = tk.Label(self, text="User Name:",...)
   self.name = tk.Entry(self)
   ```
2. **Judge input field is null or not**

   ```python=
   self.next_btn = tk.Button(..., command=lambda: self.get_username())

   # get input value
   USER_NAME = self.name.get()
   # check if input is empty
   if USER_NAME == "":
       self.controller.show_message("請輸入玩家名稱")
   ```

### HomePage

1. **Show user information**
2. **Show game instruction**

### MenuPage

1. **Disable game buttons which assets is not enough**
   ```python=
   # judge if assets is enough to play game
   for i in self.buttons:
     # not meet lower boundary
     if ASSETS < fee_dict[i[4]] + chip_dict[i[4]] * 5:
       self.buttons[i].configure(state=tk.DISABLED, cursor="x_cursor", bg="light grey")
   ```
2. **Disable game buttons which has finished**
   ```python=
   # if finished, change configure of button
   for i in user_finished:
     self.buttons[i].configure(state=tk.DISABLED, cursor="x_cursor",...)
   ```
3. **Show game and odds which is chosen currently**

   ```python=
   # button widgets(game and odds)
   self.buttons = {
           's_lv1': tk.Button(..., command=lambda: self.get_datasetMenu("s_lv1")),
       ...
   }
   self.odds2X = tk.Button(..., command=lambda: self.get_oddsMenu(5))

   # get chosen button
   def get_datasetMenu(self, btn):
       CURRENT_DATASET = btn
   def get_oddsMenu(self, btn):
       CURRENT_ODDS = btn
   # show to user
   self.current_dataset_var.set("目前選取的題庫是： " + dataset_dict[CURRENT_DATASET[0]] + CURRENT_DATASET[4])
   self.current_odds_var.set("目前選取的賠率是：" + str(CURRENT_ODDS))
   ```

4. **Judge game and odds are chosen or not**
   ```python=
   if CURRENT_DATASET == "":
       self.controller.show_message("請選取題庫")
   # check if CURRENT_ODDS is empty
   elif CURRENT_ODDS == 0:
       self.controller.show_message("請選取賠率")
   ```
5. **Read file and sort questions in random order**
   ```python=
   # read file
   filename = FILE_PATH + CURRENT_DATASET + ".csv"
   with open(filename, encoding="utf-8-sig") as f:
       rows = csv.reader(f)
       ...
   # random pick 5 numbers as index of question
   ques_index = random.sample(range(0, len(ques_list)), 5)
   ```

### GamePage

1. **Show question and choices**

   ```python=
   # set tkinter variables
   self.question_var = tk.StringVar()
   self.choiceA_var = tk.StringVar()
   ...

   # get question
   self.question_var.set(ques_list[ques_index[0]][0])
   # get choiceA~D
   self.choiceA_var.set(ques_list[ques_index[0]][1])
   self.choiceB_var.set(ques_list[ques_index[0]][2])
   self.choiceC_var.set(ques_list[ques_index[0]][3])
   self.choiceD_var.set(ques_list[ques_index[0]][4])

   # delete completed question in ques_index after submit answer
       ques_index.pop(0)

   # update every 0.8s
   self.after(800, self.update_info)
   ```

2. **Show correct / wrong answer on button**

   ```python=
   # choice buttons
   self.choice_btn = {'1': tk.Button(..., command=lambda: self.submit_answer(0)),
   ...
   }

   # change btn color according to submit answer
   def submit_answer(self, ans):
       # correct answer
       if ans == int(ques_list[ques_index[0]][5]):
           self.choice_btn[str(ans+1)].configure(bg="light green")
       # wrong answer
       else:
           self.choice_btn[str(ans+1)].configure(bg="light coral")
           self.choice_btn[str(int(ques_list[ques_index[0]][5])+1)
                           ].configure(bg="light green")
   ```

3. **Caluculate assets after every question**

   ```python=
   if ans == int(ques_list[ques_index[0]][5]):
       # calculate assets
           ASSETS += CURRENT_ODDS * chip_dict[CURRENT_DATASET[4]]
       # wrong answer
       else:
           # calculate assets
           ASSETS -= CURRENT_ODDS * chip_dict[CURRENT_DATASET[4]]
   ```

4. **Judge assets is enough for other tasks**
   ```python=
   # finish game
   if len(ques_index) == 0:
       # assets not enough for next game
       if ASSETS < 6000000:
           BANKRUPTCY = True
       elif level_finished['1'] == 4 and ASSETS < 30000000:
           BANKRUPTCY = True
       elif level_finished['1'] == 4 and level_finished['2'] == 4 and ASSETS < 60000000:
            BANKRUPTCY = True
       # assets enough for next game
       else:
           ...
   ```

### ResultPage

1. show game result (username, assets, earn/lose )
2. show buttons of playing more or shutting down frame

## Notice

Users of Mac OS are unable to use `cursor='x_cursor'`,please change it to `cursor='arrow'` or other feasible cursor type
