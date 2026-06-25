import customtkinter as ctk
from app.database.logs_model import LogsModel
from tkinter import ttk

from app.database.clients_model import ClientsModel
from app.database.services_model import ServicesModel
from app.database.finance_model import FinanceModel
from app.database.users_model import UsersModel

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os
import pandas as pd

from CTkMessagebox import CTkMessagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from app.utils.path import ICON_PATH



class ReportsView(ctk.CTkFrame):

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
            text="Relatórios",
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
            "Clientes",
            str(ClientsModel.count())
        ).pack(
            side="left",
            padx=10
        )

        self.create_card(
            cards_frame,
            "Serviços",
            str(ServicesModel.count())
        ).pack(
            side="left",
            padx=10
        )

        self.create_card(
            cards_frame,
            "Barbeiros",
            str(UsersModel.barber_count())
        ).pack(
            side="left",
            padx=10
        )

        self.create_card(
            cards_frame,
            "Receita",
            f"R$ {FinanceModel.total_revenue():.2f}"
        ).pack(
            side="left",
            padx=10
        )

        buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        ctk.CTkButton(
            buttons_frame,
            text="Exportar Relatório",
            width=180,
            command=self.export_report
        ).pack(
            side="right"
        )

        graph_frame = ctk.CTkFrame(
            self,
            height=250,
            corner_radius=15
        )

        graph_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        graph_frame.pack_propagate(False)

        self.load_chart(graph_frame)


        charts_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        charts_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        services_frame = ctk.CTkFrame(
            charts_frame,
            corner_radius=15,
            height=250
        )

        services_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        services_frame.pack_propagate(False)

        barbers_frame = ctk.CTkFrame(
            charts_frame,
            corner_radius=15,
            height=250
        )

        barbers_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        barbers_frame.pack_propagate(False)

        self.load_services_chart(services_frame)

        self.load_barber_chart(barbers_frame)



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
            "barbeiro",
            "atendimentos",
            "receita"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        self.tree.heading(
            "barbeiro",
            text="Barbeiro"
        )

        self.tree.heading(
            "atendimentos",
            text="Atendimentos"
        )

        self.tree.heading(
            "receita",
            text="Receita"
        )

        self.tree.column(
            "barbeiro",
            width=250
        )

        self.tree.column(
            "atendimentos",
            width=150
        )

        self.tree.column(
            "receita",
            width=180
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.load_report()

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
    

    def load_report(self):

        self.tree.delete(
            *self.tree.get_children()
        )

        data = FinanceModel.barber_report()

        for item in data:

            self.tree.insert(
                "",
                "end",
                values=(
                    item["barber"],
                    item["appointments"],
                    f"R$ {item['total']:.2f}"
                )
            )

        

    def load_chart(self, parent):

        data = FinanceModel.monthly_revenue()

        months = []
        totals = []

        for item in data:
            months.append(item["month"])
            totals.append(item["total"])

        figure = Figure(
            figsize=(6, 2.5),
            dpi=100
        )

        ax = figure.add_subplot(111)

        ax.bar(
            months,
            totals
        )

        ax.set_title(
            "Faturamento por Mês"
        )

        ax.set_ylabel(
            "R$"
        )

        canvas = FigureCanvasTkAgg(
            figure,
            master=parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


    def load_services_chart(self, parent):

        data = FinanceModel.top_services()

        names = []
        totals = []

        for item in data:
            names.append(item["service"])
            totals.append(item["total"])

        figure = Figure(
            figsize=(4, 2.5),
            dpi=100
        )

        ax = figure.add_subplot(111)

        if sum(totals) == 0:

            ax.text(
                0.5,
                0.5,
                "Sem dados",
                ha="center",
                va="center",
                fontsize=14
            )

        else:

            ax.pie(
                totals,
                labels=names,
                autopct="%1.0f%%"
            )

        ax.set_title(
            "Serviços Mais Vendidos"
        )

        canvas = FigureCanvasTkAgg(
            figure,
            master=parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )



    def load_barber_chart(self, parent):

        data = FinanceModel.barber_revenue()

        names = []
        totals = []

        for item in data:
            names.append(item["barber"])
            totals.append(item["total"])

        figure = Figure(
            figsize=(4, 2.5),
            dpi=100
        )

        ax = figure.add_subplot(111)

        ax.barh(
            names,
            totals
        )

        ax.set_title(
            "Receita por Barbeiro"
        )

        ax.set_xlabel(
            "R$"
        )

        canvas = FigureCanvasTkAgg(
            figure,
            master=parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )



    def export_report(self):

        window = ctk.CTkToplevel(self)

        window.title("Exportar Relatório")

        window.geometry("300x180")

        window.after(200, lambda: window.iconbitmap(str(ICON_PATH)))

        

        ctk.CTkLabel(
            window,
            text="Formato",
            font=("Arial", 18)
        ).pack(
            pady=(20, 10)
        )

        format_menu = ctk.CTkOptionMenu(
            window,
            values=[
                "PDF",
                "Excel"
            ]
        )

        format_menu.pack(
            pady=10
        )

        def export():

            format_type = format_menu.get()

            if format_type == "PDF":
                self.export_pdf()

            else:
                self.export_excel()

            window.destroy()

        window.grab_set()

        ctk.CTkButton(
            window,
            text="Exportar",
            command=export
        ).pack(
            pady=20
        )


    
    def export_pdf(self):

        desktop = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        path = os.path.join(
            desktop,
            "relatorio_barbearia.pdf"
        )

        doc = SimpleDocTemplate(path)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "Relatório da Barbearia",
                styles["Title"]
            )
        )

        elements.append(
            Spacer(1, 20)
        )

        elements.append(
            Paragraph(
                f"Clientes: {ClientsModel.count()}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Serviços: {ServicesModel.count()}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Receita: R$ {FinanceModel.total_revenue():.2f}",
                styles["Normal"]
            )
        )

        elements.append(
            Spacer(1, 20)
        )

        data = FinanceModel.barber_report()

        for item in data:

            elements.append(
                Paragraph(
                    f"{item['barber']} - "
                    f"{item['appointments']} atendimentos - "
                    f"R$ {item['total']:.2f}",
                    styles["Normal"]
                )
            )

        doc.build(elements)

        CTkMessagebox(
            title="Sucesso",
            message="PDF exportado para a Área de Trabalho.",
            icon="check"
        )



    def export_excel(self):

        desktop = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        path = os.path.join(
            desktop,
            "relatorio_barbearia.xlsx"
        )

        data = FinanceModel.barber_report()

        rows = []

        for item in data:

            rows.append({
                "Barbeiro": item["barber"],
                "Atendimentos": item["appointments"],
                "Receita": item["total"]
            })

        df = pd.DataFrame(rows)

        df.to_excel(
            path,
            index=False
        )

        CTkMessagebox(
            title="Sucesso",
            message="Excel exportado para a Área de Trabalho.",
            icon="check"
        )