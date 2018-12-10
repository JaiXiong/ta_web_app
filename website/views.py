from django.shortcuts import render
from django.views import View
from ta_app.commands import Commands
from website.models import Account


class Home(View):
    ui = Commands()

    def get(self, request):
        return render(request, "website/index.html")

    def post(self, request):
        out = self.ui.call_command(request.POST["command"])
        return render(request, "website/index.html", {"out": out})


class Login(View):
    ui = Commands()

    def get(self, request):

        if "name" in request.session:
            name = request.session["name"]
        else:
            name = "no user logged in, please log in"
        return render(request, "website/login.html", {"name": name})

    def post(self, request):

        name = request.POST["username"]
        password = request.POST["password"]
        request.session["name"] = name
        request.session["password"] = password
        out = self.ui.login(name, password)
        ctx = {"out": out, "name": name }
        return render(request, "website/login.html", ctx)

class Search(View):
    ui = Commands()

    def get(self, request):
        if "name" in request.session:
            name = request.session["name"]
        else:
            name = "no user logged in, please log in"
        return render(request, "website/search.html", {"name": name})

    def post(self, request):
        user = ""
        password = ""
        role = ""
        address = ""
        email = ""
        phone = ""
        db = Account.objects.all()
        searchuser = request.POST["searchuser"]
        name = request.session["name"]
        request.session["name"] = name
        current = self.ui.get_account(name)
        if current.role == "Supervisor" or current.role == "Administrator":
            searchthis = self.ui.get_account(searchuser)
            if db.filter(user=name).count() == 0:
                return "Invalid search, try again"
            else:
                name = request.session["name"]
                user = searchthis.user
                password = searchthis.password
                role = searchthis.role
                address = searchthis.street_address
                email = searchthis.email_address
                phone = searchthis.phone_number
        else:
            print("Invalid permissions to view information")
        ctx = {user, password, role, address, email, phone}
        return render(request, "website/search.html", {"ctx": ctx}, {"name": name})