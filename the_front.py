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

trans = {
        "AMT_CREDIT":"montant_du_credit",
        "AMT_ANNUITY":"Rente de prêt",
        "AMT_GOODS_PRICE":"prix du bien",
        "REGION_POPULATION_RELATIVE":"niveau popularisation region_du_client",
        "DAYS_BIRTH":"âge du client en jour * -1",
        "DAYS_REGISTRATION":"nombre jour entre demande et dernière modification dossier *-1",
        "DAYS_ID_PUBLISH":"nombre jour entre demande et dernière modification piece identité *-1",
        "EXT_SOURCE_1":"valeur source externe 1",
        "EXT_SOURCE_2":"valeur source externe 2",
        "EXT_SOURCE_3":"valeur source externe 3",
        "LIVINGAREA_AVG":"estimation moyenne habitation client",
        "DAYS_LAST_PHONE_CHANGE":"nombre jours depuis dernier changement du téléphone * -1",
        "INCOME_CREDIT_PERC":"pourcentage crédit par rapport aux revenus",
        "INCOME_PER_PERSON":"revenu par personne du foyer",
        "ANNUITY_INCOME_PERC":"pourcentage crédit sur revenus annuels",
        "PAYMENT_RATE":"taux de paiement",
        "DAYS_EMPLOYED_PERC":"ratio entre durée emploi actuel et âge client *-1",
        "APPS_EXT_SOURCE_MEAN":"moyenne des valeurs source externes",
        "APPS_EXT_SOURCE_STD":"ecart type des valeurs sources externes",
        "APP_EXT_SOURCE_2*EXT_SOURCE_3*DAYS_BIRTH":"SOURCE extern 2*SOURCE externe 3*age_en_jour *-1",
        "CREDIT_TO_GOODS_RATIO":"ratio entre valeur credit et valeur biens client",
        "INCOME_TO_EMPLOYED_RATIO":"ratio entre durée emploi actuel et revenus",
        "INCOME_TO_BIRTH_RATIO":"ratio entre revenus et âge client",
        "ID_TO_BIRTH_RATIO":"ratio âge pièce identité et âge client",
        "CAR_TO_BIRTH_RATIO":"ratio entre âge voiture et âge client *-1"
    }


def human_translation(val):

    return trans[val]


granted_pop_clients = pd.read_csv('granted_pop_clients.csv')
granted_pop_clients.rename(columns=trans, inplace=True)
granted_pop_clients.loc['mean'] = granted_pop_clients.mean()
nb_var = [trans[i] if i in trans.keys() else i for i in most_imp]
refused_pop =  pd.read_csv('refused_pop.csv')[most_imp]
granted_pop =  pd.read_csv('granted_pop.csv')[most_imp]


case = pd.Series(dict(zip(most_imp,placebo[0])))
print("case   :", case)
st.write(f'''
 # OC credit 
 ''')
if 'temp_cli' not in st.session_state:
    st.session_state['temp_cli'] = 'f1f775dc-283a-4960-a40d-977d1b6237f7'

if 'hand_temp_cli' not in st.session_state:
    st.session_state['hand_temp_cli'] = ''

last_clients = ['f1f775dc-283a-4960-a40d-977d1b6237f7','c72522e1-00af-4903-824a-027a2e9fbfda','bd2b7917-a04f-4f81-a5fa-405306c9663d','26107121-8da6-454f-953e-dbad0f309dbf','f426a68f-c66a-4202-bdc7-ec6d93a9afd5']

st.write(f'''## Consultez les fiches de vos derniers clients:''')
for el in last_clients:
    el = st.button(f"{el}", key=el)


placeholder = st.empty()
st.session_state['hand_temp_cli'] = st.text_input('Vous pouvez aussi entrer un id client manuellement :')
st.write(" exemple de client: '935f0753-920d-4977-b021-17d00a140'  - ou  - '6cc62c73-dae7-43c7-84fe-c5437'")
if st.session_state['hand_temp_cli'] != "":
    st.session_state['temp_cli'] = st.session_state['hand_temp_cli']



for el in last_clients:
    if st.session_state.get(el):
        st.session_state['hand_temp_cli'] = el
        st.session_state['temp_cli'] = el


st.write(f"Vous consultez le client n° {st.session_state.temp_cli}")


the_disp = pd.concat([granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']],
                      granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[
    nb_var]  # Ajout de la ligne moyenne au dataframe
#Columns traduction

luc = st.bar_chart(the_disp[nb_var].T,x=nb_var)
st.write('Filtrer le nombre de variables:')
a,b,c,d = st.columns(4)
if a.button('25'):
    st.session_state['hand_temp_cli'] = el
    st.write(st.session_state['temp_cli'])
    nb_var = [trans[i] if i in trans.keys() else i for i in most_imp]
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1, granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    luc.bar_chart(the_disp[nb_var].T, x=nb_var)

if b.button('12'):
    st.session_state['hand_temp_cli'] = el
    st.write(st.session_state['temp_cli'])
    nb_var = [trans[i] if i in trans.keys() else i for i in sel_twelve]
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1,granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    luc.bar_chart(the_disp[nb_var].T, x=nb_var)

if c.button('6'):
    st.session_state['hand_temp_cli'] = el
    st.write(st.session_state['temp_cli'])
    nb_var = [trans[i] if i in trans.keys() else i for i in sel_six]
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1, granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    luc.bar_chart(the_disp[nb_var].T, x=nb_var)

if d.button('3'):
    st.session_state['temp_cli'] = el
    st.session_state['hand_temp_cli'] = st.session_state['temp_cli']
    st.write(st.session_state['temp_cli'])
    nb_var = [trans[i] if i in trans.keys() else i for i in sel_three]
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1, granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    luc.bar_chart(the_disp[nb_var].T, x=nb_var)

st.write(f'''Entrez l'id souhaité''')

st.write(f'''
 ## pour un accès équitable au prêt bancaire
 Remplissez le formulaire ci-dessous pour évaluer votre de capacité de remboursement
 ''')



actual = {}
col1, col2 = st.columns(2)

for i in most_imp:
    if str(i) != str('DAYS_BIRTH'):
        if most_imp.index(i) % 2 == 0:
            actual[f"{i}"] = col1.number_input(
                f"Entrez {human_translation(i)}")  # traduction temporaire des valeurs brutes
        else:
            actual[f"{i}"] = col2.number_input(
                f"Entrez {human_translation(i)}")  # traduction temporaire des valeurs brutes

age = st.slider('Âge du demandeur', 0, 110, 29)
actual['DAYS_BIRTH'] = age * 365 * (-1)
nc_df = pd.Series(actual)
st.write("Vous indiquz que le demandeur est âgé de ", age, 'ans')


if st.button("Évaluer"):
    good_order = {}
    for io in most_imp:
        good_order[io] = actual[io] #making sure of the good order
    newclient = {"vector": list(good_order.values())}
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
    st.title('''En orange(classe: 1) Les variables influençant le refus du prêt''')
    st.title('''En bleu(classe: 0) Les variables influençant la délivrance du prêt''')
    good_order = {}
    for io in most_imp:
        good_order[io] = actual[io]
    newclient = {"newclient":good_order}#make sure order is not disturbed
    limedisplay = requests.post(
        "https://loan.cleverapps.io/lime", json=newclient
    )
    components.html(limedisplay.text,height=800)











