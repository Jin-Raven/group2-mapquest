import urllib.parse
import requests
import colorama
from colorama import init, Fore
from tabulate import tabulate

#Added colors and tables
init(autoreset=True)

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "gWCflqBbUBhDyGlxHavdpmiIwfGWO5tl"

while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break

    dest = input("Destination: ")
    if dest == "quit" or orig == "q":
        break

    #Added Selection of KM/MI output
    while True:
        unit = input("Choose a unit [km/mi]: ")
        if (unit.lower() == "km"):
            break
        elif (unit.lower() == "mi"):
            break
        else:
            print("\nPlease enter a valid input.\n")

    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print(Fore.GREEN + "API Status: " + str(json_status) + " = A successful route call.\n")
        print(Fore.WHITE + "=============================================")
    
       #Added KM/MI output with table
        if (unit.lower() == "km"):
              data = [[orig, dest, json_data["route"]["formattedTime"], str("{:.2f}".format((json_data["route"]["distance"])*1.61)), str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))]]
              print(Fore.LIGHTBLUE_EX  + tabulate(data, headers=["From", "To", "Trip Duration", "Kilometers", "Fuels Used(Ltr)"]))
         
        elif (unit.lower() == "mi"):
            data = [[orig, dest, json_data["route"]["formattedTime"], str("{:.2f}".format(json_data["route"]["distance"])), str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78))]]
            print(Fore.LIGHTBLUE_EX  + tabulate(data, headers=["From", "To", "Trip Duration", "Miles", "Fuels Used(Ltr)"]))


        print("=============================================") 

        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print(Fore.LIGHTYELLOW_EX + (each["narrative"])+ " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))

        print("=============================================") 
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************")
    else:
        print("**********************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to: ")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("**********************************************\n")


    #Added if user wants to reinput another location
    repeat = input('Restart? (Y/N): ')
    print("")
    if (repeat.lower() == 'yes' or repeat.lower() == 'y'):
        continue
    else:
        break