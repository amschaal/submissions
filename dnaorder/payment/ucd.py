from rest_framework import serializers
from dnaorder.dafis import validate_dafis
from dnaorder.payment import PaymentType

class UCDPaymentSerializer(serializers.Serializer):
    payment_type = serializers.CharField(required=False)
    payment_info = serializers.CharField(required=False)
    def validate(self, data):
        from dnaorder.models import Submission
        PAYMENT_TYPES = [Submission.PAYMENT_UC,Submission.PAYMENT_WIRE_TRANSFER,Submission.PAYMENT_PO]
        payment_type = data.get('payment_type')
        payment_info = data.get('payment_info')
        if not payment_type:
            raise serializers.ValidationError({"payment_type":"Please choose a payment type"})
        if payment_type == Submission.PAYMENT_CREDIT_CARD and payment_info:
            raise serializers.ValidationError({"payment_info":"Do not enter anything into payment info when choosing credit card!"})
        elif payment_type == Submission.PAYMENT_DAFIS:
            if not validate_dafis(payment_info):
                raise serializers.ValidationError({"payment_info":"The account is invalid.  Please ensure that the chart and account are valid and in the form 'chart-account'."})
        elif payment_type in [Submission.PAYMENT_UC,Submission.PAYMENT_WIRE_TRANSFER,Submission.PAYMENT_PO] and not payment_info:
            raise serializers.ValidationError({"payment_info":"Please enter payment details."})
        return data

class UCDPaymentType(PaymentType):
    id = 'UCDPaymentType'
    name = 'UC Davis Payment'
    serializer = UCDPaymentSerializer