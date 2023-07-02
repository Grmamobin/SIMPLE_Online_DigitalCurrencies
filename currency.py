import requests  # to search via net
from requests import Request, Session
import csv
import datetime  # to find time and date
import pandas as pd
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
import os
import matplotlib.pyplot as plt
import numpy as np
import io

def start():
 print('********************* Digital currencies 🪙 *********************')
 print('|-------------------------------|------------------------------------------|')
 print('|1) add online coin             |2) get info about your Digital currencies |')
 print('|-------------------------------|------------------------------------------|')
 print('|3) favourite list              |4) show the plot                          |')
 print('|-------------------------------|------------------------------------------|')
 print('|5) load all data that you saved|6) exit                                   |')
 print('|-------------------------------|------------------------------------------|')
    
 choose = int(input())
 match choose:
    case 1:  ####################################################################################### first part
        list_currency = []
        
        key = "95f9f8d9-aca9-4bf3-9ddd-1f08c9f6dc1b"   #api key use for json part
        url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'    #data that shoul be all come from here
        
        flag = True
        
        while flag:
            print('plz input the name of the currency 🤠: ')
            currency_name = str(input())
            
            url = f'https://coinmarketcap.com/currencies/{currency_name}/'
            
            response = requests.get(url)
            
            def IsValid(response):
                if response.status_code == 404:  # it means error 404 that means it doesnt exist and actually it does not valid
                    return False
                else:
                    return True
                
            if IsValid(response):
                
                print('yeehhh this is valid you can continue 😀...........')
                
                list_currency.append(currency_name)         #add every currancy to list
                
                print('Do you wanna send another 🤠 ?(yes/no)')
                answer = str(input())
                
                if answer == 'no':
                    flag = False
                    
                    
            else:
               print('Try again')

       
        filename = "user_Currency.csv"   #this is the file that save and load data of digital currency
    
        def get_price(coin):
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=USD"
            response = requests.get(url)
            
            if response.status_code == 200:
                price = float(response.json()[coin]["usd"])
                print(price)
                return price
            else:
                return None
        currency = 0
        fields = ['Name', 'Price', 'Date']
        with open(filename, 'w',newline='') as csvfile:
            
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            
            for currency in list_currency:
              price = get_price(currency)
              date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    #add date format it likes date of birth format as you wanna know
              if price is not None:
                  print(f'Price: {price:.4f} USDT for {currency}')
                  writer.writerow({'Name': currency, 'Price': price, 'Date': date})
              else:
                  print('Net is so weak 😥')
        start()    
                        
    case 2:   ####################################################################################### second part
        
        with open('user_Currency.csv', mode ='r')as file: 
            
            csvFile = csv.reader(file)
            rows = list(csvFile)
            
            if os.stat('user_Currency.csv').st_size == 0:                  #check if the file is empty return to start part
                print("there is nothing writen in this file 😥")
                start()
            else: 
               for line in rows: 
                 print(line)
                 
            print("These are all you have in category 😉... About which currency do you wanna get info ? plz write it's name 😏:" )
            coin_name = str(input())
            
            df = pd.read_csv('user_Currency.csv')      # read the csv file into a DataFrame
            df.set_index('Name', inplace=True)
            DateLast = df.loc[coin_name, 'Date']
            DateNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  #find current data to find the avg
            PriceLast = df.loc[coin_name, 'Price']
            
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_name}&vs_currencies=USD"
            response = requests.get(url)
            
            if response.status_code == 200:
                PriceNow = float(response.json()[coin_name]["usd"])
                
            #lets calculate the avg
            DateLast = datetime.datetime.strptime(DateLast, '%Y-%m-%d %H:%M:%S')   # Convert the dates to datetime objects
            DateNow = datetime.datetime.strptime(DateNow, '%Y-%m-%d %H:%M:%S')
            
            Price_avg = (PriceNow + float(PriceLast)) / 2
            time_diff = (DateNow - DateLast) / 2
            Date_avg = DateLast + time_diff
            
            print(Price_avg ,Date_avg)
            
            #lets create matplot
            y1 = [PriceNow];  x1 = [DateNow]   #red cycle
            y2 = [float(PriceLast)]; x2 = [DateLast]   #blue cycle
            y3 = [Price_avg]; x3 = [Date_avg]    #green cycle
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.plot(x1, y1, '-ro', markersize=5)  # red line with circles
            plt.plot(x2, y2, '-bo', markersize=5)  # blue line with circles
            plt.plot(x3, y3, '-go', markersize=5)  # green line with circles
            plt.plot([x1[0], x2[0], x3[0]], [y1[0], y2[0], y3[0]], '-y')  # connect these dot with themselves
            plt.show()
            
            #bonus feature [[[[TODO NOT FINNISH]]]]
            x = np.array([DateLast.timestamp(), DateNow.timestamp()])
            slope, intercept = np.polyfit(x, [PriceLast, PriceNow], 1)
            future_dates = [DateNow + datetime.timedelta(days=i) for i in range(1, 8)]
            future_x = np.array([d.timestamp() for d in future_dates])
            future_y = slope * future_x + intercept
            plt.plot(future_dates, future_y, 'r--', label='Forecast')
            plt.legend()
            plt.show()
            
            start()
            
    case 3:  ####################################################################################### third part
        fields = ['Name']
        favourite_list = 'user_FavouriteList.csv'
        
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        "NOTE: IF YOU WANNA USE CASE 3 MAKE SUER THAT YOU UN COMMENT THIS PART ON YOUR PC 
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
        """  with open(favourite_list, 'w') as csvfile:
              writer = csv.DictWriter(csvfile, fieldnames=fields)
              writer.writeheader() """
              
              
        print('this is all you have in your favourite list 😏:')
        with open('user_FavouriteList.csv', mode ='r')as file: 
            
            csvFile = csv.reader(file)
            rows = list(csvFile)
            
            if os.stat('user_FavouriteList.csv').st_size == 0:                  #check if the file is empty return to start part
                print("there is nothing writen in this file 😖")
            else: 
               for line in rows: 
                 print(line)
            print('Do you want to add some currency from the user_currency file to your favourite list 🤠 ? (yes/no)')
            answer = str(input())
            if answer == 'yes':
                print('Please write its name here 😜:')
                coin_currency = str(input())
                with open('user_Currency.csv', mode='r') as csv__:
                    csvFile = csv.reader(csv__)
                    for row in csvFile:
                        if coin_currency in row:
                            with open('user_FavouriteList.csv', mode='a') as file2:
                                write = csv.writer(file2)
                                write.writerow(row)
                                print('------------🫡Added successfully----------')
                                start()
            start()                    
            
    case 4: ####################################################################################### fourth part
     coin_list = []

     def get_historical_price(coin, days_ago):
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days_ago}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            prices = data["prices"]
            price = prices[0][1] 
            
            return price
        else:
            return None

     print('so if you wanna see all of your currency, that\'s it ->😃')
     with open('user_Currency.csv', mode='r') as file:
         csvFile = csv.reader(file)
         rows = list(csvFile)

         if os.stat('user_Currency.csv').st_size == 0:  # check if the file is empty and return to the start part
             print("There is nothing that you saved in this file 😯😳")
             start()
         else:
             for line in rows:
                print(line)

     print('How many currencies (that you have) do you want to compare?😲')
     amount = int(input())  # the maximum selection is 6

     print('THEN write the range of time that you are looking for...😲...')  # TIME
     time_coin = int(input())  # for example, if you input 10, that means about 10 days ago.... NOTE: the maximum selection is 30 days ago

     fig, axes = plt.subplots(1,amount,figsize=(10, 5))  # Create subplots
    
     for coin in range(amount):
         print('Input your currency that exists in this file and take info about them 😀')  # NAME
         choose = input()
         coin_list.append(choose)
         
     #plot1 = plt.subplot2grid((3, 3), (0, 2), rowspan=3, colspan=2)
     
     for amount__, currency in enumerate(coin_list):
         # Let's write its plot
    
         x = np.arange(1, int(time_coin+1),1)
         y = [get_historical_price(currency, i) for i in x]
         
         ax = axes[amount__]
         ax.step(x, y)
         ax.set_title(currency)
         #save this plot
    
         data = np.vstack((x, y)).T
         
         with open('data.txt', 'a') as file:
           np.savetxt(file, data, header='day,price', fmt='%d,%.2f')
         
     plt.tight_layout()
     plt.show()
     
     # Now it's suggestion part
     best_coin = None
     max_price_diff = float('-inf')
     print('This is the best coin that we suggested for you ~~~~>')
     for currecny in coin_list:
         
         find_diff = abs(float(get_historical_price(currency, time_coin)) - float(get_historical_price(currency, 1)))
         if find_diff > max_price_diff:
             max_price_diff = find_diff
             best_coin = currency
        
                 
     print(best_coin)
     start()
     
    case 5: ####################################################################################### fifth part
        print('Wait for a second..😃..😃..😃..😃..😃..😃..😃..')
        with open('data.txt', 'r') as f:
            file_data = f.read()
            sections = file_data.split('#')
            for section in sections:
              if section.strip() == '': # Skip empty sections
                continue
              section_lines = section.strip().split('\n')[1:]
                
              data = np.genfromtxt(io.StringIO('\n'.join(section_lines)), delimiter=',')
              plt.step(data[:, 0], data[:, 1])
            
              plt.xlabel('Day')
              plt.ylabel('Price')
              plt.title('Price History')
              plt.show()
    
        start()
        
    case 6: ####################################################################################### sixth part
        
        print('🤠 🤠 HOPE YOU ENJOY 🤠 🤠')
                        
start()
