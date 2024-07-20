# Fund Transfer Web App

A Django web application for managing and transferring funds between accounts.

The app supports importing accounts from various file formats, listing accounts, retrieving account details, and transferring funds.

It is Dockerized for easy deployment.


## Feature


- **Import Accounts**: Upload accounts from CSV, JSON for now and can be extended to XML, Excel and other formats.
- **List Accounts**: View all accounts with pagination.
- **Account Details**: Retrieve detailed information about a specific account.
- **Transfer Funds**: Transfer funds between accounts with validation.
- **Pagination**: Accounts are paginated for easier navigation.

## Important Features

### **Atomic Transactions**

To ensure that fund transfers and importing accounts from file are processed atomically, we use Django's `transaction.atomic`.


### **Generic File Import**

The app supports importing data from various file formats.

### **Unit Tests**

The app includes unit tests for models, views, and forms.

### **Dockerized**

The app is Dockerized for easy deployment and setup.


## Installation

### Prerequisites

- Python
- Docker (optional but recommended for easier setup)

### Setup Without Docker

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yaaa3ser/Account-Transfer-Task.git
   cd account-transfer-task
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

6. **Access the App**

   Open your browser and navigate to `http://127.0.0.1:8000/`.

### Setup With Docker

1. **Build and Run the Docker Container**

   ```bash
   docker-compose up --build
   ```

2. **Access the App**

   Open your browser and navigate to `http://localhost:8000/`.

## Configuration

- **Settings**: Update `settings.py` for environment-specific configurations (e.g., SECRET_KEY).
- **Static Files**: Ensure `base.css` and `base.js` are correctly included in the `static/` directory.

## File Formats

### CSV
- **Format**: `ID,Name,Balance`
- **Example**:
  ```csv
    ID,Name,Balance
  8a0d5d45-d5fc-4d4c-b9ab-8a68bca05f36,Yasser Issa,69.00
  ```

### JSON
- **Format**: List of dictionaries
- **Example**:
  ```json
  [
    {
      "ID": "8a0d5d45-d5fc-4d4c-b9ab-8a68bca05f36",
      "Name": "Yasser Issa",
      "Balance": 69.00
    }
  ]
  ```

## Acknowledgments

- Bootstrap for styling
- Django for the web framework
- Docker for containerization
