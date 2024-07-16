# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:01:56 2024

@author: a9037
"""
import customtkinter as ctk

class CopyDataPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = ctk.CTkLabel(self, text="Copy 資料功能頁面")
        label.pack(padx=10, pady=10)
