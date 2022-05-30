from time import sleep
import FlightRadar24 as fl
from bs4 import BeautifulSoup
import requests
import webbrowser
from colorama import Fore, Back, Style

api=fl.Api()


def open_website(url,incognito=False):
    if incognito:
        browser=webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome %s --incognito')
        browser.open_new(url)
    else:
        browser=webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome %s')
        browser.open_new(url)

def get_key(val,dict):
    for key, value in dict.items():
         if val in value:
             return key
 
    return None

def get_aiport_iata(country):

    all_airports = api.get_airports()
    data = []

    for airport in all_airports['rows']:
        if airport["country"].lower() == country.lower():
            temp = {}
            temp["name"] = airport["name"]
            temp["iata"] = airport['iata']

            data.append(temp)
    return data

def open_web_flight(flight_id):
    for i in flight_id:
        if i.isdigit():
            index = flight_id.index(i)
            break

    code=flight_id[:index]
    
    for airline in api.get_airlines()['rows']:
        if airline['Code'] == code:
            icao = airline['ICAO']
            break
    

    result=api.get_flights(icao)
    result.pop('full_count')
    result.pop('version')
    result.pop('stats')
    key=get_key(flight_id,result)



    url=f'https://www.flightradar24.com/{flight_id}/{key}'
    open_website(url=url,incognito=True)


def get_airline_code(airline_name):
    all_airlines = api.get_airlines()
    for airline in all_airlines['rows']:
        print(airline['Name'].lower(),airline_name.lower())
        if airline["Name"].lower() == airline_name.lower():
            airline_id = airline["Code"]
    print(airline_id)
    return airline_id



def list_flights(arr_iata,dep_iata,year,month,date,hour):
    
    base_url=f'https://www.flightstats.com/v2/flight-tracker/route/{arr_iata}/{dep_iata}/?year={year}&month={month}&date={date}&hour={hour}'
    
    res=requests.get(base_url)
    soup=BeautifulSoup(res.content,'html.parser')
    data=soup.find_all('h2',class_='table__CellText-sc-1x7nv9w-15 fcTUax')
    
    
    if len(data)!=0:
        flights_data={}
        for i in range(0,len(data),3):
            flights_data[data[i].text]=[data[i+1].text,data[i+2].text]
        return flights_data
    else:
        return None

