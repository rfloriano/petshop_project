from django.contrib import admin
from django.http import HttpResponseRedirect

class OneEntry(admin.ModelAdmin):
    def modify(self):
        try:
            conf = self.model.objects.get(pk=1)
            return HttpResponseRedirect("/admin/%s/%s/%s/" % (self.model._meta.app_label, str(self.model.__name__).lower(), conf.pk))
        except:
            return HttpResponseRedirect("/admin/%s/%s/add/" % (self.model._meta.app_label, str(self.model.__name__).lower()))

    def changelist_view(self, request):
        return self.modify()

    def has_add_permission(self, request):
        permission = super(OneEntry, self).has_add_permission(request)
        if permission:
            try:
                conf = self.model.objects.get(pk=1)
                return False
            except:
                return True
        else:
            return permission

    def has_change_permission(self, request, obj=None):
        permission = super(OneEntry, self).has_change_permission(request, obj)
        if permission:
            try:
                conf = self.model.objects.get(pk=1)
                return True
            except:
                return False
        else:
            return permission
