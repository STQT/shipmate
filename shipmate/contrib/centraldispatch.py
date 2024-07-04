import enum
import logging

import requests
import pandas as pd

from dataclasses import dataclass
from typing import Tuple, TypedDict, List
from enum import Enum

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.mail import send_mail

from shipmate.addresses.models import City
from shipmate.cars.models import CarsModel
from shipmate.contrib.models import ConditionChoices
from shipmate.leads.models import LeadVehicles
from shipmate.orders.models import Order

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
    cd_vehicle_type_mapping = {
        Type.VehicleType.Car: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.Boat: CarsModel.VehicleTYPES.BOAT,
        Type.VehicleType.ATV: CarsModel.VehicleTYPES.ATV,
        Type.VehicleType.Large_Yacht: CarsModel.VehicleTYPES.LARGE,
        Type.VehicleType.Heavy_Equipment: CarsModel.VehicleTYPES.HEAVY,
        Type.VehicleType.Motorcycle: CarsModel.VehicleTYPES.MOTORCYCLE,
        Type.VehicleType.Pickup: CarsModel.VehicleTYPES.PICKUP,
        Type.VehicleType.RV: CarsModel.VehicleTYPES.RV,
        Type.VehicleType.SUV: CarsModel.VehicleTYPES.SUV,
        Type.VehicleType.Travel_Trailer: CarsModel.VehicleTYPES.TRAVEL,
        Type.VehicleType.Van: CarsModel.VehicleTYPES.VAN,
        Type.VehicleType.Other: CarsModel.VehicleTYPES.OTHER,

    }

    form = Type.CentralDispatchForm(
        postalCode=(o_zip, d_zip),
        enclosed=enclosed,
        vehicleType=cd_vehicle_type_mapping[vehicle_type],
        num_vehicles=vehicles_count
    )

    return CentralDispatch(URL).parse(form)


def collect_cd_info(pk, origin: City, destination: City, carrier_pay: int,
                    cod_to_carrier: int, trailer_type, condition,
                    available_date, last_date, comment, vehicles: List[LeadVehicles],
                    is_cash=True):
    cash = "cash/certified funds" if is_cash else "check"
    condition = "operable" if condition == ConditionChoices.DRIVES else "inop"
    vehicles_str = ""
    for num, vehicle in enumerate(vehicles):
        if num > 1:
            vehicles_str += ";"
        vehicles_str += (f"{vehicle.vehicle_year}|{vehicle.vehicle.mark.name}|"
                         f"{vehicle.vehicle.name}|{vehicle.vehicle.vehicle_type}")
    text = (f"{pk},{origin.name},{origin.state.code},"
            f"{origin.zip},{destination.name},{destination.state.code},{destination.zip},"
            f"{carrier_pay:.2f},{cod_to_carrier:.2f},"
            f"{cash},1,none,{trailer_type},{condition},"
            f"{available_date.strftime('%Y-%m-%d')},{last_date.strftime('%Y-%m-%d')},{comment},{vehicles_str}*")
    return text


def post_cd(order: Order):
    text = f"UID({settings.CD_UID})*\n"
    text += collect_cd_info(
        pk=order.pk, origin=order.origin, destination=order.destination, carrier_pay=order.payment_carrier_pay,
        cod_to_carrier=order.payment_cod_to_carrier, trailer_type=order.trailer_type, condition=order.condition,
        available_date=order.date_est_ship, last_date=order.date_est_ship, comment=order.cd_note,
        vehicles=order.order_vehicles.all(), is_cash=True
    )
    x = send_mail(subject="", from_email=settings.CD_EMAIL,
                  message=text, recipient_list=["cdupd-v4@centraldispatch.com"],
                  auth_user=settings.CD_EMAIL, auth_password=settings.CD_EMAIL_PASSWORD
                  )
    logging.info(f"Sended to CD: {order.pk} | {x}")


def repost_cd(order: Order):
    text = f"UID({settings.CD_UID})*\n"
    text += f"DELETE({order.pk})*\n"
    text += collect_cd_info(
        pk=order.pk, origin=order.origin, destination=order.destination, carrier_pay=order.payment_carrier_pay,
        cod_to_carrier=order.payment_cod_to_carrier, trailer_type=order.trailer_type, condition=order.condition,
        available_date=order.date_est_ship, last_date=order.date_est_ship, comment=order.cd_note,
        vehicles=order.order_vehicles.all(), is_cash=True
    )
    logging.info(f"Reposted to CD: {order.pk} | {text}")


def delete_cd(order: Order):
    text = f"UID({settings.CD_UID})*\n"
    text += f"DELETE({order.pk})*"
    logging.info(f"Deleted to CD: {order.pk} | {text}")

