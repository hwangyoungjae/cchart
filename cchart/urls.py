"""cchart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
import web.views
import web.views_edu

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', web.views.main_page),

    url(r'^test$', web.views.test.as_view()),
    url(r'^test_test$', web.views.test_page),

    url(r'^request$', web.views.request_page),
    url(r'^request.meta$', web.views.request_meta_page),






    url(r'^edu/compound.data$', web.views_edu.compound_data),
    url(r'^edu/compound$', web.views_edu.compound),

    url(r'^edu/costaverage$', web.views_edu.costaverage),
    url(r'^edu/costaverage.data$', web.views_edu.costaverage_data),

    url(r'^edu/costaverage2$', web.views_edu.costaverage2),
    url(r'^edu/costaverage.data2$', web.views_edu.costaverage_data2),

    url(r'^edu/realtime$', web.views_edu.realtime),
    url(r'^edu/realtimeT$', TemplateView.as_view(template_name='edu/realtime.html')),
    url(r'^edu/realtime.data$', web.views_edu.realtime_data),

    # url(r'^test$', web.views.MyFormView.as_view()),
    # url(r'^ttt$', web.views.ttt),



]
