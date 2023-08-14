# Planetarium Api project
![favicon.ico](favicon.ico)

## Description

API-project for managing planetarium show sessions, making reservations

## Table of content

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)

## Features

All users:

    - Registration (only as client of planetarium, not admin)
    - Authorisation
    - Review and updating current authorisated user's profile info
    - Review all show sessions

General users:

    - Rewiew of all their owns reservations
    - Creating new reservations

Admins:

    - Managing planetarium info (about themes, shows, sessions, etc.)
    - Rewiew of all reservations

## Installation
Python3 must be already installed
1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/OlhaTryhub/planetarium-api.git
    ```
2. Change into the project directory:
    ```bash
   cd your-repo
    ```
3. Create and activate a virtual environment (optional but recommended):
   ```bash
    python -m venv venv
    venv\Scripts\activate  # On Mac, use: source venv/bin/activate
   ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt 
    ```
5. Apply database migrations:
    ```bash
    python manage.py migrate
    ```

## Usage
1. For using app as admin you must create your own superuser with command:
    ```bash
    python manage.py createsuperuser
    ```
2. Start your local Django REST server:
    ```bash
    python manage.py runserver
    ```
3. Open your web browser and navigate to http://127.0.0.1:8000/ to access the application.

_To see all available endpoints navigate to one of next endpoint:_ 
    - http://127.0.0.1:8000/api/doc/swagger/ 
![img_14.png](readme_images/img_14.png)
    - http://127.0.0.1:8000/api/doc/redoc/
![img_15.png](readme_images/img_15.png)

NOTE: You have to have superuser credentials for access. You can use ModHeader.

## Demo

**Show themes list**

(Admin only)

![img_5.png](readme_images/img_5.png)

**Show theme details**

(Admin only)

![img_6.png](readme_images/img_6.png)

**Astronomy shows list**

(Admin only)

![img_8.png](readme_images/img_8.png)

**Astronomy show details**

(Admin only)

![img_7.png](readme_images/img_7.png)

**Show session list:**
![img_1.png](readme_images/img_1.png)

Admins:
![img_4.png](readme_images/img_4.png)

General users:
![img.png](readme_images/img.png)

**Show session detail:**

Admins:
![img_2.png](readme_images/img_2.png)

General users:
![img_3.png](readme_images/img_3.png)

**Planetarium domes list**

(Admin only)

![img_9.png](readme_images/img_9.png)

**Planetarium dome details**

(Admin only)

![img_10.png](readme_images/img_10.png)

**Reservations list**

![img_11.png](readme_images/img_11.png)

Admins:

![img_12.png](readme_images/img_12.png)

General users:

![img_13.png](readme_images/img_13.png)
