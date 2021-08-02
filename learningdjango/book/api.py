from rest_framework import serializers , routers , viewsets
from .models import Book
from .serializer import BookSerializer

class BookApiView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    # queryset = Book.objects.filter(published=True)
    serializer_class = BookSerializer

router = routers.DefaultRouter()
router.register(r'book/list' , BookApiView)
