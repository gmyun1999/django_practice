from django.contrib import admin
from .models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['subject']
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)

