import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

st.title("Phishing Website Detection using Machine Learning")
st.write(
    "This ML-based app is developed for educational purposes. "
    "Objective of the app is detecting phishing websites. "
    "You can see the details of approach, data set, and feature set if you click on below."
)

with st.expander("PROJECT DETAILS"):
    st.subheader("Approach")
    st.write(
        "I used _supervised learning_ to classify phishing and legitimate websites. "
        "Content-based approach focusing on HTML of websites. "
        "Scikit-learn used for ML models."
    )
    st.write(
        "I created my own dataset and defined features, some from literature and some based on my observations. "
        "Requests library is used to collect data, BeautifulSoup to parse HTML and extract features."
    )
    st.write(
        "Source code and dataset available here: "
        "_https://github.com/emre-kocyigit/phishing-website-detection-content-based_"
    )

st.subheader("Dataset")
st.write("Data from _phishtank.org_ & _tranco-list.eu_.")
st.write(
    "Total: 26584 websites ==> **16060 legitimate** | **10524 phishing**. "
    "Dataset created in October 2022."
)

# ----- PIE CHART ----- #
labels = ['Phishing', 'Legitimate']
phishing_rate = int(ml.phishing_df.shape[0] / (ml.phishing_df.shape[0] + ml.legitimate_df.shape[0]) * 100)
legitimate_rate = 100 - phishing_rate
sizes = [phishing_rate, legitimate_rate]
explode = (0.1, 0)

fig, ax = plt.subplots()
ax.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
ax.axis('equal')
st.pyplot(fig)

st.write("Features + URL + Label => DataFrame")
st.markdown("label = 1 for phishing, 0 for legitimate")
number = st.slider("Select number of rows to display", 0, 100)
st.dataframe(ml.legitimate_df.head(number))

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(ml.df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='phishing_legitimate_structured_data.csv',
    mime='text/csv',
)

st.subheader("Features")
st.write("Only content-based features are used. URL-based features like length are excluded.")

st.subheader("Results")
st.write("7 ML classifiers tested with k-fold cross-validation. Confusion matrices, accuracy, precision, recall calculated.")
st.table(ml.df_results)

st.write("NB -> Gaussian Naive Bayes | SVM -> Support Vector Machine | DT -> Decision Tree")
st.write("RF -> Random Forest | AB -> AdaBoost | NN -> Neural Network | KN -> K-Neighbors")

with st.expander("EXAMPLE PHISHING URLs:"):
    st.write("_https://rtyu38.godaddysites.com/_")
    st.write("_https://karafuru.invite-mint.com/_")
    st.write("_https://defi-ned.top/h5/#/_")
    st.caption("Phishing pages have short lifecycle! Examples may become outdated.")

# ----- Model selection ----- #
choice = st.selectbox(
    "Please select your machine learning model",
    [
        "Gaussian Naive Bayes", "Support Vector Machine", "Decision Tree",
        "Random Forest", "AdaBoost", "Neural Network", "K-Neighbours"
    ]
)

# Load selected model
model_dict = {
    "Gaussian Naive Bayes": ml.nb_model,
    "Support Vector Machine": ml.svm_model,
    "Decision Tree": ml.dt_model,
    "Random Forest": ml.rf_model,
    "AdaBoost": ml.ab_model,
    "Neural Network": ml.nn_model,
    "K-Neighbours": ml.kn_model
}
model = model_dict[choice]
st.write(f"{choice} model is selected!")

# ----- URL input and prediction ----- #
url = st.text_input("Enter the URL to analyze")
if st.button("Check!"):
    try:
        response = requests.get(url.strip(), verify=False, timeout=5)
        if response.status_code != 200:
            st.error(f"HTTP connection was not successful for the URL: {url}")
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = [fe.create_vector(soup)]  # must be 2D array
            result = model.predict(vector)
            if result[0] == 0:
                st.success("This web page seems legitimate!")
                st.balloons()
            else:
                st.warning("Attention! This web page is potential PHISHING!")
                st.snow()
    except requests.exceptions.RequestException as e:
        st.error(f"Error analyzing the URL: {e}")
