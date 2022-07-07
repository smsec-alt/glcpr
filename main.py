import requests
import pandas as pd
import streamlit as st
from datetime import datetime
from quickstart import credentials, download_dataframe

st.set_page_config(page_title="Cash Prices", layout='wide',)



def canada_cash_prices():
    params = {
        'DN': '6dd2ea91-22e6-4095-9d2a-67ef8c822897',
        'l': 'English',
    }

    data = {
        '__VIEWSTATE': '/wEPDwUKMTM5MTE1ODI1Mg8WBB4JQ2FjaGVkS2V5BSx+L0FwcHMvQUdSX0FwcHMvTWFya2V0VHJlbmRzL1NlYXJjaEZvcm0uYXNjeB4GbXlEYXRhMuICAAEAAAD/////AQAAAAAAAAAMAgAAAEhBcHBfQ29kZS5jZHl4ZW5lbCwgVmVyc2lvbj0wLjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwFAQAAABlNYXJrZXRUcmVuZHNQZXJzaXN0ZWREYXRhCQAAAAxzZWFyY2hTdHJpbmcIcGFnZU5hbWUIX2NvbnRleHQJX3Bvc3RiYWNrDl94bWxEYXRhU291cmNlCl9Gb3JtVGl0bGUNX0Zvcm1Gb290Tm90ZQpfZGJUb1F1ZXJ5Cl9zaG93V2Vla3MBAQEAAQEBAQABAQIAAAAKCgoBBgMAAAAQR3JhaW5JblN0b3JlLnhtbAYEAAAANUdyYWluIC0gPGI+U2Fza2F0Y2hld2FuIENhc2ggUHJpY2VzICgkIHBlciB0b25uZSk8L2I+BgUAAAAABgYAAAAHR3JhaW5TSwELZBgCBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBgUpY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSR1Y3RsJGxiQ3JvcFR5cGUFJWN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkdWN0bCRsYlllYXIFJWN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkdWN0bCRsYldlZWsFLGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkdWN0bCRyYk9yZGVyQnlZZWFyBSxjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJHVjdGwkcmJPcmRlckJ5V2VlawUsY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSR1Y3RsJHJiT3JkZXJCeVdlZWsFKGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkdWN0bCRndlJlc3VsdHMPPCsACgEIAgFkahV7RV71TUozglTcYVWoL/g1UbE=',
        '__VIEWSTATEGENERATOR': '8054DF51',
        '__EVENTVALIDATION': '/wEWcwKJ9cGgBgKZz6+RDwKF0/PvAwKC04v6DQK009/uAwKIr4zxAwLD3NeTBQLy3KnBAQKO5I3aAgLv7+K7CgKDodO5BQLsouDlDALNirTPAQLNiqDiCALNityGBwLQnaKuBALQnd7CDALQnYqqDgLQnabNBgLQndLhDQLQnc6EBALQnfq/AwLQnZbSCwLQnYL1AgLQnb6oCQK7pIyxDgK7pLjUBgK7pJQ9ArukgNAIArukvIsHArukqK4OArukxMIGAruk8OUNAruk7JgEArukmLMDAv/H8cUGAv/H7fgNAv/H2cEIAv/H9eQHAv/H4Z8OAv/HnbIFAv/HidUNAv/HpYgEAv/H0awDAv/HzccLAsLu0+gIAsLuz4MHAsLuu+sCAsLu148JAsLuwyICwu7/xQgCwu7r+AcCwu6Hkw4Cwu6ztgUCwu6v6Q0C9YSTrgcC9YSPwQ8C9YSD4AgCiuXH/AoCleXH/AoClOXH/AoCl+XH/AoCluXH/AoCkeXH/AoCkOXH/AoCk+XH/AoCguXH/AoCjeXH/AoCleWH/woCleWL/woCleWP/woCleWz/woCleW3/woCleW7/woCleW//woCleWj/woCleXn/AoCleXr/AoClOWH/woClOWL/woClOWP/woClOWz/woClOW3/woClOW7/woClOW//woClOWj/woClOXn/AoClOXr/AoCl+WH/woCl+WL/woCl+WP/woCl+Wz/woCl+W3/woCl+W7/woCl+W//woCl+Wj/woCl+Xn/AoCl+Xr/AoCluWH/woCluWL/woCluWP/woCluWz/woCluW3/woCluW7/woCluW//woCluWj/woCluXn/AoCluXr/AoCkeWH/woCkeWL/woCkeWP/woCkeWz/woC54/0yQICiI+MxQUCsrzP3wTiUSIs4GTlPqigIqClNRLZ5d01/Q==',
        'ctl00$ContentPlaceHolder1$uctl$lbCropType': [
            'Canola1Can',
            'Wheat1CWRS',
            'Wheat1CPS',
            'Wheat1CWAD',
            'Wheat3CW',
            'WheatCWFeed',
            'Oats3CW',
            'BarleyFD',
            'Barley1CW',
            'Rye1CW',
            'Flax1CW',
        ],
        'ctl00$ContentPlaceHolder1$uctl$lbYear': list(map(lambda x: str(x), range(1978, datetime.now().year+1))),
        'ctl00$ContentPlaceHolder1$uctl$lbWeek': '0',
        'ctl00$ContentPlaceHolder1$uctl$OrderBy': 'rbOrderByYear',
        'ctl00$ContentPlaceHolder1$uctl$btnSearchFormSubmit': 'Submit',
    }

    response = requests.post('https://applications.saskatchewan.ca/Default.aspx', params=params,  data=data)


    table = pd.read_html(response.text)[0]
    table['PublishedDate (m/d/y)'] = pd.to_datetime(table['PublishedDate (m/d/y)'])
    table.drop(['ThisYear', 'Week'], axis=1, inplace=True)
    table =  table.melt(id_vars='PublishedDate (m/d/y)')
    table.columns = ['TRADEDATE', 'NAME', 'CLOSE']
    table = table[['TRADEDATE', 'CLOSE', 'NAME']]
    table = table.dropna()
    table = table.sort_values(by=['NAME', 'TRADEDATE'])
    table['NAME'] = table['NAME'].replace('Barley1 CW', 'BarleyFeed')
    table['NAME'] = table['NAME'].replace('BarleyFeed', 'Barley Feed')
    table['NAME'] = table['NAME'].str.replace('1','')
    table['NAME'] = table['NAME'].str.replace('2','')
    table['NAME'] = table['NAME'].str.replace('3','')
    table = table.query('NAME != "Wheat CW"')
    table.to_csv(r'G:\My Drive\cash_prices\cash_prices_canada.csv', index=None)


def russia_cash_prices():
    df_cpt = pd.read_excel('https://fs.moex.com/files/24378')
    df_cpt.columns = ['TRADEDATE', 'CLOSE', 'Volume']
    df_cpt['TRADEDATE'] = pd.to_datetime(df_cpt['TRADEDATE'], format='%d.%m.%Y')
    df_cpt.drop('Volume', axis=1, inplace=True)
    df_cpt['NAME'] = 'WHCPT'
    df_cpt.to_csv(r'G:\My Drive\cash_prices\cash_prices_russia.csv', index=None)

def main():
    russia_cash_prices()
    canada_cash_prices()


if __name__ == '__main__':
    main()
