import enum

import requests
import pandas as pd

from dataclasses import dataclass
from typing import Tuple, TypedDict
from enum import Enum

from bs4 import BeautifulSoup
from django.conf import settings

URL = "https://site.centraldispatch.com/protected/cargo/sample-prices-lightbox"


class Type:
    class VehicleType(Enum):
        Boat = "Boat"
        Car = "Car"
        ATV = "ATV"
        Heavy_Equipment = "Heavy Equipment"
        Large_Yacht = "Large Yacht"
        Motorcycle = "Motorcycle"
        Pickup = "Pickup"
        RV = "RV"
        SUV = "SUV"
        Travel_Trailer = "Travel Trailer"
        Van = "Van"
        Other = "Other"

    @dataclass
    class CentralDispatchForm:
        postalCode: Tuple[str, str]
        enclosed: bool
        num_vehicles: int
        vehicleType: Enum

    class Params(TypedDict):
        num_vehicles: int
        ozip: int
        dzip: int
        enclosed: int
        inop: int
        vehicle_types: str
        miles: int
        custom_key: str


class CentralDispatch:
    def __init__(self, url, cookies=None, headers=None):
        self.url = url
        self.cookies = cookies if cookies else {
            "PHPSESSID": settings.CD_SESSID
        }
        self.headers = headers if headers else {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }

    def __get_page_content(self, params):
        with requests.Session() as s:
            s.cookies.update(self.cookies)
            s.get(self.url, headers=self.headers, params=params)
            response = s.get(self.url, headers=self.headers, params=params)
            response.raise_for_status()

            with open('data.html', 'w', encoding='utf-8') as file:
                file.write(response.text)
            return response.text

    def __parse_listing(self, html_content):
        soup = BeautifulSoup(html_content, 'lxml')

        table = soup.find_all('div', class_='table-responsive')

        if table:
            table = table[0]
            return table

    def parse(self, form: Type.CentralDispatchForm):
        params: Type.Params = {
            'num_vehicles': 1,
            'ozip': form.postalCode[0],
            'dzip': form.postalCode[1],
            'enclosed': int(form.enclosed),
            'inop': 0,
            'vehicle_types': form.vehicleType.value,
            'miles': 0,
            '66699bb89ee85': '66699bb89ee87'
        }
        html_content = self.__get_page_content(params)
        table = self.__parse_listing(html_content)
        if table:
            df = pd.read_html(str(table))
            df0: pd.DataFrame = df[0]
            data = df0.to_dict()
            return data
        else:
            return dict()


def get_central_dispatch_price(o_zip, d_zip, enclosed: bool, vehicle_type: enum, vehicles_count: int):
    cd_vehicle_type = Type.VehicleType.Car
    for t in Type.VehicleType:
        if t.value.lower() == vehicle_type:
            cd_vehicle_type = t.value

    form = Type.CentralDispatchForm(
        postalCode=(o_zip, d_zip),
        enclosed=enclosed,
        vehicleType=cd_vehicle_type,
        num_vehicles=vehicles_count
    )

    return CentralDispatch(URL).parse(form)
