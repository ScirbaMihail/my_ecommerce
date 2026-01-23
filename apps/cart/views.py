# drf
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

# local
from apps.cart.serializers import CartSerializer, CartItemInputSerializer
from apps.cart.models import Cart
from apps.cart.services import CartService


# Create your views here.
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related("products").all()
    serializer_class = CartSerializer

    def get_serializer_class(self):
        if self.action == 'items' and self.request.method == "POST":
            return CartItemInputSerializer
        return super().get_serializer_class()


    @action(detail=True, methods=["get", "post"])
    def items(self, request: Request, pk=None):
        if request.method == "GET":
            return self._get_items(pk)
        return self._add_item(request, pk)

    def _get_items(self, pk=None):
        succeeded, response = CartService.get_items(pk)
        return Response(
            response,
            status=status.HTTP_200_OK if succeeded else status.HTTP_404_NOT_FOUND,
        )

    def _add_item(self, request: Request, pk=None):
        serializer = CartItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        succeeded, response = CartService.add_product(pk, serializer.validated_data)
        return Response(
            response,
            status=status.HTTP_201_CREATED if succeeded else status.HTTP_404_NOT_FOUND,
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path="items/(?P<item_id>[^/.]+)",
    )
    def remove_item(self, request: Request, pk=None, item_id=None):
        succeeded, response = CartService.remove_product(pk, item_id)
        return Response(
            response,
            status=(
                status.HTTP_204_NO_CONTENT if succeeded else status.HTTP_404_NOT_FOUND
            ),
        )
