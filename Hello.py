import pandas as pd
import streamlit as st
from quickstart import credentials, download_dataframe
from resources import get_chart, get_seasonality_chart


st.set_page_config(page_title="Cash Prices", layout='wide',)
creds = credentials()


def main():   
    with st.sidebar:
        add_country = st.selectbox("Choose a Region", ('Canada', 'Russia', 'Europe', 'Argentina', 'Australia'))
        country_name=add_country
        df = download_dataframe(creds=creds, filename=f'cash_prices_{country_name.lower()}.csv', parse_dates=['TRADEDATE'])
        if add_country == 'Europe':
            add_state = st.selectbox("Choose a State", tuple(df['STATE'].unique()))
            country_name=add_state
            df = df.query('STATE==@country_name')
        all_categories = tuple(df['NAME'].unique())
        min_start_wwht, max_start_wwht = df['TRADEDATE'].min(), df['TRADEDATE'].max()
               
        if len(all_categories) > 1:
            add_2legs = st.checkbox('Include 2 Legs')
            if add_2legs:
                col11, col21 = st.columns(2)
                leg1 = col11.selectbox("Leg 1", all_categories)
                leg2 = col21.selectbox("Leg 2", all_categories[::-1])
                add_operation = st.selectbox("Select a function", ('Spread', 'Ratio'))
            else:
                add_category = st.selectbox("Choose a Category", all_categories)
                add_logs = st.checkbox('Include Logs')
        else:
            add_category = all_categories[0]
            add_logs = st.checkbox('Include Logs')
        col1, col2 = st.columns(2)
        start = col1.date_input("Start Date", min_start_wwht, min_value=min_start_wwht, max_value=max_start_wwht)
        end = col2.date_input("End Date", max_start_wwht, min_value=min_start_wwht, max_value=max_start_wwht)
        if add_country == 'Europe':
            add_metadata = st.checkbox('Show Metadata')
    
    
    st.markdown('### Cash Prices')         
    if (len(all_categories) > 1) and (add_2legs):
        subdf = df.query('TRADEDATE>=@start & TRADEDATE<=@end')
        
        df_cat1, df_cat2 = subdf.query('NAME == @leg1'), subdf.query('NAME == @leg2')
        df_cat1.rename({'CLOSE': leg1}, axis=1, inplace=True)
        df_cat2.rename({'CLOSE': leg2}, axis=1, inplace=True)
        df_all = df_cat1.merge(df_cat2, on='TRADEDATE')
        if add_operation == 'Spread':
            df_all['Result'] = df_all[leg1] - df_all[leg2]
        else:
            df_all['Result'] = df_all[leg1] / df_all[leg2]
        st.plotly_chart(get_chart(df_all, 'TRADEDATE', 'Result', f'{country_name} -- {leg1}-{leg2} Cash Prices {add_operation}',
                                  labels={'Result':add_operation, 'TRADEDATE':''}))
        st.plotly_chart(get_seasonality_chart(df_all, 'TRADEDATE', 'Result', f'{country_name} -- {leg1}-{leg2} Cash Prices {add_operation} Seasonality',
                                              labels={'Result':add_operation, 'DATE':'', 'YEAR':'Year'}))
        
    else:    
        subdf = df.query('NAME==@add_category & TRADEDATE>=@start & TRADEDATE<=@end')
        st.plotly_chart(get_chart(subdf, 'TRADEDATE', 'CLOSE', f'{country_name} -- {add_category} Cash Prices', logs=add_logs,
                                  labels={'CLOSE':add_category, 'TRADEDATE':'', 'YEAR':'Year'}))
        st.plotly_chart(get_seasonality_chart(subdf, 'TRADEDATE', 'CLOSE', f'{country_name} -- {add_category} Cash Prices Seasonality',
                                              labels={'CLOSE':add_category, 'TRADEDATE':'', 'YEAR':'Year'}))
# 
    if (add_country == 'Europe') and (add_metadata):
        st.markdown('### Metadata')     
        df_metadata = pd.read_csv(f'./metadata/metadata_{add_country.lower()}.csv')
        st.write(df_metadata.query('STATE==@country_name'))
    
if __name__ == '__main__':
    main()