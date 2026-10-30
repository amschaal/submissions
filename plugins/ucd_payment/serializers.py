import logging

from rest_framework import serializers

from dnaorder.models import Submission
from plugins import BasePaymentSerializer, PaymentType

from . import aggie_enterprise
from .chartstring import parse

logger = logging.getLogger(__name__)

PAYMENT_TYPES = {
    Submission.PAYMENT_DAFIS: 'UC Davis chartstring',
    Submission.PAYMENT_PO: 'Purchase Order',
}
CHOOSE_PAYMENT_TYPE = 'Please choose a payment type: a UC Davis chartstring or a purchase order.'
MISSING_PAYMENT_INFO = {
    Submission.PAYMENT_DAFIS: 'Please enter the chartstring to be billed.',
    Submission.PAYMENT_PO: 'Please enter the purchase order number.',
}
MISSING_CONTACT = {
    'financial_contact_name': 'Please enter the name of the financial contact.',
    'financial_contact_email': "Please enter the financial contact's email address.",
}


class UCDChartstringPaymentSerializer(BasePaymentSerializer):
    """Payment by UC Davis Aggie Enterprise chartstring or by purchase order, and nothing else."""
    # None are required, so representing a submission without payment ({}) doesn't fail; validate() requires them.
    payment_type = serializers.ChoiceField(choices=list(PAYMENT_TYPES.items()), required=False, error_messages={
        'null': CHOOSE_PAYMENT_TYPE, 'invalid_choice': CHOOSE_PAYMENT_TYPE})
    payment_info = serializers.CharField(required=False, allow_blank=True)
    financial_contact_name = serializers.CharField(required=False, allow_blank=True)
    financial_contact_email = serializers.EmailField(required=False, allow_blank=True)
    display = serializers.SerializerMethodField()

    def get_display(self, obj):
        payment_type = obj.get('payment_type', '')
        label = 'PO Number' if payment_type == Submission.PAYMENT_PO else 'Chartstring'
        return {
            'Payment Type': PAYMENT_TYPES.get(payment_type, payment_type),
            label: obj.get('payment_info', ''),
            'Financial Contact': obj.get('financial_contact_name', ''),
            'Financial Contact Email': obj.get('financial_contact_email', ''),
        }

    def validate(self, data):
        payment_type, payment_info = data.get('payment_type'), data.get('payment_info')
        errors = {field: message for field, message in MISSING_CONTACT.items() if not data.get(field)}
        if payment_type not in PAYMENT_TYPES:
            errors['payment_type'] = CHOOSE_PAYMENT_TYPE
        elif not payment_info:
            errors['payment_info'] = MISSING_PAYMENT_INFO[payment_type]
        elif payment_type == Submission.PAYMENT_DAFIS:
            try:
                chartstring = parse(payment_info)
            except ValueError as e:
                errors['payment_info'] = str(e)
            else:
                data['payment_info'] = chartstring.string
                chartstring_errors = aggie_enterprise_errors(chartstring)
                if chartstring_errors:
                    errors['payment_info'] = chartstring_errors
        if errors:
            raise serializers.ValidationError(errors)
        # Stored payment is read back with the plugin it names, so it can only name this one.
        data['plugin_id'] = self._plugin_id
        return data


def aggie_enterprise_errors(chartstring):
    if not aggie_enterprise.is_configured():
        return []
    try:
        return aggie_enterprise.validate(chartstring)
    except aggie_enterprise.AggieEnterpriseError as e:
        # The format has been checked; don't hold up submissions while Aggie Enterprise is unavailable.
        logger.warning('Unable to validate chartstring %s with Aggie Enterprise: %s', chartstring.string, e)
        return []


class UCDChartstringPaymentType(PaymentType):
    id = 'UCDChartstringPaymentType'
    name = 'UC Davis chartstring or purchase order'
    serializer = UCDChartstringPaymentSerializer
