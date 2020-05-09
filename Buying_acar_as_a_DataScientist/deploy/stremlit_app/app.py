import pandas as pd
import streamlit as st
from utils import *
import altair as alt
import matplotlib.pyplot as plt
import webbrowser



def main():
    st.image("images/logo.png")
    st.write("# Car Recommendation System Dashboard")
    options = ['Project Motivation', 'Dashboard','Contact me']
    choice = st.sidebar.selectbox("Options", options)

    if choice =='Project Motivation':
        st.sidebar.info("The Project")
        st.markdown(proj_mot)
        st.subheader('Application Diagram')
        st.image("images/Diagram.png")

    elif choice == 'Dashboard':
        st.sidebar.info("Dashboard")
        st.subheader('Cars information')
        st.info(" This dashboard shows information regarding the cars with the highest scores")
        data = load_data()

        if st.checkbox('Show Data'):
            st.dataframe(data.head())
            if st.checkbox('Show Shape'):
                st.write(data.shape)
            if st.checkbox('Show Columns'):
                columns = data.columns.to_list()
                st.write(columns)
            if st.checkbox('Show Data Information'):
                #st.write(data[cols].sum())
                #st.write(data['model'].value_counts())
                #st.write(data['mileage'].describe().T)
                data_info(data)

            if st.checkbox('Show Car Classes'):
                st.write(data['brand'].value_counts())

        st.header('Scatter plot')
        st.subheader('Brand - Price')
        scatter = scater_price_mileage(data)
        scatter


        st.header('Bar Charts')
        st.subheader('Model - Mean Price')
        mean_price_chart = mean_price(data)
        mean_price_chart

        st.subheader('Model - Motor power')
        model_power_price_ = model_power_price(data)
        model_power_price_


        st.subheader('Model - Regdate')
        chart1 = model_regdate_count(data)
        chart1
        st.subheader('Financial Status - Regdate')
        chart2 = financial_regdate(data)
        chart2
        st.subheader('Model - Motor power')
        chart3 = model_power_count(data)
        chart3
        st.subheader('Model - Motor power')
        model_power_price_ = model_power_price(data)
        model_power_price_





    elif choice == 'Contact me':
        st.sidebar.info("Jonathan Cabreira")
        url1 = 'https://www.linkedin.com/in/jonathan-cabreira-4635aa103/'
        url2 = 'https://medium.com/@cabreirajm'
        url3 = 'https://github.com/jmcabreira'
        if st.sidebar.button('Linkedin'):
            webbrowser.open_new_tab(url1)
        if st.sidebar.button('Medium'):
            webbrowser.open_new_tab(url2)
        if st.sidebar.button('GitHub'):
            webbrowser.open_new_tab(url3)

        st.sidebar.image("images/pic.png", width =  300)
        st.subheader('About me:')
        st.markdown(about_me)



proj_mot = """ After a year living on the Emerald Isle – Ireland – it is time to move back to Brazil.

It is very difficult to live in Rio de Janeiro, Brazil without a car and I am now in the market to buy a new one. As you probably know, I am a data-driven person, and based on that I decided to approach this problem as a good Data Scientist.

I built a car recommendation system. The web app searches for cars on a webpage processes the data and passes it through a machine learning model in order to list and display cars that are more related to what I am looking for."""

about_me = """ I am an electrical engineer turned data scientist who loves leveraging data-driven solutions that make an impact on business and society. My first encounter with data science occurred when I worked as a research analyst at the Applied Computational Intelligence Laboratory (Fluminense Federal University) in which I built Artificial Neural Network models for power forecast.

Thereafter, I won a scholarship that allowed me to study at the University of Toronto in Canada. After this experience, I was given the opportunity to work with electrical projects and project management in a small company in Rio de Janeiro, Brazil. My third working contract involved tasks related to the project management of two electrical substation construction projects in a multinational company.

Right now, I’m currently trying to buy a car ( as a data scientist :) ). In other words, I am working on a personal project which includes web scraping, data analysis, machine learning, and web application (link below).

App: https://car-recommender-jmcabreira.herokuapp.com/

Skills: Python, SQL, Pandas, scikit-learn, Machine Learning """



if __name__ == '__main__':
    main()