def flight_status(flight_id,year,month,date):
    for i in str(flight_id):
        if i.isdigit():
            index=str(flight_id).index(i)
            break
    airline=flight_id[:index]
    id=flight_id[index:]   

    base_url=f'https://www.flightstats.com/v2/flight-tracker/{airline}/{id}?year={year}&month={month}&date={date}'

    res=requests.get(base_url)
    soup=BeautifulSoup(res.content,'html.parser')
    try:
        status=soup.find("div",class_='text-helper__TextHelper-sc-8bko4a-0 hYcdHE').text
    except:
        status=soup.find("div",class_='text-helper__TextHelper-sc-8bko4a-0 iicbYn').text
    
            
    arr_city=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 efwouT')[0].text
    arr_airport=soup.find_all('div',class_='text-helper__TextHelper-sc-8bko4a-0 cHdMkI')[0].text

    dep_city=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 efwouT')[1].text
    dep_airport=soup.find_all('div',class_='text-helper__TextHelper-sc-8bko4a-0 cHdMkI')[1].text

    scheduled_arr_time=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[0].text
    actual_arr_time=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[1].text

    scheduled_dep_time=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[2].text
    actual_dep_time=soup.find_all("div",class_='text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[3].text

    terminal_arr=soup.find_all("div",class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[0].text
    gate_arr=soup.find_all("div",class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[1].text

    terminal_dep=soup.find_all("div",class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[2].text
    gate_dep=soup.find_all("div",class_='ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx')[3].text

    return status,arr_city,arr_airport,dep_city,dep_airport,scheduled_arr_time,actual_arr_time,scheduled_dep_time,actual_dep_time,terminal_arr,gate_arr,terminal_dep,gate_dep    
    

def main():
    print()
    print('''███████╗██╗     ██╗ ██████╗ ██╗  ██╗████████╗    ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗     
██╔════╝██║     ██║██╔════╝ ██║  ██║╚══██╔══╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    
█████╗  ██║     ██║██║  ███╗███████║   ██║          ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝    
██╔══╝  ██║     ██║██║   ██║██╔══██║   ██║          ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗    
██║     ███████╗██║╚██████╔╝██║  ██║   ██║          ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║    
╚═╝     ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    
                                                                                                            ''')

    print()
    print(Fore.GREEN+"--"*40+Fore.RESET)
    
    print(Fore.CYAN+"""  _____           _   _                __        __         _           _    ___ 
 |_   _|__   ___ | | | |__  _   _   _  \ \      / /__  __ _| | __      / \  |_ _|
   | |/ _ \ / _ \| | | '_ \| | | | (_)  \ \ /\ / / _ \/ _` | |/ /____ / _ \  | | 
   | | (_) | (_) | | | |_) | |_| |  _    \ V  V /  __/ (_| |   <_____/ ___ \ | | 
   |_|\___/ \___/|_| |_.__/ \__, | (_)    \_/\_/ \___|\__,_|_|\_\   /_/   \_\___|
                            |___/                                                """+Fore.RESET)
    
    print(Fore.GREEN+"--"*40+Fore.RESET)
    
    
    while True:
        print(Fore.GREEN+"""
        1. List of flights on a particular day
        2. Flight status
        3. Track Flight
        
        99. Exit"""+Fore.RESET)

        print()
        choice = int(input(Fore.YELLOW+"Enter your choice: "+Fore.RESET))

        if choice==1:
            arrival_airport_country = input(Fore.GREEN+"""Enter Country Name Of the Arrival Airport: """+Fore.RESET)
            arr_data = get_aiport_iata(arrival_airport_country)
            if len(arr_data)==0:
                print(Fore.RED+"--"*40+Fore.RESET)
                print(Fore.RED+"No Airport Found"+Fore.RESET)
                print(Fore.RED+"--"*40+Fore.RESET)

            else:
                print(Fore.YELLOW+"--"*40+Fore.RESET)

                print(Fore.YELLOW+f"                    IATA Code of Airports In {arrival_airport_country}"+Fore.RESET)
                print()
                
                for each in arr_data:
                    print(Fore.YELLOW+f"{each['name']}:{each['iata']}"+Fore.RESET)
                
            
                print(Fore.YELLOW+"--"*40+Fore.RESET)

            arrival_airport = input(Fore.GREEN+"Enter IATA Code Of Arrival Airport: "+Fore.RESET)
            
            departure_airport_country = input(Fore.GREEN+"""Enter Country Name Of the Departure Airport: """+Fore.RESET)
            dep_data = get_aiport_iata(departure_airport_country)

            if len(dep_data) == 0:
                print(Fore.RED+"--"*40+Fore.RESET)
                print(Fore.RED+"No Airport Found"+Fore.RESET)
                print(Fore.RED+"--"*40+Fore.RESET)
            else:
                print(Fore.YELLOW+"--"*40+Fore.RESET)
                
                print(Fore.YELLOW+f"                    IATA Code of Airports In {departure_airport_country}"+Fore.RESET)
                print()

                for each in dep_data:
                    print(Fore.YELLOW+f"{each['name']}:{each['iata']}"+Fore.RESET)
                
            
                print(Fore.YELLOW+"--"*40+Fore.RESET)
            
            dep_airport = input(Fore.GREEN+"Departure Airport: "+Fore.RESET)
            date = input(Fore.GREEN+"Date(YYYY-MM-DD): "+Fore.RESET)
            print()
            print(Fore.CYAN+"""Select Time Interval-
    1. 00:00 - 06:00
    2. 06:00 - 12:00
    3. 12:00 - 18:00
    4. 18:00 - 00:00"""+Fore.RESET)
            print()
            ask_time = int(input(Fore.YELLOW+"Enter your choice: "+Fore.RESET))
            if  ask_time == 1:
                hour = "0"
            elif ask_time == 2:
                hour = "6"
            elif ask_time == 3:
                hour = "12"
            else:
                hour = "18"


            flights=list_flights(arrival_airport,dep_airport,year=date.split('-')[0],month=date.split('-')[1],date=date.split('-')[2],hour=hour)
            if flights == None:
                print(Fore.RED+"--"*40+Fore.RESET)
                print(Fore.RED+"No Flights Found! Try using another time slot."+Fore.RESET)
                print(Fore.RED+"--"*40+Fore.RESET)
            else:
                print(Fore.GREEN+"--"*40+Fore.RESET)
                print(Fore.GREEN+"                    List Of Flights"+Fore.RESET)
                print(Fore.GREEN+"--"*40+Fore.RESET)


                for flight in flights:
                    print()
                    print(Fore.GREEN+f"{flight}"+Fore.RESET)
                    print(Fore.GREEN+'--'*40+Fore.RESET)
                    print(Fore.GREEN+f'Departure Time:{flights[flight][0]}'+Fore.RESET)
                    print(Fore.GREEN+f'Arrival Time:{flights[flight][1]}'+Fore.RESET)
                    print(Fore.GREEN+'--'*40+Fore.RESET)
                
                sleep(1)
        
        elif choice == 2:
            print()
            airline_name = input(Fore.CYAN+"Enter Airline Name: "+Fore.RESET)
            airline_id = get_airline_code(airline_name)

            
            data=flight_status("SG123","2022","5","28")
            print(Fore.GREEN+"--"*40+Fore.RESET)

            print(Fore.GREEN+"                    Flight Status"+Fore.RESET)
            print(Fore.GREEN+f"Status: {data[0]}"+Fore.RESET)
            print(Fore.GREEN+f"Arrival City: {data[1]}"+Fore.RESET)
            print(Fore.GREEN+f"Arrival Airport: {data[2]}"+Fore.RESET)
            print(Fore.GREEN+f"Departure City: {data[3]}"+Fore.RESET)
            print(Fore.GREEN+f"Departure Airport: {data[4]}"+Fore.RESET)
            print(Fore.GREEN+f"Scheduled Arrival Time: {data[5]}"+Fore.RESET)
            print(Fore.GREEN+f"Actual Arrival Time: {data[6]}"+Fore.RESET)
            print(Fore.GREEN+f"Scheduled Departure Time: {data[7]}"+Fore.RESET)
            print(Fore.GREEN+f"Actual Departure Time: {data[8]}"+Fore.RESET)
            print(Fore.GREEN+f"Arrival Terminal: {data[9]}"+Fore.RESET)
            print(Fore.GREEN+f"Arrival Gate: {data[10]}"+Fore.RESET)
            print(Fore.GREEN+f"Departure Terminal: {data[11]}"+Fore.RESET)
            print(Fore.GREEN+f"Departure Gate: {data[12]}"+Fore.RESET)

            print(Fore.GREEN+"--"*40+Fore.RESET)

            sleep(1)

        elif choice == 3:
            flight_id = input(Fore.CYAN+"Enter Flight ID: "+Fore.RESET)
            open_web_flight(flight_id)
            sleep(1)
            

        elif choice == 99:            
            print(Fore.CYAN+"Good Bye."+Fore.RESET)
            break
        
if __name__=="__main__":
    main()

