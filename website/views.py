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
        print("inside get login")
        if "name" in request.session:
            name = request.session["name"]
        else:
            name = "no user logged in, please log in"
        return render(request, "website/login.html", {"name": name})

    def post(self, request):
        print("inside post login")
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
        print("inside get search")
        if "name" in request.session:
            name = request.session["name"]
        else:
            name = "no user logged in, please log in"
        return render(request, "website/search.html", {"name": name})

    def post(self, request):
        print("inside post search")
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
        print("current: "+ name)
        #current = self.ui.get_current_user()
        #print(current)
        current = self.ui.get_account(name)
        print(current)
        print(current.role)
        if current.role == "Supervisor":
            print("yay im supervisor")
        if (current.role == "Administrator"):
            print("yay im admin")
        if current.role == "Supervisor" or current.role == "Administrator":
            #print("Invalid permissions to view user")
            #else:
            print("did it make it here????")
            searchthis = self.ui.get_account(searchuser)
            print("trying to search: " + searchthis.user)
            if db.filter(user=name).count() == 0:
                return "Invalid search, try again"
            else:
                print("current information:")
                name = request.session["name"]
                print("user info:" + name)
                user = searchthis.user
                print(user)
                password = searchthis.password
                print(password)
                role = searchthis.role
                print(role)
                address = searchthis.street_address
                print(address)
                email = searchthis.email_address
                print(email)
                phone = searchthis.phone_number
                print(phone)
        else:
            print("Invalid permissions to view information")
        ctx = {user, password, role, address, email, phone}
        return render(request, "website/search.html", {"ctx": ctx}, {"name": name})