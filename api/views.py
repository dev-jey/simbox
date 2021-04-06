from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from mods.models import Mod
from .serializers import ModSerializer


class ModListView(generics.ListAPIView):
    queryset = Mod.objects.filter(
        visible=True,
        verified=True
    )

    serializer_class = ModSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    filterset_fields = ["simulators", "type"]
    search_fields = ["title"]
    pagination_class = PageNumberPagination
