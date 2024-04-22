import os
import pickle
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

    
# getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# loading the saved models

diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('heartdisease_model.sav', 'rb'))

lung_cancer_model=pickle.load(open('lung_cancer_model.sav', 'rb'))

hepatitis_model=pickle.load(open('hepatitis_model.sav', 'rb'))

parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

# sidebar for navigation
with st.sidebar: 
    selected = option_menu('Poly-Patho-Prognosis',

                           ['Diabetes Prediction',
                            'Heart Attack Prediction',
                            'Lung Cancer Prediction',
                            'Hepatitis Prediction',
                            "Parkinson's Prediction"],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart','lungs', 'clipboard2-heart','person'],
                           default_index=0)


# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    def add_bg_from_url():
        st.markdown(
             f"""
             <style>
             .stApp {{
                 background-image: url("https://png.pngtree.com/background/20210710/original/pngtree-science-grid-globe-banner-background-picture-image_1021087.jpg");
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
             unsafe_allow_html=True
         )

    add_bg_from_url()    
    # page title
    st.title('Diabetes Prediction')

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        HighBP = st.text_input('0 = no high BP:Shimmer 1 = high BP')

    with col2:
        HighChol = st.text_input('0 = no high cholesterol:Shimmer 1 = high cholesterol')

    with col3:
        CholCheck = st.text_input('0 = no cholesterol check in 5 years:Shimmer 1 = yes cholesterol check in 5 years')

    with col1:
        BMI = st.text_input('Body Mass Index Value:Shimmer (BMI)')

    with col2:
        Smoker = st.text_input('Have you smoked at least 100 cigarettes in your entire life?  0 = no 1 = yes')

    with col3:
        Stroke = st.text_input('(Ever told) you had a stroke.:Shimmer 0 = no 1 = yes')

    with col1:
        HeartDiseaseorAttack = st.text_input('coronary heart disease(CHD) or myocardial infarction(MI):Shimmer 0 = no 1 = yes	')

    with col2:
        PhysActivity = st.text_input('physical activity in past 30 days - not including job:Shimmer 0 = no 1 = yes')
    
    with col3:
        Fruits = st.text_input('Consume Fruit 1 or more times per day:Shimmer 0 = no 1 = yes')

    with col1:
        Veggies = st.text_input('Consume Vegetables 1 or more times per day:Shimmer 0 = no 1 = yes')

    with col2:
        HvyAlcoholConsump = st.text_input('Heavy drinkers:Shimmer 0 = no 1 = yes')
    
    with col3:
        AnyHealthcare = st.text_input('Have taken any health care in the last 6 months? 0 = no 1 = yes')

    with col1:
        NoDocbcCost = st.text_input('Was there a time in the past 12 months when you needed to see a doctor but could not because of cost?:Shimmer 0 = no 1 = yes	')

    with col2:
        GenHlth = st.text_input('General Health : scale 1-5:Shimmer 1 = excellent 2 = very good :Shimmer 3 = good 4 = fair 5 = poor')
    
    with col3:
        MentHlth = st.text_input('In the Last 30 days how many days Mental state was good?:Shimmer scale 1-30 days')

    with col1:
        PhysHlth = st.text_input('In the Last 30 days how many days physical state was good?  scale 1-30 days')

    with col2:
        DiffWalk = st.text_input('Do you have serious difficulty walking or climbing stairs?:Shimmer 0 = no 1 = yes	')

    with col3:
        Sex = st.text_input('Sex :Shimmer 0 = female 1 = male')

    with col1:
        Age = st.text_input('Age:Shimmer Enter Your Age')

    with col2:
        Education = st.text_input('Education level (EDUCA see codebook) :Shimmerscale 1-6 ')

    with col3:
        Income = st.text_input('Income scale (INCOME2 see codebook):Shimmer scale 1-8 ')


    # code for Prediction
    diab_diagnosis = ''

    # creating a button for Prediction
    submit_button = st.button("Diabetes Test Result")
    if submit_button:

        user_input = [HighBP,HighChol,CholCheck,BMI, Smoker, Stroke,HeartDiseaseorAttack,PhysActivity,Fruits,Veggies,HvyAlcoholConsump,AnyHealthcare, NoDocbcCost,GenHlth,MentHlth,PhysHlth,DiffWalk,Sex,Age,Education,Income]

        user_input = [float(x) for x in user_input]

        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person has high risk of having Diabetes'
        else:
            diab_diagnosis = 'Congratulations..... The person does not have Diabetes'

    st.success(diab_diagnosis)
    
    csv_file_path = "Diabetes Data Collection.csv"
    data = pd.DataFrame(columns=["Diabetes_binary",	"HighBP", "HighChol", "CholCheck",	"BMI",	"Smoker",	"Stroke", "HeartDiseaseorAttack",	"PhysActivity", "Fruits",	"Veggies",	"HvyAlcoholConsump",	"AnyHealthcare",	"NoDocbcCost",	"GenHlth",	"MentHlth",	"PhysHlth",	"DiffWalk",	"Sex",	"Age",	"Education",	"Income"])
    if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path)
    if submit_button:
        new_row = {"Diabetes_binary": diab_prediction[0], "HighBP": HighBP,	"HighChol":HighChol, "CholCheck":CholCheck, "BMI":BMI,	"Smoker":Smoker, "Stroke":Stroke,	"HeartDiseaseorAttack":HeartDiseaseorAttack,	"PhysActivity":PhysActivity,	
                   "Fruits":Fruits,	"Veggies":Veggies,	"HvyAlcoholConsump":HvyAlcoholConsump,	"AnyHealthcare":AnyHealthcare,	"NoDocbcCost":NoDocbcCost,	"GenHlth":GenHlth,	"MentHlth":MentHlth,	"PhysHlth":PhysHlth,	"DiffWalk":DiffWalk,	
                   "Sex":Sex,	"Age":Age,	"Education":Education,	"Income":Income}
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv(csv_file_path, index=False)
        #if st.button('Privacy Policy'):
        st.write("YOUR DATA HAS BEEN SAVED. YOUR DATA IS SAFE WITH US AND ONLY MIGHT BE USED FOR RESEARCH PURPOSE. WE ARE HIGHLY GREATFUL FOR YOUR AMAZING CONTRIBUTION TOWARDS MANKIND.")
        st.write("THANK YOU & STAY HEALTHY!!")
        
        
# Heart Disease Prediction Page
if selected == 'Heart Attack Prediction':
    def add_bg_from_url():
        st.markdown(
             f"""
             <style>
             .stApp {{
                 background-image: url("https://png.pngtree.com/background/20230520/original/pngtree-3d-illustration-of-a-human-heart-in-bluish-light-picture-image_2676710.jpg");
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
             unsafe_allow_html=True
         )

    add_bg_from_url()    
    # page title
    
    st.title('Heart Attack Prediction')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
    
    heart_diagnosis = ''

    # creating a button for Prediction

    submit_button = st.button("Heart Attack Result")
    if submit_button:

        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person has high risk of having a Cardiac Arrest'
        else:
            heart_diagnosis = 'Congratulations..... The person dont have a risk of having a Cardiac Arrest'

    st.success(heart_diagnosis)
    
    #Data Collection
    csv_file_path = "Heart Attack Data Collection.csv"
    data = pd.DataFrame(columns=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"])
    if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path)
    if submit_button:
        new_row = {"age":age, "sex":sex, "cp":cp, "trestbps":trestbps, "chol":chol, "fbs":fbs, "restecg":restecg, "thalach":thalach, "exang":exang, "oldpeak":oldpeak, "slope":slope, "ca":ca, "thal":thal }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv(csv_file_path, index=False)
        #if st.button('Privacy Policy'):
        st.write("YOUR DATA HAS BEEN SAVED. YOUR DATA IS SAFE WITH US AND ONLY MIGHT BE USED FOR RESEARCH PURPOSE. WE ARE HIGHLY GREATFUL FOR YOUR AMAZING CONTRIBUTION TOWARDS MANKIND.")
        st.write("THANK YOU & STAY HEALTHY!!")
        
        
#Lung Cancer Prediction Page
if selected == "Lung Cancer Prediction":
    def add_bg_from_url():
        st.markdown(
             f"""
             <style>
             .stApp {{
                 background-image: url("https://static.vecteezy.com/system/resources/previews/013/761/414/non_2x/futuristic-abstract-symbol-of-the-human-lung-concept-blue-respiratory-system-pneumonia-asthma-low-poly-geometric-3d-wallpaper-background-illustration-vector.jpg");
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
             unsafe_allow_html=True
         )

    add_bg_from_url()    
    # page title
    st.title("Lung Cancer Prediction")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        index = st.text_input('Enter any number')

    with col2:
        Age = st.text_input('Enter Age')

    with col3:
        Gender = st.text_input('Sex  0 = female 1 = male')

    with col4:
        AirPollution = st.text_input('The level of air pollution exposure of the patient')

    with col1:
        Alcoholuse = st.text_input('The level of alcohol use of the patient')

    with col2:
        DustAllergy = st.text_input('The level of dust allergy of the patient')

    with col3:
        OccuPationalHazards = st.text_input('The level of occupational hazards of the patient')

    with col4:
        GeneticRisk = st.text_input('The level of genetic risk of the patient')

    with col1:
        chronicLungDisease = st.text_input('The level of chronic lung disease of the patient')

    with col2:
        BalancedDiet = st.text_input('The level of balanced diet of the patient')

    with col3:
        Obesity = st.text_input('The level of obesity of the patient')

    with col4:
        Smoking = st.text_input('The level of smoking of the patient')

    with col1:
        PassiveSmoker = st.text_input('The level of passive smoker of the patient')

    with col2:
        ChestPain = st.text_input('The level of chest pain of the patient')

    with col3:
        CoughingofBlood = st.text_input('The level of coughing of blood of the patient')

    with col4:
        Fatigue = st.text_input('The level of fatigue of the patient')

    with col1:
        WeightLoss = st.text_input('The level of weight loss of the patient')

    with col2:
        ShortnessofBreath= st.text_input('The level of shortness of breath of the patient')

    with col3:
        Wheezing = st.text_input('The level of wheezing of the patient')

    with col4:
        SwallowingDifficulty = st.text_input('The level of swallowing difficulty of the patient')

    with col1:
       ClubbingofFingerNails = st.text_input('The level of clubbing of finger nails of the patient.')

    with col2:
        FrequentCold =st.text_input('The Level of Frequent Cold:Shimmer of the patient')
    
    with col3:
        DryCough = st.text_input('The level of Dry Cough of the patient')
        
    with col4:
        Snoring = st.text_input('The level of snoring of the patient')

    # code for Prediction
    lungs_diagnosis=' '

    # creating a button for Prediction    
    submit_button = st.button("Lung Cancer Test Result")
    if submit_button:

        user_input = [index	, Age, Gender,	AirPollution,	Alcoholuse, DustAllergy, OccuPationalHazards, GeneticRisk, chronicLungDisease, BalancedDiet, Obesity, Smoking, PassiveSmoker, ChestPain	, CoughingofBlood,	Fatigue, WeightLoss, ShortnessofBreath, Wheezing, SwallowingDifficulty,	ClubbingofFingerNails,	FrequentCold,	DryCough,	Snoring]


        user_input = [float(x) for x in user_input]

        lungCancer_prediction = lung_cancer_model.predict([user_input])

        if lungCancer_prediction[0] == 1:
            lungs_diagnosis = "The person has high risk of having Lung Cancer"
        else:
            lungs_diagnosis = "Congratulations..... The person does not have Lung Cancer"

    st.success(lungs_diagnosis)
    
    csv_file_path = "Lung Cancer Data Collection.csv"
    data = pd.DataFrame(columns=["index",	"Patient Id",	"Age",	"Gender",	"Air Pollution",	"Alcohol use",	"Dust Allergy",	"OccuPational Hazards",	"Genetic Risk",	"chronic Lung Disease",	"Balanced Diet",	"Obesity",	"Smoking",	"Passive Smoker",	"Chest Pain",	"Coughing of Blood",	"Fatigue",	"Weight Loss",	"Shortness of Breath",	"Wheezing",	"Swal0ing Difficulty",	"Clubbing of Finger Nails",	"Frequent Cold",	"Dry Cough",	"Snoring",	"Level"])
    if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path)
    if submit_button:
        new_row = {"index":index,	"Patient Id":" ",	"Age":Age,	"Gender":Gender,	"Air Pollution":AirPollution,	"Alcohol use":Alcoholuse,	"Dust Allergy":DustAllergy,
                   "OccuPational Hazards":OccuPationalHazards,	"Genetic Risk":GeneticRisk,	"chronic Lung Disease":chronicLungDisease,	"Balanced Diet":BalancedDiet,	"Obesity":Obesity,
                   "Smoking":Smoking,	"Passive Smoker":PassiveSmoker,	"Chest Pain":ChestPain,	"Coughing of Blood":CoughingofBlood,	"Fatigue":Fatigue,	"Weight Loss":WeightLoss,	
                   "Shortness of Breath":ShortnessofBreath,	"Wheezing":Wheezing,	"Swal0ing Difficulty":SwallowingDifficulty,	"Clubbing of Finger Nails":ClubbingofFingerNails,
                   "Frequent Cold":FrequentCold,	"Dry Cough":DryCough,	"Snoring":Snoring,	"Level":lungCancer_prediction[0]}
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv(csv_file_path, index=False)
        #if st.button('Privacy Policy'):
        st.write("YOUR DATA HAS BEEN SAVED. YOUR DATA IS SAFE WITH US AND ONLY MIGHT BE USED FOR RESEARCH PURPOSE. WE ARE HIGHLY GREATFUL FOR YOUR AMAZING CONTRIBUTION TOWARDS MANKIND.")
        st.write("THANK YOU & STAY HEALTHY!!")
        
        
# Hepatitis Prediction Page
if selected == "Hepatitis Prediction":
    def add_bg_from_url():
        st.markdown(
             f"""
             <style>
             .stApp {{
                 background-image: url("https://static.vecteezy.com/system/resources/previews/013/761/406/original/futuristic-abstract-symbol-of-the-human-liver-concept-for-the-treatment-of-cirrhosis-a-hepatitis-disease-low-poly-geometric-3d-wallpaper-background-illustration-vector.jpg");
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
             unsafe_allow_html=True
         )

    add_bg_from_url()    
  
    # page title
    
    st.title("Hepatitis Prediction")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        Age = st.text_input('Enter Age')

    with col2:
        Gender = st.text_input('Sex  1 = female 2 = male')

    with col3:
        BMI = st.text_input('Body Mass Index Value')

    with col4:
        Fever = st.text_input(' Fever: [Absent=1], [Present=2]')

    with col1:
        NauseaVomting = st.text_input('Nausea/Vomting:Shimmer [Absent=1], [Present=2]')

    with col2:
        Headache = st.text_input('Headache:Shimmer [Absent=1], [Present=2]')

    with col3:
        Diarrhea = st.text_input('Diarrhea:Shimmer [Absent=1], [Present=2]')

    with col4:
        Fatigue_generalizedboneache = st.text_input('Fatigue & generalized bone ache:Shimmer [Absent=1], [Present=2]')

    with col1:
        Jaundice = st.text_input('Jaundice: [Absent=1], [Present=2]')

    with col2:
        Epigastricpain = st.text_input('Epigastric pain: [Absent=1], [Present=2]')

    with col3:
        WBC = st.text_input('White blood cells Count')
    
    with col4:
        RBC = st.text_input('Red blood cells Count')
    
    with col1:
        HGB = st.text_input('Hemoglobin Count')
        
    with col2:
        Plat = st.text_input('Platelets Count')

    with col3:
        AST1 = st.text_input('aspartate transaminase ratio value')

    with col4:
        ALT1 = st.text_input('alanine transaminase ratio 1 week value')

    with col1:
        ALT4 = st.text_input('alanine transaminase ratio 4 week value')

    with col2:
        ALT12 = st.text_input('alanine transaminase ratio 12 weeks value')

    with col3:
        ALT24 = st.text_input('alanine transaminase ratio 24 weeks value')

    with col4:
        ALT36 = st.text_input('alanine transaminase ratio 36 weeks value')

    with col1:
        ALT48 = st.text_input('alanine transaminase ratio 48 weeks value')

    with col2:
        ALTafter24w = st.text_input('after 24 warnings alanine transaminase ratio 24 weeks value')

    with col3:
        RNABase = st.text_input('RNA Base Value')

    with col4:
        RNA4 = st.text_input('RNA 4 Value')

    with col1:
        RNA12 = st.text_input('RNA 12 Value')
        
    with col2:
        RNAEOT = st.text_input('RNA end-of-treatment Value')

    with col3:
        RNAEF = st.text_input('RNA Elongation Factor Value')

    with col4:
        BaselinehistologicalGrading = st.text_input('Baseline histological Grading Value')



    # code for Prediction
    hepatitis_diagnosis = ''

    # creating a button for Prediction    
    submit_button = st.button("Hepatitis Test Result")
    if submit_button:

        user_input = [Age, Gender, BMI, Fever, NauseaVomting, Headache, Diarrhea, Fatigue_generalizedboneache, Jaundice, Epigastricpain, WBC, RBC, HGB, Plat, AST1, ALT1, ALT4, ALT12, ALT24, ALT36,	ALT48,	ALTafter24w, RNABase, RNA4,	RNA12,	RNAEOT, RNAEF,	BaselinehistologicalGrading]

        user_input = [float(x) for x in user_input]

        hepatitis_prediction = hepatitis_model.predict([user_input])

        if hepatitis_prediction[0] == 1:
            hepatitis_diagnosis = "The person has high risk of having Hepatitis"
        else:
            hepatitis_diagnosis = "Congratulations..... The person does not have Hepatitis"

    st.success(hepatitis_diagnosis)
    
    csv_file_path = "Lung Cancer Data Collection.csv"
    data = pd.DataFrame(columns=["Age", "Gender","BMI",	"Fever", "Nausea/Vomting",	"Headache", "Diarrhea", 	"Fatigue & generalized bone ache", 	"Jaundice",
                                 "Epigastric pain", 	"WBC",	"RBC",	"HGB",	"Plat",	"AST 1",	"ALT 1",	"ALT4",	"ALT 12",	"ALT 24",	"ALT 36",	"ALT 48",
                                 "ALT after 24 w",	"RNA Base",	"RNA 4",	"RNA 12",	"RNA EOT",	"RNA EF",	"Baseline histological Grading",	"Baseline histological staging"])
    if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path)
    if submit_button:
        new_row = {"Age":Age, "Gender":Gender,"BMI":BMI,	"Fever":Fever, "Nausea/Vomting":NauseaVomting,	"Headache":Headache, "Diarrhea":Diarrhea, 	"Fatigue & generalized bone ache":Fatigue_generalizedboneache, 	"Jaundice":Jaundice,
                  "Epigastric pain":Epigastricpain, 	"WBC":WBC,	"RBC":RBC,	"HGB":HGB,	"Plat":Plat,	"AST 1":AST1,	"ALT 1":ALT1,	"ALT4":ALT4,	"ALT 12":ALT12,	"ALT 24":ALT24,	"ALT 36":ALT36,	"ALT 48":ALT48,
                  "ALT after 24 w":ALTafter24w,	"RNA Base":RNABase,	"RNA 4":RNA4,	"RNA 12":RNA12,	"RNA EOT":RNAEOT,	"RNA EF":RNAEF,	"Baseline histological Grading":BaselinehistologicalGrading,	"Baseline histological staging":hepatitis_prediction[0]}
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv(csv_file_path, index=False)
        #if st.button('Privacy Policy'):
        st.write("YOUR DATA HAS BEEN SAVED. YOUR DATA IS SAFE WITH US AND ONLY MIGHT BE USED FOR RESEARCH PURPOSE. WE ARE HIGHLY GREATFUL FOR YOUR AMAZING CONTRIBUTION TOWARDS MANKIND.")
        st.write("THANK YOU & STAY HEALTHY!!")
        
        

# Parkinson's Prediction Page
if selected == "Parkinson's Prediction":
    def add_bg_from_url():
        st.markdown(
             f"""
             <style>
             .stApp {{
                 background-image: url("https://miro.medium.com/v2/resize:fit:1400/0*_5ug7mUKThcPdMsZ");
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
             unsafe_allow_html=True
         )

    add_bg_from_url() 
    

    # page title
    st.title("Parkinson's Disease Prediction")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    # code for Prediction
    parkinsons_diagnosis = ''

    # creating a button for Prediction    
    submit_button = st.button("Parkinson's Test Result")
    if submit_button:

        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                      RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

        user_input = [float(x) for x in user_input]

        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            parkinsons_diagnosis = "The person has high risk of having Parkinson"
        else:
            parkinsons_diagnosis = "Congratulations..... The person does not have Parkinson"

    st.success(parkinsons_diagnosis)
    
    csv_file_path = "Parkinson Data Collection.csv"
    data = pd.DataFrame(columns=["name",	"MDVP:Fo(Hz)",	"MDVP:Fhi(Hz)",	"MDVP:Flo(Hz)",	"MDVP:Jitter(%)",	"MDVP:Jitter(Abs)",	"MDVP:RAP",	"MDVP:PPQ",	"Jitter:DDP","MDVP:Shimmer",	
                                 "MDVP:Shimmer(dB)",	"Shimmer:APQ3",	"Shimmer:APQ5",	"MDVP:APQ",	"Shimmer:DDA",	"NHR",	"HNR",	"status",	
                                 "RPDE",	"DFA",	"spread1",	"spread2",	"D2",	"PPE"])
    if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path)
    if submit_button:
        new_row = {"name":" ",	"MDVP:Fo(Hz)":fo,	"MDVP:Fhi(Hz)":fhi,	"MDVP:Flo(Hz)":flo,	"MDVP:Jitter(%)":Jitter_percent,	"MDVP:Jitter(Abs)":Jitter_Abs,	"MDVP:RAP":RAP,	"MDVP:PPQ":PPQ,	"Jitter:DDP":DDP,
                   "MDVP:Shimmer":Shimmer,	"MDVP:Shimmer(dB)":Shimmer_dB,	"Shimmer:APQ3":APQ3,	"Shimmer:APQ5":APQ5,	"MDVP:APQ":APQ,	"Shimmer:DDA":DDA,	"NHR":NHR,	"HNR":HNR,	"status":parkinsons_prediction[0],	"RPDE":RPDE,	
                   "DFA":DFA,	"spread1":spread1,	"spread2":spread2,	"D2":D2,	"PPE":PPE}
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv(csv_file_path, index=False)
        #if st.button('Privacy Policy'):
        st.write("YOUR DATA HAS BEEN SAVED. YOUR DATA IS SAFE WITH US AND ONLY MIGHT BE USED FOR RESEARCH PURPOSE. WE ARE HIGHLY GREATFUL FOR YOUR AMAZING CONTRIBUTION TOWARDS MANKIND.")
        st.write("THANK YOU & STAY HEALTHY!!")
        
        
        
        
        
        
        
        