import json
import requests
import pandas
from bs4 import BeautifulSoup
import sys


def get_data_from_url(url):
    r = requests.get(url)
    c = r.content

    soup = BeautifulSoup(c, 'html.parser')
    body = json.loads(soup.text)

    allCars = []

    try:
        for car in body['data']:
            currentCar = {}
            currentCar['Price'] = car['price']['value']['raw']
            for parameter in car['parameters']:
                if parameter['key'] == 'year':
                    currentCar["Year"] = parameter['value']
                elif parameter['key'] == 'petrol':
                    currentCar["fuel"] = parameter['value']
                elif parameter['key'] == 'mileage':
                    currentCar["Kms"] = parameter['value']
                elif parameter['key'] == 'model':
                    currentCar["model"] = parameter['value']
                elif parameter['key'] == 'make':
                        currentCar["make"] = parameter['value']
            currentCar["Location"] = car['locations_resolved']['ADMIN_LEVEL_3_name']
            allCars.append(currentCar)
    except:
        print(body)
        print("Unexpected error:", sys.exc_info()[0])

    nextPage = False
    print(body)
    if len(body['data']) > 0 and ('next_page_url' in body['metadata']):
        nextPage = True
    return [allCars, nextPage]

# data to CSV
cumulativeCarData = []
make = ["maruti-suzuki", "hyundai", "tata", "mahindra", "cars-honda", "toyota", "ford", "fiat", "bmw", "mercedes-benz", "audi", "nissan", "chevrolet", "hindustan-motors", "mahindra-renault", "mitsubishi", "renault", "skoda", "volkswagen", "cars-other", "ashok-leyland", "aston-martin", "bentley", "bugatti", "caterham", "daewoo", "datsun", "dc", "eicher-polaris", "ferrari", "force-motors", "icml", "isuzu", "jaguar", "jeep", "lamborghini", "land-rover", "maserati", "mini", "opel", "porsche", "premier", "rolls-royce", "san", "ssangyong", "volvo", "kia", "mg"]
for mk in make:
    for i in range(100):
        url = "https://www.olx.in/api/relevance/search?category=84&facet_limit=100&location=1000001&location_facet_limit=20&page=" + str(i) + "&make=" + mk + "&user=16c51545605x55b78a6c"
        dataFromFunction = get_data_from_url(url)
        cumulativeCarData += dataFromFunction[0]
        print(i+1, "th page completed")
        df = pandas.DataFrame(cumulativeCarData)
        df.index += 1
        df.to_csv("Olx-Scraped_data.csv", mode='a', header=False, index=False)
        if not dataFromFunction[1]:
            break

