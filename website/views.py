from django.shortcuts import render
from ta_app.commands_interface import CommandsInterface


# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, "website/index.html")

    def post(self, request):
        out = doStuff(request.POST["command"], commandList)
        return render(request, "website/index.html", {"out": out})