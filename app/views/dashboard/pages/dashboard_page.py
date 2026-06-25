import customtkinter as ctk

from app.database.clients_model import ClientsModel
from app.database.services_model import ServicesModel
from app.database.users_model import UsersModel
from app.database.appointments_model import AppointmentsModel
from datetime import datetime



class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, user):
        super().__init__(parent)

        self.user = user

        self.configure(
            fg_color="transparent"
        )

        self.create_widgets()

    def create_widgets(self):

        welcome = ctk.CTkLabel(
            self,
            text=f"Bem-vindo, {self.user[1]}",
            font=("Arial", 18)
        )

        welcome.pack(
            anchor="w",
            padx=30,
            pady=(20, 0)
        )

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 34, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(0, 25)
        )

        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=20
        )

        self.create_card(
            cards_frame,
            "Clientes",
            str(ClientsModel.count())
        )

        self.create_card(
            cards_frame,
            "Serviços",
            str(ServicesModel.count())
        )

        self.create_card(
            cards_frame,
            "Usuários",
            str(UsersModel.count())
        )

        self.create_card(
            cards_frame,
            "Agendamentos",
            str(AppointmentsModel.count())
        )

        appointments_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        appointments_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        appointments_title = ctk.CTkLabel(
            appointments_frame,
            text="Agendamentos Recentes",
            font=("Arial", 22, "bold")
        )

        appointments_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        appointments = AppointmentsModel.today()

        if not appointments:

            ctk.CTkLabel(
                appointments_frame,
                text="Nenhum agendamento hoje.",
                font=("Arial", 16)
            ).pack(
                pady=30
            )

        else:

            for appointment in appointments:

                status = appointment["status"]

                if status == "Agendado":
                    emoji = "🟡"

                elif status == "Concluído":
                    emoji = "🟢"

                elif status == "Pago":
                    emoji = "💰"

                else:
                    emoji = "🔴"

                text = (
                    f"{appointment['appointment_time']} • "
                    f"{appointment['client']} • "
                    f"{appointment['barber']} • "
                    f"{emoji} {status}"
                )

                ctk.CTkLabel(
                    appointments_frame,
                    text=text,
                    font=("Arial", 15)
                ).pack(
                    anchor="w",
                    padx=20,
                    pady=5
                )

    def create_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            width=180,
            height=120,
            corner_radius=15
        )

        card.pack(
            side="left",
            padx=10
        )

        card.pack_propagate(False)

        card_title = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 18)
        )

        card_title.pack(
            pady=(25, 5)
        )

        card_value = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 32, "bold")
        )

        card_value.pack()