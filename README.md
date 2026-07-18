# Farm Management REST API

Backend application for managing farm data through RESTful API services.
Developed as part of the **PT AIGRA EON INDONESIA** Fullstack Developer (Backend Focus) Coding Test.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Folder Structure](#folder-structure)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
  - [Base URL](#base-url)
  - [Response Format](#response-format)
  - [Endpoints](#endpoints)
  - [Status Codes](#status-codes)
- [Database Schema](#database-schema)
- [Request and Response Examples](#request-and-response-examples)
- [License](#license)

---

## Overview

Farm Management REST API adalah backend service yang menyediakan operasi CRUD (Create, Read, Update, Delete) untuk mengelola data farm/pertanian. API ini dibangun dengan arsitektur berlapis yang memisahkan routing, business logic, dan data access layer secara jelas. Setiap response menggunakan format envelope yang konsisten untuk memudahkan konsumsi dari sisi client.

Fitur utama:

- CRUD lengkap untuk entitas Farm
- Validasi request otomatis melalui Pydantic schema
- Penanganan error terpusat dengan format response yang konsisten
- Auto-generated API documentation (Swagger UI dan ReDoc)
- Dukungan PostgreSQL sebagai database utama dan SQLite sebagai alternatif lokal

---

## Architecture

Projek ini menggunakan arsitektur **layered/service-based** yang terdiri dari empat lapisan utama:

```
Request
  |
  v
[Routes]  -->  Menerima HTTP request, validasi parameter, delegasi ke service
  |
  v
[Services]  -->  Business logic, error handling, interaksi dengan model
  |
  v
[Models]  -->  ORM mapping ke tabel database (SQLAlchemy)
  |
  v
[Database]  -->  PostgreSQL / SQLite
```

Pemisahan ini memastikan setiap lapisan hanya bertanggung jawab terhadap satu concern, sehingga kode lebih mudah di-maintain, di-test, dan di-extend.

---

## Folder Structure

```
AIGRA-FULLSTACK/
|
|-- app/                          # Package utama aplikasi
|   |-- __init__.py               # Inisialisasi package app
|   |-- main.py                   # Entry point, konfigurasi FastAPI, registrasi routes
|   |
|   |-- core/                     # Konfigurasi inti aplikasi
|   |   |-- __init__.py
|   |   |-- database.py           # Engine, session factory, dan dependency get_db
|   |   |-- exceptions.py         # Global exception handlers (422, 4xx, 500)
|   |
|   |-- models/                   # SQLAlchemy ORM models
|   |   |-- __init__.py
|   |   |-- farm.py               # Model Farm (mapping ke tabel 'farms')
|   |
|   |-- schemas/                  # Pydantic schemas untuk validasi dan serialisasi
|   |   |-- __init__.py
|   |   |-- farm.py               # FarmCreate, FarmUpdate, FarmResponse, ApiResponse
|   |
|   |-- routes/                   # Definisi endpoint API
|   |   |-- __init__.py
|   |   |-- farm_routes.py        # CRUD endpoints untuk /farms
|   |
|   |-- services/                 # Business logic layer
|   |   |-- __init__.py
|   |   |-- farm_service.py       # Fungsi CRUD yang berinteraksi dengan database
|   |
|   |-- utils/                    # Utility functions
|       |-- __init__.py
|       |-- response.py           # Helper success_response dan error_response
|
|-- .env                          # Environment variables (tidak di-commit)
|-- .env.example                  # Template environment variables
|-- .gitignore                    # File dan folder yang dikecualikan dari Git
|-- requirements.txt              # Daftar dependency Python
|-- farm.db                       # SQLite database file (development)
|-- README.md                     # Dokumentasi projek
```

Penjelasan tiap direktori:

| Direktori      | Tanggung Jawab                                                                 |
|----------------|--------------------------------------------------------------------------------|
| `app/core`     | Konfigurasi database dan penanganan exception secara global                    |
| `app/models`   | Definisi tabel database menggunakan SQLAlchemy ORM                             |
| `app/schemas`  | Validasi input request dan serialisasi output response menggunakan Pydantic    |
| `app/routes`   | Definisi endpoint HTTP, menerima request dan mendelegasikan ke service         |
| `app/services` | Business logic murni, semua operasi database dilakukan di sini                 |
| `app/utils`    | Fungsi helper yang digunakan lintas modul                                      |

---

## Technology Stack

| Teknologi         | Versi    | Fungsi                                   | Alasan Pemilihan                                                                                                 |
|-------------------|----------|------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Python            | 3.10+    | Bahasa pemrograman utama                 | Sintaks yang bersih, ekosistem library yang luas, dan standar industri untuk backend development                  |
| FastAPI           | 0.115.12 | Web framework                            | Performa tinggi berbasis ASGI, auto-generated documentation, native async support, dan type-safe dengan Pydantic |
| Uvicorn           | 0.34.3   | ASGI server                              | Server ASGI yang ringan dan cepat, standar deployment untuk aplikasi FastAPI                                      |
| SQLAlchemy        | 2.0.41   | ORM (Object-Relational Mapping)          | ORM paling mature di Python, mendukung berbagai database, query builder yang fleksibel                           |
| Pydantic          | 2.11.4   | Data validation dan serialisasi          | Terintegrasi native dengan FastAPI, validasi otomatis berdasarkan type hints, performa tinggi                    |
| psycopg2-binary   | 2.9.10   | PostgreSQL driver                        | Driver PostgreSQL paling stabil dan widely-used untuk Python, versi binary untuk kemudahan instalasi             |
| python-dotenv     | 1.1.0    | Environment variable management          | Memisahkan konfigurasi dari kode, standar 12-factor app methodology                                              |
| PostgreSQL        | -        | Database utama (production)              | RDBMS open-source yang reliable, mendukung ACID compliance, skalabilitas baik untuk data terstruktur             |
| SQLite            | -        | Database alternatif (development)        | Zero-configuration, file-based database yang cocok untuk development dan testing lokal                           |

---

## Prerequisites

Pastikan tools berikut sudah terinstall di sistem:

- **Python** 3.10 atau lebih baru
- **pip** (Python package manager)
- **PostgreSQL** (untuk production) atau gunakan SQLite (untuk development lokal)
- **Git** (untuk clone repository)

---

## Installation

1. Clone repository:

```bash
git clone <repository-url>
cd AIGRA-FULLSTACK
```

2. Buat dan aktifkan virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependency:

```bash
pip install -r requirements.txt
```

---

## Configuration

1. Salin file `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

2. Edit file `.env` dan sesuaikan `DATABASE_URL` dengan konfigurasi database:

```env
# PostgreSQL (production / staging)
DATABASE_URL=postgresql://postgres:password@localhost:5432/farm_db

# SQLite (development lokal)
DATABASE_URL=sqlite:///./farm.db
```

3. Jika menggunakan PostgreSQL, pastikan database sudah dibuat terlebih dahulu:

```sql
CREATE DATABASE farm_db;
```

Tabel akan dibuat secara otomatis saat aplikasi pertama kali dijalankan.

---

## Running the Application

Jalankan server development dengan perintah berikut:

```bash
uvicorn app.main:app --reload
```

Server akan berjalan di `http://127.0.0.1:8000`.

Opsi tambahan:

```bash
# Menjalankan di port tertentu
uvicorn app.main:app --reload --port 8080

# Menjalankan agar dapat diakses dari network lain
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Setelah server berjalan, dokumentasi API dapat diakses melalui:

| URL                              | Keterangan                      |
|----------------------------------|---------------------------------|
| `http://127.0.0.1:8000/docs`    | Swagger UI (interactive)        |
| `http://127.0.0.1:8000/redoc`   | ReDoc (read-only documentation) |

---

## API Documentation

### Base URL

```
http://127.0.0.1:8000
```

### Response Format

Semua endpoint mengembalikan response dengan format envelope yang konsisten:

```json
{
  "success": true,
  "message": "Deskripsi hasil operasi",
  "data": {}
}
```

| Field     | Tipe    | Keterangan                                                       |
|-----------|---------|------------------------------------------------------------------|
| `success` | boolean | `true` jika operasi berhasil, `false` jika terjadi error        |
| `message` | string  | Pesan deskriptif tentang hasil operasi                           |
| `data`    | any     | Payload data (object, array, atau `null` jika tidak ada data)    |

---

### Endpoints

#### Root

| Method | Endpoint | Deskripsi                     |
|--------|----------|-------------------------------|
| GET    | `/`      | Health check, cek status API  |

#### Farms

| Method | Endpoint        | Deskripsi                         |
|--------|-----------------|-----------------------------------|
| GET    | `/farms`        | Mengambil seluruh data farm       |
| GET    | `/farms/{id}`   | Mengambil data farm berdasarkan ID|
| POST   | `/farms`        | Membuat data farm baru            |
| PUT    | `/farms/{id}`   | Mengupdate data farm berdasarkan ID (partial update) |
| DELETE | `/farms/{id}`   | Menghapus data farm berdasarkan ID|

---

### Status Codes

Berikut adalah daftar lengkap HTTP status code yang digunakan oleh API ini beserta penjelasan kapan masing-masing dikembalikan:

| Status Code | Status Text                | Konteks Penggunaan                                                                                   |
|-------------|----------------------------|------------------------------------------------------------------------------------------------------|
| `200`       | OK                         | Request berhasil diproses. Digunakan pada GET (retrieve), PUT (update), dan DELETE (delete) yang sukses |
| `201`       | Created                    | Resource baru berhasil dibuat. Dikembalikan saat POST `/farms` berhasil membuat farm baru              |
| `404`       | Not Found                  | Resource tidak ditemukan. Dikembalikan saat GET, PUT, atau DELETE mereferensikan `farm_id` yang tidak ada di database |
| `422`       | Unprocessable Entity       | Validasi request body gagal. Dikembalikan saat field yang dikirim tidak memenuhi aturan validasi Pydantic (misal: `name` kosong, `size` bernilai negatif, tipe data salah) |
| `500`       | Internal Server Error      | Error tak terduga di sisi server. Dikembalikan saat terjadi exception yang tidak ter-handle secara spesifik |

#### Detail Response per Status Code

**200 -- OK**

```json
{
  "success": true,
  "message": "Farms retrieved successfully",
  "data": [ ... ]
}
```

**201 -- Created**

```json
{
  "success": true,
  "message": "Farm created successfully",
  "data": {
    "id": 1,
    "name": "Green Valley Farm",
    "location": "Central Java, Indonesia",
    "size": 25.5,
    "crop_type": "Rice",
    "created_at": "2026-07-18T03:00:00Z",
    "updated_at": "2026-07-18T03:00:00Z"
  }
}
```

**404 -- Not Found**

```json
{
  "success": false,
  "message": "Farm not found",
  "data": null
}
```

**422 -- Unprocessable Entity**

```json
{
  "success": false,
  "message": "Validation error",
  "data": [
    "body -> name: String should have at least 1 character",
    "body -> size: Input should be greater than 0"
  ]
}
```

**500 -- Internal Server Error**

```json
{
  "success": false,
  "message": "Internal server error",
  "data": null
}
```

---

## Database Schema

### Tabel: `farms`

| Kolom        | Tipe           | Constraint                     | Keterangan                              |
|--------------|----------------|--------------------------------|-----------------------------------------|
| `id`         | Integer        | PRIMARY KEY, AUTO INCREMENT    | Identifier unik untuk setiap farm       |
| `name`       | String(255)    | NOT NULL                       | Nama farm                               |
| `location`   | String(255)    | NOT NULL                       | Lokasi geografis farm                   |
| `size`       | Float          | NOT NULL                       | Ukuran farm dalam satuan hektar         |
| `crop_type`  | String(255)    | NULLABLE                       | Jenis tanaman yang dibudidayakan        |
| `created_at` | DateTime (TZ)  | NOT NULL, DEFAULT now()        | Timestamp pembuatan record              |
| `updated_at` | DateTime (TZ)  | NOT NULL, DEFAULT now(), ON UPDATE now() | Timestamp terakhir record diperbarui |

---

## Request and Response Examples

### POST /farms -- Membuat Farm Baru

**Request Body:**

```json
{
  "name": "Green Valley Farm",
  "location": "Central Java, Indonesia",
  "size": 25.5,
  "crop_type": "Rice"
}
```

**Response (201):**

```json
{
  "success": true,
  "message": "Farm created successfully",
  "data": {
    "id": 1,
    "name": "Green Valley Farm",
    "location": "Central Java, Indonesia",
    "size": 25.5,
    "crop_type": "Rice",
    "created_at": "2026-07-18T03:00:00Z",
    "updated_at": "2026-07-18T03:00:00Z"
  }
}
```

### GET /farms -- Mengambil Seluruh Farm

**Response (200):**

```json
{
  "success": true,
  "message": "Farms retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Green Valley Farm",
      "location": "Central Java, Indonesia",
      "size": 25.5,
      "crop_type": "Rice",
      "created_at": "2026-07-18T03:00:00Z",
      "updated_at": "2026-07-18T03:00:00Z"
    }
  ]
}
```

### GET /farms/{id} -- Mengambil Farm Berdasarkan ID

**Response (200):**

```json
{
  "success": true,
  "message": "Farm retrieved successfully",
  "data": {
    "id": 1,
    "name": "Green Valley Farm",
    "location": "Central Java, Indonesia",
    "size": 25.5,
    "crop_type": "Rice",
    "created_at": "2026-07-18T03:00:00Z",
    "updated_at": "2026-07-18T03:00:00Z"
  }
}
```

### PUT /farms/{id} -- Mengupdate Farm

Hanya field yang disertakan dalam request body yang akan diperbarui (partial update).

**Request Body:**

```json
{
  "size": 30.0,
  "crop_type": "Corn"
}
```

**Response (200):**

```json
{
  "success": true,
  "message": "Farm updated successfully",
  "data": {
    "id": 1,
    "name": "Green Valley Farm",
    "location": "Central Java, Indonesia",
    "size": 30.0,
    "crop_type": "Corn",
    "created_at": "2026-07-18T03:00:00Z",
    "updated_at": "2026-07-18T04:00:00Z"
  }
}
```

### DELETE /farms/{id} -- Menghapus Farm

**Response (200):**

```json
{
  "success": true,
  "message": "Farm deleted successfully",
  "data": {
    "id": 1,
    "name": "Green Valley Farm",
    "location": "Central Java, Indonesia",
    "size": 30.0,
    "crop_type": "Corn",
    "created_at": "2026-07-18T03:00:00Z",
    "updated_at": "2026-07-18T04:00:00Z"
  }
}
```

---

## Validation Rules

Berikut aturan validasi yang diterapkan pada request body:

### FarmCreate (POST)

| Field       | Tipe            | Wajib | Aturan                                       |
|-------------|-----------------|-------|----------------------------------------------|
| `name`      | string          | Ya    | Minimal 1 karakter, maksimal 255 karakter    |
| `location`  | string          | Ya    | Minimal 1 karakter, maksimal 255 karakter    |
| `size`      | float           | Ya    | Harus lebih besar dari 0                     |
| `crop_type` | string atau null| Tidak | Maksimal 255 karakter, default `null`        |

### FarmUpdate (PUT)

| Field       | Tipe            | Wajib | Aturan                                       |
|-------------|-----------------|-------|----------------------------------------------|
| `name`      | string atau null| Tidak | Minimal 1 karakter, maksimal 255 karakter    |
| `location`  | string atau null| Tidak | Minimal 1 karakter, maksimal 255 karakter    |
| `size`      | float atau null | Tidak | Harus lebih besar dari 0                     |
| `crop_type` | string atau null| Tidak | Maksimal 255 karakter                        |

Semua field pada FarmUpdate bersifat opsional. Hanya field yang dikirimkan yang akan diperbarui.

---

## License

This project is developed as part of the PT AIGRA EON INDONESIA Fullstack Developer Coding Test.
