import pandas as pd


def russia_cash_prices():
    df_cpt = pd.read_excel('https://fs.moex.com/files/24378')
    df_cpt.columns = ['TRADEDATE', 'CLOSE', 'Volume']
    df_cpt['TRADEDATE'] = pd.to_datetime(df_cpt['TRADEDATE'], format='%d.%m.%Y')
    df_cpt.drop('Volume', axis=1, inplace=True)
    df_cpt['NAME'] = 'WHCPT'
    df_cpt.to_csv(r'G:\My Drive\cash_prices\cash_prices_russia.csv', index=None)

def main():
    russia_cash_prices()


if __name__ == '__main__':
    main()
