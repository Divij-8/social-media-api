# 🚀 Scalable Social Media Backend API

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

A high-performance, stateless REST API built with **FastAPI** and **PostgreSQL**. Designed for scalability using containerization and modern backend practices.

**[🔴 Live Demo (Swagger UI)](https://social-media-api.onrender.com/docs)** *(Note: Hosted on free tier, may take 50s to wake up)*

---

## ⚡ Key Features

* **🔐 Secure Authentication:** OAuth2 implementation with JWT (JSON Web Tokens) and bcrypt password hashing.
* **🏗️ Robust CRUD Operations:** Complete management for Users, Posts, and Votes.
* **👍 Voting System:** Reddit-style voting logic ensuring one vote per user per post.
* **👥 Follow System:** User-to-user following and relationship tracking.
* **🐳 Containerized:** Fully dockerized application for consistent deployment across environments.
* **🛡️ Data Validation:** Strict schema enforcement using Pydantic models.
* **🧪 Automated Testing:** Comprehensive test suite using `pytest` for unit and integration testing.

---

## 🛠️ Tech Stack

| Category | Technology | Usage |
| :--- | :--- | :--- |
| **Framework** | FastAPI | High-performance async web framework |
| **Database** | PostgreSQL | Primary relational database |
| **ORM** | SQLModel / SQLAlchemy | Database interaction and ORM |
| **Validation** | Pydantic | Data validation and settings management |
| **Authentication** | JWT + OAuth2 | Secure token-based authentication |
| **Security** | bcrypt | Password hashing and verification |
| **DevOps** | Docker & Docker Compose | Containerization and orchestration |
| **Testing** | Pytest | Test automation |

---

## 🚀 Getting Started (Run Locally)

### Option 1: Using Docker (Recommended)
The easiest way to run the app. Ensure you have Docker Desktop installed.

```bash
# 1. Clone the repository
git clone https://github.com/Divij-8/social-media-api.git
cd social-media-api

# 2. Create a .env file with your PostgreSQL credentials
# Example:
# POSTGRES_USER=socialmedia_user
# POSTGRES_PASSWORD=your_secure_password
# POSTGRES_DB=socialmedia
# DATABASE_URL=postgresql://socialmedia_user:your_secure_password@db:5432/socialmedia

# 3. Build and Run
docker compose up --build
```

The API will be available at `http://localhost:8000`.

### Option 2: Manual Setup

If you prefer running without Docker:

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup Environment Variables
# Create a .env file with your PostgreSQL credentials

# 4. Run the Server
uvicorn app.main:app --reload
```

---

## 📚 API Documentation

FastAPI provides automatic interactive documentation.
Once the server is running, navigate to:

* **Swagger UI:** [`http://localhost:8000/docs`](http://localhost:8000/docs) - Interactive testing.
* **ReDoc:** [`http://localhost:8000/redoc`](http://localhost:8000/redoc) - Clean documentation reference.

### Main Endpoints

- **Auth:** `/auth/*` - User registration and login
- **Users:** `/users/*` - User profile management
- **Posts:** `/posts/*` - Create, read, update, delete posts
- **Votes:** `/votes/*` - Vote on posts
- **Follow:** `/follow/*` - Follow/unfollow users

---

## 🧪 Running Tests

This project uses `pytest` for testing. A separate test database is spun up to ensure data isolation.

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_posts.py -v
```

---

## 📂 Project Structure

```
social-media-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database setup and connection
│   ├── models.py               # SQLModel database models
│   ├── oauth2.py               # OAuth2 token handling
│   ├── security.py             # Password hashing & verification
│   └── routers/
│       ├── auth.py             # Authentication endpoints
│       ├── users.py            # User management endpoints
│       ├── posts.py            # Post management endpoints
│       ├── vote.py             # Voting endpoints
│       └── follow.py           # Follow system endpoints
├── tests/
│   ├── conftest.py             # Pytest fixtures and configuration
│   ├── test_users.py           # User endpoint tests
│   ├── test_posts.py           # Post endpoint tests
│   └── test_follow.py          # Follow system endpoint tests
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 📈 Next Steps: Enterprise-Grade Backend

This project served as a foundation for learning FastAPI and Python backend development. For enterprise-grade backend systems with advanced features like distributed transactions, reactive streams, and complex microservices architecture, I am transitioning to **Java with Spring Boot** to explore:

- Spring Cloud for microservices
- Advanced ORM with Hibernate/JPA
- Reactive programming with Project Reactor
- Enterprise-level security and performance optimization
- Distributed systems and scalability patterns

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Divij Mazumdar** — Aspiring Backend Engineer & AI Student

[GitHub](https://github.com/Divij-8) | [LinkedIn](https://linkedin.com/in/divij-mazumdar)

---

<div align="center">

**Made with ❤️ using FastAPI and PostgreSQL**

⭐ If you found this helpful, consider giving it a star!

</div>
