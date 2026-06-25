import customtkinter as ctk

from app.database.users_model import UsersModel
from app.database.clients_model import ClientsModel
from app.database.services_model import ServicesModel
from app.database.appointments_model import AppointmentsModel
from app.database.logs_model import LogsModel

from app.views.login.login_view import LoginView
from app.views.dashboard.dashboard_view import DashboardView

from app.utils.session_manager import load_session


UsersModel.create_table()
UsersModel.create_default_admin()

ClientsModel.create_table()
ServicesModel.create_table()
AppointmentsModel.create_table()
LogsModel.create_table()

ctk.set_appearance_mode("dark")

saved_user = load_session()

if saved_user:

    user = UsersModel.get_by_username(
        saved_user
    )

    if user:

        app = DashboardView(user)

    else:

        app = LoginView()

else:

    app = LoginView()

app.mainloop()