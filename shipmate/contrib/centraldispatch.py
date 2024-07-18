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
        Boat = "boat"
        Car = "car"
        ATV = "atv"
        Heavy_Equipment = "heavy equipment"
        Large_Yacht = "large yacht"
        Motorcycle = "motorcycle"
        Pickup = "pickup"
        RV = "rv"
        SUV = "suv"
        Travel_Trailer = "travel trailer"
        Van = "van"
        Other = "other"

        ATV_UTV = "atv_utv"
        HEAVY_DUP = "heavy_equipment"
        PICKUP_CREW_CAB = "pickup crew cab"
        PICKUP_EXTD_CAB = "pickup extd. cab"
        PickupFullSize = "pickup full-size"
        PickupSmall = "pickup small"
        RVTrailer = "rv_trailer"
        Hatchback = "hatchback"
        GolfCart = "golf_cart"
        CONVERTIBLE = "convertible"
        COUPE = "coupe"
        Sedan = "sedan"
        SedanLarge = "sedan large"
        SedanMidsize = "sedan midsize"
        SEDANSMALL = "sedan small"
        SUVLARGE = "suv large"
        SUVMidSize = "suv mid-size"
        SUVSmall = "suv small"
        MINIVAN = "mini-van"
        VANEXTDLENGTH = "van extd. length"
        VANFULLSIZE = "van full-size"
        VanMini = "van mini"
        VanMinivan = "van/minivan"
        VehicleType = "car"
        Wagon = "wagon"

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
        Type.VehicleType.Car.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.Boat.value: CarsModel.VehicleTYPES.BOAT,
        Type.VehicleType.ATV.value: CarsModel.VehicleTYPES.ATV,
        Type.VehicleType.Large_Yacht.value: CarsModel.VehicleTYPES.LARGE,
        Type.VehicleType.Heavy_Equipment.value: CarsModel.VehicleTYPES.HEAVY,
        Type.VehicleType.Motorcycle.value: CarsModel.VehicleTYPES.MOTORCYCLE,
        Type.VehicleType.Pickup.value: CarsModel.VehicleTYPES.PICKUP,
        Type.VehicleType.RV.value: CarsModel.VehicleTYPES.RV,
        Type.VehicleType.SUV.value: CarsModel.VehicleTYPES.SUV,
        Type.VehicleType.Travel_Trailer.value: CarsModel.VehicleTYPES.TRAVEL,
        Type.VehicleType.Van.value: CarsModel.VehicleTYPES.VAN,
        Type.VehicleType.Other.value: CarsModel.VehicleTYPES.OTHER,

        Type.VehicleType.ATV_UTV.value: CarsModel.VehicleTYPES.ATV,
        Type.VehicleType.HEAVY_DUP.value: CarsModel.VehicleTYPES.HEAVY,
        Type.VehicleType.PICKUP_CREW_CAB.value: CarsModel.VehicleTYPES.PICKUP,
        Type.VehicleType.PICKUP_EXTD_CAB.value: CarsModel.VehicleTYPES.PICKUP,
        Type.VehicleType.PickupFullSize.value: CarsModel.VehicleTYPES.PICKUP,
        Type.VehicleType.PickupSmall.value: CarsModel.VehicleTYPES.PICKUP,
        Type.VehicleType.RVTrailer.value: CarsModel.VehicleTYPES.RV,
        Type.VehicleType.Hatchback.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.GolfCart.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.CONVERTIBLE.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.COUPE.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.Sedan.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.SedanLarge.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.SedanMidsize.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.SEDANSMALL.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.SUVLARGE.value: CarsModel.VehicleTYPES.SUV,
        Type.VehicleType.SUVMidSize.value: CarsModel.VehicleTYPES.SUV,
        Type.VehicleType.SUVSmall.value: CarsModel.VehicleTYPES.SUV,
        Type.VehicleType.MINIVAN.value: CarsModel.VehicleTYPES.VAN,
        Type.VehicleType.VANEXTDLENGTH.value: CarsModel.VehicleTYPES.VAN,
        Type.VehicleType.VANFULLSIZE.value: CarsModel.VehicleTYPES.VAN,
        Type.VehicleType.VanMini.value: CarsModel.VehicleTYPES.VAN,
        Type.VehicleType.VanMinivan.value: CarsModel.VehicleTYPES.VAN,
        Type.VehicleType.VehicleType.value: CarsModel.VehicleTYPES.CAR,
        Type.VehicleType.Wagon.value: CarsModel.VehicleTYPES.CAR,

    }

    form = Type.CentralDispatchForm(
        postalCode=(o_zip, d_zip),
        enclosed=enclosed,
        vehicleType=cd_vehicle_type_mapping[vehicle_type.lower()],
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
        if num > 0:
            vehicles_str += "; "
        vehicles_str += (f"{vehicle.vehicle_year}|{vehicle.vehicle.mark.name}|"
                         f"{vehicle.vehicle.name}|{vehicle.vehicle.vehicle_type}")
    text = (f"{pk},{origin.name},{origin.state.code},"
            f"{origin.zip},{destination.name},{destination.state.code},{destination.zip},"
            f"{carrier_pay:.2f},{cod_to_carrier:.2f},"
            f"{cash},1,none,{trailer_type},{condition},"
            f"{available_date.strftime('%Y-%m-%d')},{last_date.strftime('%Y-%m-%d')},{comment},{vehicles_str}*")
    return text


def _send_message_to_cd(message):
    send_mail(subject="", from_email=settings.CD_EMAIL,
              message=message, recipient_list=["cdupd-v4@centraldispatch.com"],
              auth_user=settings.CD_EMAIL, auth_password=settings.CD_EMAIL_PASSWORD
              )


def post_cd(order: Order):
    text = f"UID({settings.CD_UID})*\n"
    text += collect_cd_info(
        pk=order.pk, origin=order.origin, destination=order.destination, carrier_pay=order.payment_carrier_pay,
        cod_to_carrier=order.payment_cod_to_carrier, trailer_type=order.trailer_type, condition=order.condition,
        available_date=order.date_est_ship, last_date=order.date_est_ship, comment=order.cd_note,
        vehicles=order.order_vehicles.all(), is_cash=True
    )
    _send_message_to_cd(text)
    logging.info(f"Sended to CD: {order.pk}")


def repost_cd(order: Order):
    text = f"UID({settings.CD_UID})*\n"
    text += f"DELETE({order.pk})*\n"
    text += collect_cd_info(
        pk=order.pk, origin=order.origin, destination=order.destination, carrier_pay=order.payment_carrier_pay,
        cod_to_carrier=order.payment_cod_to_carrier, trailer_type=order.trailer_type, condition=order.condition,
        available_date=order.date_est_ship, last_date=order.date_est_ship, comment=order.cd_note,
        vehicles=order.order_vehicles.all(), is_cash=True
    )
    _send_message_to_cd(text)
    logging.info(f"Reposted to CD: {order.pk}")


def delete_cd(order: Order):
    text = f"UID({settings.CD_UID})*\n"
    text += f"DELETE({order.pk})*"
    _send_message_to_cd(text)
    logging.info(f"Deleted to CD: {order.pk} | {text}")
