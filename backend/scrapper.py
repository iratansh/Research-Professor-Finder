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
##########################################################################################  
# These are the constants that are used in the scrapper, I just put there here for
# easy access and so that it is visible to the reader of this code.
#! Constants
BATCH_SIZE = 50
DATABASE_NAME = "../professorInfo.db"
DIRECTORY = "https://apps.ualberta.ca/directory/search/advanced?DepartmentId=200150&AcceptingUndergraduate=False&Refine=true"
global LARGEST_TABLE
LARGEST_TABLE = 0
global FACULTY
FACULTY = ""

# Functions
async def scrape_professor_detail(page: Page, faculty, rowInfo=None):
    container = await page.wait_for_selector(".content > .container", timeout=5000)

    contact = header = overview = links = courses = email = None
    children = await container.query_selector_all("div.row")
    if children and len(children) > 1:
        header_el = children[-1]
        header = (await header_el.inner_html()).strip() or None
    else:
        header = None
    text_overview = None
    
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
    email = page.url.split("/")[-1] + "@ualberta.ca"

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
            "INSERT INTO professors (faculty, name, html_header, html_contact, html_overview, html_links, html_courses, title, phone, location, text_overview, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (faculty, name, header, contact, overview, links, courses, personTitle, phoneNum, location, text_overview, email)
        )
        await db.commit()

async def scrape_professor_from_row(row, faculty, browser: Browser, pbar):
    link = await row.query_selector(".result-name a")
    if not link:
        pbar.update(1)
        return

    href = await link.get_attribute("href")
    if not href:
        pbar.update(1)
        return
    
    prof_page = await browser.new_page()
    try:
        await prof_page.goto("https://apps.ualberta.ca" + href)
        await scrape_professor_detail(prof_page, faculty, rowInfo=row)
    except Exception as e:
        for _ in range(3):
            await prof_page.goto("https://apps.ualberta.ca" + href)
            try:
                await scrape_professor_detail(prof_page, faculty, rowInfo=row)
                break
            except Exception as e:
                tqdm.tqdm.write(f"\033[93m!! Failed to reload professor page {prof_page.url}. !!\033[0m")

        link_text = (await link.text_content()).strip() if link else None
        tqdm.tqdm.write(f"\033[91m!! Failed to scrape professor {link_text}: {e} !!\033[0m")
    finally:
        await prof_page.close()
        pbar.update(1)

async def scrape_professor_from_table(page: Page, faculty, browser: Browser):
    global LARGEST_TABLE, FACULTY
    rows = await page.query_selector_all("table > tbody > tr")

    if rows and len(rows) > LARGEST_TABLE:
        LARGEST_TABLE = len(rows)
        FACULTY = faculty

    pbar = tqdm.tqdm(total=len(rows), desc=f"⚠️  {faculty.split("-")[0].strip()}", leave=False, position=0)

    for j in range(0, len(rows), BATCH_SIZE):
        batch = rows[j:j+BATCH_SIZE]
        tasks = [scrape_professor_from_row(row, faculty, browser, pbar) for row in batch]
        await asyncio.gather(*tasks)
    
    pbar.close()

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
        tqdm.tqdm.write(f"Could not find table or breadcrumb for faculty {faculty}.")

# Main
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
                email TEXT,
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

        with tqdm.tqdm(total=len(departments), desc="Total Progress", position=1) as dept_pbar:
            for dept_value, faculty in departments:
                try:
                    await page.goto(DIRECTORY)
                    select_menu = await page.wait_for_selector("#DepartmentId", state="visible")
                    await select_menu.select_option(value=dept_value)
                    await page.locator('#Title').fill("professor")
                    await page.locator('button', has_text='Search').click()
                    await process_faculty(page, faculty, browser)
                except Exception as e:
                    # Failure message with red background and off white text
                    tqdm.tqdm.write(f"❌ {faculty}")
                else:
                    # Success message with green background and off white text
                    tqdm.tqdm.write(f"✅ {faculty}")
                dept_pbar.update(1)
            

        tqdm.tqdm.write(f"Largest table: {LARGEST_TABLE} for {FACULTY}")
        await browser.close()

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())