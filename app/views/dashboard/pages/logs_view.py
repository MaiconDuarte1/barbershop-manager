import customtkinter as ctk
from tkinter import ttk

from app.database.logs_model import LogsModel


class LogsView(ctk.CTkFrame):

    def __init__(self, parent, user):
        super().__init__(parent)

        self.user = user

        self.configure(
            fg_color="transparent"
        )

        self.create_widgets()

        self.load_logs()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Logs do Sistema",
            font=("Arial", 32, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(20, 10)
        )

        top_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        self.search_entry = ctk.CTkEntry(
            top_frame,
            width=300,
            placeholder_text="Pesquisar logs..."
        )

        self.search_entry.pack(
            side="left"
        )

        self.today_button = ctk.CTkButton(
            top_frame,
            text="Hoje"
        )

        self.today_button.pack(
            side="right"
        )

        self.week_button = ctk.CTkButton(
            top_frame,
            text="7 dias"
        )

        self.week_button.pack(
            side="right",
            padx=10
        )

        self.month_button = ctk.CTkButton(
            top_frame,
            text="30 dias"
        )

        self.month_button.pack(
            side="right"
        )

        table_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        columns = (
            "data",
            "usuario",
            "acao"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "data",
            text="Data/Hora"
        )

        self.tree.heading(
            "usuario",
            text="Usuário"
        )

        self.tree.heading(
            "acao",
            text="Ação"
        )

        self.tree.column(
            "data",
            width=180
        )

        self.tree.column(
            "usuario",
            width=150
        )

        self.tree.column(
            "acao",
            width=500
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    def load_logs(self):

        self.tree.delete(*self.tree.get_children())

        logs = LogsModel.get_all()

        for log in logs:

            self.tree.insert(
                "",
                "end",
                values=(
                    log["created_at"],
                    log["username"],
                    log["action"]
                )
            )

    def search_logs(self):
        pass

    def filter_today(self):
        pass

    def filter_week(self):
        pass

    def filter_month(self):
        pass