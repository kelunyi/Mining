from Tix import Tk
from Tkinter import Menu, StringVar, OptionMenu, Scrollbar
from ttk import Label
from rbc import RBC
from scotia import Scotia
from cibc import CIBC
import mysql.connector
from _tkinter import *
__author__ = 'Shengnuo'


##VAIRABLE DECLARATION STARTS##########################33

rbc = RBC()
scotia = Scotia()
scotia.mine_to_database()
#rbc.mine_to_database()

###################VAIRABLE DECLARATION ENDS##########################33


'''
company_label.grid(row=0, column=0)
company_options_menu.grid(row=0, column=1)
root.mainloop()
'''
#scotia.mining()

'''
bank1 = Scotia()
#bank1.mining()

bank2 = RBC()
#bank2.mining()

bank1.get_scotia()
'''
