import customtkinter as ctk

from tkinter import ttk

from CTkMessagebox import CTkMessagebox

from app.database.appointments_model import AppointmentsModel
from app.database.clients_model import ClientsModel
from app.database.services_model import ServicesModel
from app.database.users_model import UsersModel
from app.database.logs_model import LogsModel
from datetime import datetime
from app.utils.path import ICON_PATH


HORARIOS = [
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00"
]


class AppointmentsView(ctk.CTkFrame):

    def __init__(self, parent, user):
        super().__init__(parent)

        self.user = user

        self.configure(
            fg_color="transparent"
        )

        self.create_widgets()
        self.load_appointments()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Agendamentos",
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

        self.date_entry = ctk.CTkEntry(
            top_frame,
            width=120,
            placeholder_text="Data"
        )

        self.date_entry.pack(
            side="left",
            padx=(0, 10)
        )

        self.search_entry = ctk.CTkEntry(
            top_frame,
            width=250,
            placeholder_text="Pesquisar cliente..."
        )

        self.search_entry.pack(
            side="left"
        )

        self.new_button = ctk.CTkButton(
            top_frame,
            text="+ Novo Agendamento",
            width=180,
            command=self.add_appointment
        )

        self.new_button.pack(
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
        "hora",
        "cliente",
        "servico",
        "barbeiro",
        "data",
        "status"
    )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.tree.heading("hora", text="Hora")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("servico", text="Serviço")
        self.tree.heading("barbeiro", text="Barbeiro")
        self.tree.heading("data", text="Data")
        self.tree.heading("status", text="Status")

        self.tree.column("hora", width=100)
        self.tree.column("cliente", width=200)
        self.tree.column("servico", width=180)
        self.tree.column("barbeiro", width=180)
        self.tree.column("data", width=120)
        self.tree.column("status", width=120)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

        bottom_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        bottom_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        self.edit_button = ctk.CTkButton(
            bottom_frame,
            text="Editar",
            width=120,
            state="disabled",
            command=self.edit_appointment
        )

        self.edit_button.pack(
            side="left"
        )

        self.delete_button = ctk.CTkButton(
            bottom_frame,
            text="Excluir",
            width=120,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            state="disabled",
            command=self.delete_appointment
        )

        self.delete_button.pack(
            side="left",
            padx=10
        )

        self.finish_button = ctk.CTkButton(
            bottom_frame,
            text="Concluir",
            width=120,
            state="disabled",
            command=self.finish_appointment
        )

        self.finish_button.pack(
            side="left"
        )

        self.pay_button = ctk.CTkButton(
        bottom_frame,
        text="Receber",
        width=120,
        state="disabled",
        command=self.pay_appointment
    )

        self.pay_button.pack(
            side="left",
            padx=10
        )

        self.cancel_button = ctk.CTkButton(
        bottom_frame,
        text="Cancelar",
        width=120,
        fg_color="#DC2626",
        hover_color="#B91C1C",
        state="disabled",
        command=self.cancel_appointment
    )

        self.cancel_button.pack(
            side="left"
        )

    def on_select(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        status = self.tree.item(
            selected[0]
        )["values"][5]

        self.edit_button.configure(
            state="disabled"
        )

        self.delete_button.configure(
            state="disabled"
        )

        self.finish_button.configure(
            state="disabled"
        )

        self.pay_button.configure(
            state="disabled"
        )

        self.cancel_button.configure(
            state="disabled"
        )

        if status == "Agendado":

            self.edit_button.configure(
                state="normal"
            )

            self.delete_button.configure(
                state="normal"
            )

            self.finish_button.configure(
                state="normal"
            )

            self.cancel_button.configure(
                state="normal"
            )

        elif status == "Concluído":

            self.pay_button.configure(
                state="normal"
            )

            self.cancel_button.configure(
                state="normal"
            )


    def delete_appointment(self):

        selected = self.tree.selection()

        if not selected:
            return

        answer = CTkMessagebox(
            title="Excluir",
            message="Deseja excluir este agendamento?",
            icon="question",
            option_1="Não",
            option_2="Sim"
        )

        if answer.get() == "Sim":

            self.tree.delete(
                selected[0]
            )

    def finish_appointment(self):

        selected = self.tree.selection()

        if not selected:
            return

        values = list(
            self.tree.item(
                selected[0],
                "values"
            )
        )

        values[4] = "Concluído"

        self.tree.item(
            selected[0],
            values=values
        )

        LogsModel.add(
        self.user[1],
        "Concluiu um agendamento")

        CTkMessagebox(
            title="Sucesso",
            message="Agendamento concluído.",
            icon="check"
        )

    def finish_appointment(self):

        selected = self.tree.selection()

        if not selected:
            return

        appointment_id = int(selected[0])




        AppointmentsModel.update_status(
            appointment_id,
            "Concluído"
        )

        self.load_appointments()

        CTkMessagebox(
            title="Sucesso",
            message="Agendamento concluído.",
            icon="check"
        )


    def pay_appointment(self):

        selected = self.tree.selection()

        if not selected:
            return

        appointment_id = int(selected[0])

        AppointmentsModel.update_status(
            appointment_id,
            "Pago"
        )

        self.load_appointments()

        CTkMessagebox(
            title="Sucesso",
            message="Pagamento registrado.",
            icon="check"
        )


    def cancel_appointment(self):

        selected = self.tree.selection()

        if not selected:
            return

        appointment_id = int(selected[0])

        AppointmentsModel.update_status(
            appointment_id,
            "Cancelado"
        )

        self.load_appointments()

        CTkMessagebox(
            title="Sucesso",
            message="Agendamento cancelado.",
            icon="check"
        )

    
    def load_appointments(self):

        self.tree.delete(*self.tree.get_children())

        appointments = AppointmentsModel.get_all()

        for appointment in appointments:

            date = datetime.strptime(
                appointment["appointment_date"],
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

            self.tree.insert(
                "",
                "end",
                iid=appointment["id"],
                values=(
                    appointment["appointment_time"],
                    appointment["client"],
                    appointment["service"],
                    appointment["barber"],
                    date,
                    appointment["status"]
                )
            )

    def add_appointment(self):

        window = ctk.CTkToplevel(self)

        window.title("Novo Agendamento")

        window.geometry("500x600")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))

        

        ctk.CTkLabel(
            window,
            text="Novo Agendamento",
            font=("Arial", 24, "bold")
        ).pack(
            pady=20
        )

    # ---------------- CLIENTES ----------------

        clients = ClientsModel.get_names()

        if not clients:

            CTkMessagebox(
                title="Atenção",
                message="Cadastre clientes primeiro.",
                icon="warning"
            )

            window.destroy()

            return

        ctk.CTkLabel(
            window,
            text="Cliente"
        ).pack()

        client_dict = {
            c["name"]: c["id"]
            for c in clients
        }

        client_menu = ctk.CTkOptionMenu(
            window,
            values=list(client_dict.keys()),
            width=300
        )

        client_menu.pack(
            pady=(5, 15)
        )

    # ---------------- SERVIÇOS ----------------

        services = ServicesModel.get_names()

        if not services:

            CTkMessagebox(
                title="Atenção",
                message="Cadastre serviços primeiro.",
                icon="warning"
            )

            window.destroy()

            return

        ctk.CTkLabel(
            window,
            text="Serviço"
        ).pack()

        service_dict = {
            s["name"]: s["id"]
            for s in services
        }

        service_menu = ctk.CTkOptionMenu(
            window,
            values=list(service_dict.keys()),
            width=300
        )

        service_menu.pack(
            pady=(5, 15)
        )

    # ---------------- BARBEIROS ----------------

        barbers = UsersModel.get_barbers()

        if not barbers:

            CTkMessagebox(
                title="Atenção",
                message="Cadastre barbeiros primeiro.",
                icon="warning"
            )

            window.destroy()

            return
        
        window.grab_set()


        ctk.CTkLabel(
            window,
            text="Barbeiro"
        ).pack()

        barber_dict = {
            b["username"]: b["id"]
            for b in barbers
        }

        barber_menu = ctk.CTkOptionMenu(
            window,
            values=list(barber_dict.keys()),
            width=300
        )

        barber_menu.pack(
            pady=(5, 15)
        )

    # ---------------- DATA ----------------

        ctk.CTkLabel(
            window,
            text="Data (DD/MM/AAAA)"
        ).pack()

        date_entry = ctk.CTkEntry(
            window,
            width=300,
            placeholder_text="DD/MM/AAAA"
        )

        date_entry.pack(
            pady=(5, 15)
        )

    # ---------------- HORÁRIOS ----------------

        ctk.CTkLabel(
            window,
            text="Horário"
        ).pack()

        time_menu = ctk.CTkOptionMenu(
            window,
            values=HORARIOS,
            width=300
        )

        time_menu.pack(
            pady=(5, 20)
        )

    # ---------------- SALVAR ----------------

        def save():

            client_id = client_dict[
                client_menu.get()
            ]

            service_id = service_dict[
                service_menu.get()
            ]

            barber_id = barber_dict[
                barber_menu.get()
            ]


            date_input = date_entry.get().strip()

            try:

                date = datetime.strptime(
                    date_input,
                    "%d/%m/%Y"
                ).strftime("%Y-%m-%d")

            except ValueError:

                CTkMessagebox(
                    title="Data inválida",
                    message="Use DD/MM/AAAA.",
                    icon="warning"
                )

                return
            
            time = time_menu.get()


            if not date:

                CTkMessagebox(
                    title="Atenção",
                    message="Informe a data.",
                    icon="warning"
                )

                return

            if len(date) != 10:

                CTkMessagebox(
                    title="Data inválida",
                    message="Utilize DD/MM/AAAA.",
                    icon="warning"
                )

                return

            if AppointmentsModel.exists(
                barber_id,
                date,
                time
            ):

                CTkMessagebox(
                    title="Horário ocupado",
                    message="Este barbeiro já possui um agendamento nesse horário.",
                    icon="warning"
                )

                return

            AppointmentsModel.create(
                client_id,
                service_id,
                barber_id,
                date,
                time
            )

            LogsModel.add(
                self.user[1],
                "Criou um agendamento"
            )

            self.load_appointments()

            window.grab_release()

            window.withdraw()

            window.after(
                100,
                window.destroy
            )

            CTkMessagebox(
                title="Sucesso",
                message="Agendamento criado.",
                icon="check"
            )

        save_button = ctk.CTkButton(
            window,
            text="Salvar Agendamento",
            width=300,
            height=40,
            command=save
        )

        save_button.pack(
            pady=20
        )
            

    def delete_appointment(self):

        selected = self.tree.selection()

        if not selected:
            return

        appointment_id = int(selected[0])

        AppointmentsModel.delete(
            appointment_id
        )

        # LogsModel.add(...)

        self.load_appointments()

    def edit_appointment(self):

        selected = self.tree.selection()

        if not selected:

            CTkMessagebox(
                title="Atenção",
                message="Selecione um agendamento.",
                icon="warning"
            )

            return

        appointment_id = int(selected[0])

        appointment = AppointmentsModel.get_by_id(
            appointment_id
        )

        clients = ClientsModel.get_names()
        services = ServicesModel.get_names()
        barbers = UsersModel.get_barbers()

        client_dict = {
            c["name"]: c["id"]
            for c in clients
        }

        service_dict = {
            s["name"]: s["id"]
            for s in services
        }

        barber_dict = {
            b["username"]: b["id"]
            for b in barbers
        }

        reverse_clients = {
            c["id"]: c["name"]
            for c in clients
        }

        reverse_services = {
            s["id"]: s["name"]
            for s in services
        }

        reverse_barbers = {
            b["id"]: b["username"]
            for b in barbers
        }

        window = ctk.CTkToplevel(self)

        window.title("Editar Agendamento")

        window.geometry("450x550")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))

        window.grab_set()

        ctk.CTkLabel(
            window,
            text="Editar Agendamento",
            font=("Arial", 24, "bold")
        ).pack(
            pady=20
        )

        ctk.CTkLabel(
            window,
            text="Cliente"
        ).pack()

        client_menu = ctk.CTkOptionMenu(
            window,
            values=list(client_dict.keys())
        )

        client_menu.set(
            reverse_clients[
                appointment["client_id"]
            ]
        )

        client_menu.pack(
            pady=10
        )

        ctk.CTkLabel(
            window,
            text="Serviço"
        ).pack()

        service_menu = ctk.CTkOptionMenu(
            window,
            values=list(service_dict.keys())
        )

        service_menu.set(
            reverse_services[
                appointment["service_id"]
            ]
        )

        service_menu.pack(
            pady=10
        )

        ctk.CTkLabel(
            window,
            text="Barbeiro"
        ).pack()

        barber_menu = ctk.CTkOptionMenu(
            window,
            values=list(barber_dict.keys())
        )

        barber_menu.set(
            reverse_barbers[
                appointment["barber_id"]
            ]
        )

        barber_menu.pack(
            pady=10
        )

        ctk.CTkLabel(
            window,
            text="Data"
        ).pack()

        date_entry = ctk.CTkEntry(
            window,
            width=250
        )

        date_formatada = datetime.strptime(
            appointment["appointment_date"],
            "%Y-%m-%d"
        ).strftime("%d/%m/%Y")

        date_entry.insert(
            0,
            date_formatada
        )

        date_entry.pack(
            pady=10
        )

        ctk.CTkLabel(
            window,
            text="Horário"
        ).pack()

        time_menu = ctk.CTkOptionMenu(
            window,
            values=HORARIOS,
            width=300
        )

        time_menu.set(
            appointment["appointment_time"]
        )

        time_menu.pack(
            pady=10
        )

        ctk.CTkLabel(
            window,
            text="Status"
        ).pack()

        status_menu = ctk.CTkOptionMenu(
            window,
            values=[
            "Agendado",
            "Concluído",
            "Pago",
            "Cancelado"
        ]
        )

        status_menu.set(
            appointment["status"]
        )

        status_menu.pack(
            pady=10
        )

        def save():

            client_id = client_dict[
                client_menu.get()
            ]

            service_id = service_dict[
                service_menu.get()
            ]

            barber_id = barber_dict[
                barber_menu.get()
            ]

            date_input = date_entry.get().strip()

            try:

                date = datetime.strptime(
                    date_input,
                    "%d/%m/%Y"
                ).strftime("%Y-%m-%d")

            except ValueError:

                CTkMessagebox(
                    title="Data inválida",
                    message="Use DD/MM/AAAA.",
                    icon="warning"
                )

                return

            time = time_menu.get()

            status = status_menu.get()

            if not date or not time:

                CTkMessagebox(
                    title="Atenção",
                    message="Preencha todos os campos.",
                    icon="warning"
                )

                return
            

            if (
                barber_id != appointment["barber_id"]
                or date != appointment["appointment_date"]
                or time != appointment["appointment_time"]
            ):

                if AppointmentsModel.exists(
                    barber_id,
                    date,
                    time
                ):

                    CTkMessagebox(
                        title="Horário ocupado",
                        message="Este barbeiro já possui um agendamento nesse horário.",
                        icon="warning"
                    )

                    return
            

            AppointmentsModel.update(
                appointment_id,
                client_id,
                service_id,
                barber_id,
                date,
                time,
                status
            )

            LogsModel.add(
            self.user[1],
            f"Editou o agendamento {appointment_id}")

            self.load_appointments()

            window.grab_release()

            window.destroy()

            CTkMessagebox(
                title="Sucesso",
                message="Agendamento atualizado.",
                icon="check"
            )

        ctk.CTkButton(
        window,
        text="Salvar Alterações",
        width=300,
        height=40,
        command=save
    ).pack(
        pady=25
    )