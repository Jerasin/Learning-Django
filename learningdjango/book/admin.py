from django.contrib import admin

from .models import Category , Book , Author , BookComments

#Start Config Admin Paage

# กำหนดบรรทัดเริ่มต้นมาให้อัตโนมัติ
class BookCommentsStackedInline(admin.StackedInline):
    model = BookComments
# กำหนดบรรทัดเริ่มต้นแบบกำหนดเอง กำหนดผ่าน Extra
class BookTabularInline(admin.TabularInline):
    model = BookComments
    extra = 2

class BookAdmin(admin.ModelAdmin):
    list_display = ['code' , 'name' , 'category' , 'price' , 'published' , 'show_image' ]
    list_filter = ['published']
    search_fields = ['name', 'code']
    prepopulated_fields = {'slug' : ['name']}
    fieldsets = (
        (None , {'fields' : ['name', 'slug' ,'code','description', 'level' ,  'price', 'published','image' ]}),
        ('Category',{'fields': ['category','author'] , 'classes': ['collapse']}),
    )
    inlines = [ BookTabularInline]

    


#End Config Admin Paage

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book , BookAdmin)

# Register your models here.

