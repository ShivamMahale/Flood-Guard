# FloodGuard: Flood Prediction and Early Warning System

FloodGuard is a comprehensive flood prediction and early warning system built with Streamlit. This application allows users to sign up, log in, and access various pages including home, about, and contact. Users can submit contact information, which is stored in a MySQL database.

## Features

- User authentication (**Signup and Login**)
- **Home**, **About**, and **Contact** pages
- **Contact form** to collect user information
- Data storage using **MySQL**
- Modern UI using **Streamlit**

## Installation

### Prerequisites

- Python 3.7 or higher
- MySQL Server

### Install Python


If you don't have Python installed, you can download it from the official [Python website](https://www.python.org/downloads/). Follow the instructions for your operating system to install Python.

To check if Python is installed and to verify the version, run:

```sh
python --version
```
### Clone the Repository

```sh
git clone https://github.com/bachannayak/flood-guard.git
cd flood-guard
```
### Install Dependencies

```sh
pip install -r requirements.txt
```
## Configuration

### MySQL Database
Ensure you have a MySQL database set up with the necessary table. You can create a database and table using the following SQL commands:
```sh
CREATE DATABASE flood_guard;
USE flood_guard;
```
```sh
CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT
);
```
Update the MySQL connection details in contact_page.py:

```sh
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='your_host',
            user='your_username',
            password='your_password',
            database='flood_guard'
        )
        if connection.is_connected():
            st.success("Connected to the database!")
    except Error as e:
        st.error(f"The error '{e}' occurred")
    return connection
```

## Usage

### Running the Application

```sh
streamlit run app.py
```

### Project Structure

```sh
flood-guard/
├── contact_page.py
├── app.py
├── requirements.txt
└── README.md
```

- **contact_page.py:** Contains the contact page and database interaction logic.
- **app.py:** Main application file that handles user authentication and page navigation.
+ **requirements.txt:** List of required Python packages.
* **README.md:** Project documentation.

## Acknowledgements
- Streamlit
- MySQL
- Pandas
- NumPy
- Altair

## Contact
For any inquiries or feedback, please contact us at [shivam.mahale9@gmail.com].

## Application Pages

### Login Page

![image](https://github.com/bachannayak/flood-guard/assets/76477737/5b1ac25c-d5f1-4f1a-861c-ddea7be443f3) 

### Home Page 

![image](https://github.com/bachannayak/flood-guard/assets/76477737/ce6f2610-bf52-4765-983e-b0a47a636719) 

![image](https://github.com/bachannayak/flood-guard/assets/76477737/375435dd-d43b-4b7c-816b-e86988eca932)


### Contact Page

![image](https://github.com/bachannayak/flood-guard/assets/76477737/3d2d4882-41c6-4612-95ba-225937533954)


#### Development of remaining pages is in progress............

