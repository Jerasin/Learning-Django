from django.contrib import admin

from .models import Category , Book , Author

#Start Config Admin Paage
class BookAdmin(admin.ModelAdmin):
    list_display = ['code' , 'name' , 'category' , 'price' , 'published' ]
    list_filter = ['published']
    search_fields = ['name', 'code']
    prepopulated_fields = {'slug' : ['name']}
    fieldsets = (
        (None , {'fields' : ['name','code','description','price', 'published']}),
        ('Category',{'fields': ['category','author'] , 'classes': 'collapse'})
    )
#Start Config Admin Paage

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book , BookAdmin)

# Register your models here.

