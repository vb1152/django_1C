from django.contrib import admin

# Register your models here.
from desk_app.models import User, ICparams, ICgroups, Producers, IC_scu

admin.site.register(User)#, ICparams, ICgroups, Producers, IC_scu)
admin.site.register(ICparams)
admin.site.register(ICgroups)
admin.site.register(Producers)
admin.site.register(IC_scu)

