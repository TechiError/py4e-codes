import subprocess
import os
import re


def submit_review(page):
    page.wait_for_load_state("domcontentloaded")

    text = page.locator(
        'xpath=//*[@id="body_container"]/p[3]'
    ).inner_text().strip()

    submitted = int(re.findall(r"(\d+)", text)[0])
    print(f"Reviews submitted so far: {submitted}")

    for i in range(5 - submitted):
        page.locator(
            'xpath=//*[@id="body_container"]/p[2]/a'
        ).click()

        page.locator(
            'xpath=//*[@id="body_container"]/div[3]/div[4]/form[1]/input[4]'
        ).fill("4")

        page.locator(
            'xpath=//*[@id="body_container"]/div[3]/div[4]/form[1]/input[5]'
        ).click()

        # Wait for confirmation message ONLY
        page.wait_for_selector(
            'xpath=//*[@id="flashmessages"]/div',
            timeout=10000
        )

        print(f"Submitted review {i + 1}/{5 - submitted}")


def run(item, page, flist):
    og_url = page.url
    fl = "ss.py"

    page.wait_for_load_state("domcontentloaded")

    # If no upload inputs → peer review page
    if page.locator('xpath=//*[@id="uploaded_file_0"]').count() == 0:
        submit_review(page)
        return

    # Run data generation
    subprocess.run(["python", fl], check=True)

    # Open local map HTML
    ph = os.path.abspath("course4/geodata/where.html")
    page.goto(f"file:///{ph}", wait_until="domcontentloaded")

    # Wait for map to actually exist
    page.wait_for_selector("#map", timeout=15000)

    # Trigger popup + zoom
    page.evaluate(
        """
        () => {
            overlay.setOffset([-4, -40]);

            function openPopupByName(name) {
                vectorSource.getFeatures().forEach(feature => {
                    if (feature.get('name') === name) {
                        const coord = feature.getGeometry().getCoordinates();

                        map.getView().animate({
                            center: coord,
                            zoom: 14,
                            duration: 800
                        });

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
    # 🔥 WAIT FOR REAL MAP RENDER
    page.evaluate(
        """
        () => {
            return new Promise(resolve => {
                map.once('rendercomplete', () => resolve(true));
            });
        }
        """
    )
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    screenshot_path = os.path.abspath("screenshots/geodata.png")
    page.screenshot(path=screenshot_path)

    # Go back to assignment page
    page.goto(og_url, wait_until="domcontentloaded")

    # Upload files
    page.locator(
        'xpath=//*[@id="uploaded_file_0"]'
    ).set_input_files("screenshots/geoload.png")

    page.locator(
        'xpath=//*[@id="uploaded_file_1"]'
    ).set_input_files("screenshots/geodump.png")

    page.locator(
        'xpath=//*[@id="uploaded_file_2"]'
    ).set_input_files(screenshot_path)

    # Submit assignment (this DOES navigate)
    with page.expect_navigation(wait_until="domcontentloaded"):
        page.locator(
            'xpath=//*[@id="body_container"]/form/input[2]'
        ).click()

    # Confirm submission
    page.wait_for_selector(
        'xpath=//*[@id="flashmessages"]/div',
        timeout=15000
    )

    submit_review(page)
    print(item["title"], "completed.")
