# 🚗 Cruisewave — Car Rental Service (Python + MySQL)

**Cruisewave** is a car rental service management system developed using **Python** and **MySQL**, designed as a Grade XII Computer Science project. It simulates real-world car rental applications with user login, car browsing, rental, and payment functionality — all via a clean CLI-based experience.

---

## 📌 Features

- 🔐 **User Authentication**: Sign up/login system with secure password storage  
- 🚘 **Car Listings**: Browse available cars with detailed specs and pricing  
- 📅 **Booking System**: Rent cars with start/end date, duration, and delivery time  
- 💳 **Payment Integration**: Supports card payment with optional saving for reuse  
- 📄 **Order History**: Track and view all previous rentals  
- 🏠 **Address Management**: Save delivery addresses for future orders  
- 🔄 **Session Options**: Rent car, view rentals, logout, or exit program  

---

## ⚙️ Tech Stack

- **Python 3.11.4** – Core language  
- **MySQL 8.0.35** – Relational database backend  
- **MySQL Connector** – Database connectivity (`mysql.connector`)  
- **VS Code** – Development environment  
- **Modules used**:  
  - `datetime` & `time` for handling dates/times  
  - `pwinput` for hidden password input  
  - `os` for terminal handling  

---

## 🧠 Design Overview

The system uses multiple MySQL tables:
- `userdata` for account details  
- `car` for vehicle inventory  
- `card` for payment methods  
- `data` for addresses  
- `previousordcar` for rental history  

The backend uses Python functions to execute SQL queries through a cursor object. It also includes validation, date parsing, and error handling to simulate a smooth and realistic flow.

---

## 🚀 Future Enhancements

- GUI integration using **Tkinter** or **PyQt**  
- Web-based interface with **Flask** or **Django**  
- OTP-based login and email validation  
- Admin dashboard for car/add/remove management  
- Payment gateway integration  

---

## 📚 Learnings & Outcome

This project strengthened my understanding of:
- Database interactions with Python  
- Real-life service architecture  
- Modular coding practices  
- Handling user input and data validation  

---

> 📢 **Note**: This project is intended for educational and personal portfolio purposes only. Redistribution or reuse of the code without permission is not allowed.
