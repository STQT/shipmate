from dataclasses import dataclass
from typing import Literal
import datetime
import os
import time
from playwright.sync_api import Page
import csv
import re
import logging
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

logger_handler = logging.StreamHandler()

logger.addHandler(logger_handler)


PLAYWRIGHT_WS_URL = "ws://playwright_ocean:53333/playwright"

@dataclass
class FieldValuesDestinationOrigin:
    orderId: str = ""
    companyName: str = ""
    originAddress1: str = ""
    originContact: str = ""
    originPhone1: str = ""
    originPhone2: str = ""
    originPhone3: str = ""
    originCompanyName: str = ""
    originBuyerNumber: str = ""
    originAddress2: str = ""
    originCity: str = ""
    OriginState: str = ""
    originZip: str = ""
    destinationContact: str = ""
    destinationPhone1: str = ""
    destinationPhone2: str = ""
    destinationPhone3: str = ""
    destinationCompanyName: str = ""
    destinationBuyerNumber: str = ""
    destinationAddress1: str = ""
    destinationAddress2: str = ""
    destinationCity: str = ""
    destinationState: str = ""
    destinationZip: str = ""


@dataclass
class VehicleInformation:
    ymmRadio: Literal[0, 1]
    ymmVehicleYear: int
    ymmMake: str
    ymmModel: str
    ymmVehicleType: Literal[
        'ATV', 'Boat', 'Car', 'Heavy Equipment', 'Large Yacht', 'Motorcycle', 'Pickup', 'RV', 'SUV', 'Travel Trailer', 'Van', 'Other']
    qty: str = ''


@dataclass
class FieldValuesVehicleInformation:
    notRunningRadio: Literal[0, 1]
    selTrailerType: Literal['Open', 'Enclosed', 'Driveaway']
    vehicles: list[VehicleInformation]


@dataclass
class FieldValuesPickupDelivDates:
    dateAvailable: str  # date in format dd/mm/yyyy
    datePickup: str  # date in format dd/mm/yyyy
    dateDelivery: str  # date in format dd/mm/yyyy
    datePickupType: Literal['Estimated', 'Exactly', 'No Earlier Than', 'No Later Than']
    dateDeliveryType: Literal['Estimated', 'Exactly', 'No Earlier Than', 'No Later Than']


@dataclass
class FieldValuesPricingAndPayments:
    minPayPrice: str
    codAmount: str
    cod_payment_method: Literal['Cash/Certified Funds', 'Check']
    cod_where: Literal['D', 'P']


@dataclass
class FieldValuesAdditionalInformation:
    txtOrderId: str
    balancePaymentMethod: Literal['Cash', 'Certified Funds', 'Company Check', 'Comchek', 'TCH']
    balanceTime: Literal[
        'immediately', '2 business days (Quick Pay)', '5 business days', '10 business days', '15 business days', '30 business days']
    balanceWhere: Literal['pickup', 'delivery', 'receiving a signed Bill of Lading']
    additionalInfo: str = ''
    dispatchCustomerNotes: str = ''


