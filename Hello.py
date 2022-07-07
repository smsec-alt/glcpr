import logging
import streamlit as st
# from resources import summary_dict
from quickstart import credentials, download_dataframe


logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
st.set_page_config(page_title="Cash Prices", layout='wide',)
creds = credentials()

with st.sidebar:
    add_country = st.selectbox("Choose a Country", ('Russia', 'Australia', 'Argentina', 'Canada'))


def main():   
    df = download_dataframe(creds=creds, filename=f'cash_prices_{add_country}.csv')
    st.write(df)
    
if __name__ == '__main__':
    main()