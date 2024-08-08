from django.shortcuts import render
from django.views import View

from cart.models import Cart
from .models import Order, OrderItem


from rest_framework.views import APIView
from rest_framework.response import Response

from order.serializers import GeneratePayLinkSerializer

from payme.methods.generate_link import GeneratePayLink

from drf_yasg.utils import swagger_auto_schema


class GeneratePayLinkAPIView(APIView):
    @swagger_auto_schema(
        request_body=GeneratePayLinkSerializer,
        responses={200: "{'pay_link': str}"}
    )
    def post(self, request, *args, **kwargs):
        """
        Generate a payment link for the given order ID and amount.

        Request parameters:
            - order_id (int): The ID of the order to generate a payment link for.
            - amount (int): The amount of the payment.

        Example request:
            curl -X POST \
                'http://your-host/shop/pay-link/' \
                --header 'Content-Type: application/json' \
                --data-raw '{
                "order_id": 999,
                "amount": 999
            }'

        Example response:
            {
                "pay_link": "http://payme-api-gateway.uz/bT0jcmJmZk1vNVJPQFFoP05GcHJtWnNHeH"
            }
        """
        serializer = GeneratePayLinkSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        pay_link = GeneratePayLink(**serializer.validated_data).generate_link()

        return Response({"pay_link": pay_link})



class MyOrdersView(View):
    def get(self, request):
        my_orders = Order.objects.filter(user=request.user)
        context = {
            'my_orders': my_orders
        }
        return render(request, 'user/my_orders.html', context)


class PaymentView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        context = {
            'cart': cart,
        }
        return render(request, 'cart/booking.html', context)
    
    
    
    
    