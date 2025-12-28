import subprocess, re


def run(item, page, flist):
    fl = flist[item["title"]]
    adata = page.locator('//*[@id="body_container"]/p[7]/a').get_attribute("href")
    result = subprocess.run(
        ["python", fl],
        input=adata,
        text=True,
        capture_output=True,
    )
    print("Output:")
    print(result.stdout.splitlines()[-1])
    print("Errors:")
    print(result.stderr)
    with page.expect_file_chooser() as fc_info:
        page.locator('//*[@id="body_container"]/form/input[2]').click()
    file_chooser = fc_info.value
    file_chooser.set_files("trackdb.sqlite")
    page.locator('//*[@id="body_container"]/form/input[3]').click()
    page.wait_for_selector("#flashmessages > div")
    page.wait_for_timeout(2000)
    print(item["title"], "completed.")
    page.close()
