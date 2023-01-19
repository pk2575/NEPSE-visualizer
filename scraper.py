
import requests
import pandas as pd

#get companies' list from nepalipaisa website as dataframe
def get_comp_list():
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
    "referer": "https://www.google.com/"}

    response = requests.get("https://merolagani.com/CompanyList.aspx", headers=headers)
    raw = pd.read_html(response.text)
    df = pd.concat(raw)
    return df.reset_index(drop=True)
    

#get raw data from merolagani as dataframe
def get_all_data(symbol):

    try:
        df =  pd.read_html(f"https://merolagani.com/CompanyDetail.aspx?symbol={symbol}")

        if len(df) <4:
            print(f"not all tables found for {symbol}, check webpage")
            return None
        return df
    except ValueError:
        print(f"no table found for {symbol} , check webpage")

        


class company:
    #set company attributes
    def __init__(self,name,symbol,df):
        self.symbol =symbol
        self.df = df
        self.name = name
        self.mkt_price = 0
        self.percent_change = "0%"
        self.hi_lo = "0-0"
        self.two_month_avg = 0
        self.yr_yield = "0%" 
        self.eps = "0"
        self.book_value = 0
        self.pe_ratio = 0
        self.dividend = "0"
        self.bonus = "0"
        self.shr_outstanding = 0

    #get company's general details as df
    def get_details(self):
        details_df = self.df[0]
        df = {
        "sector":[details_df[1].iloc[0]],
        "shr_outstanding" : [details_df[1].iloc[1]],
        "mkt_price" : [details_df[1].iloc[2]],
        "percent_change" : [details_df[1].iloc[3]],
        "hi_lo" : [details_df[1].iloc[5]],
        "two_month_avg" : [details_df[1].iloc[6]],
        "yr_yield" : [details_df[1].iloc[7]],
        "eps" : [details_df[1].iloc[8]],
        "pe_ratio" : [details_df[1].iloc[9]],
        "book_value" : [details_df[1].iloc[10]],
        "dividend" : [details_df[1].iloc[12]],
        "mkt_cap" : [details_df[1].iloc[-1]],
        "month_avg_vol" : [details_df[1].iloc[-2]]}

        return pd.DataFrame(df,index = [self.symbol])
    
    #get company's dividend history as dataframe
    def get_dividends(self):

        try:
            df = self.df[1]
            df.drop("#",inplace= True, axis= 1)
            df = df.transpose()
            df.columns = df.iloc[1]
            df.drop("Value",inplace= True, axis= 0)
            df.rename(index={'Fiscal Year':self.symbol},inplace=True)
            return df.loc[:,~df.columns.duplicated()]

        except IndexError:
            print( f"tables not found for {self.symbol}, check website")
        
    #get company's bonus history as dataframe
    def get_bonus(self):

        try:
            df = self.df[2]
            df.drop("#",inplace= True, axis= 1)
            df = df.transpose()
            df.columns = df.iloc[1]
            df.drop("Fiscal Year",inplace= True, axis= 0)
            df.rename(index={'Value':self.symbol},inplace=True)
            return df.loc[:,~df.columns.duplicated()]

        except IndexError:
            print( f"tables not found for {self.symbol}, check website")

    #get company's right share history as dataframe
    def get_right_share(self):

        try:
            df = self.df[3]
            df.drop("#",inplace= True, axis= 1)
            df = df.transpose()
            df.columns = df.iloc[1]
            df.drop("Fiscal Year",inplace= True, axis= 0)
            df.rename(index={'Value':self.symbol},inplace=True)
            return df.loc[:,~df.columns.duplicated()]

            
        except IndexError:
            print( f"tables not found for {self.symbol}, check website")


#preleminary steps for scraping, creating company list and empty lists
gnrl_details, dividends, bonuses, right_share =[],[],[],[]
comp_list = get_comp_list()
comp_list["Symbol"] = comp_list["Symbol"].str.replace(" ", "%")


#Cleaning data and filling lists
for index in range (len(comp_list)):
    
    print(index)
    name = comp_list.loc[index,"Company Name"]
    symbol = comp_list.loc[index,"Symbol"]
    df = get_all_data(symbol)

    if df is None :
        continue
    comp = company(name,symbol,df)

    gnrl_details.append(comp.get_details())
    dividends.append(comp.get_dividends())
    bonuses.append(comp.get_bonus())
    right_share.append(comp.get_right_share())



#converting lists to dataframes and saving the files
comp_list.to_csv("F:\\Programming\\Python\\full_project\\NEPSE scraper\\data\\comp_list.csv", index=True)
pd.concat(gnrl_details).to_csv("F:\\Programming\\Python\\full_project\\NEPSE scraper\\data\\gnrl_details.csv", index=True)
pd.concat(dividends).to_csv("F:\\Programming\\Python\\full_project\\NEPSE scraper\\data\\dividends.csv", index=True)
pd.concat(bonuses).to_csv("F:\\Programming\\Python\\full_project\\NEPSE scraper\\data\\bonuses.csv", index=True)
pd.concat(right_share).to_csv("F:\\Programming\\Python\\full_project\\NEPSE scraper\\data\\right_share.csv", index=True)
    


