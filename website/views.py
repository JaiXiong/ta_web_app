from django.shortcuts import render
from django.views import View
from ta_app.commands import Commands
from website.models import Account, Course


# creates account by checking db, then if exist return notice, else check all params are not empty string
# if successful, return string with name of account created.
def create_account(args):
    if args[0] == "create_account":
        if Account.filter(name=args[1]).count() > 0:
            return "User exist already"
        else:
            if len(args) < 4:
                return "not enough arguments during create account"
            if args[1] is not None and args[2] is not None and args[3] is not None:
                user = Account(user=args[1], password=args[2], role=args[3])
                user.save()
                return args[1] + " account has been created"
            else:
                return args[1] + " not successfully created"
    else:
        return ""

# this was implemented by ross already, but ill leave this here till we figure out how/when who's to merge/pu;ll
def create_course(args):
    #   def create_course(self, name, section, days, times, labs):
    user = Account.all()
    course = Course.all()
    if args[0] == "create_course":
        if user.filter(args[1]).count() == 0:
            return "user "+args[1]+" doesn't exist"
        else:
            if len(args) < 6:
                return "invalid number of items in create course"
            if len(args[2]) < 3:
                info = course(section=args[2], days=args[3], times=args[4], labs=args[5])
                info.save
    else:
        return ""


def login(args):
    return


def logout(args):
    return


def create_account(args):
    return""


def edit_account(args):
    return""


def assign_instructor(args):
    return""


def assign_ta_to_course(args):
    return""


def assign_ta_to_lab(args):
    return""


def edit_contact_info(args):
    return""


def view_course_assignments(args):
    return""


def view_ta_assignments(args):
    return""


def read_contact_info(args):
    return""


commandList = [create_account, create_course, login, logout, edit_account, assign_instructor, assign_ta_to_course,
               read_contact_info, view_ta_assignments, view_course_assignments, edit_contact_info, assign_ta_to_lab]

def doStuff(s, commandList):
    args = s.split(" ")
    for i in commandList:
        out = i(args)
        if out != "": #if i matches arg[0], stop looping
            break
    if out == "":
        out = "command not found"
    return out

# Create your views here.


class Home(View):
    ui = Commands()

    def get(self, request):
        return render(request, "main/index.html")

    def post(self, request, ui):
        out = ui.call_command(request.POST["command"], ui.command_list)
        return render(request, "main/index.html", {"out": out})
