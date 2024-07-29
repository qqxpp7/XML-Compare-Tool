# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:15:11 2024

@author: a9037
"""

import tkinter as tk
import shared_data as sd
import customtkinter as ctk

class ComparisonPage_2(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        '''
        右邊畫面分為上、中、下三個區域
        ''' 
        self.top_right_frame = ctk.CTkFrame(self)
        self.top_right_frame.pack(pady=5, padx=10, fill="x")

        self.middle_right_frame = ctk.CTkFrame(self)
        self.middle_right_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        self.bottom_right_frame = ctk.CTkFrame(self)
        self.bottom_right_frame.pack(pady=5, padx=10, fill="x")
        
        #右中左-中中-中右
        '''
        中間區域分三個小視窗
        ''' 
        self.mylabel = tk.Label(self.middle_right_frame, bg='#87CEFA', text='選擇忽略或比對的key')
        self.mylabel.pack(fill="both",side=tk.TOP) 
        
        self.left_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.left_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        self.mid_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.mid_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        self.rig_middle_right_frame = ctk.CTkFrame(self.middle_right_frame)
        self.rig_middle_right_frame.pack(pady=5, padx=5, side="left", fill="both", expand=True)
        
        '''
        上面區域

        
        '''
        self.mylabel = tk.Label(self.top_right_frame,  text='2/3    選擇Element')
        self.mylabel.pack(fill="both",side=tk.LEFT) 
        
        self.choose_button = ctk.CTkButton(self.top_right_frame, text="下一頁", width=200)
                                         
        self.choose_button.pack(side=tk.RIGHT, pady=5, padx=5)
        
        self.return_button = ctk.CTkButton(self.top_right_frame, text="上一頁", width=200
                                         , command=lambda: self.controller.show_frame("ComparisonPage"))
        self.return_button.pack(side=tk.LEFT, pady=5, padx=5)