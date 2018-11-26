from django.shortcuts import render
from ta_app.commands_interface import CommandsInterface


class Commands(CommandsInterface):

    def login(self, user, password):
        pass

    def logout(self):
        pass

    def create_course(self, name, section, days, times, labs):
        pass

    def create_account(self, user, password, role):
        pass

    def delete_account(self, user, password, role):
        pass

    def edit_account(self, user):
        pass

    def assign_instructor(self, user, course):
        pass

    def assign_ta_to_course(self, user, course):
        pass

    def assign_ta_to_lab(self, user, course, lab):
        pass

    def read_contact_info(self):
        pass

    def edit_contact_info(self):
        pass

    def view_course_assignments(self):
        pass

    def view_ta_assignments(self):
        pass

    def help(self):
        pass

    def get_current_user(self):
        pass

    def call_command(self, command):
        pass

from django.shortcuts import render
from django.views import View
from website.models import Course, Account


def login(args):
    return""


def logout(args):
    return""


def create_course(args):
    if args[0] == "create_course":
        exist_count1 = Course.objects.filter(name=args[1]).count()

        if len(args) != 6:
            return "Please input valid arguments for all fields to create a course"
        else:
            d = args[3].split("/")
            valid1 = True
            for day in d:
                if day not in ["M", "T", "W", "R", "F", "S", "U", "O"]:
                    valid1 = False

            times = args[4].split("-")
            stl = times[0].split(":")
            etl = times[1].split(":")

            valid2 = True
            ls = args[5].split("/")
            for lab in ls:
                if len(lab) > 3 or not lab.isnumeric():
                    valid2 = False

            if exist_count1 > 1:
                return "Course " + args[1] + " - " + args[2] + " already exists in the data base."
            elif len(args[2]) > 3 or not args[2].isnumeric():
                return "Section must be a three digit number"
            elif not valid1:
                return "Days of week are noted as M, T, W, R, F, S, U, O"
            elif len(times[0]) > 5 or int(stl[0]) > 23 or int(stl[1]) > 59:
                return "valid start time is 00:00 to 23:59"
            elif len(times[1]) > 5 or int(etl[0]) > 23 or int(etl[1]) > 59:
                return "valid end time is 00:00 to 23:59"
            elif stl[0] > etl[0] or (stl[0] == etl[0] and stl[1] > etl[1]):
                return "end time can not be earlier than start time"
            elif not valid2:
                return "Lab sections must be a three digit number"
            else:
                o = Course(name=args[1],
                           section=args[2],
                           days_of_week=args[3],
                           start_time=times[0],
                           end_time=times[1],
                           lab_sections=args[5])
                o.save()
            return "Course " + args[1] + " has been added to the data base."
    else:
        return ""


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

commandList = [login, logout, create_course, create_account, edit_account, assign_instructor, assign_ta_to_course,
               assign_ta_to_lab, edit_contact_info, view_course_assignments, view_ta_assignments, read_contact_info]


def doStuff(s, commandList):
    args = s.split(" ")
    for i in commandList:
        out = i(args)
        if out != "":  # if i matches arg[0], stop looping
            break
    if out == "":
        out = "command not found"
    return out


# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, "website/index.html")

    def post(self, request):
        out = doStuff(request.POST["command"], commandList)
        return render(request, "website/index.html", {"out": out})