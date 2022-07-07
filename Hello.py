import streamlit as st
from quickstart import credentials, download_dataframe
from resources import get_chart


st.set_page_config(page_title="Cash Prices", layout='wide',)
creds = credentials()


def main():   
    with st.sidebar:
        add_country = st.selectbox("Choose a Country", ('Russia', 'Australia', 'Argentina', 'Canada'))
        df = download_dataframe(creds=creds, filename=f'cash_prices_{add_country.lower()}.csv', parse_dates=['TRADEDATE'])
        min_start_wwht, max_start_wwht = df['TRADEDATE'].min(), df['TRADEDATE'].max()
        add_category = st.multiselect("Choose a Category", list(df['NAME'].unique()))
        
        start = st.date_input("Start Date", min_start_wwht, min_value=min_start_wwht, max_value=max_start_wwht)
        end = st.date_input("End Date", max_start_wwht, min_value=min_start_wwht, max_value=max_start_wwht)
        
    for cat in add_category:
        st.plotly_chart(get_chart(df.query('NAME==@cat & TRADEDATE>=@start & TRADEDATE<=@end'), 'TRADEDATE', 'CLOSE', f'{add_country} - {cat} Cash Prices'))

    
if __name__ == '__main__':
    main()