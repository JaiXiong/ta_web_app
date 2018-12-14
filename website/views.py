from django.shortcuts import render
from django.views import View
from ta_app.commands import Commands
from website.models import Account
from django.http import HttpResponseRedirect

# Create your views here.


class Home(View):
    ui = Commands()

    def get(self, request):
        return render(request, "website/index.html")

    def post(self, request):
        out = self.ui.call_command(request.POST["command"])
        return render(request, "website/index.html", {"out": out})


class Login(View):

    def get(self, request):
        if "user" not in request.session:
            request.session["user"] = None
        request.session['redirect_to'] = request.GET['next']
        return render(request, "website/login.html")

    def post(self, request):
        co = Commands()
        name = request.POST["user_name"]
        password = request.POST["password"]
        out = co.login(name, password)
        request.session["user"] = co.current_user.user
        if co.current_user.user == name and "redirect_to" in request.session:
            return HttpResponseRedirect(request.session["redirect_to"])
        return render(request, "website/login.html", {"return_statement": out})


class Logout(View):

    def get(self, request):
        co = Commands()
        co.current_user.user = request.session["user"]
        out = co.logout()
        request.session["user"] = None
        return render(request, "website/login.html", {"return_statement": out})

    """def post(self, request):
        co = Commands()
        name = request.POST["user_name"]
        password = request.POST["password"]
        out = co.login(name, password)
        request.session["user"] = co.current_user.user
        if co.current_user.user == name and "redirect_to" in request.session:
            return HttpResponseRedirect(request.session["redirect_to"])
        return render(request, "website/login.html", {"return_statement": out})"""


class CreateCourse(View):
    co = Commands()
    create_course_header = "Create A Course"

    def get(self, request):
        if "user" in request.session:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/create_course.html", {"header": self.create_course_header})

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            name = request.POST['course_name']
            section = request.POST['course_section']
            days_of_week = request.POST['course_days']
            time = request.POST['course_time']
            labs = request.POST['lab_sections']
            out = self.co.create_course(name, section, days_of_week, time, labs)
            return render(request, "website/create_course.html", {"header": self.create_course_header,
                                                                  "return_statement": out})
        else:
            out = "Please log in to create a course"
            return render(request, "website/create_course.html", {"header": self.create_course_header,
                                                                  "return_statement": out})


class AssignInstructor(View):
    co = Commands()
    instructor_header = "Assign An Instructor To A Course"
    ta_to_lab = False

    def get(self, request):
        if "user" in request.session:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/assign.html", {"header": self.instructor_header,
                                                       "is_ta_to_lab": self.ta_to_lab})

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            user = request.POST["user_name"]
            course = request.POST["course_name"]
            out = self.co.assign_instructor(user, course)
            return render(request, "website/assign.html", {"header": self.instructor_header,
                                                           "is_ta_to_lab": self.ta_to_lab,
                                                           "return_statement": out})
        else:
            out = "Please log in to assign an instructor to a course"
            return render(request, "website/assign.html", {"header": self.instructor_header,
                                                           "is_ta_to_lab": self.ta_to_lab,
                                                           "return_statement": out})


class AssignTaToCourse(View):
    co = Commands()
    ta_to_course_header = "Assign TA To A Course"
    ta_to_lab = False

    def get(self, request):
        if "user" in request.session:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/assign.html", {"header": self.ta_to_course_header,
                                                       "is_ta_to_lab": self.ta_to_lab,
                                                       "is_ta_to_lab": self.ta_to_lab})

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            user = request.POST["user_name"]
            course = request.POST["course_name"]
            out = self.co.assign_ta_to_course(user, course)
            return render(request, "website/assign.html", {"header": self.ta_to_course_header,
                                                           "is_ta_to_lab": self.ta_to_lab,
                                                           "return_statement": out})
        else:
            out = "Please log in to assign an instructor to a course"
            return render(request, "website/assign.html", {"header": self.ta_to_course_header,
                                                           "return_statement": out})


class AssignTaToLab(View):
    co = Commands()
    ta_to_lab_header = "Assign TA To A Lab Section"
    ta_to_lab = True

    def get(self, request):
        if "user" in request.session:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/assign.html", {"header": self.ta_to_lab_header,
                                                       "is_ta_to_lab": self.ta_to_lab})

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            user = request.POST["user_name"]
            course = request.POST["course_name"]
            out = self.co.assign_ta_to_course(user, course)
            return render(request, "website/assign.html", {"header": self.ta_to_lab_header,
                                                           "is_ta_to_lab": self.ta_to_lab,
                                                           "return_statement": out})
        else:
            out = "Please log in to assign an instructor to a course"
            return render(request, "website/assign.html", {"header": self.ta_to_lab_header,
                                                           "is_ta_to_lab": self.ta_to_lab,
                                                           "return_statement": out})


class ViewContactInfo(View):
    co = Commands()
    view_contact_header = "Contact Information"

    def get(self, request):
        if "user" in request.session:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/view_contact_info.html", {"header": self.view_contact_header,
                                                                  "return_statement": ""})

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            accounts = self.co.read_contact_info()
            role = request.POST["select"]
            account_list = []
            if role == "All Users":
                account_list = accounts
            else:
                for a in accounts:
                    if a.role == role:
                        account_list.append(a)
            return render(request, "website/view_contact_info.html", {"header": self.view_contact_header,
                                                                      "account_list": account_list,
                                                                      "return_statement": ""})
        else:
            out = "Please log in to view contact information"
            return render(request, "website/view_contact_info.html", {"header": self.view_contact_header,
                                                                      "account_list": "",
                                                                      "return_statement": out})