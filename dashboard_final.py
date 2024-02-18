import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px
import seaborn as sns
from PIL import Image
#configuration d'images
st.set_page_config(
    page_title="Sleep health and life style dashbord",
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="expanded")
df=pd.read_csv(r"C:\Users\Dima D'origine\Downloads\Sleep_health_and_lifestyle_dataset.csv")
#preprocessing 
#changer les valeurs identiques
df['Occupation'] = df['Occupation'].replace('Software Engineer', 'Engineer')
df['Occupation'] = df['Occupation'].replace('Sales Representative', 'Salesperson')
df["BMI Category"] = df["BMI Category"].replace('Normal Weight','Normal')
#suppression des colonnes inutiles et des valeurs manquantes
colonnes_a_supprimer = ['Person ID','Blood Pressure']
df.drop(columns=colonnes_a_supprimer, inplace=True)
print(df)
#st.dataframe(df)
# Sidebar filtrage
with st.sidebar:
    st.title('Dashbord Sleep health and life style 🛌')
    st.image('https://singularityhub.com/wp-content/uploads/2019/02/learning-while-sleeping-neuroscience-shutterstock-686222875.png')
     ## categories
    cat_filter=st.sidebar.selectbox('select categorie',['Occupation','Gender','BMI Category'])
    ##filtrage par profession
    profession_list = list(df['Occupation'].unique())
    selected_profession = st.selectbox('select profession', profession_list)
    ###filtrage par sex"""
    selected_Gender = st.selectbox('select Gender',(df['Gender'].unique()))
    filtered_data = df[(df['Occupation'] == selected_profession) & (df['Gender'] == selected_Gender)]
###################title
st.title("Sleep health and life style Dashbord 📊")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

#Ouvrir l'image
st.image('https://assets.risescience.com/5e763da3d25345967394eea0/64486ee0812b4e51021a16af_what-color-light-is-best-for-sleep-n.jpg',width=600)
### les metrics
#row 1
max_sleep_duration = filtered_data['Sleep Duration'].max()
min_sleep_duration = filtered_data['Sleep Duration'].min()
avg_sleep_duration = round(filtered_data['Sleep Duration'].mean(),2)
total_Quality_of_Sleep=int(filtered_data["Quality of Sleep"].sum())
average=round(filtered_data["Quality of Sleep"].mean(),1)
star_rating= ":star:" * int(round(average, 0))
a1,a2,a3,a4=st.columns(4)
with a1 :
    a1.metric('Max sleep duration ', max_sleep_duration)
with a2 :
    a2.metric('Min sleep duration',min_sleep_duration)
with a3 :
    a3.metric('Average sleep duration', avg_sleep_duration)
with a4 :
    st.write("Quality of Sleep Rating:")
    st.subheader(f"{average} {star_rating}")
#row 2
a4,a5,a6=st.columns(3)
min_stress_level = filtered_data['Stress Level'].min()
a4.metric('Min stress level',min_stress_level)
max_stress_level = filtered_data['Stress Level'].max()
a5.metric('Max stress level',max_stress_level)
average_stress_level =round(filtered_data['Stress Level'].mean(),2) 
a6.metric('Average Stress level', average_stress_level)
#Création des graphes
# Filtrer les données en fonction de la catégorie sélectionnée
filtered_data = df[cat_filter]
# Obtenir le pourcentage de chaque catégorie
category_percentage = filtered_data.value_counts(normalize=True) * 100
# Créer le graphique interactif avec Plotly Express
fig = px.pie(names=category_percentage.index, 
             values=category_percentage.values,
             title=f'percentage of {cat_filter}')
# Afficher le graphique interactif
st.plotly_chart(fig)
fig=px.scatter(data_frame=df,x='Age',y='Sleep Duration',title='Age vs sleep duration',color=cat_filter)
st.plotly_chart(fig,use_container_width=True)


