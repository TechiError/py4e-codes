[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

Code samples and assignments from the **Python for Everybody (PY4E)** course-series by Dr. Charles Severance.  
This repository contains solved exercises, practice scripts, and notes organized per course and chapter.

---

## 📚 Table of Contents
- [PY4E Codes](https://github.com/TechiError/py4e-codes.git)
  - [🔍 About](#-about)
  - [🗂 Repository Structure](#-repository-structure)
  - [⚙ Installation](#-installation)
  - [▶ Usage](#-usage)
  - [🛠 Technologies Used](#-technologies-used)
  - [🤝 Contributing](#-contributing)
  - [📌 Code of Conduct](#-code-of-conduct)
  - [📎 FAQ](#-faq)
  - [📝 License](#-license)
  - [⭐ Thank You!](#-thank-you)

---

## 🔍 About

This repository serves as a learning reference while completing the **PY4E Specialization** (Coursera / University of Michigan).

Contains:
- All Python code written during the courses
- Assignments
- Practice scripts
- Parsing examples
- Web scraping
- API usage
- Databases
- Geodata examples

---

## 🗂 Repository Structure

<pre>
py4e-codes/
│
├── course1/           # Getting Started, Variables, Loops
├── course2/           # Regular Expressions, Networking
├── course3/           # Data & Databases
├── course4/           # Web Applications & GeoData
│   └── geodata/       # XML, JSON, Geodata scripts
│
├── requirements.txt
└── README.md
</pre>

---

## ⚙ Installation

### Install Python

To install Python, follow these general steps:

1.  Go to the official [Python website](https://www.python.org/downloads/) and download the latest version for your operating system.
2.  Run the installer.
3.  **Important:** Before clicking "Install Now," ensure you check the box that says **"Add Python to PATH"**. This makes it easier to run Python from your command line.

![Python Installer showing Add to PATH checkbox](https://github.com/user-attachments/assets/c1b4daee-f5c3-4943-9dfb-ef18de64e866)

4.  Follow the on-screen instructions to complete the installation.
5.  Verify the installation by opening a command prompt or terminal and typing:

    ```bash
    python --version
    ```

[Download The Codes](https://github.com/techierror/py4e-codes/archive/refs/heads/main.zip)

<details>
<summary>Clone The Repo</summary>
    
```bash
git clone https://github.com/TechiError/py4e-codes.git
cd py4e-codes
```
</details>

Install required packages:

```bash
pip install -r requirements.txt
```

---

## ▶ Usage

Navigate into a course folder and run Python programs:

```bash
python course1/hello_world.py
python course2/parse_text_str.py
python course3/regex_sum.py
python course4/first_db.py
```

Run GeoData tools:

```bash
python course4/geodata/geoload.py
python course4/geodata/geodump.py
```

## 🛠 Technologies Used

* Python 3.x
* urllib
* BeautifulSoup
* JSON
* SQLite
* OpenStreetMap Geodata APIs
* Regular Expressions

---

## 🤝 Contributing

Contributions are always welcome!

1. Fork this repository
2. Create a new branch
3. Commit changes
4. Submit a Pull Request

Examples of contributions:

* Code improvements
* Bug fixes
* Missing answers
* Better comments
* README improvements

---

## 📌 Code of Conduct

Be respectful, constructive, and collaborative.
Follow standard open-source contribution etiquette.

---

## ❓ FAQ

### Is this the official PY4E repository?
No, this is a personal learning repository.

### Can beginners use this?
Absolutely!

### Can I contribute?
Yes! PRs welcome 🙂

### I installed Python but `python` command doesn’t work, what should I do?
Try running:

```bash
python3 --version
```
If that works, use ```python3``` instead of ```python```.

---


## 📝 License

This repository is licensed under the **MIT License**.

See the full license text in the `LICENSE` file.

---

## ⭐ Thank You!

If this repository helps you learn Python faster, please consider giving it a GitHub ⭐ star! 😊🚀
