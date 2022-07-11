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
               
        if len(list(df['NAME'].unique())) > 1:
            add_2legs = st.checkbox('Include 2 Legs')
            if add_2legs:
                col1, col2 = st.columns(2)
                leg1 = col1.selectbox("Choose a Category", tuple(df['NAME'].unique()))
                leg2 = col2.selectbox("Choose a Category", tuple(df['NAME'].unique()))
            else:
                add_category = st.selectbox("Choose a Category", tuple(df['NAME'].unique()))
                add_logs = st.checkbox('Include Logs')
        col1, col2 = st.columns(2)
        start = col1.date_input("Start Date", min_start_wwht, min_value=min_start_wwht, max_value=max_start_wwht)
        end = col2.date_input("End Date", max_start_wwht, min_value=min_start_wwht, max_value=max_start_wwht)
                        
    # for cat in add_category:
    #     st.plotly_chart(get_chart(df.query('NAME==@cat & TRADEDATE>=@start & TRADEDATE<=@end'), 'TRADEDATE', 'CLOSE', f'{add_country} - {cat} Cash Prices', logs=add_logs))
    st.plotly_chart(get_chart(df.query('NAME==@cat & TRADEDATE>=@start & TRADEDATE<=@end'), 'TRADEDATE', 'CLOSE', f'{add_country} - {add_category} Cash Prices', logs=add_logs))

# np.log2(data['Salary'])
    
if __name__ == '__main__':
    main()