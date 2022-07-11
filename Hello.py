import streamlit as st
from quickstart import credentials, download_dataframe
from resources import get_chart


st.set_page_config(page_title="Cash Prices", layout='wide',)
creds = credentials()


def main():   
    with st.sidebar:
        add_country = st.selectbox("Choose a Country", ('Russia', 'Australia', 'Argentina', 'Canada'))
        df = download_dataframe(creds=creds, filename=f'cash_prices_{add_country.lower()}.csv', parse_dates=['TRADEDATE'])
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
                # add_category = df['NAME'].unique().values[0]
                add_logs = st.checkbox('Include Logs')
        else:
            add_category = all_categories[0]
            add_logs = st.checkbox('Include Logs')
        col1, col2 = st.columns(2)
        start = col1.date_input("Start Date", min_start_wwht, min_value=min_start_wwht, max_value=max_start_wwht)
        end = col2.date_input("End Date", max_start_wwht, min_value=min_start_wwht, max_value=max_start_wwht)
                        
    # for cat in add_category:
    #     st.plotly_chart(get_chart(df.query('NAME==@cat & TRADEDATE>=@start & TRADEDATE<=@end'), 'TRADEDATE', 'CLOSE', f'{add_country} - {cat} Cash Prices', logs=add_logs))
    if (len(all_categories) > 1) and (add_2legs):
        subdf = df.query('TRADEDATE>=@start & TRADEDATE<=@end')
        # st.plotly_chart(get_chart(subdf, 'TRADEDATE', 'CLOSE', f'{add_country} - {add_category} Cash Prices', logs=add_logs))
        
        df_cat1, df_cat2 = subdf.query('NAME == @leg1'), subdf.query('NAME == @leg2')
        df_cat1.rename({'CLOSE': leg1}, axis=1, inplace=True)
        df_cat2.rename({'CLOSE': leg2}, axis=1, inplace=True)
        df_all = df_cat1.merge(df_cat2, on='TRADEDATE')
        if add_operation == 'Spread':
            df_all['Result'] = df_all[leg1] - df_all[leg2]
        else:
            df_all['Result'] = df_all[leg1] / df_all[leg2]
        st.plotly_chart(get_chart(df_all, 'TRADEDATE', 'Result', f'{add_country} - {leg1}-{leg2} {add_category} Cash Prices'))
        
    else:    
        subdf = df.query('NAME==@add_category & TRADEDATE>=@start & TRADEDATE<=@end')
        st.plotly_chart(get_chart(subdf, 'TRADEDATE', 'CLOSE', f'{add_country} - {add_category} Cash Prices', logs=add_logs))

# np.log2(data['Salary'])
    
if __name__ == '__main__':
    main()