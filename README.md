# NeuralFin-Backend

NeuralFin-Backend is the back-end component of the NeuralFin project, responsible for handling data processing, storage, and analysis of financial reports for MENA companies.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction
NeuralFin-Backend provides the core functionalities for downloading, preprocessing, and analyzing financial data. It integrates with a PostgreSQL database and employs advanced NLP techniques for financial analysis.

## Features
- Download and preprocess financial reports.
- Manage and query a PostgreSQL database.
- Implement NLP techniques for financial data analysis.
- Provide APIs for front-end integration.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/ranystephan/NeuralFin-Backend.git
    ```
2. Navigate to the project directory:
    ```bash
    cd NeuralFin-Backend
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Set up the PostgreSQL database and apply migrations:
    ```bash
    python manage.py migrate
    ```
2. Start the server:
    ```bash
    python manage.py runserver
    ```
3. Access the API at:
    ```text
    http://localhost:8000
    ```

## Project Structure
- `neuralfin/`: Main application code.
- `database/`: Database management scripts.
- `api/`: API endpoints for data access and manipulation.
- `utils/`: Utility scripts and functions.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License
This project is licensed under the MIT License.