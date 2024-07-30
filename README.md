# Heartheal Backend

This is the backend for the Heartheal application, which facilitates communication between patients and therapists. The backend is built using Flask and SQLAlchemy, and uses SQLite for the database.


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/heartheal_backend.git
    cd heartheal_backend
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    ```sh
    source venv/bin/activate
    ```

4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

5. Initialize the database:
    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```

2. The application will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Users

- **POST /users**
    - Create a new user.
    - Request Body: 
        ```json
        {
            "FirstName": "John",
            "LastName": "Doe",
            "Email": "john.doe@example.com",
            "Password": "password123"
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "FirstName": "John",
            "LastName": "Doe",
            "Email": "john.doe@example.com"
        }
        ```

### Patients

- **POST /patients**
    - Create a new patient.
    - Request Body: 
        ```json
        {
            "Age": 30,
            "Gender": "Male",
            "ContactNo": "1234567890",
            "Address": "123 Main St",
            "user_id": 1
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "Age": 30,
            "Gender": "Male",
            "ContactNo": "1234567890",
            "Address": "123 Main St",
            "user_id": 1
        }
        ```

### Therapists

- **POST /therapists**
    - Create a new therapist.
    - Request Body: 
        ```json
        {
            "LicenseNo": 12345,
            "specialization": "Psychology",
            "YearsOfExperience": 10,
            "bio": "Experienced therapist.",
            "user_id": 1
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "LicenseNo": 12345,
            "specialization": "Psychology",
            "YearsOfExperience": 10,
            "bio": "Experienced therapist.",
            "user_id": 1
        }
        ```

### App Requests

- **POST /app_requests**
    - Create a new appointment request.
    - Request Body: 
        ```json
        {
            "PatientsId": 1,
            "DateAndTime": 1627849200,
            "Status": "Pending",
            "patient_id": 1
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "PatientsId": 1,
            "DateAndTime": 1627849200,
            "Status": "Pending",
            "patient_id": 1
        }
        ```

### App Responses

- **POST /app_responses**
    - Create a new appointment response.
    - Request Body: 
        ```json
        {
            "TherapistsId": 1,
            "Date": 1627849200,
            "app_request_id": 1
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "TherapistsId": 1,
            "Date": 1627849200,
            "app_request_id": 1
        }
        ```

## Running Tests

1. Install `pytest`:
    ```sh
    pip install pytest
    ```

2. Run the tests:
    ```sh
    pytest
    ```

## License

This project is licensed under the MIT License.
