# Research Professor Information

## Scraper

![Scraper Demo](./images/scraper.gif)

### Overview
This portion of the project uses Playwright for automated browser scrapping of professor research, overview and email. This is then put into the professorInfo.db which is a sqllite3 database. If there already exists a professorInfo.db, it will get the *.old extension added to it.

### Prerequisites
To run the scraper, you will need
- Python 3.13 or higher

### Installation
1. Create and activate a python virtual environment using the following commands:
    ```bash
    python3 -m venv venv
    source ./venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

2. Then upgrade pip to it's latest version:
    ```bash
    pip install --upgrade pip
    ```

3. Install requirements for the scraper and the browser drivers:
    ```bash
    pip install -r requirements.txt && playwright install
    ```

4. And finally, you can run the Scraper:
    ```bash
    python3 ./backend/scraper.py
    ```

