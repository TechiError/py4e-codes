import subprocess, re


def run(item, page, flist):
    fl = flist[item["title"]]
    adata = (
        page.locator("#body_container > ul > li:nth-child(2) > a").inner_text().strip()
    )
    result = subprocess.run(["python", fl], input=adata, text=True, capture_output=True)
    print("Output:")
    out = re.compile(r"\d+").findall(result.stdout)[0]
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
