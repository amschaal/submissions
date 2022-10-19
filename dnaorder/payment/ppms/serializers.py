from rest_framework import serializers




from dnaorder.payment import PaymentType
from dnaorder.payment.ppms.api import group_exists


class PPMSPaymentSerializer(serializers.Serializer):
    pi_email= serializers.CharField(required=False)
    display = serializers.SerializerMethodField(read_only=True)
    def get_display(self, obj):
        return {'PPMS PI Email/Login': obj.get('pi_email','')}
    def validate(self, data):
        pi_email = data.get('pi_email', None)
        if not pi_email:
            raise serializers.ValidationError({"pi_email":"PPMS PI Email is required."})
        if not group_exists(pi_email):
            raise serializers.ValidationError({"pi_email":"Group account with PI login '{0}' does not exist in PPMS.".format(pi_email)})
        return data

class PPMSPaymentType(PaymentType):
    id = 'PPMSPaymentType'
    name = 'PPMS Payment'
    serializer = PPMSPaymentSerializer