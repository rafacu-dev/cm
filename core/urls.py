import re
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static, serve

def staticProduction(prefix, view=serve, **kwargs):
    if settings.DEBUG:
        return []
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    
    path('api/user/', include('apps.user.urls')),
    path('api/profile/', include('apps.user_profile.urls')),
    path('api/shop/', include('apps.shop.urls')),
    path('api/map/', include('apps.map.urls')),
    path('api/petition/', include('apps.petition.urls')),
    path('api/poster/', include('apps.poster.urls')),
    path('api/product/', include('apps.product.urls')),
    path('api/market/', include('apps.market.urls')),
    path('api/shopping/', include('apps.shopping.urls')),
    path('api/proposal/', include('apps.proposal.urls')),
    path('api/comments-product/', include('apps.comments_product.urls')),

    path('admin/', admin.site.urls),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticProduction(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
