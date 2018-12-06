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


class Login(View):
    ui = Commands()
    template_name = "login page"
    def get_login(self, request):
        return render(request, "website/login.html")

    def post_login(self, request):
        out = "works in progress"
        return render(request, "website/login.html", {"out": out})