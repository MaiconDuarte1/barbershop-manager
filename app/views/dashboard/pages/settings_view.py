import customtkinter as ctk
from app.database.logs_model import LogsModel
from CTkMessagebox import CTkMessagebox
from app.utils.settings_manager import (
    load_settings,
    save_settings
)

from app.database.users_model import UsersModel
import os
import shutil
from datetime import datetime
from app.database.database import DATABASE_PATH

class SettingsView(ctk.CTkFrame):

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
            text="Configurações",
            font=("Arial", 32, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(20, 20)
        )

        main_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            main_frame,
            text="Nome da Barbearia",
            font=("Arial", 16)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.shop_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            placeholder_text="Nome da Barbearia"
        )

        self.shop_entry.pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            main_frame,
            text="Nova Senha do Administrador",
            font=("Arial", 16)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.password_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            show="*",
            placeholder_text="Nova senha"
        )

        self.password_entry.pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            main_frame,
            text="Tema",
            font=("Arial", 16)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.theme_menu = ctk.CTkOptionMenu(
            main_frame,
            values=[
                "Dark",
                "Light",
                "System"
            ]
        )

        self.theme_menu.pack(
            anchor="w",
            padx=20
        )

        backup_button = ctk.CTkButton(
            main_frame,
            text="Criar Backup",
            width=180,
            command=self.create_backup
        )

        backup_button.pack(
            anchor="w",
            padx=20,
            pady=(30, 10)
        )

        restore_button = ctk.CTkButton(
        main_frame,
        text="Restaurar Backup",
        width=180,
        command=self.restore_backup
    )

        restore_button.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        save_button = ctk.CTkButton(
            main_frame,
            text="Salvar Configurações",
            width=200,
            command=self.save_settings
        )

        save_button.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        info_label = ctk.CTkLabel(
            main_frame,
            text="BarberShop Manager v1.0",
            text_color="gray"
        )

        info_label.pack(
            side="bottom",
            pady=20
        )


        settings = load_settings()

        self.shop_entry.insert(
            0,
            settings["shop_name"]
        )

        self.theme_menu.set(
            settings["theme"]
        )

    def save_settings(self):

        shop_name = self.shop_entry.get().strip()

        password = self.password_entry.get().strip()

        theme = self.theme_menu.get()

        save_settings({
            "shop_name": shop_name,
            "theme": theme
        })

        if theme == "Dark":
            ctk.set_appearance_mode("dark")

        elif theme == "Light":
            ctk.set_appearance_mode("light")

        else:
            ctk.set_appearance_mode("system")

        if password:

            UsersModel.change_password(
                self.user["id"],
                password
            )

        LogsModel.add(
            self.user["username"],
            "Alterou as configurações"
        )

        CTkMessagebox(
            title="Sucesso",
            message="Configurações salvas.",
            icon="check"
        )

    def create_backup(self):

        backup_name = datetime.now().strftime(
            "backup_%d%m%Y_%H%M.db"
        )

        shutil.copy(DATABASE_PATH, f"backups/{backup_name}")

        LogsModel.add(
            self.user["username"],
            "Criou um backup"
        )

        CTkMessagebox(
            title="Sucesso",
            message="Backup criado.",
            icon="check"
        )



    def restore_backup(self):

        backup_path = "backups"

        if not os.path.exists(backup_path):

            CTkMessagebox(
                title="Erro",
                message="Nenhum backup encontrado.",
                icon="cancel"
            )

            return

        files = sorted(
            os.listdir(backup_path)
        )

        if not files:

            CTkMessagebox(
                title="Erro",
                message="Nenhum backup encontrado.",
                icon="cancel"
            )

            return

        latest_backup = files[-1]

        shutil.copy(f"{backup_path}/{latest_backup}", DATABASE_PATH)

        LogsModel.add(
            self.user[1],
            "Restaurou backup"
        )

        CTkMessagebox(
            title="Sucesso",
            message="Backup restaurado.\nReinicie o sistema.",
            icon="check"
        )