# scrape-doctoralia

## Overview
This project is a FastAPI application that scrapes data from Doctoralia and provides an API to retrieve doctor information.

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Setup

1. **Clone the repository:**
    ```sh
    git clone git@github.com:AbrahamTheCoder/scrape-doctoralia.git

    cd scrape-doctoralia
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the application:**
    ```sh
    python app.py
    ```

## Usage

- **Check the status:**
    Open your browser and navigate to `http://localhost:3000/`. You should see a JSON response with a message and status.

- **Get doctor information:**
    Send a GET request to `http://localhost:3000/info/{doc_url}` where `{doc_url}` is the URL of the doctor's profile on Doctoralia.


## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](http://_vscodecontentref_/0) file for details.