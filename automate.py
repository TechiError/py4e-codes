from playwright.sync_api import sync_playwright
import traceback, json
from datetime import datetime

LOG_FILE = "playwright_commands.py"


def multiline_input(prompt=">>> "):
    print("Enter Python code. End with an empty line.")
    lines = []
    while True:
        line = input(prompt)
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)


def save_code(code: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n# ================================\n")
        f.write(f"# Executed at: {datetime.now()}\n")
        f.write("# ================================\n")
        f.write(code)
        f.write("\n")


with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")

    context = browser.contexts[0]
    page = context.new_page()
    page.goto("https://www.coursera.org/learn/python-network-data/home/assignments")
    output_file = "not_passed_assignments.txt"
    rows = page.locator('div.rc-AssignmentsTableRowCds[role="row"]')
    page.wait_for_selector('div.rc-AssignmentsTableRowCds[role="row"]')
    dk = []
    flist = json.loads(open("flist.json", "r", encoding="utf-8").read())
    with open(output_file, "w", encoding="utf-8") as f:
        for i in range(rows.count()):
            row = rows.nth(i)
            title = row.locator('[data-e2e="item-title-text"] a').inner_text().strip()
            subtitle = row.locator(".item-subtitle-text p").inner_text().strip()
            status = row.locator(".status-column-text p").inner_text().strip()
            if subtitle.startswith("Graded App") and status != "Passed" and not title.startswith("Peer"):
                url = row.locator('[data-e2e="item-title-text"] a').get_attribute(
                    "href"
                )
                f.write(
                    f"{title} | {subtitle} | Status: {status} | URL: https://www.coursera.org{url}\n"
                )
                title = (
                    row.locator('[data-e2e="item-title-text"] a').inner_text().strip()
                )
                dk.append(
                    {
                        "title": title,
                        "status": status,
                        "url": f"https://www.coursera.org{url}",
                    }
                )
    for item in dk:
        page.goto(item["url"])
        page.locator('//*[@id="agreement-checkbox-base"]').click()
        with context.expect_page() as new_page_info:
            page.locator(
                '//*[@id="main-container"]/div[1]/div/div/div/div/div/div[1]/div[4]/div/div[3]/div/form/button'
            ).click()
        new_page = new_page_info.value
        exec(
            "import handlers.{} as hnd\nhnd.run(item, new_page, flist)".format(
                flist[item["title"]].replace("course3/", "").replace(".py", "")
            )
        )

    page.goto("https://www.coursera.org/learn/python-databases/home/assignments")
    output_file = "not_passed_assignments.txt"
    rows = page.locator('div.rc-AssignmentsTableRowCds[role="row"]')
    page.wait_for_selector('div.rc-AssignmentsTableRowCds[role="row"]')
    dk = []
    flist = json.loads(open("flist.json", "r", encoding="utf-8").read())
    with open(output_file, "w", encoding="utf-8") as f:
        for i in range(rows.count()):
            row = rows.nth(i)
            title = row.locator('[data-e2e="item-title-text"] a').inner_text().strip()
            subtitle = row.locator(".item-subtitle-text p").inner_text().strip()
            status = row.locator(".status-column-text p").inner_text().strip()
            if (
                subtitle.startswith("Graded App")
                and status != "Passed"
                and not title.startswith("Peer")
            ):
                url = row.locator('[data-e2e="item-title-text"] a').get_attribute(
                    "href"
                )
                f.write(
                    f"{title} | {subtitle} | Status: {status} | URL: https://www.coursera.org{url}\n"
                )
                title = (
                    row.locator('[data-e2e="item-title-text"] a').inner_text().strip()
                )
                dk.append(
                    {
                        "title": title,
                        "status": status,
                        "url": f"https://www.coursera.org{url}",
                    }
                )
    for item in dk:
        if item["title"] == "Databases and Visualization (peer-graded)":
            break
        page.goto(item["url"])
        page.locator('//*[@id="agreement-checkbox-base"]').click()
        with context.expect_page() as new_page_info:
            page.locator(
                '//*[@id="main-container"]/div[1]/div/div/div/div/div/div[1]/div[4]/div/div[3]/div/form/button'
            ).click()
        new_page = new_page_info.value
        try:
            exec(
                "import handlers.{} as hnd\nhnd.run(item, new_page, flist)".format(
                    flist.get(item["title"], "geodata.py").replace("course4/", "").replace(".py", ""), item["title"]
                )
            )
        except Exception as e:
            print(f"Error in handler for {item['title']}:", e)
            break

    print("\nConnected to existing Chrome.")
    print("Available objects: page, context, browser")
    print("All executed code is saved to:", LOG_FILE)
    print("Ctrl+C to exit.\n")

    while True:
        try:
            code = multiline_input()
            if not code.strip():
                continue

            save_code(code)
            exec(code, globals(), locals())

        except KeyboardInterrupt:
            print("\nSession terminated by user.")
            break

        except Exception:
            print("\nError while executing code:")
            traceback.print_exc()
