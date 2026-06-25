import customtkinter as ctk
from tkinter import ttk
from app.database.logs_model import LogsModel
from app.database.appointments_model import AppointmentsModel

class FinanceView(ctk.CTkFrame):

    def __init__(self, parent, user):
        super().__init__(parent)

        self.user = user

        self.configure(
            fg_color="transparent"
        )

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Financeiro",
            font=("Arial", 32, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(20, 20)
        )

        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        self.create_card(
            cards_frame,
            "Total Recebido",
            f"R$ {AppointmentsModel.total_paid():.2f}"
        ).pack(
            side="left",
            padx=10
        )

        self.create_card(
            cards_frame,
            "Pagamentos",
            str(AppointmentsModel.paid_count())
        ).pack(
            side="left",
            padx=10
        )

        self.create_card(
            cards_frame,
            "Concluídos",
            str(AppointmentsModel.finished_count())
        ).pack(
            side="left",
            padx=10
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
            "cliente",
            "valor"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "data",
            text="Data"
        )

        self.tree.heading(
            "cliente",
            text="Cliente"
        )

        self.tree.heading(
            "valor",
            text="Valor"
        )

        self.tree.column(
            "data",
            width=150
        )

        self.tree.column(
            "cliente",
            width=300
        )

        self.tree.column(
            "valor",
            width=150
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.load_data()

    def create_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            width=180,
            height=100,
            corner_radius=15
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16)
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 24, "bold")
        ).pack()

        return card

    def load_data(self):


        for item in self.tree.get_children():
            self.tree.delete(item)

        data = AppointmentsModel.get_paid()

        for appointment in data:

            self.tree.insert(
                "",
                "end",
                values=(
                    appointment["appointment_date"],
                    appointment["name"],
                    f"R$ {appointment['price']:.2f}"
                )
            )