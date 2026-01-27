import subprocess
import os, re


def submit_review(page):
    x = page.locator('//*[@id="body_container"]/p[3]').inner_text().strip()
    # use regex to check first number 
    print(x)
    submitted = re.findall(r"(\d+)", x)[0]
    print(f"Reviews submitted so far: {submitted}")
    if int(submitted) >= 8:
        return
    for i in range(0, 8 - int(submitted)):
        page.locator('//*[@id="body_container"]/p[2]/a').click()
        page.locator('//*[@id="body_container"]/div[3]/div[3]/form[1]/input[4]').fill("6")
        page.locator('//*[@id="body_container"]/div[3]/div[3]/form[1]/input[5]').click()
        page.wait_for_selector('//*[@id="flashmessages"]/div')
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        print(f"Submitted review {i + 1}/ {8 - int(submitted)}")

def run(item, page, flist):
    if (page.locator('//*[@id="uploaded_file_0"]').count() == 0):
        submit_review(page)
        return
    page.locator('//*[@id="uploaded_file_0"]').set_input_files("screenshots/code.png")
    page.locator('//*[@id="uploaded_file_1"]').set_input_files("screenshots/term.png")
    with page.expect_navigation(wait_until="networkidle"):
        page.locator('//*[@id="body_container"]/form/input[2]').click()
    page.wait_for_selector('//*[@id="flashmessages"]/div')
    submit_review(page)
    print(item["title"], "completed.")
    page.close()