import customtkinter as ctk
from tkinter import ttk
from app.database.services_model import ServicesModel
from CTkMessagebox import CTkMessagebox
from app.database.logs_model import LogsModel
from app.utils.path import ICON_PATH




class ServicesView(ctk.CTkFrame):

    def __init__(self, parent, user):
        super().__init__(parent)

        self.user = user

        self.configure(
            fg_color="transparent"
        )

        self.create_widgets()
        self.load_services()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Serviços",
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
            height=40,
            placeholder_text="Pesquisar serviço..."
        )

        self.search_entry.bind("<KeyRelease>", lambda e: self.search_service())

        self.search_entry.pack(
            side="left"
        )

        self.new_button = ctk.CTkButton(
            top_frame,
            text="+ Novo Serviço",
            width=150,
            command=self.add_service
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
            "servico",
            "valor",
            "duracao"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.tree.heading(
            "servico",
            text="Serviço"
        )

        self.tree.heading(
            "valor",
            text="Valor"
        )

        self.tree.heading(
            "duracao",
            text="Duração"
        )

        self.tree.column(
            "servico",
            width=300
        )

        self.tree.column(
            "valor",
            width=120
        )

        self.tree.column(
            "duracao",
            width=120
        )

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

        self.tree.insert(
            "",
            "end",
            values=("Corte", "R$ 35,00", "30 min")
        )

        self.tree.insert(
            "",
            "end",
            values=("Barba", "R$ 25,00", "20 min")
        )

        self.tree.insert(
            "",
            "end",
            values=("Combo", "R$ 50,00", "50 min")
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
            command=self.edit_service,
            state="disabled"
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
            command=self.delete_service,
            state="disabled"
        )

        self.delete_button.pack(
            side="left",
            padx=10
        )

    def on_select(self, event):

        self.edit_button.configure(
            state="normal"
        )

        self.delete_button.configure(
            state="normal"
        )

    def add_service(self):

        window = ctk.CTkToplevel(self)

        window.title("Novo Serviço")
        window.geometry("450x350")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))


        window.grab_set()

        ctk.CTkLabel(
            window,
            text="Novo Serviço",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        name_entry = ctk.CTkEntry(
            window,
            width=300,
            placeholder_text="Nome"
        )
        name_entry.pack(pady=10)

        price_entry = ctk.CTkEntry(
            window,
            width=300,
            placeholder_text="Preço"
        )
        price_entry.pack(pady=10)

        duration_entry = ctk.CTkEntry(
            window,
            width=300,
            placeholder_text="Duração (min)"
        )
        duration_entry.pack(pady=10)

        description_entry = ctk.CTkEntry(
            window,
            width=300,
            placeholder_text="Descrição"
        )
        description_entry.pack(pady=10)

        def save():

            name = name_entry.get().strip()

            if not name:

                CTkMessagebox(
                    title="Atenção",
                    message="Informe o nome do serviço.",
                    icon="warning"
                )

                return

            price = float(price_entry.get() or 0)
            duration = int(duration_entry.get() or 0)
            description = description_entry.get().strip()

            ServicesModel.create(
                name,
                price,
                duration,
                description
            )

            # LogsModel.add(...)

            self.load_services()

            window.grab_release()
            window.destroy()

            CTkMessagebox(
                title="Sucesso",
                message="Serviço cadastrado.",
                icon="check"
            )

        ctk.CTkButton(
            window,
            text="Salvar",
            command=save
        ).pack(pady=20)

    def edit_service(self):

        selected = self.tree.selection()

        if not selected:
            return

        service_id = int(selected[0])

        service = ServicesModel.get_by_id(service_id)

        window = ctk.CTkToplevel(self)

        window.title("Editar Serviço")
        window.geometry("450x350")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))

        window.grab_set()

        name_entry = ctk.CTkEntry(window, width=300)
        name_entry.insert(0, service["name"])
        name_entry.pack(pady=10)

        price_entry = ctk.CTkEntry(window, width=300)
        price_entry.insert(0, str(service["price"]))
        price_entry.pack(pady=10)

        duration_entry = ctk.CTkEntry(window, width=300)
        duration_entry.insert(0, str(service["duration"]))
        duration_entry.pack(pady=10)

        description_entry = ctk.CTkEntry(window, width=300)
        description_entry.insert(
            0,
            service["description"] or ""
        )
        description_entry.pack(pady=10)

        def save():

            ServicesModel.update(
                service_id,
                name_entry.get(),
                float(price_entry.get()),
                int(duration_entry.get()),
                description_entry.get()
            )

            # LogsModel.add(...)

            self.load_services()

            window.destroy()

        ctk.CTkButton(
            window,
            text="Salvar",
            command=save
        ).pack(pady=20)



    def delete_service(self):

        selected = self.tree.selection()

        if not selected:
            return

        answer = CTkMessagebox(
            title="Excluir",
            message="Deseja excluir este serviço?",
            icon="question",
            option_1="Não",
            option_2="Sim"
        )

        if answer.get() == "Sim":

            service_id = int(selected[0])

            ServicesModel.delete(service_id)

            # LogsModel.add(...)

            self.load_services()

    def load_services(self):

        self.tree.delete(*self.tree.get_children())

        services = ServicesModel.get_all()

        for service in services:

            self.tree.insert(
                "",
                "end",
                iid=service["id"],
                values=(
                    service["name"],
                    f"R$ {service['price']:.2f}",
                    f"{service['duration']} min"
                )
            )


    def search_service(self):

        text = self.search_entry.get()

        self.tree.delete(*self.tree.get_children())

        services = ServicesModel.search(text)

        for service in services:

            self.tree.insert(
                "",
                "end",
                iid=service["id"],
                values=(
                    service["name"],
                    f"R$ {service['price']:.2f}",
                    f"{service['duration']} min"
                )
            )