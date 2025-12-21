import subprocess


def run(item, page, flist):
    adata = (
        page.locator('//*[@id="body_container"]/pre[2]').inner_text().strip() + "\n\n"
    )
    fl = flist[item["title"]]
    result = subprocess.run(["python", fl], input=adata, text=True, capture_output=True)
    print("Output:")
    print(result.stdout.splitlines()[-1])
    print("Errors:")
    print(result.stderr)
    page.locator('//*[@id="body_container"]/form/input[2]').fill(
        result.stdout.splitlines()[-1]
    )
    page.locator('//*[@id="body_container"]/form/input[3]').click()
    page.wait_for_selector("#flashmessages > div")
    print(item["title"], "completed.")
    page.close()
