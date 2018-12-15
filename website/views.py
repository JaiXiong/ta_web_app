from django.shortcuts import render
from django.views import View
from ta_app.commands import Commands
from website.models import Account, Course, Lab
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
        if "user" not in request.session and request.session["user"] is not None:
            request.session["user"] = None
        request.session['redirect_to'] = request.GET['next']
        return render(request, "website/login.html")

    def post(self, request):
        co = Commands()
        name = request.POST["user_name"]
        password = request.POST["password"]
        out = co.login(name, password)
        if out == 'login failed! bad username/ password':
            request.session["user"] = None
        else:
            request.session["user"] = co.current_user.user
        if co.current_user.user == name and "redirect_to" in request.session:
            return HttpResponseRedirect(request.session["redirect_to"])
        return render(request, "website/login.html", {"return_statement": out})


class Logout(View):

    def get(self, request):
        co = Commands()
        co.current_user.user = request.session["user"]
        out = co.logout()
        request.session['redirect_to'] = request.GET['next']
        request.session["user"] = None
        return render(request, "website/login.html", {"return_statement": out})

    def post(self, request):
        request.session["user"] = None
        return HttpResponseRedirect(request.session["redirect_to"])


class CreateCourse(View):
    co = Commands()
    create_course_header = "Create Course"

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
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
            request.session["labs_course"] = name
            valid = False
            out = self.co.create_course(name, section, days_of_week, time, labs)
            if out == "Course " + name + " has been added to the data base with lab sections " + labs:
                valid = True
            return render(request, "website/create_course.html", {"header": self.create_course_header,
                                                                  "valid": valid,
                                                                  "return_statement": out})
        else:
            out = "Please log in to create a course"
            return render(request, "website/create_course.html", {"header": self.create_course_header,
                                                                  "valid": False,
                                                                  "name": "",
                                                                  "sections": "",
                                                                  "return_statement": out})


class CompleteLabs(View):
    co = Commands()

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/edit_lab.html", {})

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            labs_course = request.POST['lab_course']
            section = request.POST["lab_section"]
            days_of_week = request.POST["lab_days"]
            times = request.POST["lab_time"]
            out = self.co.edit_lab(labs_course, section, days_of_week, times)
            return render(request, "website/edit_lab.html", {"return_statement": out})
        else:
            out = "Please login to edit labs"
            return render(request, "website/edit_lab.html", {"return_statement": out})


class AssignInstructor(View):
    co = Commands()
    instructor_header = "Assign Instructor To Course"
    ta_to_lab = False

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
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
    ta_to_course_header = "Assign TA To Course"
    ta_to_lab = False

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
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
    ta_to_lab_header = "Assign TA To Lab Section"
    ta_to_lab = True

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
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
            out = self.co.assign_ta_to_lab(user, course)
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
        if "user" in request.session and request.session["user"] is not None:
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


class CreateAccount(View):
    co = Commands()

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/create_account.html")

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            user = request.POST['user_name']
            password = request.POST['password']
            role = request.POST['role']
            out = self.co.create_account(user, password, role)
            print(role)
            return render(request, "website/create_account.html", {"return_statement": out})
        else:
            out = "Please log in to create an account"
            return render(request, "website/create_account.html", {"return_statement": out})


class DeleteAccount(View):
    co = Commands()

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/delete_account.html")

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            out = self.co.delete_account(request.POST["user_name"])
            return render(request, "website/delete_account.html", {"return_statement": out})
        else:
            out = "Please log in to delete an account"
            return render(request, "website/delete_account.html", {"return_statement": out})


class EditContactInfo(View):
    co = Commands()

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            current_user = ao.user
            current_password = ""
            for i in ao.password:
                current_password += '*'
            current_street = ao.street_address
            current_email = ao.email_address
            current_phone = ao.phone_number

            if current_street == "":
                current_street = "No street address on record"

            if current_email == "":
                current_email = "No email address on record"

            if current_phone == "":
                current_phone = "No current phone number on record"

            return render(request, "website/edit_contact_info.html", {"current_user": current_user,
                                                                      "current_password": current_password,
                                                                      "current_street": current_street,
                                                                      "current_email": current_email,
                                                                      "current_phone": current_phone})

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            user = self.co.current_user.user
            password = request.POST["password"]
            street_address = request.POST["street_address"]
            email_address = request.POST["email_address"]
            phone_number = request.POST["phone_number"]

            if password == "":
                password = self.co.get_account(user).password

            if street_address == "":
                street_address = ao.street_address

            if email_address == "":
                email_address = ao.email_address

            if phone_number == "":
                phone_number = ao.phone_number

            out = self.co.edit_contact_info(user, password, street_address, email_address, phone_number)

            return render(request, "website/edit_contact_info.html", {"current_user": self.co.current_user.user,
                                                                      "current_role": self.co.current_user.role,
                                                                      "return_statement": out})
        else:
            out = "Please log in to edit contact info"
            return render(request, "website/edit_contact_info.html", {"return_statement": out})


class EditAccount(View):
    co = Commands()

    def get(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
        return render(request, "website/edit_account.html")

    def post(self, request):
        if "user" in request.session and request.session["user"] is not None:
            ao = Account.objects.get(user=request.session["user"])
            self.co.current_user = ao
            user = request.POST["user_name"]
            password = request.POST["password"]
            role = request.POST["role"]
            street_address = request.POST["street_address"]
            email_address = request.POST["email_address"]
            phone_number = request.POST["email_address"]

            if password != "":
                password = self.co.get_account(user).password

            if role == "":
                role = self.co.get_account(user).role

            if street_address == "":
                street_address = self.co.get_account(user).street_address

            if email_address == "":
                email_address = self.co.get_account(user).street_address

            if phone_number == "":
                phone_number = self.co.get_account(user).phone_number

            out = self.co.edit_account(user, password, role, street_address, email_address, phone_number)
            if isinstance(out, Account):
                out = "Account has been updated"
            return render(request, "website/edit_account.html", {"return_statement": out})
        else:
            out = "Please log in to edit an account"
            return render(request, "website/edit_account.html", {"return_statement": out})