import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    # Load the data
    df_final2 = pd.read_csv('eda2.csv')
    df_final1 = pd.read_csv('eda1.csv')
    # get data only for provinces in Java Island
    java_island_provinces = ['DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'D.I Yogyakarta', 'Jawa Timur', 'Banten']

    # Filter dataset for the specified provinces
    provinces_data = df_final1[df_final1['Provinsi'].isin(java_island_provinces)].reset_index(drop=True)

    # Define color codes for the palette
    color_codes = {
        1: '#1d3d71ff',
        2: '#f26634ff',
        3: '#b19802ff',
        4: '#56a3a6ff',
        5: '#80a4edff',
        6: '#1be7ffff',
        7: '#df57bcff',
        8: '#88a0a8ff',
        9: '#00c49aff',
        10: '#EE9121ff'
    }

    # Create function for making boxplot
    st.set_option('deprecation.showPyplotGlobalUse', False)
    def boxplot_maker(dataset, commodity_type, palette):
        # Prepare the plot
        plt.figure(figsize=(10, 6))  # Adjust figure size if needed

        # Create a boxplot using seaborn
        ax = sns.boxplot(x='Provinsi', y='Harga (Rp)', data=dataset, hue='Provinsi', palette=palette, width=0.7)

        # Calculate median values
        medians = dataset.groupby(['Provinsi'])['Harga (Rp)'].median()

        # Sort medians based on the order of categories in the x-axis
        categories = dataset['Provinsi'].unique()
        medians = medians.reindex(categories)

        # Add median annotations to the plot
        for i, median in enumerate(medians):
            plt.text(i, median + 5, f'{median:.2f}', horizontalalignment='center', verticalalignment='bottom', fontdict={'color': 'black'})

        # Add title
        plt.title(f'BOXPLOT OF {commodity_type.upper()} PRICES IN PROVINCES FROM JAVA ISLAND')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Hide legend
        ax.legend().set_visible(False)

        # Show the plot
        st.pyplot()

    with st.expander("Descriptive Statistical Results"):
        # Menampilkan 5 baris pertama
        st.write("### First 5 lines from the dataframe:")
        
        st.write(provinces_data.head())

        # compare Beras Premium and Beras Medium descriptive statistical results
        beras_premium_df = provinces_data[provinces_data['Nama Komoditas']=='Beras Premium']

        # Menampilkan deskripsi statistik
        st.write("### Descriptive Statistics from the Dataframe:")
        st.write(beras_premium_df.describe())

        st.markdown("""
        ### Insight:
        1. Based on descriptive statistical study, the average price of Beras Premium is 13417 IDR.
        2. The spread of the data for both Beras Premium is represented by its standard deviation, at 1044 IDR.
        3. The range of the prices of Beras Premium starts from 11660 IDR to 17220 IDR.            
        """)
    with st.expander("The Boxplot"):
        # Call the boxplot_maker function to display the boxplot
        boxplot_maker(beras_premium_df, 'beras premium', list(color_codes.values())[1:7])

        # Menampilkan keterangan menggunakan markdown
        st.markdown("""
        ### Insight:

        - Based on the boxplot of Beras Premium, we can see some outliers from Jawa Barat and D.I Yogyakarta. On the other hand, it is important to let the outliers as it is to keep the data originality.

        - In general, the median prices in Beras Premium are ranging from 12675 IDR to 12910 IDR.

        1. DKI Jakarta

        Among the provinces, DKI Jakarta has the largest price variations for Beras Premium. The price starts from around 12300 IDR to 17200 IDR, with median price at 12870 IDR.

        2. Jawa Barat

        Jawa Barat's Beras Premium has the price ranging from around 12100 IDR to 16500 IDR, with the lowest median price compared to other provinces, at 12675 IDR .

        3. Jawa Tengah

        In Jawa Tengah, Beras Premium has the price ranging from around 12250 IDR to 16250 IDR, with the highest median price compared to other provinces, at 12790 IDR.

        4. D.I Yogyakarta

        In D.I Yogyakarta, Beras Premium has the price ranging from around 12250 IDR to 16500 IDR, with the median price at 12730 IDR.

        5. Jawa Timur

        Jawa Timur has least price variations for Beras Premium (shown by shortest box and whiskers plot). Its price us ranging from around 12100 IDR to 16000 IDR, with the median price at 12730 IDR.

        6. Banten

        Lastly, Banten's Beras Premium has the price ranging from around 11750 IDR to 16750 IDR, with the median price at 12890 IDR.
        """)

    with st.expander("The Time Series"):
        st.markdown("### DKI Jakarta")
        beras_premium_data_jakarta = df_final2[(df_final2['Komoditas (Rp)'] == 'Beras Premium') & (df_final2['Provinsi'] == 'DKI Jakarta')]

        # Convert the 'Tanggal' column to datetime format
        beras_premium_data_jakarta['Tanggal'] = pd.to_datetime(beras_premium_data_jakarta['Tanggal'], format='%d/%m/%Y')

        # Sort the data by date
        beras_premium_data_jakarta.sort_values(by='Tanggal', inplace=True)

        # Create and plot the time series
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(beras_premium_data_jakarta['Tanggal'], beras_premium_data_jakarta['Harga'], marker='o', linestyle='-')
        ax.set_title('Time Series of Beras Premium Price in DKI Jakarta')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (Rp)')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        plt.tight_layout()

        # Show plot using Streamlit
        st.pyplot(fig)

        st.write("""
        **Insights:**
        - Based on the graph of the price of premium rice in Jakarta, there is a noticeable upward trend in rice prices.
        - The price increase occurred in September 2023, from an average price of 12.739 IDR to 14.002 IDR, and remained relatively stable until the end of 2023.
        - Another increase occurred at the beginning of 2024, reaching its peak price on March 1st at 17.220 IDR per kilogram.
        """)

        st.markdown("### Jawa Barat")
        beras_premium_data_jabar = df_final2[(df_final2['Komoditas (Rp)'] == 'Beras Premium') & (df_final2['Provinsi'] == 'Jawa Barat')]

        # Convert the 'Tanggal' column to datetime format
        beras_premium_data_jabar['Tanggal'] = pd.to_datetime(beras_premium_data_jabar['Tanggal'], format='%d/%m/%Y')

        # Sort the data by date
        beras_premium_data_jabar.sort_values(by='Tanggal', inplace=True)

        # Create and plot the time series
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(beras_premium_data_jabar['Tanggal'], beras_premium_data_jabar['Harga'], marker='o', linestyle='-')
        ax2.set_title('Time Series of Beras Premium Price in Jawa Barat')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Price (Rp)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True)
        plt.tight_layout()

        # Show plot using Streamlit
        st.pyplot(fig2)

        st.write("""
        **Insights:**
        - In 2023, the average price of premium rice in West Java remained stable around 12,500 IDR until August 2023.
        - There was a price increase in September 2023, followed by stabilization at an average price of 14,000 IDR.
        - Prices rose again at the beginning of 2024, especially in February, with the average price of premium rice reaching 16,000 IDR per kilogram
        """)

        st.markdown("### Jawa Tengah")
        beras_premium_data_jateng = df_final2[(df_final2['Komoditas (Rp)'] == 'Beras Premium') & (df_final2['Provinsi'] == 'Jawa Tengah')]

        # Convert the 'Tanggal' column to datetime format
        beras_premium_data_jateng['Tanggal'] = pd.to_datetime(beras_premium_data_jateng['Tanggal'], format='%d/%m/%Y')

        # Sort the data by date
        beras_premium_data_jateng.sort_values(by='Tanggal', inplace=True)

        # Create and plot the time series
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.plot(beras_premium_data_jateng['Tanggal'], beras_premium_data_jateng['Harga'], marker='o', linestyle='-')
        ax3.set_title('Time Series of Beras Premium Price in Jawa Tengah')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Price (Rp)')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True)
        plt.tight_layout()

        # Show plot using Streamlit
        st.pyplot(fig3)
        
        st.write("""
        **Insight:**
        - In 2023, the average price of premium rice in Center Java remained stable around 12,800 IDR until August 2023.
        - There was a price increase in September 2023, followed by stabilization at an average price of 14,100 IDR.
        - Prices rose again at the beginning of 2024, especially in February, with the average price of premium rice reaching 15891 IDR per kilogram.
        """)

        st.markdown("### Yogyakarta")
        beras_premium_data_yogya = df_final2[(df_final2['Komoditas (Rp)'] == 'Beras Premium') & (df_final2['Provinsi'] == 'D.I Yogyakarta')]

        # Convert the 'Tanggal' column to datetime format
        beras_premium_data_yogya['Tanggal'] = pd.to_datetime(beras_premium_data_yogya['Tanggal'], format='%d/%m/%Y')

        # Sort the data by date
        beras_premium_data_yogya.sort_values(by='Tanggal', inplace=True)

        # Create and plot the time series
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(beras_premium_data_yogya['Tanggal'], beras_premium_data_yogya['Harga'], marker='o', linestyle='-')
        ax4.set_title('Time Series of Beras Premium Price in D.I Yogyakarta')
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Price (Rp)')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True)
        plt.tight_layout()

        # Show plot using Streamlit
        st.pyplot(fig4)

        st.write("""
        **Insight:**
        - In 2023, the average price of premium rice in D.I Yogyakarta remained stable around 12,500 IDR until August 2023.
        - There was a sharp price increase in September 2023, which continued to rise gradually until the end of the year, reaching an average price of 14,000 IDR in December.
        - Prices then surged again in February 2024, with the average price of premium rice reaching 15,851 IDR.
        """)

        st.markdown("### Jawa Timur")
        # Filter data for Beras Premium in Jawa Timur
        beras_premium_data_jatim = df_final2[(df_final2['Komoditas (Rp)'] == 'Beras Premium') & (df_final2['Provinsi'] == 'Jawa Timur')]

        # Convert the 'Tanggal' column to datetime format
        beras_premium_data_jatim['Tanggal'] = pd.to_datetime(beras_premium_data_jatim['Tanggal'], format='%d/%m/%Y')

        # Sort the data by date
        beras_premium_data_jatim.sort_values(by='Tanggal', inplace=True)

        # Create and plot the time series
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        ax5.plot(beras_premium_data_jatim['Tanggal'], beras_premium_data_jatim['Harga'], marker='o', linestyle='-')
        ax5.set_title('Time Series of Beras Premium Price in Jawa Timur')
        ax5.set_xlabel('Date')
        ax5.set_ylabel('Price (Rp)')
        ax5.tick_params(axis='x', rotation=45)
        ax5.grid(True)
        plt.tight_layout()

        # Show plot using Streamlit
        st.pyplot(fig5)

        st.write("""
        **Insight:**
        - In 2023, the average price of premium rice in East java remained stable around 12,600 IDR until August 2023.
        - There was a sharp price increase in September 2023, but remained stable with an average price of 14,000 IDR until December.
        - Prices then surged again in February 2024, with the average price of premium rice reaching 15,200 IDR.
        - Even though in East Java, on March 1st, the price has not reached 16,000 IDR, unlike other provinces in Java Island that have reached figures above 16,000
        """)

        st.markdown("### Banten")
        # Filter data for Beras Premium in Banten
        beras_premium_data_banten = df_final2[(df_final2['Komoditas (Rp)'] == 'Beras Premium') & (df_final2['Provinsi'] == 'Banten')]

        # Convert the 'Tanggal' column to datetime format
        beras_premium_data_banten['Tanggal'] = pd.to_datetime(beras_premium_data_banten['Tanggal'], format='%d/%m/%Y')

        # Sort the data by date
        beras_premium_data_banten.sort_values(by='Tanggal', inplace=True)

        # Create and plot the time series
        fig6, ax6 = plt.subplots(figsize=(10, 6))
        ax6.plot(beras_premium_data_banten['Tanggal'], beras_premium_data_banten['Harga'], marker='o', linestyle='-')
        ax6.set_title('Time Series of Beras Premium Price in Banten')
        ax6.set_xlabel('Date')
        ax6.set_ylabel('Price (Rp)')
        ax6.tick_params(axis='x', rotation=45)
        ax6.grid(True)
        plt.tight_layout()

        # Show plot using Streamlit
        st.pyplot(fig6)

        st.write("""
        **Insight:**
        - Overall, the increase in premium rice prices in Banten Province shows a consistent upward trend from the beginning of January 2023 until March 1st, 2024.
        - From the price increase graph, the most drastic increases occurred in September 2023 and February 2024.
        - Premium rice prices in Banten reached 16,690 IDR on March 1st, 2024, whereas in January 2023, the average price was only 11,922 IDR.
        """)

if __name__ == "__main__":
    run()