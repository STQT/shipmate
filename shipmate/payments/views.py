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
            send_cc_agreement(payment.order, payment, payment_id)
            OrderAttachment.objects.create(
                order=payment.order,
                type=Attachments.TypesChoices.ACTIVITY,
                title="CC authorization is sent",
                link=0,
                user=payment.order.user
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(data={"error": "No contracts"}, status=status.HTTP_400_BAD_REQUEST)


class ListOrderPaymentView(ListAPIView):  # noqa
    queryset = OrderPayment.objects.all()  # noqa
    serializer_class = OrderPaymentSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        order_guid = self.kwargs.get('order')
        queryset = self.filter_queryset(self.get_queryset().filter(order__guid=order_guid))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    permission_classes = [AllowAny]

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
        OrderAttachment.objects.create(
            order=instance.order,
            type=Attachments.TypesChoices.ACTIVITY,  # Assuming you have types for attachments
            title="CC authorization is filled",
            link=0,
            user=instance.order.user
        )
        self.send_email_with_attachments(instance, files)

    def send_email_with_attachments(self, instance, files):
        cc_front_img_file = files['cc_front_img_file']
        cc_back_img_file = files['cc_back_img_file']
        if cc_front_img_file:
            front_file_attachment = FileAttachment.objects.create(file=cc_front_img_file, text="Front credit card")
            OrderAttachment.objects.create(order=instance.order, link=front_file_attachment.pk,
                                           title="Front credit card", type=Attachments.TypesChoices.FILE)

        if cc_back_img_file:
            back_file_attachment = FileAttachment.objects.create(file=cc_back_img_file, text="Back credit card")
            OrderAttachment.objects.create(order=instance.order, link=back_file_attachment.pk,
                                           title="Back credit card", type=Attachments.TypesChoices.FILE)
        # TODO: add code for saving PDF receipt in the OrderAttachment

    def send_receipt(self, customer, file):
        subject = 'Receipt'
        body = 'Receipt'
        email = EmailMessage(subject, body, to=[customer])
        email.attach(file.name, file.read(), file.content_type)
        email.send()
        # receipt_attachment = FileAttachment.objects.create(file=file, text="Receipt")
        #
        # OrderAttachment.objects.create(
        #     order=instance.order,  # Access the order from the instance of OrderPaymentCreditCard
        #     type=Attachments.TypesChoices.FILE,
        #     title="Receipt",
        #     link=receipt_attachment.pk,  # Use the FileAttachment primary key as the link
        #     user=instance.order.user  # Access the user via the related Order model
        # )

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

        # Get the first OrderPayment associated with the given order
        try:
            credit_card = OrderPayment.objects.filter(order=order_obj).first()
        except OrderPayment.DoesNotExist:
            credit_card = None

        data = {
            'order': order_obj,
            'company': company_obj,
            'cc': True if credit_card else False,
            'payment': None
        }

        if credit_card:
            data['payment'] = {
                "amount": credit_card.amount,
                "surcharge_fee_rate": credit_card.surcharge_fee_rate,
                "discount": credit_card.discount
            }

        serializer = DetailCustomerPaymentSerializer(data, context={"request": request})
        return Response(serializer.data)


class DetailOrderCustomerPaymentView(APIView):
    serializer_class = DetailCustomerPaymentSerializer(many=False)
    permission_classes = [AllowAny]

    def get(self, request, order, payment_id):
        try:
            order_obj = Order.objects.get(guid=order)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        company_obj = CompanyInfo.objects.first()

        credit_card: OrderPayment = OrderPayment.objects.filter(pk=payment_id).first()

        data = {
            'order': order_obj,
            'company': company_obj,
            'cc': True if credit_card else False,
            'payment': None
        }
        if credit_card:
            data['payment'] = {
                "amount": credit_card.amount,
                "surcharge_fee_rate": credit_card.surcharge_fee_rate,
                "discount": credit_card.discount
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
