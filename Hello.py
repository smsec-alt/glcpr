import streamlit as st
from quickstart import credentials, download_dataframe
from resources import get_chart


st.set_page_config(page_title="Cash Prices", layout='wide',)
creds = credentials()


def main():   
    with st.sidebar:
        add_country = st.selectbox("Choose a Country", ('Russia', 'Australia', 'Argentina', 'Canada'))
        df = download_dataframe(creds=creds, filename=f'cash_prices_{add_country.lower()}.csv', parse_dates=['TRADEDATE'])
        add_category = st.selectbox("Choose a Category", tuple(df['NAME'].unique()))
        
    st.plotly_chart(get_chart(df, 'TRADEDATE', 'CLOSE', f'{add_country} - Cash Prices'))

    
if __name__ == '__main__':
    main()