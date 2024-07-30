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
            "username": "Umutoni20",
            "first_name": "Ange",
            "last_name": "Umutoni",
            "email": "umutange1@example.com",
            "password": "password123",
            "role": "user"
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "username": "Umutoni20"
            "first_name": "Ange",
            "last_name": "Umutoni",
            "email": "umutange1@example.com"
            "role": "user"
        }
        ```

### Patients

- **POST /patients**
    - Create a new patient.
    - Request Body: 
        ```json
        {
            "user_id": 1.
            "age": 30,
            "gender": "Male",
            "contact_no": "1234567890",
            "address": "123 Main St"
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "age": 30,
            "gender": "Male",
            "contact_no": "1234567890",
            "address": "123 Main St",
            "user_id": 1
        }
        ```

### Therapists

- **POST /therapists**
    - Create a new therapist.
    - Request Body: 
        ```json
        {
            "license_no": 12345,
            "specialization": "Psychology",
            "years_of_experience": 10,
            "bio": "Experienced therapist.",
            "user_id": 1
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "license_no": 12345,
            "specialization": "Psychology",
            "years_of_experience": 10,
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
            "id": 1,
            "patient_id": 1,
            "date_and_time": 1627849200,
            "status": "Pending" 
        }
        ```
    - Response: 
        ```json
        {
            "id": 1,
            "patient_id": 1,
            "date-and_time": 1627849200,
            "status": "Pending",
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
