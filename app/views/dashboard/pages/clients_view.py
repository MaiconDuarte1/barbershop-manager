import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from app.database.clients_model import ClientsModel
from app.database.logs_model import LogsModel
from app.utils.path import ICON_PATH



class ClientsView(ctk.CTkFrame):

    def __init__(self, parent, user):
        super().__init__(parent)

        self.user = user

        self.configure(
            fg_color="transparent"
        )

        self.create_widgets()
        self.load_clients()



    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Clientes",
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
            placeholder_text="Pesquisar cliente..."
        )

        self.search_entry.bind(
        "<KeyRelease>",
        lambda e: self.search_client())

        self.search_entry.pack(
            side="left"
        )

        self.search_entry.bind("<KeyRelease>", lambda event: self.search_client())

        self.new_button = ctk.CTkButton(
            top_frame,
            text="+ Novo Cliente",
            width=150,
            command=self.add_client
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
            "nome",
            "telefone",
            "ultima_visita"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.tree.heading(
            "nome",
            text="Nome"
        )

        self.tree.heading(
            "telefone",
            text="Telefone"
        )

        self.tree.heading(
            "ultima_visita",
            text="Última Visita"
        )

        self.tree.column(
            "nome",
            width=300
        )

        self.tree.column(
            "telefone",
            width=180
        )

        self.tree.column(
            "ultima_visita",
            width=180
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

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
            command=self.edit_client,
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
        command=self.delete_client,
        state="disabled"
        )


        self.delete_button.pack(
            side="left",
            padx=10
        )

        self.tree.insert(
            "",
            "end",
            values=("João", "(11)99999-9999", "15/06/2026")
        )

        self.tree.insert(
            "",
            "end",
            values=("Pedro", "(11)98888-8888", "14/06/2026")
        )

    def load_clients(self):

        self.tree.delete(*self.tree.get_children())

        clients = ClientsModel.get_all()

        for client in clients:

            self.tree.insert(
                "",
                "end",
                iid=client["id"],
                values=(
                    client["name"],
                    client["phone"],
                    client["created_at"][:10]
                )
            )

    def search_client(self, event=None):

        text = self.search_entry.get().strip()

        self.tree.delete(*self.tree.get_children())

        if text:

            clients = ClientsModel.search(text)

        else:

            clients = ClientsModel.get_all()

        for client in clients:

            self.tree.insert(
                "",
                "end",
                iid=client["id"],
                values=(
                    client["name"],
                    client["phone"],
                    client["created_at"][:10]
                )
        )
            
            
    def add_client(self):

        window = ctk.CTkToplevel(self)

        window.title("Novo Cliente")

        window.geometry("450x350")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))

        window.grab_set()

        title = ctk.CTkLabel(
            window,
            text="Novo Cliente",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=20
        )

        name_entry = ctk.CTkEntry(
            window,
            width=300,
            placeholder_text="Nome"
        )

        name_entry.pack(
            pady=10
        )

        window.after(
            100,
            lambda: name_entry.focus()
        )

        phone_entry = ctk.CTkEntry(
            window,
            width=300,
            placeholder_text="Telefone"
        )

        phone_entry.pack(
            pady=10
        )

        observations = ctk.CTkEntry(
            window,
            width=300,
            height=70,
            placeholder_text="Observações"
        )

        observations.pack(
            pady=10
        )

        def save():

            name = name_entry.get().strip()

            phone = phone_entry.get().strip()

            observations_text = observations.get().strip()

            if not name:

                CTkMessagebox(
                    title="Atenção",
                    message="Informe o nome do cliente.",
                    icon="warning"
                )

                return

            ClientsModel.create(
                name,
                phone,
                observations_text
            )

            LogsModel.add(
                self.user[1],
                f"Criou o cliente {name}"
            )

            self.load_clients()

            window.grab_release()

            window.destroy()

            CTkMessagebox(
                title="Sucesso",
                message="Cliente cadastrado.",
                icon="check"
            )

        save_button = ctk.CTkButton(
            window,
            text="Salvar",
            command=save
        )

        save_button.pack(
            pady=20
        )



    def edit_client(self):

        selected = self.tree.selection()

        if not selected:

            CTkMessagebox(
                title="Atenção",
                message="Selecione um cliente.",
                icon="warning"
            )

            return

        client_id = int(selected[0])

        client = ClientsModel.get_by_id(client_id)

        window = ctk.CTkToplevel(self)

        window.title("Editar Cliente")

        window.geometry("450x320")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))

        window.grab_set()

        title = ctk.CTkLabel(
            window,
            text="Editar Cliente",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=20
        )

        name_entry = ctk.CTkEntry(
            window,
            width=300
        )

        name_entry.insert(
            0,
            client["name"]
        )

        name_entry.pack(
            pady=10
        )

        phone_entry = ctk.CTkEntry(
            window,
            width=300
        )

        phone_entry.insert(
            0,
            client["phone"] or ""
        )

        phone_entry.pack(
            pady=10
        )

        observations = ctk.CTkEntry(
            window,
            width=300
        )

        observations.insert(
            0,
            client["observations"] or ""
        )

        observations.pack(
            pady=10
        )

        def save():

            name = name_entry.get().strip()

            phone = phone_entry.get().strip()

            obs = observations.get().strip()

            if not name:

                CTkMessagebox(
                    title="Atenção",
                    message="Informe o nome do cliente.",
                    icon="warning"
                )

                return

            ClientsModel.update(
                client_id,
                name,
                phone,
                obs
            )

            LogsModel.add(
                self.user[1],
                f"Editou o cliente {name}"
            )

            self.load_clients()

            window.grab_release()

            window.destroy()

            CTkMessagebox(
                title="Sucesso",
                message="Cliente atualizado.",
                icon="check"
            )

        save_button = ctk.CTkButton(
            window,
            text="Salvar",
            command=save
        )

        save_button.pack(
            pady=20
        )


    def delete_client(self):

        selected = self.tree.selection()

        if not selected:
            return

        answer = CTkMessagebox(
            title="Excluir",
            message="Deseja excluir este cliente?",
            icon="question",
            option_1="Não",
            option_2="Sim"
        )

        if answer.get() == "Sim":

            client_id = int(selected[0])

            ClientsModel.delete(client_id)

            LogsModel.add(
                self.user[1],
                "Excluiu um cliente"
            )

            self.load_clients()

            self.edit_button.configure(
                state="disabled"
            )

            self.delete_button.configure(
                state="disabled"
            )

            CTkMessagebox(
                title="Sucesso",
                message="Cliente removido.",
                icon="check"
            )
    
    def on_select(self, event):

        selected = self.tree.selection()

        if selected:

            self.edit_button.configure(
                state="normal"
            )

            self.delete_button.configure(
                state="normal"
            )

        