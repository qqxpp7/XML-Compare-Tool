# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:50:40 2024

@author: a9037
"""
import customtkinter as ctk

class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="搜尋頁面")
        
        label.pack(padx=10, pady=10)
