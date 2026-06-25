import customtkinter as ctk
from tkinter import ttk
from app.database.users_model import UsersModel
from CTkMessagebox import CTkMessagebox
from app.database.logs_model import LogsModel
from app.utils.path import ICON_PATH    


class UsersView(ctk.CTkFrame):

    def __init__(self, parent, user):
        super().__init__(parent)

        self.user = user

        self.configure(
            fg_color="transparent"
        )

        self.create_widgets()
        self.load_users()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Usuários",
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
            placeholder_text="Pesquisar usuário..."
        )

        self.search_entry.pack(
            side="left"
        )

        self.new_button = ctk.CTkButton(
            top_frame,
            text="+ Novo Usuário",
            width=150,
            command=self.add_user
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
            "usuario",
            "cargo",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.tree.heading(
            "usuario",
            text="Usuário"
        )

        self.tree.heading(
            "cargo",
            text="Cargo"
        )

        self.tree.heading(
            "status",
            text="Status"
        )

        self.tree.column(
            "usuario",
            width=250
        )

        self.tree.column(
            "cargo",
            width=150
        )

        self.tree.column(
            "status",
            width=150
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
            values=(
                "admin",
                "Admin",
                "Ativo"
            )
        )

        self.tree.insert(
            "",
            "end",
            values=(
                "carlos",
                "Barbeiro",
                "Ativo"
            )
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
            command=self.edit_user
        )

        self.edit_button.pack(
            side="left"
        )

        self.status_button = ctk.CTkButton(
            bottom_frame,
            text="Ativar/Desativar",
            width=150,
            state="disabled",
            command=self.toggle_status
        )

        self.status_button.pack(
            side="left",
            padx=10
        )

        self.delete_button = ctk.CTkButton(
            bottom_frame,
            text="Excluir",
            width=120,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            state="disabled",
            command=self.delete_user
        )

        self.delete_button.pack(
            side="left"
        )

    def on_select(self, event):

        self.edit_button.configure(
            state="normal"
        )

        self.status_button.configure(
            state="normal"
        )

        self.delete_button.configure(
            state="normal"
        )

    def add_user(self):
        window = ctk.CTkToplevel(self)

        window.title("Novo Usuário")
        window.geometry("400x320")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))

        window.grab_set()

        username_entry = ctk.CTkEntry(
            window,
            width=280,
            placeholder_text="Usuário"
        )
        username_entry.pack(pady=15)

        password_entry = ctk.CTkEntry(
            window,
            width=280,
            show="*",
            placeholder_text="Senha"
        )
        password_entry.pack(pady=15)

        role_menu = ctk.CTkOptionMenu(
            window,
            values=[
                "barber",
                "admin"
            ]
        )
        role_menu.pack(pady=15)

        def save():

            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                return

            UsersModel.create(
                username,
                password,
                role_menu.get()
            )

            # LogsModel.add(...)

            self.load_users()

            window.destroy()

        ctk.CTkButton(
            window,
            text="Salvar",
            command=save
        ).pack(pady=20)


    def edit_user(self):

        selected = self.tree.selection()

        if not selected:
            return

        user_id = int(selected[0])

        user = UsersModel.get_by_id(user_id)

        window = ctk.CTkToplevel(self)

        window.title("Editar Usuário")
        window.geometry("400x350")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))

        window.grab_set()

        title = ctk.CTkLabel(
            window,
            text="Editar Usuário",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=20
        )

        username_entry = ctk.CTkEntry(
            window,
            width=280
        )

        username_entry.insert(
            0,
            user["username"]
        )

        username_entry.pack(
            pady=10
        )

        password_entry = ctk.CTkEntry(
            window,
            width=280,
            show="*"
        )

        password_entry.insert(
            0,
            user["password"]
        )

        password_entry.pack(
            pady=10
        )

        role_menu = ctk.CTkOptionMenu(
            window,
            values=[
                "admin",
                "barber"
            ]
        )

        role_menu.set(
            user["role"]
        )

        if user_id == 1:

            username_entry.configure(
                state="disabled"
            )

            role_menu.configure(
                state="disabled"
            )


        role_menu.pack(
            pady=10
        )

        def save():

            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = role_menu.get()

            UsersModel.update(
                user_id,
                username,
                password,
                role
            )

            self.load_users()

            window.destroy()

            CTkMessagebox(
                title="Sucesso",
                message="Usuário atualizado.",
                icon="check"
            )

        ctk.CTkButton(
            window,
            text="Salvar",
            width=250,
            command=save
        ).pack(
            pady=20
        )



    def toggle_status(self):
        selected = self.tree.selection()

        if not selected:
            return

        user_id = int(selected[0])

        if user_id == 1:
            return

        UsersModel.toggle_active(user_id)

        # LogsModel.add(...)

        self.load_users()

    def delete_user(self):

        selected = self.tree.selection()

        if not selected:
            return

        user_id = int(selected[0])

        if user_id == 1:

            CTkMessagebox(
                title="Atenção",
                message="O administrador principal não pode ser removido.",
                icon="warning"
            )

            return

        UsersModel.delete(user_id)

        # LogsModel.add(...)

        self.load_users()

    def load_users(self):

        self.tree.delete(*self.tree.get_children())

        users = UsersModel.get_all()

        for user in users:

            role = "Administrador"

            if user["role"] == "barber":
                role = "Barbeiro"

            status = "Ativo"

            if user["active"] == 0:
                status = "Inativo"

            self.tree.insert(
                "",
                "end",
                iid=user["id"],
                values=(
                    user["username"],
                    role,
                    status
                )
            )