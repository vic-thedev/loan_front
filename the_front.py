import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
st. set_page_config(layout="wide")
backend_url = "https://loan.cleverapps.io/"

placebo = pd.read_csv('default_value777.csv')
placebo = np.array(placebo).reshape(1,-1)
population =  pd.read_csv('population_description.csv')
refused_pop =  pd.read_csv('refused_pop.csv')
granted_pop =  pd.read_csv('granted_pop.csv')
granted_pop_clients = pd.read_csv('granted_pop_clients.csv')
granted_pop_clients.loc['mean'] = granted_pop_clients.mean()

print("App is in test")
sample_request_input = {"vector": placebo.tolist()}
resp = requests.get(
    "https://loan.cleverapps.io/", json=sample_request_input
)

print(resp.json())


most_imp = ['AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE',
       'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_REGISTRATION',
       'DAYS_ID_PUBLISH', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3',
       'LIVINGAREA_AVG', 'DAYS_LAST_PHONE_CHANGE', 'INCOME_CREDIT_PERC',
       'INCOME_PER_PERSON', 'ANNUITY_INCOME_PERC', 'PAYMENT_RATE',
       'DAYS_EMPLOYED_PERC', 'APPS_EXT_SOURCE_MEAN', 'APPS_EXT_SOURCE_STD',
       'APP_EXT_SOURCE_2*EXT_SOURCE_3*DAYS_BIRTH', 'CREDIT_TO_GOODS_RATIO',
       'INCOME_TO_EMPLOYED_RATIO', 'INCOME_TO_BIRTH_RATIO',
       'ID_TO_BIRTH_RATIO', 'CAR_TO_BIRTH_RATIO']

sel_three =['PAYMENT_RATE', 'APPS_EXT_SOURCE_MEAN', 'INCOME_TO_BIRTH_RATIO']

sel_six = ['AMT_ANNUITY', 'EXT_SOURCE_3', 'PAYMENT_RATE', 'APPS_EXT_SOURCE_MEAN','INCOME_TO_EMPLOYED_RATIO', 'INCOME_TO_BIRTH_RATIO']

sel_twelve = ['AMT_ANNUITY', 'AMT_GOODS_PRICE', 'DAYS_REGISTRATION',
       'DAYS_ID_PUBLISH', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3',
       'ANNUITY_INCOME_PERC', 'PAYMENT_RATE', 'APPS_EXT_SOURCE_MEAN',
       'INCOME_TO_EMPLOYED_RATIO', 'INCOME_TO_BIRTH_RATIO']
nb_var = most_imp
refused_pop =  pd.read_csv('refused_pop.csv')[most_imp]
granted_pop =  pd.read_csv('granted_pop.csv')[most_imp]

case = pd.Series(dict(zip(most_imp,placebo[0])))
print("case   :", case)
st.write(f'''
 # OC credit 
 ''')
if 'temp_cli' not in st.session_state:
    st.session_state['temp_cli'] = 'f1f775dc-283a-4960-a40d-977d1b6237f7'

last_clients = ['f1f775dc-283a-4960-a40d-977d1b6237f7','c72522e1-00af-4903-824a-027a2e9fbfda','bd2b7917-a04f-4f81-a5fa-405306c9663d','26107121-8da6-454f-953e-dbad0f309dbf','f426a68f-c66a-4202-bdc7-ec6d93a9afd5']

st.write(f'''## Consultez les fiches de vos derniers clients:''')

for el in last_clients:
    el = st.button(f"{el}", key=el)

for el in last_clients:
    if st.session_state.get(el):
        st.session_state['temp_cli'] = el
        st.session_state.temp_cli



the_disp = pd.concat([granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']],
                      granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[
    nb_var]  # Ajout de la ligne moyenne au dataframe
luc = st.bar_chart(the_disp[nb_var].T,x=nb_var)
st.write('Modifier le nombre de variables:')
a,b,c,d = st.columns(4)
if a.button('25'):
    st.write(st.session_state['temp_cli'])
    nb_var = most_imp
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1, granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    luc.area_chart(the_disp[nb_var].T, x=nb_var)

if b.button('12'):
    st.write(st.session_state['temp_cli'])
    nb_var = sel_twelve
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1,granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    luc.area_chart(the_disp[nb_var].T, x=nb_var)

if c.button('6'):
    st.write(st.session_state['temp_cli'])
    nb_var = sel_six
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1, granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    luc.area_chart(the_disp[nb_var].T, x=nb_var)

if d.button('3'):
    st.write(st.session_state['temp_cli'])
    nb_var = sel_three
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1, granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    luc.area_chart(the_disp[nb_var].T, x=nb_var)

st.write(f'''Entrez l'id souhaité''')

st.write(f'''
 ## pour un accès équitable au prêt bancaire
 Remplissez le formulaire ci-dessous pour évaluer votre de capacité de remboursement
 ''')


age = st.slider('Âge du demandeur', 0, 110, 29)

actual = {}
col1, col2 = st.columns(2)
for i in most_imp:
    if most_imp.index(i) %2 == 0:
        actual[f"{i}"] = col1.number_input(f"Entrez {i}")
    else:
        actual[f"{i}"] = col2.number_input(f"Entrez {i}")



actual['DAYS_BIRTH'] = age * 365 * (-1)

nc_df = pd.Series(actual)
st.write("Vous avez indiqué que le demandeur est âgé de ", age, 'ans')


if st.button("Évaluer"):
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
    pd.Series(actual)
    newclient = {"newclient":actual}
    limedisplay = requests.post(
        "https://loan.cleverapps.io/lime", json=newclient
    )
    components.html(limedisplay.text,height=800)











