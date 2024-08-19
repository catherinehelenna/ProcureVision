import streamlit as st
import joblib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta,date
from bs4 import BeautifulSoup
import requests

def run():
    # Load the models
    banten_model = joblib.load('deployment/banten.joblib')
    jakarta_model = joblib.load('deployment/jakarta.joblib')
    jawa_barat_model = joblib.load('deployment/jawa_barat.joblib')
    jawa_tengah_model = joblib.load('deployment/jawa_tengah.joblib')
    jawa_timur_model = joblib.load('deployment/jawa_timur.joblib')
    yogyakarta_model = joblib.load('deployment/yogyakarta.joblib')

    # Load the datasets
    jakarta_df = pd.read_csv('deployment/jakarta_premium.csv')
    banten_df = pd.read_csv('deployment/banten_premium.csv')
    jawa_barat_df = pd.read_csv('deployment/jawa_barat_premium.csv')
    jawa_tengah_df = pd.read_csv('deployment/jawa_tengah_premium.csv')
    jawa_timur_df = pd.read_csv('deployment/jawa_timur_premium.csv')
    yogyakarta_df = pd.read_csv('deployment/yogyakarta_premium.csv')

    # create forecasting function
    def forecasting_function(province, month, best_estimator, window):
        province_forecast = province.copy()
        province_forecast['Tanggal'] = pd.to_datetime(province_forecast['Tanggal'], format="%Y-%m-%d")
        province_forecast = province_forecast.set_index('Tanggal')['Harga']
        window = window

        for i in range(month):
            X = province_forecast[-window:].values.reshape(1, -1)
            # Predict the next value using the best estimator and round it
            next_value = round(best_estimator.predict(X)[0])
            # Extract the last date and add one month to it
            last_date = province_forecast.index[-1]
            new_date = last_date + timedelta(days=1)  # Add one month (approximation)
            # Append the predicted value to the forecast series with the new date index
            province_forecast.loc[new_date] = next_value

        return province_forecast

    # create news function
    def news(province):
        st.header("Headline News")
        if selected_province == 'Jakarta':
            url = "https://www.google.com/search?client=opera-gx&hs=hof&sca_esv=7928bf8df49ca757&sxsrf=ACQVn0-hmGbRHQ8sWmLPqJO77JJoK308yA:1709749915710&q=beras+premium+jakarta&tbm=nws&source=lnms&sa=X&ved=2ahUKEwjGtoXjouCEAxWHzjgGHSzKDNYQ0pQJegQIDBAB&biw=1399&bih=759&dpr=1"
        elif selected_province == 'Banten':
            url = "https://www.google.com/search?q=beras+premium+banten&client=opera-gx&hs=2T0&sca_esv=7928bf8df49ca757&biw=1399&bih=759&tbm=nws&sxsrf=ACQVn09c-Mf4WiX0Ca8dz5fK7e7TtKJe9Q%3A1709749917458&ei=nbboZZrIG4eY4-EPgJm2OA&ved=0ahUKEwjaivDjouCEAxUHzDgGHYCMDQcQ4dUDCA0&uact=5&oq=beras+premium+banten&gs_lp=Egxnd3Mtd2l6LW5ld3MiFGJlcmFzIHByZW1pdW0gYmFudGVuMgUQIRigATIFECEYnwVI8AtQowRYoQpwAHgAkAEAmAF_oAGSBaoBAzguMbgBA8gBAPgBAZgCCaACwgXCAgYQABgWGB7CAggQABiABBiABMICCBAAGBYYHhgPmAMAiAYBkgcDNy4yoAfpKQ&sclient=gws-wiz-news"
        elif selected_province == 'Jawa Barat':
            url = "https://www.google.com/search?q=beras+premium+jawa+barat&client=opera-gx&hs=YU0&sca_esv=7928bf8df49ca757&biw=1399&bih=759&tbm=nws&sxsrf=ACQVn0-M6Bb4neYvLlIW-GBRJgtdQs3YoA%3A1709749949621&ei=vbboZdDCJa-u4-EPhY2AqAQ&ved=0ahUKEwiQlZvzouCEAxUv1zgGHYUGAEUQ4dUDCA0&uact=5&oq=beras+premium+jawa+barat&gs_lp=Egxnd3Mtd2l6LW5ld3MiGGJlcmFzIHByZW1pdW0gamF3YSBiYXJhdDIFECEYoAEyBRAhGJ8FSMkLUK0EWKsKcAB4AJABAJgBXaAB5gWqAQIxMbgBA8gBAPgBAZgCC6ACnQbCAggQABiABBiABMICBhAAGBYYHsICCBAAGBYYHhgPwgIKEAAYgAQYgAQYDcICCBAAGAgYHhgNwgIHECEYChigAZgDAIgGAZIHBDEwLjGgB_8t&sclient=gws-wiz-news"
        elif selected_province == 'Jawa Tengah':
            url = "https://www.google.com/search?q=beras+premium+jawa+tengah&client=opera-gx&hs=oU0&sca_esv=7928bf8df49ca757&biw=1399&bih=759&tbm=nws&sxsrf=ACQVn0_64MuQT7TR4OYfE6ORvlCpHNmOJQ%3A1709749965703&ei=zbboZbO-KpbG4-EP4O2DkAE&ved=0ahUKEwjz2PD6ouCEAxUW4zgGHeD2ABIQ4dUDCA0&uact=5&oq=beras+premium+jawa+tengah&gs_lp=Egxnd3Mtd2l6LW5ld3MiGWJlcmFzIHByZW1pdW0gamF3YSB0ZW5nYWgyBRAhGJ8FSKoaULwTWLoYcAF4AJABAJgBWqABtASqAQE4uAEDyAEA-AEBmAIIoAKXBMICBRAhGKABwgIGEAAYFhgewgIIEAAYFhgeGA_CAgcQIRgKGKABmAMAiAYBkgcDNy4xoAeYEg&sclient=gws-wiz-news"
        elif selected_province == 'Jawa Timur':
            url = "https://www.google.com/search?q=beras+premium+jawa+timur&client=opera-gx&hs=WAL&sca_esv=7928bf8df49ca757&biw=1399&bih=759&tbm=nws&sxsrf=ACQVn0_lca0xAB3Arco6519Lu2aaVOmJig%3A1709749985903&ei=4bboZZHgNqCe4-EP3ICEkAo&ved=0ahUKEwjR1MGEo-CEAxUgzzgGHVwAAaIQ4dUDCA0&uact=5&oq=beras+premium+jawa+timur&gs_lp=Egxnd3Mtd2l6LW5ld3MiGGJlcmFzIHByZW1pdW0gamF3YSB0aW11cjIFECEYoAEyBRAhGJ8FSIEJUIQCWOcHcAB4AJABAJgBXKAB1QOqAQE3uAEDyAEA-AEBmAIHoAL3A8ICBhAAGBYYHsICCBAAGBYYHhgPwgIEECEYFcICBxAhGAoYoAGYAwCIBgGSBwE3oAe1Fw&sclient=gws-wiz-news"
        elif selected_province == 'Yogyakarta':
            url = "https://www.google.com/search?q=beras+premium+jogja&client=opera-gx&hs=NV0&sca_esv=7928bf8df49ca757&biw=1399&bih=759&tbm=nws&sxsrf=ACQVn08eCU2cyVDBXnjEaCThU9C-i48zkw%3A1709750000319&ei=8LboZfyTE-Th4-EPzcyYiA4&ved=0ahUKEwj8y7GLo-CEAxXk8DgGHU0mBuEQ4dUDCA0&uact=5&oq=beras+premium+jogja&gs_lp=Egxnd3Mtd2l6LW5ld3MiE2JlcmFzIHByZW1pdW0gam9namEyCBAAGIAEGIAESN0fUABY0R5wBHgAkAEAmAFwoAHaBKoBAzguMbgBA8gBAPgBAZgCDaACngXCAgYQABgWGB7CAggQABgWGB4YD8ICBRAhGKABwgIFECEYnwXCAgoQABiABBiABBgNmAMAkgcEMTIuMaAHvh4&sclient=gws-wiz-news"

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")

        # Extract headlines from the parsed HTML content
        headlines = [headline.text for headline in soup.find_all('h3')]
        
        # Display headlines
        for i, headline in enumerate(headlines, start=1):
            st.write(f"{i}. {headline}")

    #--------------------------------------------------------------------------------------------------------------------
    
    st.title("Final Project Model Deployment")
    page = st.selectbox(label='Choose Option', options=['Predict', 'News'])

    if page == "Predict":
        with st.form("Input the province and length of prediction"):
            province_list = ('Jakarta', 'Banten', 'Jawa Barat', 'Jawa Tengah','Jawa Timur', 'Yogyakarta')
            selected_province = st.selectbox('Supported Province', province_list)
            n_month = st.slider('Days of prediction since 2023-03-01:', 1, 30)

            if selected_province == 'Jakarta':
                n_model = jakarta_model
                province = jakarta_df
                n_window = 3
            elif selected_province == 'Banten':
                n_model = banten_model
                province = banten_df
                n_window = 3
            elif selected_province == 'Jawa Barat':
                n_model = jawa_barat_model
                province = jawa_barat_df
                n_window = 3
            elif selected_province == 'Jawa Tengah':
                n_model = jawa_tengah_model
                province = jawa_tengah_df
                n_window = 2
            elif selected_province == 'Jawa Timur':
                n_model = jawa_timur_model
                province = jawa_timur_df
                n_window = 3
            elif selected_province == 'Yogyakarta':
                n_model = yogyakarta_model
                province = yogyakarta_df
                n_window = 3

            sub = st.form_submit_button('Predict')
            if sub:
                province_forecast_poly = forecasting_function(province, n_month,n_model,n_window)
                fig, ax = plt.subplots(figsize=(20, 5))
                province_forecast_poly.plot(color='blue', label='Forecast', ax=ax)
                province['Tanggal'] = pd.to_datetime(province['Tanggal'], format="%Y-%m-%d")
                province = province.set_index('Tanggal')['Harga'] 
                province.plot(color='red', label='Actual', ax=ax)
                plt.legend()

                # Display the plot in Streamlit
                st.header("Forecast Plot")
                st.pyplot(fig)
                # Display the last 7 values
                st.header("Price of the Predicted Week")
                st.write(province_forecast_poly.tail(7))
                # Display the budget
                st.header("Weekly Budget Reccomendation")
                MAE = 115
                st.write(f"Weekly budget range for beras premium: Rp {province_forecast_poly.tail(7)[1].min() - MAE}-{province_forecast_poly.tail(7)[1].max() + MAE}")

    elif page == "News":
        province_list = ('Jakarta', 'Banten', 'Jawa Barat', 'Jawa Tengah','Jawa Timur', 'Yogyakarta')
        selected_province = st.selectbox('Supported Province', province_list)
        news(selected_province)

if __name__ == "__main__":
    run()