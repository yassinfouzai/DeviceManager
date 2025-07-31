# Device Management Web Application

## 📌 Objective
This project aims to develop a web-based platform where administrators can manage organizational devices, and regular users can borrow, return, and track them efficiently.

## 🧩 Problem Statement
- Devices are scattered across multiple locations.
- No system exists to track who borrowed what device and when.
- There's no record of missing, broken, or returned devices.
- Manual tracking is error-prone and time-consuming.

## 🎯 Project Goals
To address the above issues, this application will:
- Provide real-time visibility into device statuses.
- Automate tracking of borrow/return operations.
- Enable request verification and approval.
- Generate printable receipts for all transactions.
- Produce detailed reports on device usage and conditions.

---

## ✅ Functional Requirements

### 👥 User Roles

| Role  | Permissions |
|-------|-------------|
| **Admin** | Add/update/delete/view devices, manage users, approve/reject requests, print receipts, track device condition, view statistics |
| **User**  | Browse devices, print receipts, submit borrow requests, view personal history, return/report device issues |

### 🔧 Core Features

- **Authentication**: Registration, login, logout with role-based access.
- **Device Management**: Add/edit device information, status tracking.
- **Borrowing Requests**: Users submit requests; admins manage them.
- **Receipt Generation**: PDF receipts with transaction details.
- **Borrowing History**: Personal and global access to borrowing logs.
- **Status Tracking**: Real-time updates, problem reporting, admin updates.

---

## ⚙️ Technical Specifications

| Component       | Technology             |
|----------------|-------------------------|
| Frontend       | Django (Template Engine)|
| Backend        | Django                  |
| API            | Django REST Framework   |
| Database       | SQLite                  |
| Styling        | Tailwind CSS            |
| Deployment     | _To be determined_      |
| Authentication | Django (with Role-based Access Control) |

---

## 🎨 Design Specifications

### 🧭 Navigation
- Top bar for primary actions, including profile and logout access.

### 🎨 Color Scheme
- Toggle between light and dark mode for better accessibility.

### 📄 Pages Overview

| Page                    | Access      | Description |
|-------------------------|-------------|-------------|
| Login/Register          | All         | User authentication |
| Dashboard               | Admin       | Overview of activities |
| Device List             | All         | View all devices with filters |
| Device Details          | All         | View specific device info and history |
| Request Form            | User        | Submit borrowing requests |
| Request Management      | Admin       | Approve/reject requests |
| Personal Borrowing Logs | User        | View personal borrowing history |
| Global Borrowing Logs   | Admin       | View all borrowing logs |
| Receipt Page            | All         | View/print receipts |
| Add/Update Device       | Admin       | Manage device information |

---

## 📝 Prepared by
**Fouzai Mohamed Yassine**

---


