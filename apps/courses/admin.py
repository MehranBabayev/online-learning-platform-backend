from django.contrib import admin
from .models import Category, Course, Lesson

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'description')
    search_fields = ('name', 'category_type')
    list_filter = ('category_type',)
    ordering = ('name',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'created_at')
    search_fields = ('title', 'instructor__name', 'category__name')
    list_filter = ('category', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_instructor(self, obj):
        return obj.instructor.name
    get_instructor.admin_order_field = 'instructor' 
    get_instructor.short_description = 'Instructor'  
    
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('course', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('course', 'created_at')

    def get_course(self, obj):
        return obj.course.title
    get_course.admin_order_field = 'course'  
    get_course.short_description = 'Course'  

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
