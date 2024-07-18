import os

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.generics import (
    ListAPIView, CreateAPIView, get_object_or_404,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderPayment, OrderPaymentAttachment, OrderPaymentCreditCard
from .serializers import CreateOrderPaymentSerializer, OrderPaymentSerializer, \
    SigningContractSerializer, OrderPaymentAttachmentSerializer, ListOrderPaymentCreditCardSerializer, \
    CreateOrderPaymentCreditCardSerializer, CreateOrderPaymentClientCreditCardSerializer, \
    DetailCustomerPaymentSerializer, RefundPaymentSerializer
from ..attachments.models import FileAttachment
from ..company_management.models import CompanyInfo
from ..contrib.email import send_email
from ..contrib.models import Attachments
from ..orders.models import OrderAttachment, Order
from ..orders.utils import send_cc_agreement


class CreateOrderPaymentAPIView(CreateAPIView):  # noqa
    queryset = OrderPayment.objects.all()
    serializer_class = CreateOrderPaymentSerializer


class SendCCAToPaymentView(CreateAPIView):
    serializer_class = None

    def create(self, request, *args, **kwargs):
        payment_id = self.kwargs.get('payment')
        payment = get_object_or_404(OrderPayment, id=payment_id)
        contract = payment.order.contracts.all().first()
        if contract:
            send_cc_agreement(payment.order, payment)
            return Response(status=status.HTTP_201_CREATED)
        return Response(data={"error": "No contracts"}, status=status.HTTP_400_BAD_REQUEST)


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


class CreateOrderPaymentAttachmentView(CreateAPIView):
    serializer_class = OrderPaymentAttachmentSerializer


class RefundPaymentSerializerView(CreateAPIView):
    serializer_class = RefundPaymentSerializer


class ListOrderPaymentAttachmentView(ListAPIView):
    queryset = OrderPaymentAttachment.objects.all().order_by("-id")
    serializer_class = OrderPaymentAttachmentSerializer
    filterset_fields = ["order_payment"]
    pagination_class = None


class ListOrderPaymentCreditCardView(ListAPIView):
    queryset = OrderPaymentCreditCard.objects.all().order_by("-id")
    serializer_class = ListOrderPaymentCreditCardSerializer
    filterset_fields = ["order"]
    pagination_class = None


class CreateOrderCustomerPaymentCreditCardAPIView(CreateAPIView):  # noqa
    queryset = OrderPaymentCreditCard.objects.all()
    serializer_class = CreateOrderPaymentClientCreditCardSerializer

    def perform_create(self, serializer):
        files = {
            'sign_file': self.request.FILES.get('sign_file'),
            'cc_front_img_file': self.request.FILES.get('cc_front_img_file'),
            'cc_back_img_file': self.request.FILES.get('cc_back_img_file'),
        }
        validated_data = serializer.validated_data
        for file_field in ['cc_front_img_file', 'cc_back_img_file']:
            validated_data.pop(file_field, None)

        instance = OrderPaymentCreditCard.objects.create(**validated_data)
        self.send_email_with_attachments(instance, files)

    def send_email_with_attachments(self, instance, files):
        cc_front_img_file = files['cc_front_img_file']
        cc_back_img_file = files['cc_back_img_file']
        front_file_attachment = FileAttachment.objects.create(file=cc_front_img_file, text="Front credit card")
        back_file_attachment = FileAttachment.objects.create(file=cc_back_img_file, text="Back credit card")
        # TODO: add code for saving PDF receipt in the OrderAttachment
        OrderAttachment.objects.create(order=instance.order, link=front_file_attachment.pk,
                                       title="Front credit card", type=Attachments.TypesChoices.FILE)
        OrderAttachment.objects.create(order=instance.order, link=back_file_attachment.pk,
                                       title="Back credit card", type=Attachments.TypesChoices.FILE)

    def send_receipt(self, customer, file):
        subject = 'Receipt'
        body = 'Receipt'
        email = EmailMessage(subject, body, to=[customer])
        email.attach(file.name, file.read(), file.content_type)
        email.send()

    def send_cc(self, email, file):
        subject = 'CC'
        body = 'cc'
        email = EmailMessage(subject, body, to=[email])
        email.attach(file.name, file.read(), file.content_type)
        email.send()


class CreateOrderPaymentCreditCardAPIView(CreateAPIView):  # noqa
    queryset = OrderPaymentCreditCard.objects.all()
    serializer_class = CreateOrderPaymentCreditCardSerializer


class DetailOrderCustomerContractView(APIView):
    serializer_class = DetailCustomerPaymentSerializer(many=False)
    permission_classes = [AllowAny]

    def get(self, request, order):
        try:
            order_obj = Order.objects.get(guid=order)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        company_obj = CompanyInfo.objects.first()
        credit_card = order_obj.payments.filter(payment_type="credit_card").first()
        data = {
            'order': order_obj,
            'company': company_obj,
            'cc': True if credit_card else False
        }

        serializer = DetailCustomerPaymentSerializer(data, context={"request": request})
        return Response(serializer.data)


from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
import tempfile


def generate_pdf(request):
    # Render the HTML template
    html_string = render(request, 'pdfs/cca.html', {}).content.decode('utf-8')

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as output:
        # Convert HTML to PDF
        HTML(string=html_string).write_pdf(output.name)
        output.seek(0)

        # Define the file path to save the PDF
        save_dir = settings.MEDIA_ROOT + '/pdfs/output/'  # Change this to your desired directory
        os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
        pdf_file_path = os.path.join(save_dir, 'output.pdf')

        # Save the PDF to the defined file path
        with open(pdf_file_path, 'wb') as f:
            f.write(output.read())

        # Optionally, delete the temporary file
        os.unlink(output.name)

    return HttpResponse(f"PDF generated and saved successfully at {pdf_file_path}.")

    # with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as output:
    #     # Convert HTML to PDF
    #     HTML(string=html_string).write_pdf(output.name)
    #     output.seek(0)
    #
    #     # Return the PDF file as a response
    #     response = HttpResponse(output.read(), content_type='application/pdf')
    #     response['Content-Disposition'] = 'inline; filename="output.pdf"'
    #
    #     return response
