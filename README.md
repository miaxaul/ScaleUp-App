# 🚀 ScaleSub-Flask: High-Availability Assignment Submission System

Welcome to **ScaleSub-Flask**, a modern, containerized web application designed for high-performance assignment management. This project was developed as a **Final Project** to demonstrate advanced concepts in **Horizontal Scaling**, **Object Storage Integration**, and **Microservices Orchestration**.

## 📖 Project Overview
In a real-world scenario, a submission system must handle hundreds of students uploading files simultaneously. **ScaleSub-Flask** solves this by decoupling the application layers. Instead of a single monolithic server, it uses a scalable web tier, a persistent relational database, and a dedicated object storage service.

## ✨ Core Features
**Dynamic Horizontal Scaling**: The web application layer can be scaled to $N$ instances using Docker Compose, allowing for load distribution across multiple containers.
**Distributed Object Storage**: Powered by **MinIO**, providing a high-performance, S3-compatible storage layer for binary data (assignment files).
**Relational Metadata Management**: Utilizes **PostgreSQL** to maintain strict data integrity for submission records, timestamps, and status tracking.
**Automated Schema Initialization**: Features a built-in `init_db` function that handles database connection retries and table creation automatically upon startup.
**Stateless Web Tier**: The Flask application is designed to be stateless, ensuring that any scaled instance can handle requests without data loss.

## 🛠️ System Architecture & Stack
* **Backend Framework**: [Flask](https://flask.palletsprojects.com/) (Python 3.9-slim base image) 
* **Database**: [PostgreSQL 15](https://www.postgresql.org/) 
* **Object Storage**: [MinIO](https://min.io/) 
* Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) 

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the following installed:
* Docker Desktop (or Docker Engine)
* Docker Compose V2

### 2. Environment Setup
The system uses environment variables for security. Create a `.env` file in the root directory:
```env
# Database Configuration
DB_USER=your_user
DB_PASSWORD=your_secure_password
DB_NAME=assignment_db

# MinIO Configuration
MINIO_USER=your_admin_user
MINIO_PASSWORD=your_admin_password
```

### Author: Brielliana
