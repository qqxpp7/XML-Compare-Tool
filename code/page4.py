# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:00:48 2024

@author: a9037
"""
import os
import tkinter as tk
import customtkinter as ctk
import shared_data


class FindDifferencesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        
        self.sequence_label = ctk.CTkLabel(self, text="移動差異檔案：")
        self.sequence_label.grid(row=2, column=0, pady=10, padx=20, sticky="w")       
        self.sequence_var = tk.StringVar(value="否")
        self.sequence_options = ctk.CTkSegmentedButton(master=self,
             values=["是", "否"],variable=self.sequence_var,)        
        self.sequence_options.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        
        self.split_element_entry = self.default_input(self, 1,"報告書名稱：", 400, "Different_Report")
        
        execute_button = ctk.CTkButton(self, text="執行", command=self.execute, width=200)
        execute_button.grid(row=3, column=0, pady=10, padx=10)
        
        open_report_button = ctk.CTkButton(self, text="開啟報告", command=self.open_report, 
                                           width=200, fg_color="#CD5C5C")
        open_report_button.grid(row=4, column=0, pady=10, padx=10)
    
        
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
    
    def open_report(self):
        self.attachment_format = self.split_element_entry.get()
        
    def execute(self):
        print("執行")
        