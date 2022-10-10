import requests
import numpy as np
import pandas as pd
import zipfile, io
import streamlit as st
from datetime import datetime
pd.options.mode.chained_assignment = None


st.set_page_config(page_title="Cash Prices", layout='wide',)


def eu_cash_prices():
    
    eu_reg_dict = {
    'BG': 'Bulgaria', 
    'CZ': 'Czechia',
    'DE': 'Germany',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR':'France',
    'HR':'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LT': 'Lithuania',
    'NL': 'Netherlands',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    response = requests.get('https://agridata.ec.europa.eu/Qlik_Downloads/Cereals%20Prices.zip', headers=headers)
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    dfs = {text_file.filename: pd.read_csv(zip_file.open(text_file.filename), low_memory=False, parse_dates=['Week - End Date'])
           for text_file in zip_file.infolist()
           if 'Metadata' not in text_file.filename}
    df = dfs[list(filter(lambda x: 'Metadata' not in x, dfs.keys()))[0]]
    ##only domestic prices
    df = df[df['Product Stage Name']!='Free On Board - Incoterm']
    #dropping useless columns
    df = df.drop(['Sector Code', 'Weight Unit Name', 'Week - Begin Date',  'Product Group Name', 'Product Stage Name'], axis=1)
    df['EU Price'] = df['EU Price'].str.replace('€', '')
    df['EU Price'] = pd.to_numeric(df['EU Price'], errors='coerce')
    #removing duplicates in regions
    df = df[df['Market Name']!='La Pallice']
    #removing small regions
    df = df[df['Member State Code'].isin(['CY', 'UK', 'EL', 'AT', 'BE'])==False]
    #include only regions with ly data
    df['temp'] = df['Member State Code']+df['Product Name']+df['Market Name']
    df = df[df['temp'].isin(df[df['Week - End Date'].dt.year == pd.to_datetime("today").year]['temp'].unique())]
    df = df.drop(['temp'], axis=1)
    #summary
    df = df.groupby(['Member State Code', 'Product Name', 'Week - End Date'], as_index=False).mean()
    df.columns = ['STATE', 'NAME', 'TRADEDATE', 'CLOSE']
    df['STATE'] = df['STATE'].replace(eu_reg_dict)
    df.to_csv(r'G:\My Drive\cash_prices\cash_prices_europe.csv', index=None)


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


def retrieve_argy_cash_prices(min_page: int):
    def argy_process_page(page_number: int):
        try:
            print(page_number)
            table = pd.read_html(f'https://www.bcr.com.ar/es/mercados/mercado-de-granos/cotizaciones/cotizaciones-locales/mercado-fisico-de-rosario/precios-{page_number}')[0]
            table.columns = table.iloc[1,:]
            table = table.iloc[2:,:]
            current_date = table.columns[-1]
            table.columns = ['location', 'delivery_date']+list(table.columns[2:-2])+['quality', 'prices']
            table = table.dropna(subset=['location'])
            table['grain'] = np.where(table[table.columns[4]].isna(), table['location'], np.nan)
            table['grain'] = table['grain'].ffill()
            table = table[table.columns[table.columns.isna()==False]]
            table = table.dropna()
            table['prices'] = table['prices'].apply(lambda x: x.replace(' ','').replace('u$s',''))
            table['prices'] = pd.to_numeric(table['prices'], errors='coerce')
            table = table.dropna(subset='prices')
            table['date'] = current_date
            table['page'] = page_number
            table = table[['location', 'delivery_date', 'quality', 'prices', 'grain', 'date', 'page']]
            return table
        except:
            return None
    table = pd.concat([argy_process_page(page) for page in range(min_page, 3260)])
    return table
    
    
def argy_cash_prices():
    months_dict = {
        'abril':4,
        'agosto':8,
        'diciembre':12,
        'enero':1,
        'febrero':2,
        'julio':7,
        'junio':6,
        'marzo':3,
        'mayo':5,
        'noviembre':11,
        'octubre':10,
        'septiembre':9}
    table_old = pd.read_csv(r'G:\My Drive\cash_prices\cash_prices_argentina_raw.csv')
    last_page = table_old['page'].max()+1

    try:
        table_new = retrieve_argy_cash_prices(last_page)
        table = pd.concat([table_old, table_new])
    except ValueError:
        table = table_old
    table.to_csv(r'G:\My Drive\cash_prices\cash_prices_argentina_raw.csv', index=None)

    table['grain'][table['grain'].str.contains('Corn')] = 'Corn'
    table['grain'][table['grain'].str.contains('Wheat')] = 'Wheat'
    table['grain'][table['grain'].str.contains('wheat')] = 'Wheat'
    table['grain'][table['grain'].str.contains('Barley')] = 'Barley'
    table['grain'][table['grain'].str.contains('Sunflower')] = 'Sunflower'
    table['grain'][table['grain'].str.contains('Soy')] = 'Soya'
    table = table[table['grain'].isin(['Corn', 'Wheat', 'Barley', 'Sunflower', 'Soya'])]
    table = table[table['delivery_date'].str.contains('Desc')]
    table['date'] = pd.to_datetime(table['date'], errors='coerce', format="%d/%m/%Y")
    table['prices'] = pd.to_numeric(table['prices'], errors='coerce')
    table = table.dropna()
    table = table[table['prices']>50]
    table = table.groupby(['date', 'grain'], as_index=False)['prices'].mean()
    table.columns = ['TRADEDATE', 'NAME', 'CLOSE']
    table = table[table['NAME']!='Soya']
    table.to_csv(r'G:\My Drive\cash_prices\cash_prices_argentina.csv', index=None)
    
def brz_cash_prices():
    url='https://portaldeinformacoes.conab.gov.br/downloads/arquivos/PrecosSemanalUF.txt'

    map_dict = {
        'MILHO': 'Corn',
        'TRIGO': 'Wheat',
        'SOJA': 'Soybeans',
    }

    table = pd.read_csv(url, sep=';')
    table['produto'] = table['produto'].str.strip()
    table['uf'] = table['uf'].str.strip()
    table['valor_produto_kg'] = pd.to_numeric(table['valor_produto_kg'].replace(',','.', regex=True))
    table['data_inicial_final_semana'] = table['data_inicial_final_semana'].str.strip()
    table['data_inicial_final_semana'] = pd.to_datetime(table['data_inicial_final_semana'].str.split(' - ').str[0], format='%d-%m-%Y')
    table = table.loc[(table['produto'].isin(map_dict.keys()))&(table['dsc_nivel_comercializacao']=='PREÇO RECEBIDO P/ PR')]

    table = table.groupby(['produto', 'uf','data_inicial_final_semana'], as_index=False)['valor_produto_kg'].mean()
    table.columns = ['NAME', 'STATE', 'TRADEDATE', 'CLOSE']
    table['CLOSE'] = table['CLOSE']*1000
    table['NAME'] = table['NAME'].replace(map_dict)
    table.to_csv(r'G:\My Drive\cash_prices\cash_prices_brazil.csv', index=None)


def usa_cash_prices():
    def process_report(report_id: int):
        # print(report_id)
        conversion_dict = {
            'Wheat': 0.36744,
            'Corn': 0.393680,
            'Soybeans': 0.367440,
            'Sorghum': 0.393680,
            'Barley': 0.459300,
            'Millet': 0.36744,
            'White Oats': 0.648420,
            'Sunflower Seeds': 0.734870,
        }
        response = requests.get(f'https://marsapi.ams.usda.gov/services/v1.2/reports/{report_id}?q=delivery_point=Country%20Elevators&allSections=true', auth=('api_key', '3D/lwIkPEFlr+GS5E8suDG6WJY/bMxxu'))
        df = pd.json_normalize(response.json()[1]['results'])
        df['basis'] = df[['basis Min', 'basis Max']].mean(axis=1)
        df['factor'] = df['commodity'].replace(conversion_dict)
        df['factor'] = pd.to_numeric(df['factor'], errors='coerce')
        df['basis'] = df['basis']*df['factor']
        df['avg_price'] = df['avg_price']*df['factor']
        df['commodity'] = np.where(df['commodity']=="Wheat", df['class'] + " "+df['commodity'],df['commodity'])
        df['report_date'] = pd.to_datetime(df['report_date'])

        df = df[['report_date','market_location_state','trade_loc', 'commodity', 'basis', 'avg_price']]
        df = df.melt(id_vars=['market_location_state','report_date', 'commodity', 'trade_loc'])
        df = df.groupby(['market_location_state','report_date', 'commodity', 'variable'], as_index=False).mean()
        return df

    reports_list = [2711, 2771, 2850, 2851, 2886, 2912, 2932, 3100, 3186, 3192, 3225, 3463]
    table = pd.concat([process_report(report_id) for report_id in reports_list])
    table = table.dropna()
    table.columns = ['STATE', 'TRADEDATE', 'NAME', 'VARIABLE', 'CLOSE']
    table['VARIABLE'] = table['VARIABLE'].replace({'avg_price':'Cash Price', 'basis':'Basis'})
    table.to_csv(r'G:\My Drive\cash_prices\cash_prices_usa.csv', index=None)


def main():
    print('usa')
    usa_cash_prices()
    print('canada')
    canada_cash_prices()
    print('eu')
    eu_cash_prices()
    print('argy')
    argy_cash_prices()
    print('brz')
    brz_cash_prices()
    print('rus')
    russia_cash_prices()


if __name__ == '__main__':
    main()
