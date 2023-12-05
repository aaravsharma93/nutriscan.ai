from django.contrib import admin
from .models import NutrientsListTable, DataTable, DailyAllowanceSheet, UserTable


admin.site.register(UserTable)
admin.site.register(NutrientsListTable)
admin.site.register(DataTable)
admin.site.register(DailyAllowanceSheet)
