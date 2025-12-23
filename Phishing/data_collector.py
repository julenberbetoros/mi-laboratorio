# -----------------------------
# 6.9 De URL a Vector Numérico
# -----------------------------

import requests as re
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from bs4 import BeautifulSoup
import pandas as pd
import feature_extraction as fe

disable_warnings(InsecureRequestWarning)


# -----------------------------
# CONFIGURACIÓN
# -----------------------------

# url_filename = "top-1m.csv"
url_filename = "verified_online.csv"


begin_index = 0
end_index = 50   # 🔴 dejamos 50 para pruebas


# -----------------------------
# CARGA ROBUSTA DE URLs
# -----------------------------

df = pd.read_csv(url_filename, header=None)

# CASO PHISHING (tiene columna 'url')
if "url" in df.columns:
    url_list = df["url"].astype(str).tolist()

# CASO LEGÍTIMOS (top-1m.csv → dominio en columna 1)
else:
    url_list = df.iloc[:, 1].astype(str).tolist()

collection_list = url_list[begin_index:end_index]


def normalize_url(url):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "http://" + url


collection_list = [normalize_url(url) for url in collection_list]


# -----------------------------
# CREACIÓN DE DATOS ESTRUCTURADOS
# -----------------------------

def create_structured_data(url_list):
    data_list = []

    for i, url in enumerate(url_list):
        try:
            response = re.get(url, verify=False, timeout=4)

            if response.status_code != 200:
                print(i, "HTTP error:", url)
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            vector = fe.create_vector(soup)
            vector.append(url)
            data_list.append(vector)

        except re.exceptions.RequestException as e:
            print(i, "-->", e)

    return data_list


data = create_structured_data(collection_list)

if len(data) == 0:
    print("⚠️ No data collected.")
    exit()


columns = [
    "has_title",
    "has_input",
    "has_button",
    "has_image",
    "has_submit",
    "has_link",
    "has_password",
    "has_email_input",
    "has_hidden_element",
    "has_audio",
    "has_video",
    "number_of_inputs",
    "number_of_buttons",
    "number_of_images",
    "number_of_option",
    "number_of_list",
    "number_of_TH",
    "number_of_TR",
    "number_of_href",
    "number_of_paragraph",
    "number_of_script",
    "length_of_title",
    "URL",
]

df_out = pd.DataFrame(data, columns=columns)

# -----------------------------
# ETIQUETADO
# -----------------------------

df_out["label"] = 1
df_out.to_csv("structured_data_phishing.csv", index=False)


print("✅ structured_data_legitimate.csv created successfully")
