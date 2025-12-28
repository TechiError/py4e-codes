import subprocess, re


def run(item, page, flist):
    fl = flist[item["title"]]
    adata = (
        page.locator("#body_container > ul > li:nth-child(2) > a").inner_text().strip()
    )
    pos = (
        page.locator("#body_container > ul > li:nth-child(2) > b:nth-child(3)")
        .inner_text()
        .strip()
    )
    count = (
        page.locator("#body_container > ul > li:nth-child(2) > b:nth-child(4)")
        .inner_text()
        .strip()
    )
    result = subprocess.run(
        ["python", fl],
        input=adata + "\n" + pos + "\n" + count,
        text=True,
        capture_output=True,
    )
    print("Output:")
    out = result.stdout.strip().split()[-1]
    print(out)
    print("STDERR:")
    print(result.stderr)
    with open(fl, "r", encoding="utf-8") as f:
        pcode = f.read()
    page.locator("#body_container > form > input[type=text]:nth-child(3)").fill(out)
    page.locator("#body_container > form > textarea").fill(pcode)
    page.locator("#body_container > form > input[type=submit]:nth-child(4)").click()
    page.wait_for_selector("#flashmessages > div")
    print(item["title"], "completed.")
    page.close()
