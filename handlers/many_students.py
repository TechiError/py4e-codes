import subprocess

def run(item, page, flist):
    fl = flist[item["title"]]
    with page.expect_download() as download_info:
        page.locator(
            '//*[@id="body_container"]/ul/li/a'
        ).click()
    download = download_info.value
    download.save_as("./" + download.suggested_filename)
    print(f"Downloaded file to: {str(download.path())}")
    result = subprocess.run(
        ["python", fl],
        input=str(download.path()),
        text=True,
        capture_output=True,
    )
    print("Output:")
    print(result.stdout.splitlines()[-1])
    print("Errors:")
    print(result.stderr)
    page.locator('//*[@id="body_container"]/form/input[2]').fill(result.stdout.splitlines()[-1])
    page.locator('//*[@id="body_container"]/form/input[3]').click()
    page.wait_for_selector("#flashmessages > div")
    print(item["title"] + "completed.")
    page.close()