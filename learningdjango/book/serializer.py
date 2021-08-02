from rest_framework import serializers
from .models import Book 

# serializers คือตัวแปลง boj -> str
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['code' , 'description' ,'name' , 'price' , 'category' , 'level']
