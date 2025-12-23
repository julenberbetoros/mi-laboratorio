from bs4 import BeautifulSoup

# -----------------------------------
# HTML de prueba
# -----------------------------------
with open("mini_dataset/1.html", "r", encoding="utf-8") as f:
    test = f.read()

soup = BeautifulSoup(test, "html.parser")

# ===================================
# 6.6.3 Características Binarias
# ===================================

def has_title(soup):
    if soup.title and soup.title.text.strip():
        return 1
    return 0

def has_input(soup):
    return 1 if len(soup.find_all("input")) > 0 else 0

def has_button(soup):
    return 1 if len(soup.find_all("button")) > 0 else 0

def has_image(soup):
    return 1 if len(soup.find_all("image")) > 0 else 0

def has_link(soup):
    return 1 if len(soup.find_all("link")) > 0 else 0

def has_submit(soup):
    for input_tag in soup.find_all("input"):
        if input_tag.get("type") == "submit":
            return 1
    return 0

def has_password(soup):
    for input_tag in soup.find_all("input"):
        if (input_tag.get("type") == "password" or
            input_tag.get("name") == "password" or
            input_tag.get("id") == "password"):
            return 1
    return 0

def has_email_input(soup):
    for input_tag in soup.find_all("input"):
        if (input_tag.get("type") == "email" or
            input_tag.get("name") == "email" or
            input_tag.get("id") == "email"):
            return 1
    return 0

def has_hidden_element(soup):
    for input_tag in soup.find_all("input"):
        if input_tag.get("type") == "hidden":
            return 1
    return 0

def has_audio(soup):
    return 1 if len(soup.find_all("audio")) > 0 else 0

def has_video(soup):
    return 1 if len(soup.find_all("video")) > 0 else 0

# ===================================
# 6.6.4 Características Cuantitativas
# ===================================

def number_of_inputs(soup):
    return len(soup.find_all("input"))

def number_of_buttons(soup):
    return len(soup.find_all("button"))

def number_of_images(soup):
    image_tags = len(soup.find_all("image"))
    count = 0
    for meta in soup.find_all("meta"):
        if meta.get("type") == "image" or meta.get("name") == "image":
            count += 1
    return image_tags + count

def number_of_option(soup):
    return len(soup.find_all("option"))

def number_of_list(soup):
    return len(soup.find_all("li"))

def number_of_TH(soup):
    return len(soup.find_all("th"))

def number_of_TR(soup):
    return len(soup.find_all("tr"))

def number_of_href(soup):
    count = 0
    for link in soup.find_all("link"):
        if link.get("href"):
            count += 1
    return count

def number_of_paragraph(soup):
    return len(soup.find_all("p"))

def number_of_script(soup):
    return len(soup.find_all("script"))

def length_of_title(soup):
    if soup.title and soup.title.text:
        return len(soup.title.text.strip())
    return 0

# ===================================
# Pruebas
# ===================================

print("has_title -->", has_title(soup))
print("has_input -->", has_input(soup))
print("has_button -->", has_button(soup))
print("has_image -->", has_image(soup))
print("has_submit -->", has_submit(soup))
print("has_link -->", has_link(soup))
print("has_password -->", has_password(soup))
print("has_email_input -->", has_email_input(soup))
print("has_hidden_element -->", has_hidden_element(soup))
print("has_audio -->", has_audio(soup))
print("has_video -->", has_video(soup))

print("number_of_inputs -->", number_of_inputs(soup))
print("number_of_buttons -->", number_of_buttons(soup))
print("number_of_images -->", number_of_images(soup))
print("number_of_option -->", number_of_option(soup))
print("number_of_list -->", number_of_list(soup))
print("number_of_TH -->", number_of_TH(soup))
print("number_of_TR -->", number_of_TR(soup))
print("number_of_href -->", number_of_href(soup))
print("number_of_paragraph -->", number_of_paragraph(soup))
print("number_of_script -->", number_of_script(soup))
print("length_of_title -->", length_of_title(soup))
