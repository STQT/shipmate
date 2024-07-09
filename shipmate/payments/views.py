from rest_framework import status
from rest_framework.generics import (
    ListAPIView, CreateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderPayment, OrderPaymentAttachment
from .serializers import CreateOrderPaymentSerializer, OrderPaymentSerializer, \
    SigningContractSerializer, DetailContractSerializer, CreateOrderPaymentAttachmentListSerializer, \
    OrderPaymentAttachmentSerializer


class CreateOrderPaymentAPIView(CreateAPIView):  # noqa
    queryset = OrderPayment.objects.all()
    serializer_class = CreateOrderPaymentSerializer


class ListOrderPaymentView(ListAPIView):  # noqa
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        order_guid = self.kwargs.get('order')
        queryset = self.filter_queryset(self.get_queryset().filter(order__guid=order_guid))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SignOrderPaymentView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SigningContractSerializer

    # def post(self, request, order, contract):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         agreement = serializer.validated_data.pop('agreement')
    #         terms = serializer.validated_data.pop('terms')
    #         try:
    #             contract_obj = OrderPayment.objects.get(id=contract)
    #         except OrderPayment.DoesNotExist:
    #             logger.error(f"OrderPayment with id {contract} not found")
    #             return Response({'error': 'OrderPayment not found'}, status=status.HTTP_404_NOT_FOUND)
    #
    #         order_obj: Order = contract_obj.order
    #         if order_obj.guid != order:
    #             logger.error(f"Order with guid {order} not found")
    #             return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    #         contract_obj.signed = True
    #         contract_obj.signer_name = serializer.validated_data['signer_name']
    #         contract_obj.signer_initials = serializer.validated_data['signer_initials']
    #         x_real_ip = request.META.get('HTTP_X_REAL_IP')
    #         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #         if x_forwarded_for:
    #             ip = x_forwarded_for.split(',')[0]
    #         else:
    #             ip = x_real_ip or request.META.get('REMOTE_ADDR')
    #         contract_obj.sign_ip_address = ip
    #         contract_obj.signed_time = timezone.now()
    #         contract_obj.save()
    #
    #         if order_obj.status == OrderStatusChoices.ORDERS:
    #             order_obj.status = OrderStatusChoices.BOOKED
    #             order_obj.save()
    #
    #         # Send email with ZIP attachment
    #         customer_email = order_obj.customer.email
    #
    #         email = EmailMessage(
    #             subject='Signed Contract and Terms',
    #             from_email=settings.DEFAULT_FROM_EMAIL,
    #             body='Dear Customer, please find attached the signed contract and terms.',
    #             to=[customer_email],
    #         )
    #         email.attach(agreement.name, agreement.read(), agreement.content_type)
    #         email.attach(terms.name, terms.read(), terms.content_type)
    #
    #         try:
    #             email.send()
    #             logger.info(f"Email sent successfully to {customer_email}")
    #         except Exception as e:
    #             logger.error(f"Error sending email: {e}")
    #             logger.error(f"From email: {settings.DEFAULT_FROM_EMAIL}")
    #             return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #         return Response(self.serializer_class(contract_obj).data, status=status.HTTP_200_OK)
    #
    #     logger.error(f"Invalid data: {serializer.errors}")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailOrderPaymentView(APIView):
    # serializer_class = DetailContractSerializer(many=False)
    permission_classes = [AllowAny]
    #
    # def get(self, request, order, contract):
    #     pdf_obj_mapper = {
    #         OrderPayment.TypeChoices.HAWAII: Hawaii,
    #         OrderPayment.TypeChoices.GROUND: Ground,
    #         OrderPayment.TypeChoices.INTERNATIONAL: International
    #     }
    #     try:
    #         contract_obj = OrderPayment.objects.get(id=contract)
    #     except OrderPayment.DoesNotExist:
    #         return Response({'error': 'OrderPayment not found'}, status=status.HTTP_404_NOT_FOUND)
    #     order_obj = contract_obj.order
    #     if order_obj.guid != order:
    #         return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    #     company_obj = CompanyInfo.objects.first()
    #     pdf_obj = pdf_obj_mapper[contract_obj.contract_type].objects.all().order_by('-is_default')
    #     pdf_obj = pdf_obj.first()
    #     if not pdf_obj:
    #         return Response({"error": f'Default contract not exists for {contract_obj.contract_type}'})
    #
    #     data = {
    #         'order': order_obj,
    #         'contract': contract_obj,
    #         'company': company_obj,
    #         'pdf': pdf_obj
    #     }
    #
    #     serializer = DetailContractSerializer(data)
    #     return Response(serializer.data)


class CreateOrderPaymentAttachmentView(APIView):
    serializer_class = CreateOrderPaymentAttachmentListSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateOrderPaymentAttachmentListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOrderPaymentAttachmentView(ListAPIView):
    queryset = OrderPaymentAttachment.objects.all().order_by("-id")
    serializer_class = OrderPaymentAttachmentSerializer
    filterset_fields = ["order_payment"]
    pagination_class = None
