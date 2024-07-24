from itertools import chain

from django.db import models
from django.db.models import Q, Value
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shipmate.contrib.centraldispatch import get_central_dispatch_price
from shipmate.contrib.models import TrailerTypeChoices
from shipmate.leads.models import Leads
from shipmate.mails.data import static_dict
from shipmate.mails.serializers import ModulesListSerializer, CDPriceSerializer, GlobalSearchSerializer, \
    GlobalSearchIDSerializer, CDPOSTPriceSerializer
from shipmate.orders.models import Order
from shipmate.quotes.models import Quote


class StaticDictView(APIView):
    serializer_class = ModulesListSerializer(many=True)

    def get(self, request):
        serializer_data = ModulesListSerializer(static_dict, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)


class GetCDPriceAPIView(APIView):
    serializer_class = CDPriceSerializer

    def get(self, request, obj, guid):
        obj_mapper = {
            "quote": Quote,
            "leads": Leads,
            "order": Order
        }
        reverse_relation_mapper = {
            "quote": "quote_vehicles",
            "leads": "lead_vehicles",
            "order": "order_vehicles"
        }
        try:
            rel_obj: Leads = obj_mapper[obj].objects.get(guid=guid)
        except KeyError:
            return Response({"obj": ["Select only from: quote, leads, order"]}, status=status.HTTP_400_BAD_REQUEST)
        except obj_mapper[obj].DoesNotExist:
            return Response({"obj": ["Object does not exists from DB"]}, status=status.HTTP_404_NOT_FOUND)

        vehicles_list = getattr(rel_obj, reverse_relation_mapper[obj])
        data = get_central_dispatch_price(
            rel_obj.origin.zip,
            rel_obj.destination.zip,
            False if rel_obj.trailer_type == TrailerTypeChoices.OPEN else True,
            vehicles_list.all()[0].vehicle.vehicle_type if vehicles_list.all() else "car",
            vehicles_list.count()
        )
        collected_data = {  # noqa
            'cargo': [],
            'route': [],
            'price': [],
            'accepted': [],
            'comparable': [],
            'title': ""
        }
        for i in data:
            for j in data[i]:
                if j == 5:
                    continue
                key = self.set_dict_key(i)
                collected_data[key].append(data[i][j])
            collected_data['title'] = i
        if not collected_data:
            return Response({"nodata": ["CD Price doesnt return data"]}, status=status.HTTP_204_NO_CONTENT)
        serializer_data = self.serializer_class(collected_data)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    def set_dict_key(self, key):
        mapper = {
            "Cargo": "cargo",
            "Route": "route",
            "Price": "price",
            "Accepted by Carrier?": "accepted"
        }
        try:
            return mapper[key]
        except KeyError:
            return "comparable"


class GetCDPricePOSTAPIView(APIView):
    serializer_class = CDPOSTPriceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            origin_zip = validated_data['origin_zip']
            destination_zip = validated_data['destination_zip']
            trailer_type = validated_data['trailer_type']
            vehicle_type = validated_data['vehicle_type']
            vehicles_length = validated_data['vehicles_length']

            data = get_central_dispatch_price(
                origin_zip,
                destination_zip,
                False if trailer_type == TrailerTypeChoices.OPEN else True,
                vehicle_type.lower(),
                vehicles_length
            )
            collected_data = {
                'cargo': [],
                'route': [],
                'price': [],
                'accepted': [],
                'comparable': [],
                'title': ""
            }
            for i in data:
                for j in data[i]:
                    if j == 5:
                        continue
                    key = self.set_dict_key(i)
                    collected_data[key].append(data[i][j])
                collected_data['title'] = i
            if not collected_data:
                return Response({"nodata": ["CD Price doesnt return data"]}, status=status.HTTP_204_NO_CONTENT)
            serializer_data = self.serializer_class(collected_data)
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def set_dict_key(self, key):
        mapper = {
            "Cargo": "cargo",
            "Route": "route",
            "Price": "price",
            "Accepted by Carrier?": "accepted"
        }
        try:
            return mapper[key]
        except KeyError:
            return "comparable"


class GlobalSearchAPIView(APIView):
    serializer_class = GlobalSearchSerializer

    def _get_content(self, klass, query, status):
        query = query.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        q_objects = (Q(origin__name__icontains=query) |  # noqa
                     Q(origin__state__name__icontains=query) |
                     Q(destination__name__icontains=query) |
                     Q(destination__state__name__icontains=query) |
                     Q(customer__name__icontains=query) |
                     Q(customer__email__icontains=query) |
                     Q(customer__phone__icontains=query))

        if query.isdigit():
            q_objects |= Q(id=query)
        queryset = klass.objects.select_related(
            'origin', 'destination', 'customer', 'user', 'extra_user'
        ).filter(q_objects).annotate(
            status_type=Value(status, output_field=models.CharField())
        )[:10]
        return queryset

    def get(self, request, type, q, *args, **kwargs):
        status_type = type
        leads = self.get_leads(q)
        quotes = self.get_quotes(q)
        orders = self.get_orders(q)
        data = {
            "data": []
        }
        if status_type == "all":
            data["data"] = list(chain(leads, quotes, orders))
        elif status_type == "orders":
            data['data'] = orders
        elif status_type == "quotes":
            data['data'] = quotes
        elif status_type == "leads":
            data['data'] = leads
        serializer = self.serializer_class(data)

        return Response(serializer.data)

    def get_orders(self, query):
        return self._get_content(Order, query, "Orders")

    def get_quotes(self, query):
        return self._get_content(Quote, query, "Quotes")

    def get_leads(self, query):
        return self._get_content(Leads, query, "Leads")


class GlobalSearchIDAPIView(APIView):
    serializer_class = GlobalSearchIDSerializer

    def _get_content(self, klass, query):
        queryset = klass.objects.filter(pk=query).exists()
        return queryset

    def get(self, request, pk, *args, **kwargs):
        leads = self.get_leads(pk)
        quotes = self.get_quotes(pk)
        orders = self.get_orders(pk)

        serializer = self.serializer_class({
            'leads': leads,
            'quotes': quotes,
            'orders': orders
        })

        return Response(serializer.data)

    def get_orders(self, query):
        return self._get_content(Order, query)

    def get_quotes(self, query):
        return self._get_content(Quote, query)

    def get_leads(self, query):
        return self._get_content(Leads, query)
