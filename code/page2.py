# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:44:42 2024

@author: a9037
"""
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import shared_data

class PositionSettingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.top_right_frame = ctk.CTkFrame(self)
        self.top_right_frame.pack(pady=10, padx=10, fill="x")

        self.bottom_right_frame = ctk.CTkFrame(self)
        self.bottom_right_frame.pack(pady=10, padx=10, fill="both", expand=True)
       
        self.path_before_entry = self.create_path_selector(self.top_right_frame, 0, "Before 資料夾:", 400, "Browse", self.select_folder)
        self.path_after_entry = self.create_path_selector(self.top_right_frame, 1, "After 資料夾:", 400, "Browse", self.select_folder)
        self.report_output_entry = self.create_path_selector(self.top_right_frame, 2, "報告產出資料夾：", 400, "Browse", self.select_folder)
        
        save_button = ctk.CTkButton(self.top_right_frame, text="儲存", command=self.save_path, width=100)
        save_button.grid(row=3, column=2, columnspan=3, pady=20, padx=20)

        self.attachment_format_entry = self.default_input(self.bottom_right_frame, 0, "加副檔名：", 400, "xml")
        
        self.before_button_var = tk.IntVar(value=1)
        self.after_button_var = tk.IntVar(value=1)

        self.add_extension_before_button = self.create_toggle_button(self.bottom_right_frame, "Before", 1, 0, 
            lambda: self.on_button_click(self.before_button_var, self.add_extension_before_button))

        self.add_extension_after_button = self.create_toggle_button(self.bottom_right_frame, "After", 1, 1, 
            lambda: self.on_button_click(self.after_button_var, self.add_extension_after_button))
        
        ok_button = ctk.CTkButton(self.bottom_right_frame, text="修改", command=self.execute, width=100)
        ok_button.grid(row=2, column=4, columnspan=2, pady=10, padx=10)

    def create_path_selector(self, frame, row, label_text, entry_width, button_text, command):
        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.grid(row=row, column=0, pady=20, padx=20, sticky="w")
        entry = ctk.CTkEntry(frame, width=entry_width)
        entry.grid(row=row, column=1)
        button = ctk.CTkButton(frame, text=button_text, command=lambda: command(entry))
        button.grid(row=row, column=2)
        return entry

    def select_folder(self, entry):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, tk.END)
            entry.insert(0, folder_path)

    def save_path(self):
        shared_data.before_path.set(self.path_before_entry.get())
        shared_data.after_path.set(self.path_after_entry.get())
        shared_data.report_output_path.set(self.report_output_entry.get())
        messagebox.showinfo("信息", "路徑已保存")

    def default_input(self, frame, row, label_text, entry_width, default_text):
        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.grid(row=row, column=0, pady=20, padx=20, sticky="w")
        entry = ctk.CTkEntry(frame, width=entry_width)
        entry.grid(row=row, column=1, sticky="w")
        entry.insert(0, default_text)
        return entry

    def toggle_button(self, button, var):
        if var.get() == 1:
            button.configure(fg_color="blue")
        else:
            button.configure(fg_color="gray")

    def on_button_click(self, button_var, button):
        button_var.set(1 if button_var.get() == 0 else 0)
        self.toggle_button(button, button_var)

    def create_toggle_button(self, frame, text, row, column, command):
        button = ctk.CTkButton(frame, text=text, command=command, width=100, fg_color="blue")
        button.grid(row=row, column=column, pady=30, padx=30, sticky="w")
        return button

    def add_extension_to_files(self, folder_path, extension):
        if not folder_path or not extension:
            return
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                base, ext = os.path.splitext(filename)
                new_filename = f"{base}.{extension}"
                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_file_path)

    def execute(self):
        self.attachment_format = self.attachment_format_entry.get()
        
        if self.before_button_var.get() == 1:
            self.add_extension_to_files(shared_data.before_path.get(), self.attachment_format)
        if self.after_button_var.get() == 1:
            self.add_extension_to_files(shared_data.after_path.get(), self.attachment_format)       
        messagebox.showinfo("信息", "文件名已修改")