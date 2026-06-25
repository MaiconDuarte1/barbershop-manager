import customtkinter as ctk

from CTkMessagebox import CTkMessagebox

from app.controllers.auth_controller import AuthController
from app.views.dashboard.dashboard_view import DashboardView
from app.utils.path import ICON_PATH
from app.database.users_model import UsersModel

from app.utils.settings_manager import get_app_name

from app.utils.session_manager import (
    save_session,
    load_session,
    clear_session
)

from app.utils.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT
)

from app.utils.theme import (
    BACKGROUND,
    CARD,
    TEXT_SECONDARY,
    ENTRY_BORDER,
    BUTTON,
    BUTTON_HOVER
)


class LoginView(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.auth_controller = AuthController()


        self.login_attempts = 0
        self.max_attempts = 5

        self.title(get_app_name())

        self.iconbitmap(str(ICON_PATH))

        self.center_window()

        self.resizable(False, False)

        ctk.set_appearance_mode("dark")

        self.configure(
            fg_color=BACKGROUND
        )

        self.bind("<Return>", lambda event: self.login())

        self.create_widgets()


    def center_window(self):

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"
        )

    def create_widgets(self):

        self.card = ctk.CTkFrame(
            self,
            width=500,
            height=600,
            fg_color=CARD,
            corner_radius=20
        )

        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.card.pack_propagate(False)

        title = ctk.CTkLabel(
            self.card,
            text=f"{get_app_name()}",
            font=("Arial", 34, "bold")
        )

        title.pack(
            pady=(50, 5)
        )

        subtitle = ctk.CTkLabel(
            self.card,
            text="Management System",
            text_color=TEXT_SECONDARY,
            font=("Arial", 16)
        )

        subtitle.pack(
            pady=(0, 40)
        )

        login_label = ctk.CTkLabel(
            self.card,
            text="LOGIN",
            font=("Arial", 24, "bold")
        )

        login_label.pack(
            pady=(0, 25)
        )

        self.username_entry = ctk.CTkEntry(
            self.card,
            width=350,
            height=45,
            placeholder_text="Username",
            border_color=ENTRY_BORDER
        )

        self.username_entry.pack(
            pady=10
        )

        password_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )

        password_frame.pack(
            pady=10
        )

        self.password_visible = False

        self.password_entry = ctk.CTkEntry(
            password_frame,
            width=300,
            height=45,
            placeholder_text="Password",
            show="*",
            border_color=ENTRY_BORDER
        )

        self.password_entry.pack(
            side="left"
        )

        self.show_password_button = ctk.CTkButton(
            password_frame,
            text="👁",
            width=45,
            height=45,
            command=self.toggle_password
        )

        self.show_password_button.pack(
            side="left",
            padx=(5, 0)
        )

        options_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )

        options_frame.pack(
            fill="x",
            padx=70,
            pady=(15, 30)
        )

        self.remember_var = ctk.BooleanVar()

        self.remember_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="Remember me",
            variable=self.remember_var
        )

        self.remember_checkbox.pack(
            side="left"
        )

        forgot_label = ctk.CTkLabel(
            options_frame,
            text="Forgot password?",
            text_color=TEXT_SECONDARY
        )

        forgot_label.pack(
            side="right"
        )

        self.login_button = ctk.CTkButton(
            self.card,
            text="LOGIN",
            width=350,
            height=45,
            fg_color=BUTTON,
            hover_color=BUTTON_HOVER,
            command=self.login
        )

        self.login_button.pack()

    def toggle_password(self):

        if self.password_visible:

            self.password_entry.configure(show="*")

            self.password_visible = False

        else:

            self.password_entry.configure(show="")

            self.password_visible = True

    def login(self):

        if self.login_attempts >= self.max_attempts:

            CTkMessagebox(
                title="Bloqueado",
                message="Muitas tentativas inválidas.",
                icon="warning"
            )

            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username:

            CTkMessagebox(
                title="Atenção",
                message="Informe o usuário.",
                icon="warning"
            )

            return

        if not password:

            CTkMessagebox(
                title="Atenção",
                message="Informe a senha.",
                icon="warning"
            )

            return

        if len(username) > 30:

            CTkMessagebox(
                title="Atenção",
                message="Usuário muito longo.",
                icon="warning"
            )

            return

        if len(password) > 50:

            CTkMessagebox(
                title="Atenção",
                message="Senha muito longa.",
                icon="warning"
            )

            return

        if len(password) < 4:

            CTkMessagebox(
                title="Atenção",
                message="A senha deve possuir pelo menos 4 caracteres.",
                icon="warning"
            )

            return

        user = UsersModel.authenticate(
        username,
        password
        )

        if user:

            if self.remember_var.get():
                save_session(username)
            else:
                clear_session()

            self.withdraw()

            dashboard = DashboardView(user)

            dashboard.mainloop()

            self.destroy()

        else:

            CTkMessagebox(
                title="Erro",
                message="Usuário ou senha inválidos.",
                icon="cancel"
            )
