import customtkinter as ctk

from app.views.dashboard.pages.dashboard_page import DashboardPage
from app.views.dashboard.pages.clients_view import ClientsView
from app.views.dashboard.pages.services_view import ServicesView
from app.views.dashboard.pages.appointments_view import AppointmentsView
from app.views.dashboard.pages.users_view import UsersView
from app.views.dashboard.pages.logs_view import LogsView
from app.views.dashboard.pages.finance_view import FinanceView
from app.views.dashboard.pages.reports_view import ReportsView
from app.views.dashboard.pages.settings_view import SettingsView
from app.utils.session_manager import clear_session
from app.utils.path import ICON_PATH
from app.utils.settings_manager import get_app_name


from app.utils.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT
)

from app.utils.theme import (
    BACKGROUND,
    SIDEBAR,
    TOPBAR,
    CONTENT,
    BUTTON,
    BUTTON_HOVER,
    DANGER,
    DANGER_HOVER
)



class DashboardView(ctk.CTk):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.title(get_app_name())

        self.iconbitmap(str(ICON_PATH))

        self.center_window()

        self.resizable(False, False)

        self.configure(
            fg_color=BACKGROUND
        )

        self.create_layout()

        self.after(100, lambda: self.show_page(DashboardPage))

    def center_window(self):

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"
        )

    def create_layout(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=CONTENT,
            corner_radius=0
        )

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()

        self.create_topbar()

        self.create_content()

    def create_sidebar(self):

        logo = ctk.CTkLabel(
            self.sidebar,
            text=f"{get_app_name()}",
            font=("Arial", 28, "bold")
        )

        logo.pack(
            pady=(30, 40)
        )

        self.create_menu_button("🏠 Dashboard", lambda: self.show_page(DashboardPage))
        self.create_menu_button("📅 Agendamentos", lambda: self.show_page(AppointmentsView))
        self.create_menu_button("👥 Clientes",  lambda: self.show_page(ClientsView))
        self.create_menu_button("✂️ Serviços", lambda: self.show_page(ServicesView))

        if self.user[3] == "admin":

            self.create_menu_button("💰 Financeiro", lambda: self.show_page(FinanceView))
            self.create_menu_button("📊 Relatórios", lambda: self.show_page(ReportsView))
            self.create_menu_button("👤 Usuários", lambda: self.show_page(UsersView))
            self.create_menu_button("📜 Logs", lambda: self.show_page(LogsView) )
            self.create_menu_button("⚙️ Configurações", lambda: self.show_page(SettingsView))

        logout_button = ctk.CTkButton(
            self.sidebar,
            text="🚪 Sair",
            fg_color=DANGER,
            hover_color=DANGER_HOVER,
            command=self.logout
        )

        logout_button.pack(
            side="bottom",
            pady=30,
            padx=15,
            fill="x"
        )

    def create_menu_button(self, text, command):

        button = ctk.CTkButton(
        self.sidebar,
        text=text,
        height=45,
        anchor="w",
        fg_color=BUTTON,
        hover_color=BUTTON_HOVER,
        command=command
    )

        button.pack(
            fill="x",
            padx=15,
            pady=5
        )

    def create_topbar(self):

        self.topbar = ctk.CTkFrame(
            self.main_frame,
            height=70,
            fg_color=TOPBAR,
            corner_radius=0
        )

        self.topbar.pack(
            fill="x"
        )

        self.topbar.pack_propagate(False)

        user_label = ctk.CTkLabel(
            self.topbar,
            text=f"{self.user[1]} ({self.user[3]})",
            font=("Arial", 16)
        )

        user_label.pack(
            side="right",
            padx=20
        )

    def create_content(self):

        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=CONTENT
        )

        self.content_frame.pack(
            fill="both",
            expand=True
        )

        title = ctk.CTkLabel(
            self.content_frame,
            text="Dashboard",
            font=("Arial", 34, "bold")
        )

        title.pack(
            pady=50
        )

    def logout(self):

        clear_session()

        self.destroy()

        from app.views.login.login_view import LoginView

        login = LoginView()

        login.mainloop()


    def show_page(self, page_class):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        page = page_class(
            self.content_frame,
            self.user
        )

        page.pack(
            fill="both",
            expand=True
        )