class Dispatch:
    def __init__(self,
                 fieldValuesDestinationOrigin: FieldValuesDestinationOrigin,
                 fieldValuesVehicleInformation: FieldValuesVehicleInformation,
                 fieldValuesPickupDelivDates: FieldValuesPickupDelivDates,
                 fieldValuesPricingAndPayments: FieldValuesPricingAndPayments,
                 fieldValuesAdditionalInformation: FieldValuesAdditionalInformation):
        self.fieldValuesDestinationOrigin = fieldValuesDestinationOrigin
        self.fieldValuesVehicleInformation = fieldValuesVehicleInformation
        self.fieldValuesPickupDelivDates = fieldValuesPickupDelivDates
        self.fieldValuesPricingAndPayments = fieldValuesPricingAndPayments
        self.fieldValuesAdditionalInformation = fieldValuesAdditionalInformation

    def request(self):
        with sync_playwright() as p:
            browser = p.chromium.connect(PLAYWRIGHT_WS_URL)
            context = browser.new_context(viewport={"width": 1280, "height": 1280})
            self.page = context.new_page()
            self.page.goto('https://site.centraldispatch.com')
            self.page.context.add_cookies([{"name": "PHPSESSID", "value": "d8c31e17ad2af8e81f1d44f804022f7d",
                                            "path": '/', "domain": '.site.centraldispatch.com'}])
            self.page.goto('https://site.centraldispatch.com/protected/cargo/')
            self.page.goto('https://site.centraldispatch.com/protected/cargo/my-vehicles')
            searchSelector = self.page.wait_for_selector('//*[@id="searchForm"]/div[1]/select')
            searchInput = self.page.query_selector('//*[@id="searchText"]')
            searchSelector.select_option('order_id')
            searchInput.fill(self.fieldValuesDestinationOrigin.orderId)

            searchSubmitButton = self.page.wait_for_selector('//*[@id="table-search-submit"]')
            searchSubmitButton.click()

            editButton = self.page.wait_for_selector(
                '//html/body/div[1]/div/form/div/table/tbody/tr/td[8]//a[contains(., "Assign")]')
            editButton.click()

            carrierCompanyNameInput = self.page.wait_for_selector('input#carrier_companyName')
            carrierCompanyNameInput.fill(self.fieldValuesDestinationOrigin.companyName)
            autocompleteSelector = self.page.wait_for_selector('ul#carrier_companyName_autocomplete')
            autocompleteSelector.query_selector('//li[1]').click()

            self._fillInputsByType('origin')
            self._fillInputsByType('destination')
            self._fillVehicleInformation()
            self._fillPickupDelivDates()
            self._fillPricingAndPayments()
            self._fillAdditionalInformation()

            self.page.click('input#acknowledge')
            self.page.click('input#submitListing')

            return True

    def _fillInputsByType(self, type):
        fieldsList = ['contact', 'address1', 'phone1', 'phone2', 'phone3', 'companyName', 'buyerNumber']
        if type == 'origin':
            for field in fieldsList:
                fieldKey = 'origin' + str.capitalize(field)
                fieldValue = getattr(self.fieldValuesDestinationOrigin, fieldKey, None)
                if fieldValue:
                    originField = 'input#origin_' + field
                    fieldToFill = self.page.wait_for_selector(originField)
                    fieldToFill.fill(fieldValue)
        if type == 'destination':
            for field in fieldsList:
                fieldKey = 'destination' + str.capitalize(field)
                fieldValue = getattr(self.fieldValuesDestinationOrigin, fieldKey, None)
                if fieldValue:
                    destinationField = 'input#destination_' + field
                    self.page.wait_for_selector(destinationField)
                    fieldToFill = self.page.query_selector(destinationField)
                    fieldToFill.fill(fieldValue)

    def _fillVehicleInformation(self):
        notRunningSelector = f'input#notRunningRadio0' if self.fieldValuesVehicleInformation.notRunningRadio == 0 else f'input#runningRadio0'
        self.page.click(notRunningSelector)
        trailerTypeSelector = f'select#selTrailerType'
        self.page.select_option(trailerTypeSelector, self.fieldValuesVehicleInformation.selTrailerType)
        for idx, vehicle in enumerate(self.fieldValuesVehicleInformation.vehicles):

            ymmSelector = f'input#ymmRadio{idx}' if vehicle.ymmRadio == 1 else f'input#vinRadio{idx}'
            self.page.click(ymmSelector)

            self.page.fill(f'input#ymmVehicleYear{idx}', str(vehicle.ymmVehicleYear))
            self.page.fill(f'input#ymmMake{idx}', vehicle.ymmMake)
            self.page.fill(f'input#ymmModel{idx}', vehicle.ymmModel)
            self.page.select_option(f'select#ymmVehicleType{idx}', vehicle.ymmVehicleType)
            self.page.fill(f'input#qty{idx}', vehicle.qty)
            if len(self.fieldValuesVehicleInformation.vehicles) == idx + 1:
                return
            self.page.click('a.addVehicle.btn.btn-default.btn-lg')

    def _fillPickupDelivDates(self):

        self.page.evaluate(
            f'document.querySelector("input#dateAvailable").value = "{self.fieldValuesPickupDelivDates.dateAvailable}"')
        self.page.evaluate(
            f'document.querySelector("input#datePickup").value = "{self.fieldValuesPickupDelivDates.datePickup}"')
        self.page.evaluate(
            f'document.querySelector("input#dateDelivery").value = "{self.fieldValuesPickupDelivDates.dateDelivery}"')

        self.page.select_option('select#datePickupType', self.fieldValuesPickupDelivDates.datePickupType)
        self.page.select_option('select#dateDeliveryType', self.fieldValuesPickupDelivDates.dateDeliveryType)

    def _fillPricingAndPayments(self):
        self.page.fill('input#minPayPrice', self.fieldValuesPricingAndPayments.minPayPrice)
        self.page.fill('input#codAmount', self.fieldValuesPricingAndPayments.codAmount)
        self.page.select_option('select#cod_payment_method', self.fieldValuesPricingAndPayments.cod_payment_method)
        self.page.select_option('select#cod_where', self.fieldValuesPricingAndPayments.cod_where)

    def _fillAdditionalInformation(self):
        self.page.fill('input#txtOrderId', self.fieldValuesAdditionalInformation.txtOrderId)
        self.page.fill('input#additionalInfo', self.fieldValuesAdditionalInformation.additionalInfo)
        self.page.fill('textarea#dispatchCustomerNotes', self.fieldValuesAdditionalInformation.dispatchCustomerNotes)
        self.page.select_option('select#balancePaymentMethod',
                                self.fieldValuesAdditionalInformation.balancePaymentMethod)
        self.page.select_option('select#balanceTime', self.fieldValuesAdditionalInformation.balanceTime)
        self.page.select_option('select#balanceWhere', self.fieldValuesAdditionalInformation.balanceWhere)


