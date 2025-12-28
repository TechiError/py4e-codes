import subprocess

def run(item, page, flist):
    fl = flist[item["title"]]
    page.wait_for_load_state("networkidle")
    locator = page.locator('#body_container pre')
    adata = locator.last.inner_text().strip()
    result = subprocess.run(
        ["python", fl],
        input=adata,
        text=True,
        capture_output=True
    )
    out = result.stdout.strip().split(":")[-1].strip()
    print("Output:")
    print(out)
    print("STDERR:")
    print(result.stderr)
    with open(fl, "r", encoding="utf-8") as f:
        pcode = f.read()
    page.locator('//*[@id="body_container"]/form/input[2]').fill(out)
    page.locator('//*[@id="body_container"]/form/textarea').fill(pcode)
    page.locator('//*[@id="body_container"]/form/input[3]').click()
    page.wait_for_selector('//*[@id="flashmessages"]/div')
    print(item["title"], "completed.")
    page.close()