# from django.contrib.auth.models import User
# from . import UserSerializer
from rest_framework.response import Response
from rest_framework import  viewsets 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FormParser, JSONParser  , MultiPartParser
from users.models import NewUser

class UserListView(viewsets.ViewSet):

    def list(self,request):
        try:
            queryset = NewUser.objects.all()
            serializer = CustomUserSerializer(queryset, many=True)
            return Response({'result': serializer.data })
        except:
            return Response({'result': "Not Found" })

class CustomUserCreate(viewsets.ViewSet):
    parser_classes = [JSONParser ,FormParser , MultiPartParser]

    permission_classes = [AllowAny]

    def create(self, request):
        
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    user = serializer.save()
                    if user:
                        json = serializer.data
                        return Response(json, status=status.HTTP_201_CREATED)
                except Exception as error: 
                    return Response(status=404 , data={"result" : "Save Failed Please Check Email and Username"})


class UserView(viewsets.ViewSet):

    def retrieve(self,request , pk=None):
        try:
            queryset = NewUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(queryset)
            return Response({'result': serializer.data })
        except:
            return Response({'result': "Not Found" })


class UserUpdateView(viewsets.ViewSet):

    def update(self,request , pk=None):
        try:
            session = NewUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(instance=session,data=request.POST)
            if serializer.is_valid():
                # prnit(**request.data)
                serializer.save()         
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=404)
        except Exception  as error:
            return Response({'result': str(error) })

class UserDeleteView(viewsets.ViewSet):

    def destroy(self,request , pk=None):
        try:
            session = NewUser.objects.get(pk=pk)
            print("session")
            session.delete()
            serializer = CustomUserSerializer(data=session)
            return Response({'result': "Delete Successfully" })
        except Exception as error:
            return Response({'result': error })


class BlacklistTokenUpdateView(viewsets.ModelViewSet):
    def create(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
