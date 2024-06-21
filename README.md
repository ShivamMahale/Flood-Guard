# FloodGuard: Flood Prediction and Early Warning System

FloodGuard is your ultimate solution for staying ahead of potential flood risks and ensuring the safety of your community. 
With advanced prediction algorithms and real-time monitoring capabilities, FloodGuard provides accurate forecasts 
and timely alerts to help you prepare and respond effectively to flood events. <br>
This application allows users to sign up, log in, logout,and access various pages including home, about, predict and contact. Users can submit contact information, which is stored in a MySQL database.

## Features

- User authentication (**Signup and Login**)
- **Home**, **About**, **Predict** and **Contact** pages
- **Contact form** to collect user information
- **Logout** 
- Data storage using **MySQL**
- Modern UI using **Streamlit**

## Installation

### Prerequisites

- Python 3.7 or higher
- MySQL Server
- VS Code IDE

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

CREATE TABLE `users` (
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date_joined` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`email`)
);

CREATE TABLE `iot_data` (
  `id` double DEFAULT NULL,
  `MonsoonIntensity` int DEFAULT NULL,
  `TopographyDrainage` double DEFAULT NULL,
  `RiverManagement` int DEFAULT NULL,
  `Deforestation` int DEFAULT NULL,
  `Urbanization` double DEFAULT NULL,
  `ClimateChange` int DEFAULT NULL,
  `DamsQuality` int DEFAULT NULL,
  `Siltation` int DEFAULT NULL,
  `AgriculturalPractices` int DEFAULT NULL,
  `Encroachments` double DEFAULT NULL,
  `IneffectiveDisasterPreparedness` int DEFAULT NULL,
  `DrainageSystems` double DEFAULT NULL,
  `CoastalVulnerability` int DEFAULT NULL,
  `Landslides` double DEFAULT NULL,
  `Watersheds` int DEFAULT NULL,
  `DeterioratingInfrastructure` double DEFAULT NULL,
  `PopulationScore` double DEFAULT NULL,
  `WetlandLoss` int DEFAULT NULL,
  `InadequatePlanning` double DEFAULT NULL,
  `PoliticalFactors` int DEFAULT NULL,
  `FloodProbability` double DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
);


```
Update the MySQL connection details in db.py:

```sh
db_config = {
    'host': 'your_db_host_name',
    'user': 'your_db_user_name',
    'password': 'your_db_password',
    'database': 'flood_guard'
}
```
### Dataset Import in DB
import the **iot_data.csv** file present in path **/data/iot_data.csv** in db table created in above step named **iot_data** table.

## Usage

### Running the Application

```sh
streamlit run app.py
```

### Project Structure

```sh
flood-guard/
├── .streamlit/
     ├── config.toml  
├── data/
     ├── test.csv
     ├── train.csv
      
├── home_page.py
├── about_page.py
├── predict_page.py
├── app.py
├── db.py
├── contact_page.py
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

![image](https://github.com/bachannayak/flood-guard/assets/76477737/2a198f5c-a404-4b8c-856d-52b0c4e501ff)

### Sign-Up Page

![image](https://github.com/bachannayak/flood-guard/assets/76477737/f4f80544-cfdd-4497-a955-1b0a3c277bfe)

### Home Page 

![image](https://github.com/bachannayak/flood-guard/assets/76477737/9142ea73-fb87-4e1e-b1a0-5e91943d3807)


![image](https://github.com/bachannayak/flood-guard/assets/76477737/c3f9be52-25f0-4de6-8df6-27d29e3f7d80)

![image](https://github.com/bachannayak/flood-guard/assets/76477737/7ba9f11f-60cb-444d-8358-c3bca5310cd0)

### About Page 

![image](https://github.com/bachannayak/flood-guard/assets/76477737/c078cee1-6373-4b98-a20a-07dc1a525e2e)


### Contact Page

![image](https://github.com/bachannayak/flood-guard/assets/76477737/3d2d4882-41c6-4612-95ba-225937533954)


#### Development of remaining pages is in progress............

