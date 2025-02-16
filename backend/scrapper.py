##########################################################################################
# scrapper.py
# Author: Taha Kamil
# Description: This is a simple scrapper that uses Playwright to scrape
#                   the research professors information from a website and stores
#                   it into the database.
##########################################################################################
# System libraries
import os
import re
import tqdm
import asyncio
import aiosqlite

# Third Party Libraries
from playwright.async_api import async_playwright, Page, Browser

#! Constants
DATABASE_NAME = "professorInfo.db"
DIRECTORY = "https://apps.ualberta.ca/directory/search/advanced?DepartmentId=200150&AcceptingUndergraduate=False&Refine=true"

global LARGEST_TABLE
LARGEST_TABLE = 0
global FACULTY
FACULTY = ""

async def scrape_professor_detail(page: Page, faculty, rowInfo=None):
    try:
        container = await page.wait_for_selector(".content > .container", timeout=5000)
    except Exception:
        print("Failed to load professor detail container")
        return

    header_element = await container.query_selector("div.row")
    header = (await header_element.inner_html()).strip() if header_element else None
    header = re.sub(r"\s+", " ", header).strip()

    # Initialize variables
    contact = overview = links = courses = None
    text_overview = None  # Ensure text_overview is always defined
    
    card_elements = await container.query_selector_all(".card")
    for card in card_elements:
        title_el = await card.query_selector(".card-title") or await card.query_selector(".card-header")
        title = (await title_el.text_content()).strip() if title_el else ""
        body_el = await card.query_selector(".card-body")
        if not body_el:
            continue

        if title == "Contact":
            contact = await body_el.inner_html()
        elif title == "Overview":
            overview = await body_el.inner_html()
            text_overview = await body_el.text_content()
        elif title == "Links":
            links = await body_el.inner_html()
        elif title == "Courses":
            courses = await body_el.inner_html()

    breadcrumb = await page.query_selector('[aria-label="breadcrumb"] li:last-child')
    name = (await breadcrumb.text_content()).strip() if breadcrumb else None
    if name.startswith("Viewing "):
        name = name.removeprefix("Viewing ").strip()

    personTitle = phoneNum = location = None
    if rowInfo:
        title_el = await rowInfo.query_selector("td:nth-child(2)")
        personTitle = (await title_el.text_content()).strip() if title_el else None
        phone_el = await rowInfo.query_selector("td:nth-child(4)")
        phoneNum = (await phone_el.text_content()).strip() if phone_el else None
        location_el = await rowInfo.query_selector("td:nth-child(5)")
        location = (await location_el.inner_text()).strip() if location_el else None

    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute(
            "INSERT INTO professors (faculty, name, html_header, html_contact, html_overview, html_links, html_courses, title, phone, location, text_overview) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (faculty, name, header, contact, overview, links, courses, personTitle, phoneNum, location, text_overview)
        )
        await db.commit()

async def scrape_professor_from_row(row, faculty, browser: Browser):
    link = await row.query_selector(".result-name a")
    if not link:
        return

    href = await link.get_attribute("href")
    if not href:
        return
    
    # Use the existing browser instance to create a new page
    prof_page = await browser.new_page()
    try:
        await prof_page.goto("https://apps.ualberta.ca" + href)
        await prof_page.wait_for_load_state("networkidle")
        await scrape_professor_detail(prof_page, faculty, rowInfo=row)
    except Exception as e:
        link_text = (await link.text_content()).strip() if link else None
        print(f"Failed to scrape professor {link_text}: {e}")
    finally:
        await prof_page.close()

async def scrape_professor_from_table(page: Page, faculty, browser: Browser):
    global LARGEST_TABLE, FACULTY
    rows = await page.query_selector_all("table > tbody > tr")

    if rows and len(rows) > LARGEST_TABLE:
        LARGEST_TABLE = len(rows)
        FACULTY = faculty

    batch_size = 50
    for j in tqdm.tqdm(range(0, len(rows), batch_size), desc=f"Scraping {faculty} professors", position=1, leave=False):
        batch = rows[j:j+batch_size]
        tasks = [scrape_professor_from_row(row, faculty, browser) for row in batch]
        await asyncio.gather(*tasks)

async def process_faculty(page: Page, faculty, browser: Browser):
    table_task = asyncio.create_task(
        page.wait_for_selector("table")
    )
    breadcrumb_task = asyncio.create_task(
        page.locator('[aria-label="breadcrumb"] li:last-child').wait_for(
            state="visible"
        )
    )

    done, pending = await asyncio.wait(
        [table_task, breadcrumb_task],
        return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()

    if table_task in done and not table_task.exception():
        await scrape_professor_from_table(page, faculty, browser)
    elif breadcrumb_task in done and not breadcrumb_task.exception():
        await scrape_professor_detail(page, faculty)
    else:
        print(f"Could not find table or breadcrumb for faculty {faculty}.")

async def main():
    backup_db = f"{DATABASE_NAME}.old"
    if os.path.exists(backup_db):
        os.remove(backup_db)
    if os.path.exists(DATABASE_NAME):
        os.rename(DATABASE_NAME, backup_db)

    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS professors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                faculty TEXT,
                name TEXT,
                title TEXT,
                phone TEXT,
                location TEXT,
                html_header TEXT,
                html_contact TEXT,
                html_overview TEXT,
                html_links TEXT,
                html_courses TEXT,
                text_overview TEXT
            )
        """)
        await db.commit()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(DIRECTORY)
        select_menu = await page.wait_for_selector("#DepartmentId", state="visible")
        option_elements = await select_menu.query_selector_all("option")

        departments = []
        for idx in range(2, len(option_elements)):
            value = await option_elements[idx].get_attribute("value")
            faculty = (await option_elements[idx].text_content()).strip()
            departments.append((value, faculty))

        for dept_value, faculty in tqdm.tqdm(departments, desc="Scraping departments", position=0):
            await page.goto(DIRECTORY)
            select_menu = await page.wait_for_selector("#DepartmentId", state="visible")
            await select_menu.select_option(value=dept_value)
            await page.locator('button', has_text='Search').click()

            await process_faculty(page, faculty, browser)

        print(f"Largest table: {LARGEST_TABLE} for faculty {FACULTY}")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())