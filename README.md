# BarberShop Manager

🎥 **System Demonstration:**
https://youtube.com/your-video-link

---

# BarberShop Manager

A modern desktop management system for barbershops developed in Python using CustomTkinter and SQLite.

## 🇧🇷 Made in Brazil
BarberShop Manager is a project developed in Brazil and designed primarily for Brazilian barbershops!!!!

The application provides complete management of customers, services, appointments, finances, reports, backups, and system settings.

---

## Features

### Authentication

* User login system
* Password protection
* Remember Me functionality
* Session persistence
* Login attempt control

### Dashboard

* Customer statistics
* Services statistics
* Barber statistics
* Appointments overview
* Today's appointments

### Customers

* Add customers
* Edit customers
* Delete customers
* Search customers

### Services

* Create services
* Edit services
* Remove services
* Price and duration management

### Appointments

* Create appointments
* Edit appointments
* Cancel appointments
* Complete appointments
* Receive payments

Appointment workflow:

* Scheduled
* Completed
* Paid
* Cancelled

### Financial Management

* Daily revenue
* Total revenue
* Paid appointments
* Financial history

### Reports

* Revenue reports
* Barber performance
* Customer statistics
* Service statistics

### Charts

* Monthly revenue
* Revenue by barber
* Top services

### Settings

* Shop name customization
* Theme selection
* Administrator password change
* Backup system
* Restore backups

### Export

* PDF reports
* Excel reports

---

## Technologies

* Python 3
* CustomTkinter
* SQLite
* Matplotlib
* CTkMessagebox
* OpenPyXL
* ReportLab
* PyInstaller

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/barbershop-manager.git
```

Enter the project folder:

```bash
cd barbershop-manager
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## Project Structure

```text
app/
│
├── controllers/
├── database/
├── utils/
├── views/
│
assets/
backups/
main.py
requirements.txt
```

---

## Backup System

The application includes automatic database backup and restore functionality.

The `backups/` folder is included in the repository to avoid errors during the first backup creation.

---

## Screenshots

You can add screenshots here.

---

## License

This project is licensed under the MIT License.

You are free to:

* Use
* Modify
* Distribute
* Sell
* Adapt
* Integrate into other projects

Attribution is appreciated but not required.

---

## Author

Developed by Maicon Duarte.

---

## Contributing

Contributions, improvements, and suggestions are welcome.

Feel free to fork the project and submit pull requests.

---

## Support

If you like this project, consider giving it a star on GitHub.
