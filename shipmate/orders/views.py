import logging
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Prefetch
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    DestroyAPIView, CreateAPIView,
    get_object_or_404, UpdateAPIView, GenericAPIView
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import OrderFilter, OrderAttachmentFilter
from shipmate.contrib.models import OrderStatusChoices, Attachments
from shipmate.contrib.generics import UpdatePUTAPIView, RetrieveUpdatePUTDestroyAPIView
from .models import Order, OrderAttachment, OrderLog, OrderVehicles, OrderContract
from .serializers import CreateOrderSerializer, UpdateOrderSerializer, RetrieveOrderSerializer, ListOrderSerializer, \
    OrderAttachmentSerializer, VehicleOrderSerializer, CreateOrderContractSerializer, OrderContractSerializer, \
    SigningContractSerializer, DetailContractSerializer, ProviderOrderListSerializer, DispatchingOrderSerializer, \
    DirectDispatchOrderSerializer, CDActions, PostCDSerializer, ListOrdersTeamSerializer
from .utils import send_order_contract_email
from ..attachments.models import NoteAttachment, TaskAttachment, FileAttachment
from ..company_management.models import CompanyInfo
from ..contract.models import Hawaii, Ground, International
from ..contrib.centraldispatch import post_cd, repost_cd, delete_cd
from ..contrib.pagination import CustomPagination
from ..contrib.sms import send_sms
from ..contrib.timetook import timedelta_to_text
from ..contrib.views import ArchiveView, ReAssignView
from ..insights.models import LeadsInsight
from ..lead_managements.models import Provider
from ..leads.serializers import LogSerializer
from ..leads.views import ListTeamLeadAPIView
from ..quotes.models import Quote, QuoteAttachment
from ..quotes.serializers import CreateQuoteSerializer

VEHICLE_TAG = "orders/vehicle/"
ATTACHMENTS_TAG = "orders/attachments/"
CONTRACTS_TAG = "orders/contracts/"
REASON_TAG = "orders/reason/"

User = get_user_model()

logger = logging.getLogger(__name__)


class OrderPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000

    def __init__(self):
        self.sum_price = 0
        self.reservation_price = 0

    def paginate_queryset(self, queryset, request, view=None):
        self.sum_price = queryset.aggregate(
            total_price=models.Sum('price')
        )['total_price'] or 0
        self.reservation_price = queryset.aggregate(
            total_reservation_price=models.Sum('reservation_price')
        )['total_reservation_price'] or 0

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['sum_price'] = self.sum_price
        response.data['reservation_price'] = self.reservation_price
        return response

    # def get_offset(self, request):
    #
    #     try:
    #         print("BYE")
    #         return _positive_int(
    #             request.query_params[self.offset_query_param],
    #         )
    #     except (KeyError, ValueError):
    #         print("HELLO")
    #         return 1

    def get_offset(self, request):
        """
        Override to set the offset.
        """
        # Get the offset from the request query parameters
        offset = super().get_offset(request)

        # Adjust offset to start from 1 instead of 0
        return max(0, offset - 1)


class ListOrderAPIView(ListAPIView):  # noqa
    queryset = Order.objects.prefetch_related(
        "order_vehicles"
    ).select_related("origin__state", "destination__state", "customer", "user", "extra_user")
    serializer_class = ListOrderSerializer
    filterset_class = OrderFilter
    pagination_class = OrderPagination
    ordering = ("-id",)


class CreateOrderAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def perform_create(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class UpdateOrderAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    lookup_field = 'guid'

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)

        if serializer.is_valid():
            print(serializer.instance.status)
            if serializer.instance.status == 'archived':
                OrderAttachment.objects.create(
                    order=serializer.instance,
                    type=Attachments.TypesChoices.ACTIVITY,
                    title="Backed to Orders",
                    link=0,
                    user=serializer.instance.user
                )
            serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)
            try:
                lead_insight = LeadsInsight.objects.get(order_guid=serializer.instance.guid)
                lead_insight.status = serializer.instance.status
                lead_insight.source = serializer.instance.source
                lead_insight.price = serializer.instance.price
                lead_insight.reservation_price = serializer.instance.reservation_price
                lead_insight.customer = serializer.instance.customer
                lead_insight.save()
            except Exception as e:
                print(e)

            return Response(RetrieveOrderSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: RetrieveOrderSerializer})
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteOrderAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    lookup_field = 'guid'


class DetailOrderAPIView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related(
        Prefetch('order_vehicles', queryset=OrderVehicles.objects.order_by('id')),
    )
    serializer_class = RetrieveOrderSerializer
    lookup_field = 'guid'


class ArchiveListOrderAPIView(ListAPIView):
    queryset = Order.objects.filter(status=OrderStatusChoices.ARCHIVED)
    serializer_class = ListOrderSerializer