df['Sleep Disorder'].fillna('Normal', inplace=True)
sleep_disorder_counts=df['Sleep Disorder'].value_counts()
# Créer un graphique à anneaux avec Plotly Express
fig = px.pie(df, values="Sleep Duration", names="Sleep Disorder", hole=.5, title='Percentage of each class')
st.plotly_chart(fig)

col5,col6=st.columns(2)
with col5:
# Calculer la moyenne de 'Sleep Duration' par profession
    mean_sleep_duration_by_occupation = df.groupby('Occupation')['Sleep Duration'].mean().reset_index()
    mean_sleep_duration_by_occupation_sorted = mean_sleep_duration_by_occupation.sort_values(by='Sleep Duration',
                                                                                               ascending=True)

# Créer le graphique avec Plotly
    fig = px.bar(mean_sleep_duration_by_occupation_sorted, x='Sleep Duration', y='Occupation',
            title='Sleep Duration by Occupation',
            labels={'Sleep Duration': 'Sleep Duration in h', 'Occupation': 'Occupation'},
            width=400, height=400,color_discrete_sequence=["green"])
    st.plotly_chart(fig,use_container_width=True)
with col6:
# Créer le graphique avec Plotly Express
   fig = px.bar(df, x="Occupation", y="Stress Level", title="Stress Level by Occupation",
                 color_discrete_sequence=["#800080"], width=400 , height=400)

# Afficher le graphique avec Streamlit
st.plotly_chart(fig)
filtered_data = df[(df['Occupation'] == selected_profession) & (df['Gender'] == selected_Gender)]
st.markdown("---")
sleep_duration_by_BMI_category=(filtered_data.groupby(by=["BMI Category"])[["Sleep Duration"]].mean())
sleep_duration_by_BMI_category_barchart=px.bar(sleep_duration_by_BMI_category,
                                               x="Sleep Duration",
                                               y=sleep_duration_by_BMI_category.index,
                                               title="Sleep Duration by BMI Category",
                                               orientation="h",
                                               color_discrete_sequence=["#17f50c"],
                                               )
sleep_duration_by_BMI_category_barchart.update_layout(plot_bgcolor = "rgba(0,0,0,0)",
                                                      xaxis=(dict(showgrid=False)))
sleep_duration_by_BMI_category_piechart=px.pie(sleep_duration_by_BMI_category,
                                               names=sleep_duration_by_BMI_category.index,
                                                values="Sleep Duration",
                                                hole=.3,color=sleep_duration_by_BMI_category.index,
                                                color_discrete_sequence=px.colors.sequential.RdPu_r)
left_column,right_column=st.columns(2)
left_column.plotly_chart(sleep_duration_by_BMI_category_barchart,use_container_width=True)
right_column.plotly_chart(sleep_duration_by_BMI_category_piechart,use_container_width=True)
##heatmap
# Sélectionner les colonnes d'intérêt
col7,col8=st.columns(2)
with col7:
    data = df[['Sleep Duration', 'Quality of Sleep', 'Stress Level']]
    plt.figure(figsize=(7, 7))
    corr_matrix = data.corr()
    heatmap = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f",)
    plt.title('Correlation between Sleep Duration, Quality of Sleep and Stress Level')
    st.pyplot(heatmap.figure)
# Créer un graphique avec des boîtes à moustaches
# Créer un graphique avec des boîtes à moustaches avec Plotly
fig = px.box(df, x='BMI Category', y='Physical Activity Level', labels={'BMI Category', 
                                                                        'Physical Activity Level'},
                                                                        title='Physical Activity Level by BMI category')
fig.update_layout(xaxis=dict(tickangle=30))
st.plotly_chart(fig)
#pour eliminer le style de streamlit (le menu en haut ,l'encadremant,le pied)
hide_st_style = """
            <style>
            #MainMenu{lisibility:hidden;}
            footer {visibility:hidden;}
            header {visibility:hidden;}
            <style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)


#Configuration du backGround
"""[theme]
backgroundColor="#E6E6FA"
secondaryBackgroundColor="#FFC0CB"
textColor="#000000"
primaryColor="#800000"
accentColor="#FFD700""""