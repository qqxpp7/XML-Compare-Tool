import tkinter as tk
import customtkinter as ctk
import shared_data
from page1 import SearchPage
from page2 import PositionSettingPage
from page3 import XMLSplitPage
from page4 import FindDifferencesPage
from page5 import ComparisonPage
from page6 import CopyDataPage
from page7 import ElementSplitPage

class XMLCompareTool:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Compare Tool")
        self.root.geometry("1000x600")
        
        self.selected_function = tk.StringVar(value="01 位置設定")
        self.function_buttons = {}

        self.create_left_frame()
        self.create_right_frames()
        self.create_function_buttons()

    def create_left_frame(self):
        self.left_frame = ctk.CTkFrame(self.root, width=200)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

    def create_right_frames(self):
        self.frames = {}
        self.frames["SearchPage"] = SearchPage(self.root, self)
        self.frames["PositionSettingPage"] = PositionSettingPage(self.root, self)
        self.frames["XMLSplitPage"] = XMLSplitPage(self.root, self)
        self.frames["FindDifferencesPage"] = FindDifferencesPage(self.root, self)
        self.frames["ComparisonPage"] = ComparisonPage(self.root, self)
        self.frames["CopyDataPage"] = CopyDataPage(self.root, self)
        self.frames["ElementSplitPage"] = ElementSplitPage(self.root, self)

        for frame in self.frames.values():
            frame.pack_forget()

        self.frames["PositionSettingPage"].pack(fill="both", expand=True)

    def create_function_buttons(self):
        categories = {
            "": ["搜尋"],
            "主功能": ["01 位置設定", "02 XML 拆分", "03 找出差異", "04 比對"],
            "其他功能": ["Copy 資料", "Element 分割"]
        }

        for category, functions in categories.items():
            if category:
                label = ctk.CTkLabel(self.left_frame, text=category, font=("Arial", 12, "bold"))
                label.pack(pady=5, anchor="center")
            for function in functions:
                button = ctk.CTkButton(self.left_frame, text=function, width=180, anchor="center", fg_color="white", text_color="black",
                                       command=lambda f=function: self.on_function_button_click(f))
                button.pack(pady=5, anchor="center")
                self.function_buttons[function] = button
            if category in ["", "主功能"]:
                line = ctk.CTkFrame(self.left_frame, height=2, fg_color="lightgray")
                line.pack(fill="x", pady=5)

        self.function_buttons["01 位置設定"].configure(fg_color="lightblue", text_color="black")

    def on_function_button_click(self, function):
        self.selected_function.set(function)
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") in self.function_buttons.keys():
                widget.configure(fg_color="white", text_color="black")
        self.function_buttons[function].configure(fg_color="lightblue", text_color="black")

        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[self.get_frame_key(function)].pack(fill="both", expand=True)

    def get_frame_key(self, function):
        mapping = {
            "搜尋": "SearchPage",
            "01 位置設定": "PositionSettingPage",
            "02 XML 拆分": "XMLSplitPage",
            "03 找出差異": "FindDifferencesPage",
            "04 比對": "ComparisonPage",
            "Copy 資料": "CopyDataPage",
            "Element 分割": "ElementSplitPage"
        }
        return mapping.get(function, "PositionSettingPage")        

if __name__ == "__main__":
    root = ctk.CTk()  # 創建主窗口
    shared_data.init_shared_vars()  # 初始化共享變數
    app = XMLCompareTool(root)
    root.mainloop()
