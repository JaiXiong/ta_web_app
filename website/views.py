from django.shortcuts import render
from django.views import View
from ta_app.commands import Commands


class Home(View):
    ui = Commands()

    def get(self, request):
        return render(request, "website/index.html")

    def post(self, request):
        out = self.ui.call_command(request.POST["command"])
        return render(request, "website/index.html", {"out": out})


class CreateCourse(View):
    def get(self, request):
        return render(request, "website/create_course.html")

    def post(self, request):
        pass


class CreateAccount(View):
    def get(self, request):
        return render(request, "website/create_account.html")

    def post(self, request):
        pass

