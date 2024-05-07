from customtkinter import *
from PIL import Image
import tkinter
import requests
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox
import datetime

class App(CTk):

    def __init__(self, **kw):
        super().__init__( **kw)
        self.geometry("750x550")
        self.resizable(0,0)
        set_appearance_mode("dark")

        self.title("PavApp")

        self.iconbitmap("logo2.ico")

        self.build_sidebar_ui()

        self.main_view = CTkFrame(master=self, fg_color="#204B6B", corner_radius=0, width=580, height=550)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        self.switch_main_view("LOGIN")
        
    def build_sidebar_ui(self):
        sidebar_frame = CTkFrame(master=self, fg_color="#4385B7",  width=170, height=550, corner_radius=0)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("logo2.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(150, 68))

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        self.sidebar_create_order_btn = CTkButton(master=sidebar_frame, text="Создать заявку", fg_color="transparent", font=("Arial Bold", 14), hover_color="#204B6B", anchor="w", command=lambda: self.switch_main_view("CREATE_ORDER"))

        self.sidebar_all_orders_btn = CTkButton(master=sidebar_frame, text="Все заявки", fg_color="transparent", font=("Arial Bold", 14), hover_color="#204B6B", anchor="w", command=lambda: self.switch_main_view("ALL_ORDERS"))

        self.sidebar_login_btn = CTkButton(master=sidebar_frame, text="Авторизация", fg_color="transparent", font=("Arial Bold", 14), hover_color="#204B6B", anchor="w", command=lambda: self.switch_main_view("LOGIN"))
 
        self.sidebar_logout_btn = CTkButton(master=sidebar_frame, text="Выйти", fg_color="#FF0000", font=("Arial Bold", 14), hover_color="#FF3333", anchor="w", command=self.logout_handler)
        self.sidebar_logout_btn.pack(side="bottom", fill="x", pady=(10, 0))

    def logout_handler(self):
        self.switch_main_view("LOGIN")

    def clear_main_view(self):
        for child in self.main_view.winfo_children():
            child.destroy()

    def switch_main_view(self, view):
        self.view = view
        self.clear_main_view()

        for btn in [self.sidebar_all_orders_btn, self.sidebar_create_order_btn, self.sidebar_login_btn]:
            btn.configure(fg_color="transparent")

        if self.view == "CREATE_ORDER":
            self.build_create_order_ui()
            self.sidebar_create_order_btn.configure(fg_color="#204B6B")
            self.sidebar_logout_btn.pack(fill="x", pady=(10, 0))

            self.sidebar_login_btn.pack_forget()
            self.sidebar_create_order_btn.pack(anchor="center", ipady=5, pady=(30, 0))
            self.sidebar_all_orders_btn.pack(anchor="center", ipady=5, pady=(15, 0))

        elif self.view == "ALL_ORDERS":
            self.build_all_orders_ui()
            self.sidebar_all_orders_btn.configure(fg_color="#204B6B")
            self.sidebar_logout_btn.pack_forget()

            self.sidebar_login_btn.pack_forget()
            self.sidebar_create_order_btn.pack(anchor="center", ipady=5, pady=(30, 0))
            self.sidebar_all_orders_btn.pack(anchor="center", ipady=5, pady=(15, 0))

        elif self.view == "LOGIN":
            self.build_login_ui()
            self.sidebar_login_btn.configure(fg_color="#204B6B")
            self.sidebar_logout_btn.pack_forget()

            self.sidebar_login_btn.pack(anchor="center", ipady=5, pady=(15, 0))
            self.sidebar_create_order_btn.pack_forget()
            self.sidebar_all_orders_btn.pack_forget()
                
    def create_order(self):
        url = "https://firestore.googleapis.com/v1/projects/pavapp-802bc/databases/(deafault)/documents/tickets"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        input_data = {
            "fields": {
                "ticket_number": {
                    "numberValue": self.ticket_number.get()
                },
                "equipment": {
                    "stringValue": self.equipment.get()
                },
                "fault_type": {
                    "stringValue": self.fault_type.get()
                },
                "problem_description": {
                    "stringValue": self.problem_description.get()
                },
                "client": {
                    "stringValue": self.client.get()
                },
                "status": {
                    "stringValue": self.status.get()
                },
            }
        }

        response = requests.post(url, json=input_data, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            CTkMessagebox(title="Ура", message="Заявку успешно создана", icon="проверить")
        else:
            error_message = response_data["error"]["message"]
            CTkMessagebox(title="Ошибка", message=error_message, icon="cancel")

    def build_create_order_ui(self):
        CTkLabel(master=self.main_view, text="Создание заявки", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=self.main_view, text="Номер заявки", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)
        self.ticket_number = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0)
        self.ticket_number.pack(fill="x", pady=(0,0), padx=27, ipady=10)

        CTkLabel(master=self.main_view, text="Оборудование", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)
        self.equipment = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0)
        self.equipment.pack(fill="x", pady=(0,0), padx=27, ipady=10)

        CTkLabel(master=self.main_view, text="Тип проблемы", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)
        self.fault_type = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0)
        self.fault_type.pack(fill="x", pady=(0,0), padx=27, ipady=10)

        CTkLabel(master=self.main_view, text="Описание проблемы", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)
        self.problem_description = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0)
        self.problem_description.pack(fill="x", pady=(0,0), padx=27, ipady=10)

        CTkLabel(master=self.main_view, text="Клиент", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)
        self.client = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0, width=250)
        self.client.pack(fill="x", pady=(0,0), padx=27, ipady=10)

        CTkLabel(master=self.main_view, text="Статус", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)

        self.status_var = tkinter.StringVar(value="Confirmed")

        CTkRadioButton(master=self.main_view, variable=self.status_var, value="Pending", text="В ожидании", font=("Arial Bold", 14), text_color="#fff", fg_color="#fff", border_color="#fff", hover_color="#F49A44").pack(anchor="nw", padx=27)
        CTkRadioButton(master=self.main_view, variable=self.status_var, value="In work", text="В работе", font=("Arial Bold", 14), text_color="#fff", fg_color="#fff", border_color="#fff", hover_color="#F49A44").pack(anchor="nw", padx=27)
        CTkRadioButton(master=self.main_view, variable=self.status_var, value="Done", text="Выполнено", font=("Arial Bold", 14), text_color="#fff", fg_color="#fff", border_color="#fff", hover_color="#F49A44").pack(anchor="nw", padx=27)

        CTkButton(master=self.main_view, text="Создать", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=self.create_order).pack(fill="both", side="bottom", pady=(25, 25), ipady=10, padx=(27,27))


    def update_quantity(self, new_quantity):
        if new_quantity < 1:
            return

        self.quantity = new_quantity
        self.quantity_label.configure(text=str(self.quantity).zfill(2))

    def query_all_orders(self):
        url = "https://firestore.googleapis.com/v1/projects/pavapp-802bc/databases/(deafault)/documents/tickets"

        params = {
            "mask.fieldPaths": ["ticket_number", "equipment", "fault_type", "problem_description", "client", "status"]
        }

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, params=params, headers=headers)
        response_data = response.json()

        table_data = [
            ["Номер заявки", "Оборудование", "Тип неисправности", "Описание проблемы", "Клиент", "Статус"],
            # ["MacBook Pro", "John Doe", "123 Main St", "Shipped", "1"],
            # ["Galaxy S21", "Jane Smith", "456 Park Ave", "Delivered", "2"],
            # ["PlayStation 5", "Bob Johnson", "789 Broadway", "Processing", "1"],
        ]

        for doc in response_data["documents"]:
            row = []
            if "fields" in doc:
                fields = doc["fields"]
                row.append(fields["ticket_number"]["numberValue"])
                row.append(fields["equipment"]["stringValue"])
                row.append(fields["fault_type"]["stringValue"])
                row.append(fields["problem_description"]["stringValue"])
                row.append(fields["client"]["stringValue"])
                row.append(fields["status"]["stringValue"])

                table_data.append(row)
        
        return table_data
    
    def build_all_orders_ui(self):
        table_data = self.query_all_orders()
        
        CTkLabel(master=self.main_view, text="All Orders", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        table = CTkTable(master=table_frame, column=5, values=table_data, font=("Arial", 11), text_color="#000", header_color="#F6830D", colors=["#FFCD32", "#f8b907"])
        table.pack(expand=True)

     
    def login_handler(self):
        input_data = {
            "email": self.email.get(),
            "password": self.password.get(),
            "returnSecureToken": True
        }

        response = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBN17G50AD5JFk5eoDwNWDSDQQeQ4OYx8k", 
                                  json=input_data)

        response_data = response.json()

        if response.status_code == 200:
            self.token = response_data["idToken"]
            self.switch_main_view("CREATE_ORDER")
        else:
            error_message = response_data["error"]["message"]
            CTkMessagebox(icon="cancel", message=error_message)

    def build_login_ui(self):
       CTkLabel(master=self.main_view, text="Авторизация", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)
       
       CTkLabel(master=self.main_view, text="Почта", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)

       self.email = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0)
       self.email.pack(fill="x", pady=(12,0), padx=27, ipady=10)

       CTkLabel(master=self.main_view, text="Пароль", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)

       self.password = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0, show="*")
       self.password.pack(fill="x", pady=(12,0), padx=27, ipady=10)

       self.show_password_var = tkinter.BooleanVar()
       self.show_password_checkbox = CTkCheckBox(master=self.main_view, text="Показать пароль", variable=self.show_password_var, font=("Arial Bold", 12), text_color="#fff", command=self.toggle_password_visibility)
       self.show_password_checkbox.pack(anchor="nw", pady=(10,0), padx=27)

       self.time_label = CTkLabel(master=self.main_view, text="", font=("Arial Bold", 17), text_color="#fff")
       self.time_label.pack(anchor="nw", pady=(25,0), padx=27)

       self.update_time()
       
       CTkButton(master=self.main_view, text="Войти", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=self.login_handler).pack(fill="both", side="bottom", pady=(0, 50), ipady=10, padx=(27,27))

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.time_label.after(1000, self.update_time)
    
if __name__ == "__main__":
    app = App()
    app.mainloop()