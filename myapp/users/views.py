from django.conf import settings

from django.shortcuts import render

# Create your views here.

def index(request):
    """ トップページ
    """
    cdn_path = settings.AWS_COMMON_IMAGE_RESOURCE_CDN_PATH
    context = {'cdn_path': cdn_path,}
    return render(request, 'users/index.html', context)
