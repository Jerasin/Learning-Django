from rest_framework import serializers , routers , viewsets 
from .serializer import BookSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Book
from rest_framework.parsers import FormParser, JSONParser  , MultiPartParser
import os

class TestApiView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    # parser_classes = [MultiPartParser]

    def post(self, request):
        print(request.data)
        return Response({'received data': "request.data"})


# class BookListView(APIView):

#     def get(self,request):
#         print(request.data)
#         queryset = Book.objects.all()
#         serializer = BookSerializer(queryset, many=True)
#         return Response({'result': serializer.data })


# class CreateBookView(APIView):

#     def post(self, request, filename,  media_type=None , format=None):
#         file = request.data['image'].content_type
#         file_type = file.split('/')[0]
#         print(file_type)
#         try:        
#             if file_type == 'image':
#                 serializer = BookSerializer(data=request.data)
#                 if serializer.is_valid():
#                     serializer.save();
#                     return Response(serializer.data, status=200)
#                 else:
#                     return Response(serializer.errors, status=404)
#             else:
#                 return Response(status=404 , data={"result" : "Please Check File"})
#         except Exception as error :
#             print(dir(serializer)) 
#             print(error)
#             return Response(status=404 , data={"result" : "Error"})



class BookListView(viewsets.ViewSet):

    def list(self,request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response({'result': serializer.data })

    def retrieve(self, request, pk=None):
        queryset = Book.objects.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

class CreateBookView(viewsets.ViewSet):
    parser_classes = [JSONParser ,FormParser , MultiPartParser]

    def create(self, request,  media_type=None , format=None):
        file = request.data['image'].content_type
        file_type = file.split('/')[0]
        # print(file_type)
        try:
            if file_type == 'image':
                serializer = BookSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save();
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=404)
            else:
                return Response(status=404 , data={"result" : "Please Check File"})
        except Exception as error: 
            return Response(status=404 , data={"result" : error})


class UpdateBookView(viewsets.ViewSet):
    parser_classes = [JSONParser ,FormParser , MultiPartParser]

    def update(self, request,  media_type=None , format=None , pk=None):
        file = request.data['image'].content_type
        file_type = file.split('/')[0]
        print(pk)
        try:
            if file_type == 'image':
                session  = Book.objects.get(pk=pk)
                serializer = BookSerializer(instance=session,data=request.data)
                if serializer.is_valid():
                    serializer.save();
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=404)
            else:
                return Response(status=404 , data={"result" : "Please Check File"})
        except Exception as error: 
            return Response(status=404 , data={"result" : error})


class DeleteBookView(viewsets.ViewSet):
    parser_classes = [JSONParser ,FormParser , MultiPartParser]

    def destroy(self, request,  media_type=None , format=None , pk=None):
        try:
            book_delete  = Book.objects.get(pk=pk)
            if book_delete.image:          
                os.remove(book_delete.image.path)
            book_delete.delete();
            return Response(status=200, data={"result" : "Delete Successfully"})
        except Exception as error: 
            return Response(status=404 , data={"result" : error})

    




