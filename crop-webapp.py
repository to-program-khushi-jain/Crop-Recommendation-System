import streamlit as st
import pickle
from PIL import Image
from googletrans import Translator
import certifi

# Loading models
LogReg_model = pickle.load(open('LogReg_model.pkl', 'rb'))
DecisionTree_model = pickle.load(open('DecisionTree_model.pkl', 'rb'))
NaiveBayes_model = pickle.load(open('NaiveBayes_model.pkl', 'rb'))
RF_model = pickle.load(open('RF_model.pkl', 'rb'))

translator = Translator()

def translate_to_hindi(text):
    translation = translator.translate(text, dest='hi')
    return translation.text

def classify(answer, translate=False):
    result = answer[0] + " is the best crop for cultivation here."
    if translate:
        result = translate_to_hindi(result)
    return result

def main():
    st.title("SowEasy (Crop Recommender)...")
    image = Image.open('cc.jpg')
    st.image(image)
    html_temp = """
    <div style="background-color:teal; padding:10px">
    <h2 style="color:white;text-align:center;">Find The Most Suitable Crop</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    activities = ['Naive Bayes (The Best Model)', 'Logistic Regression', 'Decision Tree', 'Random Forest']
    option = st.sidebar.selectbox("which model would you like to use?", activities)
    st.subheader(option)

    sn = st.slider('NITROGEN (N)', 0.0, 150.0)
    sp = st.slider('PHOSPHOROUS (P)', 0.0, 150.0)
    pk = st.slider('POTASSIUM (K)', 0.0, 210.0)
    pt = st.slider('TEMPERATURE', 0.0, 50.0)
    phu = st.slider('HUMIDITY', 0.0, 100.0)
    pPh = st.slider('Ph', 0.0, 14.0)
    pr = st.slider('RAINFALL', 0.0, 300.0)
    inputs = [[sn, sp, pk, pt, phu, pPh, pr]]

    translate_button = st.checkbox("Translate to Hindi")
    
    if st.button('Classify'):
        if option == 'Logistic Regression':
            st.success(classify(LogReg_model.predict(inputs), translate_button))
        elif option == 'Decision Tree':
            st.success(classify(DecisionTree_model.predict(inputs), translate_button))
        elif option == 'Naive Bayes (The Best Model)':
            st.success(classify(NaiveBayes_model.predict(inputs), translate_button))
        else:
            st.success(classify(RF_model.predict(inputs), translate_button))

if __name__ == '__main__':
    main()

