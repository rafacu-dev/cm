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
    
    path('api/user/', include('user.urls')),
    path('api/profile/', include('user_profile.urls')),
    path('api/shop/', include('shop.urls')),
    path('api/map/', include('map.urls')),
    path('api/petition/', include('petition.urls')),
    path('api/poster/', include('poster.urls')),
    path('api/product/', include('product.urls')),
    path('api/market/', include('market.urls')),
    path('api/shopping/', include('shopping.urls')),
    path('api/proposal/', include('proposal.urls')),
    path('api/comments-product/', include('comments_product.urls')),

    path('admin/', admin.site.urls),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticProduction(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
