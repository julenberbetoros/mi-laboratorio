# ===============================
# 6.3 Web Scraping con Requests
# ===============================

import requests as re
from bs4 import BeautifulSoup
import os

# -------------------------------
# 6.3.2 Petición HTTP
# -------------------------------
url = "https://www.kaggle.com"
response = re.get(url)

print("response -->", response)
print("type -->", type(response))
print("status_code -->", response.status_code)

# -------------------------------
# 6.3.4 Control de errores
# -------------------------------
if response.status_code != 200:
    print("HTTP connection is not successful. Try it again")
else:
    print("HTTP connection is successful.")

# ===============================
# 6.4 BeautifulSoup
# ===============================

soup = BeautifulSoup(response.content, "html.parser")

# -------------------------------
# Título
# -------------------------------
print("HTML title -->", soup.title)
print("Title text -->", soup.title.text if soup.title else "No title")

# -------------------------------
# Enlaces
# -------------------------------
print("Links:")
for link in soup.find_all("link"):
    print(link.get("href"))

# -------------------------------
# Texto plano
# -------------------------------
print("Text (first 500 chars):")
print(soup.get_text()[:500])

# ===============================
# 6.5 Crear Mini Dataset
# ===============================

# -------------------------------
# Crear carpeta mini_dataset
# -------------------------------
folder = "mini_dataset"
if not os.path.exists(folder):
    os.mkdir(folder)

# -------------------------------
# Función de scraping
# -------------------------------
def scrape_content(url):
    response = re.get(url)
    if response.status_code == 200:
        print(f"HTTP OK --> {url}")
        return response
    else:
        print(f"HTTP ERROR --> {url}")
        return None

# -------------------------------
# Guardar HTML
# -------------------------------
path = os.getcwd() + "/" + folder

def save_html_file(to_where, text, name):
    with open(os.path.join(to_where, name + ".html"), "w", encoding="utf-8") as f:
        f.write(text)

# -------------------------------
# Lista de URLs
# -------------------------------
url_list = [
    "https://www.kaggle.com",
    "https://stackoverflow.com",
    "https://www.researchgate.net",
    "https://www.python.org",
    "https://www.w3schools.com",
    "https://github.com",
    "https://scholar.google.com",
    "https://www.mendeley.com",
    "https://www.overleaf.com",
    "https://www.ehu.eus"
]

# -------------------------------
# Crear mini dataset
# -------------------------------
def create_mini_dataset(to_where, url_list):
    for i in range(len(url_list)):
        content = scrape_content(url_list[i])
        if content is not None:
            save_html_file(to_where, content.text, str(i))
    print("Mini dataset is created.")

# -------------------------------
# Ejecutar
# -------------------------------
create_mini_dataset(path, url_list)
