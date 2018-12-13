"""ta_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from website.views import Home, CreateCourse, ViewCourses, ViewTAs, \
                          AssignInstructor, AssignTaToCourse, AssignTaToLab, \
                          Login, ViewContactInfo

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  path('', Home.as_view(), name='home'),
  path('create_course/', CreateCourse.as_view(), name='createcourse'),
  path('assign_instructor/', AssignInstructor.as_view(), name='assigninstructor'),
  path('assign_ta_to_course/', AssignTaToCourse.as_view(), name='assigntatocourse'),
  path('assign_ta_to_lab/', AssignTaToLab.as_view(), name='assigntatolab'),
  path('login/', Login.as_view(), name="login"),
  path('view_contact_info/', ViewContactInfo.as_view(), name='viewcontact' ),
  path('viewcourses/', ViewCourses.as_view(), name="viewcourses"),
  path('viewtas/', ViewTAs.as_view(), name="viewtas"),
]