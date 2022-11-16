import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
import plost
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
    st.session_state['temp_cli'] = 'f08dc1a2-a753-4b62-b52d-5d63fe5db282'
    st.session_state['ps'] = [38.15]
if 'hand_temp_cli' not in st.session_state:
    st.session_state['hand_temp_cli'] = ''

last_clients = ['b4d44a58-045b-4dd9-9bda-7a7b6e29533d','86c2e78d-e68f-4d83-960b-b3a95f145b48','2380d868-5f66-490b-a4e9-9cf66f9a6c2b','55087e48-249b-4a82-a695-1963e98342e6','f08dc1a2-a753-4b62-b52d-5d63fe5db282']

st.write(f'''## Consultez les fiches de vos derniers clients:''')
for el in last_clients:
    el = st.button(f"{el}", key=el)


placeholder = st.empty()
st.session_state['hand_temp_cli'] = st.text_input('Vous pouvez aussi entrer un id client manuellement :')
st.write(" exemple de client: 'a2f9d59f-fd28-472f-95a2-e89a926bd73f'  - ou  - 'a1c761bf-e5e9-440f-9de5-049e2d95ef5e'")
if st.session_state['hand_temp_cli'] != "":
    st.session_state['temp_cli'] = st.session_state['hand_temp_cli']
    st.session_state['ps'] = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]['prediction_score'].values *100


for el in last_clients:
    if st.session_state.get(el):
        st.session_state['hand_temp_cli'] = el
        st.session_state['temp_cli'] = el
        st.session_state['ps'] = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]['prediction_score'].values * 100

st.markdown(f'''## Prénom et nom du client : {granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]['names'].values}''')
st.write(f"Identifiant unique : {st.session_state.temp_cli}")


def score_color(score_number):
    if score_number >= 50:
        return 'red'
    elif score_number >=35 and score_number <50:
        return 'orange'
    elif score_number <35:
        return 'green'


st.markdown(f"<h1 style='color:{score_color(st.session_state['ps'][0])}'>{st.session_state['ps'][0]}</h1>.",unsafe_allow_html=True)
the_disp = pd.concat([granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']],
                      granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[
    nb_var]  # Ajout de la ligne moyenne au dataframe


grouped = the_disp[[trans[o] for o in sel_three]].T
grouped['features'] = grouped.index
grouped.rename(columns={grouped.columns[0]:'Le client'}, inplace=True)

plost.bar_chart(data=grouped,bar='features', height=400, width=300,value=[grouped.columns[0],'mean'],group=True)

stacked = the_disp[nb_var].T
stacked.rename(columns={stacked.columns[0]:"Le client"}, inplace=True)
luc = st.bar_chart(stacked,x=nb_var)
st.write('Filtrer le nombre de variables:')
a,b,c,d = st.columns(4)
if a.button('25'):
    st.session_state['hand_temp_cli'] = el
    st.write(st.session_state['temp_cli'])
    nb_var = [trans[i] if i in trans.keys() else i for i in most_imp]
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1, granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    stacked = the_disp[nb_var].T
    stacked.rename(columns={stacked.columns[0]: "Le client"}, inplace=True)
    luc.bar_chart(stacked, x=nb_var)

if b.button('12'):
    st.session_state['hand_temp_cli'] = el
    st.write(st.session_state['temp_cli'])
    nb_var = [trans[i] if i in trans.keys() else i for i in sel_twelve]
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1,granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    stacked = the_disp[nb_var].T
    stacked.rename(columns={stacked.columns[0]: "Le client"}, inplace=True)
    luc.bar_chart(stacked, x=nb_var)

if c.button('6'):
    st.session_state['hand_temp_cli'] = el
    st.write(st.session_state['temp_cli'])
    nb_var = [trans[i] if i in trans.keys() else i for i in sel_six]
    s1 = granted_pop_clients.loc[granted_pop_clients['uuid'] == st.session_state['temp_cli']]
    the_disp = pd.concat([s1, granted_pop_clients.loc[granted_pop_clients.index == 'mean']], axis=0)[nb_var]
    stacked = the_disp[nb_var].T
    stacked.rename(columns={stacked.columns[0]: "Le client"}, inplace=True)
    luc.bar_chart(stacked, x=nb_var)



st.write('''
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
st.write("Vous indiqué que le demandeur est âgé de ", age, 'ans')


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
    refused_pop.rename({1:'Mean', 3:"Min", 8:'Demandeur'}, axis=0, inplace=True)
    granted_pop.loc[8] = actual
    granted_pop.rename({1:'Mean', 3:"Min", 8:'Demandeur'}, axis=0, inplace=True)
    st.title('Comparaison aux demandes de prêt refusées')
    st.line_chart(refused_pop.T[['Mean', 'Min', 'Demandeur']])
    st.title("comparaison au demandes de prêt accordées")
    st.line_chart(granted_pop.T[['Mean', 'Min', 'Demandeur']])





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











