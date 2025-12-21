import subprocess, re


header_map = {
    "lastmodified": "Last-Modified",
    "etag": "ETag",
    "contentlength": "Content-Length",
    "cachecontrol": "Cache-Control",
    "contenttype": "Content-Type",
}


def run(item, page, flist):
    fl = flist[item["title"]]
    res = subprocess.run(["python", fl], capture_output=True, text=True)
    out = res.stdout.splitlines()
    headers = {}
    for line in out:
        if (not line.startswith("HTTP")) and (not line == ""):
            kv = line.split(":", 1) if ":" in line else None
            headers[kv[0]] = kv[1]
    page.locator('//*[@id="body_container"]/form/input[2]').fill(
        headers.get("Last-Modified")
    )
    page.locator('//*[@id="body_container"]/form/input[3]').fill(headers.get("ETag"))
    page.locator('//*[@id="body_container"]/form/input[4]').fill(
        headers.get("Content-Length")
    )
    page.locator('//*[@id="body_container"]/form/input[5]').fill(
        headers.get("Cache-Control")
    )
    page.locator('//*[@id="body_container"]/form/input[6]').fill(
        headers.get("Content-Type")
    )
    page.locator('//*[@id="body_container"]/form/input[7]').click()
    page.wait_for_selector("#flashmessages > div")
    print(item["title"], "completed.")
    page.close()