@extend_schema(tags=[ATTACHMENTS_TAG])
class OrderAttachmentListView(UpdateModelMixin, GenericAPIView):
    serializer_class = OrderAttachmentSerializer
    filterset_class = OrderAttachmentFilter

    def get_queryset(self):
        order_id = self.kwargs.get('ordersId')  # Retrieve the lead_id from URL kwargs
        return OrderAttachment.objects.prefetch_related(
            "order_attachment_comments").filter(order_id=order_id).order_by("-id")

    # List method (same as before for GET)
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Ensure it's a partial update

        # Extract attachment_id from query parameters
        attachment_id = request.query_params.get('attachment_id')

        if not attachment_id:
            return Response({"detail": "attachment_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()  # Get the queryset filtered by lead_id
        attachment = queryset.filter(pk=attachment_id).first()  # Filter using attachment_id

        if not attachment:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(attachment, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



@extend_schema(tags=[ATTACHMENTS_TAG])
class OrderAttachmentDeleteAPIView(DestroyAPIView):
    serializer_class = OrderAttachmentSerializer  # noqa

    @transaction.atomic
    def delete(self, request, id):
        order_attachment = get_object_or_404(OrderAttachment, id=id)
        order_attachment.delete()
        model_mapping = {
            'note': NoteAttachment,
            'task': TaskAttachment,
            'file': FileAttachment,
            # Add more mappings as needed
        }
        model_class = model_mapping.get(order_attachment.type)

        if not model_class:
            raise ValidationError(
                {"type": f"`{order_attachment.type}` doesn't found from allowed deleting attachment"}
            )

        attachment_instance = model_class.objects.get(id=order_attachment.link)
        attachment_instance.delete()
        return Response({'message': 'Attachment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=[VEHICLE_TAG])
class CreateVehicleOrderAPIView(CreateAPIView):  # noqa
    queryset = OrderVehicles.objects.all()
    serializer_class = VehicleOrderSerializer


@extend_schema(tags=[CONTRACTS_TAG])
class CreateOrderContractAPIView(CreateAPIView):  # noqa
    queryset = OrderContract.objects.all()
    serializer_class = CreateOrderContractSerializer

    def perform_create(self, serializer):
        order_contract = serializer.save()
        send_order_contract_email(order_contract)


@extend_schema(tags=[CONTRACTS_TAG])
class ListOrderContractView(ListAPIView):  # noqa
    queryset = OrderContract.objects.all()  # noqa
    serializer_class = OrderContractSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        order_guid = self.kwargs.get('order')
        queryset = self.filter_queryset(self.get_queryset().filter(order__guid=order_guid))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=[CONTRACTS_TAG])
class SignOrderContractView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SigningContractSerializer

    def post(self, request, order, contract):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            agreement = serializer.validated_data.pop('agreement')
            terms = serializer.validated_data.pop('terms')
            try:
                contract_obj = OrderContract.objects.get(id=contract)
            except OrderContract.DoesNotExist:
                logger.error(f"OrderContract with id {contract} not found")
                return Response({'error': 'OrderContract not found'}, status=status.HTTP_404_NOT_FOUND)

            order_obj: Order = contract_obj.order
            if order_obj.guid != order:
                logger.error(f"Order with guid {order} not found")
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
            contract_obj.signed = True
            contract_obj.signer_name = serializer.validated_data['signer_name']
            contract_obj.signer_initials = serializer.validated_data['signer_initials']
            x_real_ip = request.META.get('HTTP_X_REAL_IP')
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = x_real_ip or request.META.get('REMOTE_ADDR')
            contract_obj.sign_ip_address = ip
            contract_obj.signed_time = timezone.now()
            contract_obj.save()
            # Creating activity history
            OrderAttachment.objects.create(
                order=order_obj,
                type=Attachments.TypesChoices.ACTIVITY,
                title="Contract is signed",
                link=0,
                user=order_obj.user
            )


            if order_obj.status == OrderStatusChoices.ORDERS:
                order_obj.status = OrderStatusChoices.BOOKED
                order_obj.save()

            def save_file(file):
                file_name = f'{timezone.now().strftime("%Y%m%d%H%M%S")}_{file.name}'
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                return f'{settings.MEDIA_URL}{file_name}'

            agreement_url = save_file(agreement)
            terms_url = save_file(terms)

            # Send email with ZIP attachment
            customer_email = order_obj.customer.email
            mate_url = ''
            mate_term_url = ''
            if 'mate' in request.build_absolute_uri(agreement_url):
                mate_url = 'https://api.matelogisticss.com'+agreement_url
                mate_term_url = 'https://api.matelogisticss.com'+terms_url
            else:
                mate_url = request.build_absolute_uri(agreement_url)
                mate_term_url = request.build_absolute_uri(terms_url)

            email = EmailMessage(
                subject='Signed Contract and Terms',
                from_email=settings.SIGN_EMAIL_USERNAME,
                body=f'Dear Customer, please find the signed contract and terms at the following links:\n\n'
                     f'Agreement: {mate_url}\n'
                     f'Terms: {mate_term_url}',
                to=[customer_email],
            )
            try:
                email.send()
                logger.info(f"Email sent successfully to {customer_email}")
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                logger.error(f"From email: {settings.SIGN_EMAIL_USERNAME}")
                return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(self.serializer_class(contract_obj).data, status=status.HTTP_200_OK)

        logger.error(f"Invalid data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=[CONTRACTS_TAG])
class DetailOrderContractView(APIView):
    serializer_class = DetailContractSerializer(many=False)
    permission_classes = [AllowAny]

    def get(self, request, order, contract):
        pdf_obj_mapper = {
            OrderContract.TypeChoices.HAWAII: Hawaii,
            OrderContract.TypeChoices.GROUND: Ground,
            OrderContract.TypeChoices.INTERNATIONAL: International
        }
        try:
            contract_obj = OrderContract.objects.get(id=contract)
        except OrderContract.DoesNotExist:
            return Response({'error': 'OrderContract not found'}, status=status.HTTP_404_NOT_FOUND)
        order_obj: Order = contract_obj.order
        if order_obj.guid != order:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        company_obj = CompanyInfo.objects.first()
        pdf_obj = pdf_obj_mapper[contract_obj.contract_type].objects.all().order_by('-is_default')
        pdf_obj = pdf_obj.first()
        if not pdf_obj:
            return Response({"error": f'Default contract not exists for {contract_obj.contract_type}'})
        credit_card = order_obj.payments.filter(payment_type="credit_card").first()

        data = {
            'order': order_obj,
            'order_data': contract_obj.order_data,
            'contract': contract_obj,
            'company': company_obj,
            'pdf': pdf_obj,
            'cc': True if credit_card else False
        }

        serializer = DetailContractSerializer(data, context={"request": request})
        return Response(serializer.data)


@extend_schema(tags=[VEHICLE_TAG])
class RetrieveUpdateDestroyVehicleOrderAPIView(RetrieveUpdatePUTDestroyAPIView):  # noqa
    queryset = OrderVehicles.objects.all()
    serializer_class = VehicleOrderSerializer


@extend_schema(parameters=[
    OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY,
                     enum=OrderStatusChoices.values,
                     description='Calculating leadsCount with status', required=True),
])
class ProviderOrderListAPIView(ListAPIView):
    queryset = Provider.objects.filter(status=Provider.ProviderStatusChoices.ACTIVE)
    pagination_class = None
    serializer_class = ProviderOrderListSerializer


class DispatchingOrderCreateAPIView(UpdatePUTAPIView):
    queryset = Order.objects.all()
    serializer_class = DispatchingOrderSerializer
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.save(status=OrderStatusChoices.DISPATCHED)
        OrderAttachment.objects.create(
            order=serializer.instance,
            type=Attachments.TypesChoices.ACTIVITY,
            title=f"Moved to Dispatched through Dispatch button",
            link=0,
            user=serializer.instance.user
        )


class DirectDispatchOrderCreateAPIView(UpdatePUTAPIView):
    queryset = Order.objects.all()
    serializer_class = DirectDispatchOrderSerializer
    lookup_field = "guid"

    def perform_update(self, serializer):
        serializer.save(
            status=OrderStatusChoices.DISPATCHED,
            updated_from=self.request.user if self.request.user.is_authenticated else None
        )
        OrderAttachment.objects.create(
            order=serializer.instance,
            type=Attachments.TypesChoices.ACTIVITY,
            title=f"Moved to Dispatched through Direct Dispatch",
            link=0,
            user=serializer.instance.user
        )


class ListOrderLogAPIView(ListAPIView):
    serializer_class = LogSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        order_id = self.kwargs['order']
        return OrderLog.objects.filter(order_id=order_id)


class ConvertQuoteToOrderAPIView(CreateAPIView):
    serializer_class = CreateOrderSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        quote_id = self.kwargs.get('quote')
        quote = get_object_or_404(Quote, id=quote_id)
        serializer.save()
        quote_id = self.kwargs.get('quote')
        quote = get_object_or_404(Quote, id=quote_id)

        # Save the Order without needing to pass quote to serializer
        order = serializer.save()

        try:
            lead_insight = LeadsInsight.objects.get(quote_guid=quote.guid)
            lead_insight.status = OrderStatusChoices.ORDERS
            lead_insight.order_guid = order.guid
            lead_insight.save()
        except Exception as e:
            print(e)

        user = quote.user
        time_took = timezone.now() - quote.created_at

        # Create OrderAttachment after order is saved
        OrderAttachment.objects.create(
            order=order,
            type=Attachments.TypesChoices.ACTIVITY,
            title=f"Converted to orders",
            link=0,
            user=user,
            time_took=timedelta_to_text(time_took)
        )
        # user = User.objects.get(id=quote.user.id)
        # print(quote.created_at)
        # print(serializer)
        # time_took = timezone.now() - quote.created_at
        # OrderAttachment.objects.create(
        #     order=serializer,
        #     type=Attachments.TypesChoices.ACTIVITY,  # Assuming you have types for attachments
        #     title=f"Converted to orders",
        #     link=0,
        #     user=user,
        #     time_took=timedelta_to_text(time_took)
        # )
        quote.delete()


class BackToQuoteOrderAPIView(CreateAPIView):
    serializer_class = None

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer_class = CreateQuoteSerializer
        order_id = self.kwargs.get('order')
        order = get_object_or_404(Order, id=order_id)
        quote_data = {
            'origin': order.origin.pk,
            'destination': order.destination.pk,
            'user': order.user.pk,
            'extra_user': order.extra_user.pk if order.extra_user else None,
            'updated_from': request.user.pk if request.user.is_authenticated else None,
            'source': order.source.pk if order.source else None,
            'customer': order.customer.pk if order.customer else None
        }
        order_data = order.__dict__
        order_data['vehicles'] = []
        for order_vehicle in order.order_vehicles.all():  # noqa
            order_data['vehicles'].append(
                {"vehicle": order_vehicle.vehicle.pk, "vehicle_year": order_vehicle.vehicle_year}
            )
        order_data['status'] = 'quote'
        order_data.update(quote_data)
        quote_serializer = serializer_class(data=order_data)
        quote_serializer.is_valid(raise_exception=True)
        quote_serializer.save()
        QuoteAttachment.objects.create(
            quote=quote_serializer.instance,
            type=Attachments.TypesChoices.ACTIVITY,  # Assuming you have types for attachments
            title="Re-converted to quote",
            link=0,
            user=order.user
        )
        order.delete()

        return Response(quote_serializer.data, status=status.HTTP_201_CREATED)


class PostToCDAPIView(CreateAPIView):
    serializer_class = PostCDSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order_id = self.kwargs.get('guid')
            order = get_object_or_404(Order, guid=order_id)
            order.status = OrderStatusChoices.POSTED
            OrderAttachment.objects.create(
                order=order,
                type=Attachments.TypesChoices.ACTIVITY,
                title=f"Moved to posted",
                link=0,
                user=order.user
            )
            try:
                lead_insight = LeadsInsight.objects.get(order_guid=order.guid)
                lead_insight.status = order.status
                lead_insight.source = order.source
                lead_insight.price = order.price
                lead_insight.reservation_price = order.reservation_price
                lead_insight.customer = order.customer
                lead_insight.save()
            except Exception as e:
                print(e)
            action = serializer.data['action']
            response_data = serializer.data
            response_data['status'] = OrderStatusChoices.POSTED
            if action == CDActions.REPOST.value:
                repost_cd(order)
            elif action == CDActions.POST.value:
                post_cd(order)
            else:
                delete_cd(order)
                order.status = OrderStatusChoices.BOOKED
                OrderAttachment.objects.create(
                    order=order,
                    type=Attachments.TypesChoices.ACTIVITY,
                    title=f"Moved to Booked",
                    link=0,
                    user=order.user
                )
                try:
                    lead_insight = LeadsInsight.objects.get(order_guid=order.guid)
                    lead_insight.status = order.status
                    lead_insight.source = order.source
                    lead_insight.price = order.price
                    lead_insight.reservation_price = order.reservation_price
                    lead_insight.customer = order.customer
                    lead_insight.save()
                except Exception as e:
                    print(e)
                response_data['status'] = OrderStatusChoices.BOOKED
            order.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=[REASON_TAG])
class ReAssignOrderView(ReAssignView):
    base_class = Order
    base_attachment_class = OrderAttachment
    base_fk_field = "order"


@extend_schema(tags=[REASON_TAG])
class ArchiveOrderView(ArchiveView):
    base_class = Order
    status_choice_class = OrderStatusChoices
    base_attachment_class = OrderAttachment
    base_fk_field = "order"


@extend_schema(parameters=[OpenApiParameter('type', enum=OrderStatusChoices)])
class ListTeamOrdersAPIView(ListTeamLeadAPIView):
    serializer_class = ListOrdersTeamSerializer


class SendSmsToContract(CreateAPIView):
    serializer_class = None

    def create(self, request, *args, **kwargs):
        contract_id = self.kwargs.get('contract')
        contract = get_object_or_404(OrderContract, id=contract_id)
        user = request.user
        text = f"Please sign the contract at the link: {settings.FRONTEND_URL}/{contract.order.guid}/{contract.pk}"
        send_sms(user.phone, [contract.order.customer.phone], text)
        return Response(status=status.HTTP_201_CREATED)
