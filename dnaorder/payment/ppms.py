from rest_framework import serializers
from dnaorder.payment import PaymentType

class PPMSPaymentSerializer(serializers.Serializer):
    pi_email= serializers.CharField()
    display = serializers.SerializerMethodField(read_only=True)
    def get_display(self, obj):
        return {'PPMS PI Email': obj.get('pi_email','')}
    def validate(self, data):
        if not data.get('pi_email', None):
            raise serializers.ValidationError({"pi_email":"PPMS PI Email is required."})
#         raise serializers.ValidationError({"pi_email":"Bad email."})
        return data
#         from dnaorder.models import Submission
#         PAYMENT_TYPES = [Submission.PAYMENT_UC,Submission.PAYMENT_WIRE_TRANSFER,Submission.PAYMENT_PO]
#         payment_type = data.get('payment_type')
#         payment_info = data.get('payment_info')
#         if payment_type == Submission.PAYMENT_CREDIT_CARD and payment_info:
#             raise serializers.ValidationError({"payment_info":"Do not enter anything into payment info when choosing credit card!"})
#         elif payment_type == Submission.PAYMENT_DAFIS:
#             if not validate_dafis(payment_info):
#                 raise serializers.ValidationError({"payment_info":"The account is invalid.  Please ensure that the chart and account are valid and in the form 'chart-account'."})
#         elif payment_type in [Submission.PAYMENT_UC,Submission.PAYMENT_WIRE_TRANSFER,Submission.PAYMENT_PO] and not payment_info:
#             raise serializers.ValidationError({"payment_info":"Please enter payment details."})
#         return data

class PPMSPaymentType(PaymentType):
    id = 'PPMSPaymentType'
    name = 'PPMS Payment'
    serializer = PPMSPaymentSerializer