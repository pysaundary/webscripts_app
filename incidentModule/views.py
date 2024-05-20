from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from  rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
# Create your views here.


from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import IncidentModel ,createIncidentId
from .serializers import IncidentSerializer

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.createBy == request.user

class ListCreateIncident(ListCreateAPIView):
    serializer_class = IncidentSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        user = self.request.user
        # Assuming 'createBy' is a field in your IncidentModel that refers to the user who created the incident.
        return IncidentModel.objects.filter(createBy=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.id:
            return Response(
                {"message": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(createBy=self.request.user,incidentId = createIncidentId() )


class IncidentRetrieveUpdateDestroyAPIView(APIView):
    
    def incidentQueryset(self,id)->tuple:
        try:
            query = IncidentModel.objects.get(incidentId = id)
            return (True,query)
        except:
            return (False,None)

    def get(self,request,id):
        user = request.user
        query = self.incidentQueryset(id)
        if not query[0]:
            return Response(
                {
                    "message":"Not Found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if  query[1].createBy.id != user.id:
            return Response(
                {
                    "message":"Not authenticated"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = IncidentSerializer(query[1])
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    def put(self,request,id):
        user = request.user
        query = self.incidentQueryset(id)
        if not query[0]:
            return Response(
                {
                    "message":"Not Found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if  query[1].createBy.id != user.id:
            return Response(
                {
                    "message":"Not authenticated"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        r_data = request.data
        r_data.pop("createBy",None)
        r_data.pop("id",None)
        r_data.pop("incidentId",None)
        serializer = IncidentSerializer(query[1],data=r_data,partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        user = request.user
        query = self.incidentQueryset(id)
        if not query[0]:
            return Response(
                {
                    "message":"Not Found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if  query[1].createBy.id != user.id:
            return Response(
                {
                    "message":"Not authenticated"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        query[1].delete()
        return Response({"message":"success"},status=status.HTTP_200_OK)
    
class SerachIncident(APIView):
    def get(self,request):
        searchWord = request.query_params.get("id",None)
        queryset = IncidentModel.objects.filter(incidentId = searchWord)
        serializer = IncidentSerializer(queryset,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)