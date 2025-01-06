import sys
import pandas as pd
import os
import re
from datetime import datetime

#get symbol and header details from stocks.property file
def get_detail_from_prop(property_file_path):
    prop_dic={}
    file=open(file=property_file_path,mode="r")

    for line in file:
        x=line.strip().split("=",1)
        prop_dic[x[0]]=x[1]
    
    file.close()
    filter_columns=prop_dic["header"].split(",")
    filter_stock_list=prop_dic["symbol"].split(",")
    return filter_columns,filter_stock_list

# filter required stock prices from live data  
def fetch_stock_data(stock_data_path,filter_columns,filter_stock_list,destination_path):

    # list all the files 
    filenames= os.listdir(stock_data_path)
    file_pattern =r"NIFTY.*\.csv"
    filtered_files=[]
    
    for file in filenames:
        if os.path.isfile(os.path.join(stock_data_path,file)) and re.search(file_pattern,file):
            filtered_files.append(file)

    print(f"\n******** Files present *********\n{filtered_files}")
    

    # ----- select the lastet file to be processed ------
    files_df=pd.DataFrame(filtered_files,columns=["file_name"])
    date_pattern=r"(\d{2})-(\w{3})-(\d{4})"

    files_df["date"]=files_df["file_name"].apply(lambda x: datetime.strptime(re.search(date_pattern,x).group(),'%d-%b-%Y'))
    
    files_df=files_df.sort_values('date',ascending=False)
    final_file=files_df.iloc[0]['file_name']
    print(f"\nLatest File to be processed: {final_file}")
    
    live_data=pd.read_csv(stock_data_path + '\\' + final_file)
    
    # current_stock_columns=live_data.columns.to_list()
    # print(current_stock_columns)

    #clean live data column names
    live_data.columns=live_data.columns.str.replace('\n','',regex=False).str.strip().str.lower()

    filter_df=live_data[filter_columns]
    final_df=filter_df[filter_df['symbol'].isin(filter_stock_list)]

    print(f"\n********* Filtered stocks' data **********\n{final_df}")

    # write data to destination
    
    with pd.ExcelWriter(destination_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        final_df.to_excel(writer, sheet_name="live_data", index=False)
    
   

if __name__=="__main__":
    
    try:
        print("********** PROGRAM STARTED ************")

        #Testing input
        # property_file_path="D:\my project\portfolio Analyzer\main\stocks.properties"
        # stock_data_path="D:\my project\portfolio Analyzer\stock_data"
        # destination_path="D:\my project\portfolio Analyzer\portfolio\Investment.xlsx"
        
        
        
        #get stocks.property file path during run time
        property_file_path=sys.argv[1]
        stock_data_path=sys.argv[2]
        destination_path=sys.argv[3]

        print(f"*******property_file_path: {property_file_path} ********")
        print(f"*******stock_data_path: {stock_data_path} ********")
        print(f"*******destination_path: {destination_path} ********")
        
        

        #get symbol and header details from stocks.property file
        filter_columns,filter_stock_list=get_detail_from_prop(property_file_path)

        print(f"filter_columns: {filter_columns}\nfilter_stock_list:{filter_stock_list}")
        
        # filter required stock prices from live data
        fetch_stock_data(stock_data_path,filter_columns,filter_stock_list,destination_path)

        print("********** PROGRAM ENDED SUCCESSFULLY ****************")
        



    except Exception as e:
        print("Exception caught: "+ str(e))
        sys.exit(1)
    


