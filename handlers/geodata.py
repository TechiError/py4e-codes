import subprocess
import os, re


def submit_review(page):
    x = page.locator('//*[@id="body_container"]/p[3]').inner_text().strip()
    # use regex to check first number 
    submitted = re.findall(r"(\d+)", x)[0]
    print(f"Reviews submitted so far: {submitted}")
    for i in range(0, 5 - int(submitted)):
        page.locator('//*[@id="body_container"]/p[2]/a').click()
        page.locator('//*[@id="body_container"]/div[3]/div[4]/form[1]/input[4]').fill("4")
        page.locator('//*[@id="body_container"]/div[3]/div[4]/form[1]/input[5]').click()
        page.wait_for_selector('//*[@id="flashmessages"]/div')
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        print(f"Submitted review {i + 1}/ {5 - int(submitted)}")

def run(item, page, flist):
    og_url = page.url
    fl = "ss.py"
    page.wait_for_load_state("networkidle")
    if (page.locator('//*[@id="uploaded_file_0"]').count() == 0):
        submit_review(page)
        return
    subprocess.run(["python", fl], text=True, capture_output=True)
    # open new tab and take screenshot
    ph = os.path.abspath("course4/geodata/where.html")
    page.goto(f"file://{ph}")
    page.wait_for_selector("#map")
    page.evaluate(
        """
    () => {overlay.setOffset([-4, -40]);

    function openPopupByName(name) {
        vectorSource.getFeatures().forEach(feature => {
            if (feature.get('name') === name) {
                const coord = feature.getGeometry().getCoordinates();

                // Zoom + center
                map.getView().animate({
                    center: coord,
                    zoom: 14,
                    duration: 800
                });

                // Show popup
                const container = document.getElementById('popup');
                const content = document.getElementById('popup-content');

                container.style.display = "block";
                content.innerHTML = name;
                overlay.setPosition(coord);
            }
        });
    }

    openPopupByName(myData[myData.length - 1][2]);
        }
    """
    )
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(5000)
    screenshot_path = os.path.abspath(f"screenshots/geodata.png", )
    page.screenshot(path=screenshot_path)
    page.goto(og_url)
    page.locator('//*[@id="uploaded_file_0"]').set_input_files("screenshots/geoload.png")
    page.locator('//*[@id="uploaded_file_1"]').set_input_files("screenshots/geodump.png")
    page.locator('//*[@id="uploaded_file_2"]').set_input_files(screenshot_path)
    with page.expect_navigation(wait_until="networkidle"):
        page.locator('//*[@id="body_container"]/form/input[2]').click()
    page.wait_for_selector('//*[@id="flashmessages"]/div')
    submit_review(page)
    print(item["title"], "completed.")
    