if __name__ == '__main__':
    fieldValuesDestinationOrigin = FieldValuesDestinationOrigin(
        orderId='4488',
        companyName='Mate Logistics Inc',
        originAddress1='123 Main St',
        originContact='John Doe',
        originPhone1='555-1234',
        originPhone2='555-5678',
        originPhone3='555-8765',
        originCompanyName='test',
        originBuyerNumber='987654321',
        destinationContact='Jane Doe',
        destinationPhone1='555-4321',
        destinationPhone2='555-8765',
        destinationPhone3='555-5678',
        destinationCompanyName='Some Company',
        destinationBuyerNumber='123456789'
    )

    vehicleInformation0 = VehicleInformation(
        ymmRadio=1,
        ymmVehicleYear=2020,
        ymmMake='Toyota',
        ymmModel='Camry',
        ymmVehicleType='Car',
        qty='1'
    )

    vehicleInformation1 = VehicleInformation(
        ymmRadio=1,
        ymmVehicleYear=2020,
        ymmMake='Toyota',
        ymmModel='Camry',
        ymmVehicleType='Car',
        qty='1'
    )

    fieldValuesVehicleInformation = FieldValuesVehicleInformation(
        notRunningRadio=1,
        selTrailerType='Enclosed',
        vehicles=[vehicleInformation0, vehicleInformation1])

    fieldValuesPickupDelivDates = FieldValuesPickupDelivDates(
        dateAvailable='07/30/2024',
        datePickup='07/31/2024',
        dateDelivery='07/31/2024',
        datePickupType='Estimated',
        dateDeliveryType='Exactly'
    )

    fieldValuesPricingAndPayments = FieldValuesPricingAndPayments(
        minPayPrice='1000',
        codAmount='500',
        cod_payment_method='Cash/Certified Funds',
        cod_where='D'
    )

    fieldValuesAdditionalInformation = FieldValuesAdditionalInformation(
        txtOrderId='30519426-ob',
        additionalInfo='Additional information here.',
        dispatchCustomerNotes='Customer notes here.',
        balancePaymentMethod='Cash',
        balanceTime='immediately',
        balanceWhere='pickup'
    )

    dispatch = Dispatch(
        fieldValuesDestinationOrigin,
        fieldValuesVehicleInformation,
        fieldValuesPickupDelivDates,
        fieldValuesPricingAndPayments,
        fieldValuesAdditionalInformation
    )

    dispatch.request()
