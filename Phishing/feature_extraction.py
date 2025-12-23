import os
import pandas as pd
from bs4 import BeautifulSoup
from features import *


def create_vector(soup):
    return [
        has_title(soup),
        has_input(soup),
        has_button(soup),
        has_image(soup),
        has_submit(soup),
        has_link(soup),
        has_password(soup),
        has_email_input(soup),
        has_hidden_element(soup),
        has_audio(soup),
        has_video(soup),
        number_of_inputs(soup),
        number_of_buttons(soup),
        number_of_images(soup),
        number_of_option(soup),
        number_of_list(soup),
        number_of_TH(soup),
        number_of_TR(soup),
        number_of_href(soup),
        number_of_paragraph(soup),
        number_of_script(soup),
        length_of_title(soup),
    ]


if __name__ == "__main__":

    DATASET_DIR = "mini_dataset"
    dataset_features = []

    for filename in os.listdir(DATASET_DIR):
        if filename.endswith(".html"):
            filepath = os.path.join(DATASET_DIR, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            vector = create_vector(soup)
            vector.append(filename)
            dataset_features.append(vector)

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
        "filename",
    ]

    df = pd.DataFrame(dataset_features, columns=columns)
    df.to_csv("features_dataset.csv", index=False)

    print("Feature extraction completed. CSV saved as features_dataset.csv")
