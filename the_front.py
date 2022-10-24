import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure
st. set_page_config(layout="wide")
backend_url = "https://loan.cleverapps.io/"

placebo = pd.read_csv('default_value_ultimate.csv')
placebo = np.array(placebo).reshape(1,-1)
population =  pd.read_csv('population_description.csv')
refused_pop =  pd.read_csv('refused_pop.csv')
granted_pop =  pd.read_csv('granted_pop.csv')

print("App is in test")
sample_request_input = {"vector": placebo.tolist()}
resp = requests.get(
    "https://loan.cleverapps.io/loan", json=sample_request_input
)

print(resp.json())
#st.write(resp.json())

most_imp = ['APPS_EXT_SOURCE_MEAN',
'CREDIT_TO_GOODS_RATIO',
'INCOME_TO_EMPLOYED_RATIO',
'PAYMENT_RATE',
'NAME_EDUCATION_TYPE',
'CODE_GENDER',
'EXT_SOURCE_3',
'EXT_SOURCE_2',
'APPS_EXT_SOURCE_STD',
'AMT_CREDIT',
'AMT_ANNUITY',
'APP_EXT_SOURCE_2*EXT_SOURCE_3*DAYS_BIRTH',
'FLAG_DOCUMENT_3',
'DAYS_EMPLOYED',
'DAYS_ID_PUBLISH',
'DAYS_LAST_PHONE_CHANGE',
'INCOME_TO_BIRTH_RATIO',
'CAR_TO_EMPLOYED_RATIO',
'ANNUITY_INCOME_PERC',
'DAYS_BIRTH']


case = pd.Series(dict(zip(most_imp,placebo[0])))

st.write(f'''
 # OC credit 
 ## pour un accès équitable au prêt bancaire
 Remplissez le formulaire ci-dessous pour évaluer votre de capacité de remboursement
 ''')
age = st.slider('Âge du demandeur', 0, 110, 29)

actual = {}
for i in most_imp:
    actual[f"{i}"] = st.number_input(f"Entrez {i}")

actual['DAYS_BIRTH'] = age*365*(-1)

nc_df = pd.Series(actual)
nc_df
st.write("Vous avez indiqué que le demandeur est âgé de ", age, 'ans')

if st.button("Évaluer"):
    '''nc_df = pd.DataFrame(actual)
    nc_df'''
    newclient = {"vector": list(nc_df.values)}

    evaluation = requests.get(
        "https://loan.cleverapps.io/loan", json=newclient
    )
    st.write(evaluation.json())
    actual_s = pd.Series(actual)
    refused_pop.loc[8] = actual
    refused_pop.rename({1:'Mean', 3:"Min", 7:'Max', 8:'Demandeur'}, axis=0, inplace=True)
    granted_pop.loc[8] = actual
    granted_pop.rename({1:'Mean', 3:"Min", 7:'Max', 8:'Demandeur'}, axis=0, inplace=True)
    st.title('Comparaison aux demandes de prêt refusées')
    st.line_chart(refused_pop.T[['Mean', 'Min', 'Max', 'Demandeur']])
    st.title("comparaison au demandes de prêt accordées")
    st.line_chart(granted_pop.T[['Mean', 'Min', 'Max', 'Demandeur']])

####Lime explication
if st.button("Expliquer"):
    print(pd.Series(actual))
    newclient = {"newclient":actual}
    limedisplay = requests.post(
        "https://loan.cleverapps.io/lime", json=newclient
    )
    components.html(limedisplay.text,height=800)











