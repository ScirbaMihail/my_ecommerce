# drf
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
class PagesViewSet(ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def list(self, request):
        return render(request, "pages/home.html")

    @action(detail=False, methods=['get', 'post'])
    def login(self, request):
        return render(request, "pages/login.html")
