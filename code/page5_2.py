# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 15:15:11 2024

@author: a9037
"""

import tkinter as tk
import shared_data as sd
import customtkinter as ctk
from tkinter import ttk, messagebox, scrolledtext

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
        self.mylabel = tk.Label(self.top_right_frame,  text='2/2    選擇Element')
        self.mylabel.pack(fill="both",side=tk.LEFT) 
        
        self.choose_button = ctk.CTkButton(self.top_right_frame, text="執行", width=200)
                                         
        self.choose_button.pack(side=tk.RIGHT, pady=5, padx=5)
        
        self.return_button = ctk.CTkButton(self.top_right_frame, text="上一頁", width=200
                                         , command=lambda: self.controller.show_frame("ComparisonPage"))
        
        self.return_button.pack(side=tk.LEFT, pady=5, padx=5)
        
        #右中左
        '''
        中間區域的左邊
        
        
        '''
        self.text_area = scrolledtext.ScrolledText(self.left_middle_right_frame, wrap=tk.NONE, width=35, height=25, font=("Helvetica",14))
        self.text_area.pack(fill=tk.BOTH, expand=1)
        
        self.x_scrollbar = tk.Scrollbar(self.left_middle_right_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        self.x_scrollbar.pack(side='bottom', fill='x')
        self.text_area['xscrollcommand'] = self.x_scrollbar.set
        #Lock the text area to read-only
        self.text_area.bind("<Key>", lambda e: "break")
        
        # 右中間框架
        '''
        中間區域的中間
        會秀出檔案的Element及Text
        wrap=tk.NONE 禁用自動換行
        '''
        self.text_area = scrolledtext.ScrolledText(self.mid_middle_right_frame, wrap=tk.NONE, width=35, height=25, font=("Helvetica",14))
        self.text_area.pack(fill=tk.BOTH, expand=1)
        
        self.x_scrollbar = tk.Scrollbar(self.mid_middle_right_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        self.x_scrollbar.pack(side='bottom', fill='x')
        self.text_area['xscrollcommand'] = self.x_scrollbar.set
        #Lock the text area to read-only
        self.text_area.bind("<Key>", lambda e: "break")
        
        #右中右
        '''
        中間區域的右邊
        展示所選擇的key視窗，以及新增(+)與刪除(-)的按鈕
        ''' 
        self.option_listbox = tk.Listbox(self.rig_middle_right_frame, font=("Helvetica",14))
        self.option_listbox.pack(fill=tk.BOTH, expand=True)
               
        self.add_button = ctk.CTkButton(self.rig_middle_right_frame, text="+", width=80, height=30)
        self.add_button.pack(side=tk.LEFT, pady=5,padx=5)

        self.remove_button = ctk.CTkButton(self.rig_middle_right_frame, text="-", width=80, height=30)
        self.remove_button.pack(side=tk.LEFT,pady=5,padx=5)
        
        '''
        下面區域
        清空舊資料的選擇
        開啟COPY資料夾的按鈕
        
        '''
        self.report_name_entry = self.default_input(self.bottom_right_frame, 0
                                                    , "報告書名稱：", 400, "Compare_Report")
        
        self.sequence_label = ctk.CTkLabel(self.bottom_right_frame, text="比對模式：")
        self.sequence_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.sequence_var = tk.StringVar(value=" 忽略 ")
        self.sequence_options = ctk.CTkSegmentedButton(master=self.bottom_right_frame,
                                                       values=[" 比對 ", " 忽略 "], variable=self.sequence_var)
        self.sequence_options.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        self.open_folder_button = ctk.CTkButton(self.bottom_right_frame, text="AI分析" 
                                                , width=200, fg_color="#CD5C5C")
        self.open_folder_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        
        self.open_folder_button = ctk.CTkButton(self.bottom_right_frame, text="開啟報告" 
                                                , width=200, fg_color="#CD5C5C")
        self.open_folder_button.grid(row=2, column=2, columnspan=2, pady=10, padx=10)
        
        
    def default_input(self, frame, row, label_text, entry_width, default_text):
        '''
        有預設輸入值的標籤與輸入框
        '''
        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.grid(row=row, column=0, pady=20, padx=20, sticky="w")
        entry = ctk.CTkEntry(frame, width=entry_width)
        entry.grid(row=row, column=1, sticky="w")
        entry.insert(0, default_text)
        return entry  
        
        
        
        
        