from django.shortcuts import render
from django.views import View
from ta_app.commands import Commands

# Create your views here.


class Home(View):
    ui = Commands()

    def get(self, request):
        return render(request, "website/index.html")

    def post(self, request):
        out = self.ui.call_command(request.POST["command"])
        return render(request, "website/index.html", {"out": out})
