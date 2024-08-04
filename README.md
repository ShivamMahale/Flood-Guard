# FloodGuard: Flood Prediction and Early Warning System

FloodGuard is your ultimate solution for staying ahead of potential flood risks and ensuring the safety of your community. 
With advanced prediction algorithms and real-time monitoring capabilities, FloodGuard provides accurate forecasts 
and timely alerts to help you prepare and respond effectively to flood events. <br>
This application allows users to sign up, log in, logout,and access various pages including home, about, predict and contact. Users can submit contact information, which is stored in a MySQL database.

## Features


- User authentication (**Signup and Login**)
- **Dashboard**, **Weather Lens**,**About**, **Predict** and **Contact** pages
- **Contact form** to collect user information
- **Logout**
- **Notification** sent flood alert notification
- Data storage using **MySQL**
- Modern UI using **Streamlit**

## Installation

### Prerequisites

- Python 3.7 or higher
- MySQL Server
- VS Code IDE
- [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). Follow to install

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
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ;


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
├── model/
     ├── LR_model.pkl
├── images/
     ├── cloud.jpg    
├── home_page.py
├── about_page.py
├── predict_page.py
├── app.py
├── db.py
├── contact_page.py
├── notification.py
├── forcast.py
├── requirements.txt
└── README.md
```

- **home_page.py:** It's a dashboard which contains IOT data visualization.
- **forcast.py:** It's a weather forcasting page which has really time data visualization.
- **contact_page.py:** Contains the contact page and database interaction logic.
- **app.py:** Main application file that handles user authentication and page navigation.
- **db.py:** It's database connection configuration and data access page
+ **requirements.txt:** List of required Python packages.
* **README.md:** Project documentation.

## Acknowledgements
- Streamlit
- MySQL
- Pandas
- NumPy
- Altair
- scikit-learn
- matplotlib
- seaborn
- secure-smtplib
- geopy
- openmeteo-requests
- requests-cache 
- retry-requests

## Contact
For any inquiries or feedback, please contact us at [shivam.mahale9@gmail.com].

## Application Pages

### Portal Entry
![image](https://github.com/user-attachments/assets/68b56f70-52fb-41a1-aea2-00c3ab40d9b5)


### Login Page

![image](https://github.com/user-attachments/assets/f5fa6d14-2349-47ed-a84f-fc3be0282cef)


### Sign-Up Page
![image](https://github.com/user-attachments/assets/44e99d36-d01e-4611-9a66-5bb1185d9721)


### Dashboard Page 

![image](https://github.com/user-attachments/assets/48d1e2c8-36b5-4c8e-9f25-d9ea6b554f43)

![image](https://github.com/user-attachments/assets/57048c57-7571-48f4-806b-4412a4a8f466)

![image](https://github.com/user-attachments/assets/d60124f9-11bd-4033-b58d-a712c1de86d0)

![image](https://github.com/user-attachments/assets/5caa5324-ea2a-446c-a053-78c7d2a343c6)

### Weather Lens Page

![image](https://github.com/user-attachments/assets/af82c271-684f-459e-9251-9deb9bd4639b)

![image](https://github.com/user-attachments/assets/635ff1b3-d6e9-4324-a14a-23d0d7b41acb)

![image](https://github.com/user-attachments/assets/93268d53-4610-4722-a620-40f248899532)

![image](https://github.com/user-attachments/assets/a2e08d06-ae70-463c-87ab-133f247488c5)


### About Page 

![image](https://github.com/user-attachments/assets/121bbacf-cc9b-4cbb-ac41-5a5e417c4580)

### Prediction Page

![image](https://github.com/user-attachments/assets/1e717c8d-b897-4da5-a9bb-2c37b49c3460)

![image](https://github.com/user-attachments/assets/ec27d771-a66c-42d2-8b2f-3beb7ba374b5)

### Contact Page

![image](https://github.com/user-attachments/assets/d8bb7ab4-78dc-4d89-846b-f8bd5ecaaaf8)


#### Thanks for visit the page....................

