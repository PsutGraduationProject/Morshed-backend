from django.contrib import admin
from django.apps import apps
from apps.user_auth.models import (
    MorshedStudent,
    OTP,
)
app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)

admin.site.register(MorshedStudent)
admin.site.register(OTP)
