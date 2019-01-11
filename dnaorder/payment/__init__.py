from rest_framework import serializers
from dnaorder.models import Submission
from dnaorder.dafis import validate_dafis

PAYMENT_TYPES = [Submission.PAYMENT_UC,Submission.PAYMENT_WIRE_TRANSFER,Submission.PAYMENT_PO]
class UCDPaymentSerializer(serializers.Serializer):
    payment_type = serializers.CharField()
    payment_info = serializers.CharField(allow_null=True, allow_blank=True, default='')
    def validate(self, data):
        payment_type = data.get('payment_type')
        payment_info = data.get('payment_info')
        if payment_type == Submission.PAYMENT_CREDIT_CARD and payment_info:
            raise serializers.ValidationError({"payment_info":"Do not enter anything into payment info when choosing credit card!"})
        elif payment_type == Submission.PAYMENT_DAFIS:
            if not validate_dafis(payment_info):
                raise serializers.ValidationError({"payment_info":"The account is invalid.  Please ensure that the chart and account are valid and in the form 'chart-account'."})
        elif payment_type in [Submission.PAYMENT_UC,Submission.PAYMENT_WIRE_TRANSFER,Submission.PAYMENT_PO] and not payment_info:
            raise serializers.ValidationError({"payment_info":"Please enter payment details."})
        return data