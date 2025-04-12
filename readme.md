# Picklify - E-commerce Platform

Welcome to **Picklify**, an advanced e-commerce platform built using the Django framework. This project is designed to provide users with a seamless online shopping experience with features like user registration, email verification, load testing, and payment gateway integration.

---

## 🔥 Features

### ✅ User Authentication
- **Register**: Users can sign up with a valid email address and password.
- **Login**: Secure login functionality with session management.
- **Email Verification**: Users must verify their email to activate their account.
- **Password Reset**: Allows users to reset their password via email.

### 📦 Product Management
- **Product Catalog**: View a list of available products with detailed descriptions.
- **Search and Filter**: Users can search for products by name and filter by category.
- **Add to Cart**: Users can add products to their shopping cart.
- **Checkout**: Users can review their cart items before proceeding to payment.

### Invoice Generation
- **Smooth Checkouts**: xhtml2pdf module used for generation of pdfs.
- **Invoive Attachments**: Receive an invoice of the order placed on the provided email address for successful placement of orders.

### 🛠️ Load Testing
- **Performance Testing**: Conduct load tests to ensure the application performs well under high traffic.

---

## 🚀 Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django
- **Database**: SQLite

---

## 📚 Prerequisites

- Python 3.8+
- Django 4.0+
- Virtualenv

---

## ⚙️ Installation Guide

1. Clone the repository:
   ```bash
   git clone https://github.com/rahull0328/Picklify.git

2. Creating Virtual Environment:
   ```bash
   python venv env
   
3. Activating the virtual environment:
   ```bash
   cd env/scripts/activate

4. Starting the Development Server:
   ```bash
   cd picklify
   python manage.py runserver

---