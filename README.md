# Device Management Web Application

## 📌 Objective
A centralized web platform enabling administrators to manage organizational devices and allowing users to borrow, return, and monitor them efficiently.

## 🧩 Problem Statement
- Devices are dispersed across multiple locations.
- No tracking system for who borrowed which device and when.
- No visibility into missing, broken, or returned devices.
- Manual processes lead to delays and human error.

## 🎯 Project Goals
- Centralized tracking of all device-related activities.
- Real-time visibility and control over device status.
- User request management and approval workflows.
- Live notification system (in-app + email).
- User-friendly interface for browsing, borrowing, and reporting.
- Reporting and analytics for administrators.

---

## ✅ Functional Requirements

### 👥 User Roles

| Role  | Permissions |
|-------|-------------|
| **Admin** | Manage devices and users, approve/reject requests, update device statuses, view full usage statistics, send notifications and emails |
| **User**  | View and borrow devices, view personal history, return or report devices, update personal profile |

### 🔧 Core Features

- **Authentication**: Secure registration, login, and logout with role-based access.
- **Device Management**: Full CRUD operations with condition and availability tracking.
- **Borrowing Requests**: Users submit requests, admins approve or reject.
- **Borrowing History**: Accessible logs for users and global view for admins.
- **Real-Time Status Updates**: Instant device condition reporting and admin status updates.
- **Profile Management**: Edit personal information and preferences.
- **Notification Center**: Live updates for request statuses and system events.
- **Email Notifications**: Auto-email on approvals, rejections, and key actions.
- **Interactive Filtering and Sorting**: Devices and requests pages include filter menus, category tabs, and sorting selectors (e.g. by status, type, or date).
- **Charts & Analytics**: Visual usage data powered by Chart.js.
- **Live UI Updates**: Real-time updates using Django Channels and WebSockets.

---

## ⚙️ Technical Specifications

| Component       | Technology                    |
|----------------|--------------------------------|
| Frontend       | Django + HTMX                  |
| Backend        | Django                         |
| API            | Django REST Framework          |
| Database       | SQLite                         |
| Styling        | Tailwind CSS                   |
| Date Picker    | Flatpickr.js                   |
| Charts         | Chart.js                       |
| WebSockets     | Django Channels (ASGI)         |
| Notifications  | In-app + Email                 |
| Authentication | Django Auth (Role-based)       |
| Deployment     | _To be defined_                |

---

## 🎨 Design Specifications

### 🧭 Navigation
Top navigation bar includes:
- Dashboard access (admin)
- Devices and requests
- Profile page
- Notification bell
- Logout button

### 📄 Pages Overview

| Page                    | Access      | Description |
|-------------------------|-------------|-------------|
| Login/Register          | All         | Authentication forms with validations |
| Dashboard               | Admin       | Summary of system stats and charts |
| Device List             | All         | Browse and filter all available devices; includes sorting and tabs |
| Device Details          | All         | View detailed device info and status |
| Request Form            | User        | Submit borrowing request with date selector |
| Request Management      | Admin       | Approve/reject/manage requests; includes sorting and filtering |
| Personal Borrowing Logs | User        | Review personal borrowing history |
| Global Borrowing Logs   | Admin       | Full overview of borrow/return history |
| Notification Center     | All         | View real-time notifications |
| Profile Page            | All         | Edit personal user data |
| Add/Update Device       | Admin       | Add or modify device entries |

---

## 📦 Technologies Used

- **Django** (backend, templates, ORM)
- **Django REST Framework** (API)
- **Django Channels** (WebSocket support)
- **Tailwind CSS** (styling)
- **HTMX** (dynamic interactions without JavaScript)
- **Chart.js** (data visualization)
- **Flatpickr.js** (date selection UI)
- **SQLite** (development database)
- **SMTP or console backend** (for email handling)

---

## 📝 Prepared by
**Fouzai Mohamed Yassine**
