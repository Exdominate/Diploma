from .serializers import ActiveDriveSerializers, ActiveDriveFilterSerializers
from rest_framework import generics
from rest_framework.permissions import  IsAuthenticated
from .models import ActiveDriver
from client.serializers import ActivePassengers
from django.db.models import  F
from rest_framework.response import Response




class ActiveDriverView(generics.CreateAPIView):
    serializer_class = ActiveDriveSerializers
    queryset = ActiveDriver.objects.all()
    permission_classes = (IsAuthenticated,)


class ActiveEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActiveDriveSerializers
    queryset = ActiveDriver.objects.all()
    permission_classes = (IsAuthenticated,)


class ActiveDriverGetPassgersToSit(generics.ListAPIView):  # доделать запрос, объекты выводятся, не работает подсчет количества объектов
    serializer_class = ActiveDriveFilterSerializers

    def get_queryset(self):
        queryset = ActivePassengers.objects.all()
        index = self.request.query_params.get('idstop', None)
        if index is not None:
            queryset = queryset.raw('''SELECT * FROM public.client_activepassengers WHERE "idStop" = %s ''',[index])
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(len(list(serializer.data)))




class ActiveDriverGetPassgersToOut(
    generics.ListAPIView):  # доделать запрос, не работает подсчет количества объектов, объекты выводятся
    serializer_class = ActiveDriveSerializers

    def get_queryset(self):
        queryset = ActiveDriver.objects.all()
        index = self.request.query_params.get('iddriver', None)
        if index is not None:
            qs = queryset.filter(idDriver__exact=index)
            q = qs.filter(numberPassengers__ToStop__exact=F('Locate'))
            queryset = q

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(len(list(serializer.data)))
