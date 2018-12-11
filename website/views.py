from django.shortcuts import render
from django.views import View
from ta_app.commands_interface import CommandsInterface
from ta_app.commands import Commands
# Create your views here.


class Home(View):
    def get(self, request):
        return render(request, "website/index.html")

    def post(self, request):
        out = ""
        #out = doStuff(request.POST["command"], commandList)
        return render(request, "website/index.html", {"out": out})


class ViewCourseAssignments(View):
    def get(self, request):
        return render(request, "website/view_courses.html")

    def post(self, request):
        ui_instance = request.session["ui_instance"]
        out = ui_instance.view_course_assignments()
        return render(request, "website/view_courses.html", {"course_list": out})


class ViewTAAssignments(View):
    def get(self, request):
        return render(request, "website/view_tas.html")

    def post(self, request):
        ui_instance = request.session["ui_instance"]
        out = ui_instance.view_ta_assignments()
        return render(request, "website/view_tas.html", {"course_list": out})
