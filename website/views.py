from django.shortcuts import render

from django.shortcuts import render
from django.views import View
from website.models import Course, Account


"""def addUser(args):
    # if args[0] == addUser, adds user named args[1]
    # returns "User <args[1]> added" or "User <args[1]> exists"
    # else returns ""
    if args[0] == "addUser":
        exist_count = user.objects.filter(name=args[1]).count()
        if exist_count >= 1:
            return "User " + args[1] + " exists already"
        else:
            o = user(name=args[1])
            o.save()
            return args[1] + " added"
    else:
        return ""


def addItem(args):
    # if args[0] == "addItem", adds item args[1] to user args[2]
    # returns "Item <args[1]> added to user <args[2]>"
    # or "User <args[2]> already has item <args[1]>"
    # or "User <args[2]> does not exist"
    # else returns ""
    if args[0] == "addItem":

        items = list(item.objects.filter(name=args[2]))
        exists = False
        exist_count = user.objects.filter(name=args[2]).count()
        if exist_count < 1:
            return "User " + args[2] + " does not exists"
        else:
            for i in items:
                if i == args[1]:
                    return "User " + args[2] + " already has " + args[1]
                    exists = True
                    break
            if exists == False:
                owner = list(user.objects.filter(name=args[2]))
                o = item(name=args[1], itemowner=owner[0])
                o.save()
                return "Item " + args[1] + " added to user " + args[2]
    else:
        return ""


def display(args):
    # if args[0] == display
    # return a string with each user followed by their items
    # items are indented
    if args[0] == "display":
        users = list(user.objects.all())
        items = list(item.objects.all())
        s = ""
        for u in users:
            s += u.name + "<br>"
            for i in items:
                if i.itemowner == u:
                    s += i.name + "<br>"
        return s
    else:
        return ""
"""


def help(args):
    pass


def login(args):
    pass


def logout(args):
    pass


def create_course(args):
    # if args[0] == addUser, adds user named args[1]
    # returns "User <args[1]> added" or "User <args[1]> exists"
    # else returns ""
    if args[0] == "create_course":
        exist_count1 = Course.objects.filter(name=args[1]).count()
        exist_count2 = exist_count1.objects.filter(section=args[2]).count()

        if len(args) < 7:
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
            ls = args[6].split("/")
            for lab in ls:
                if len(lab) > 3 or not lab.isnumeric():
                    valid2 = False

            if exist_count2 >= 1:
                return "Course " + args[1] + " - " + args[2] + " already exists in the data base."
            elif len(args[2]) > 3 or not args[2].isnumeric():
                return "Section must be a three digit number"
            elif not valid1:
                return "Days of week are noted as M, T, W, R, F, S, U, O"
            elif len(times[0]) > 5 or times[1[2]] != ":" or int(stl[0]) > 23 or int(stl[1]) > 59:
                return "valid start time is 00:00 to 23:59"
            elif len(times[1]) > 5 or times[2[2]] != ":" or int(etl[0]) > 23 or int(etl[1]) > 59:
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
                           lab_sections=args[6])
                o.save()
            return "Course " + args[1] + " has been added to the data base."
    else:
        return ""


def create_account(args):
    pass


def edit_account(args):
    pass


def assign_instructor(args):
    pass


def assign_ta_to_course(args):
    pass


def assign_ta_to_lab(args):
    pass


def edit_contact_info(args):
    pass


def view_course_assignments(args):
    pass


def view_ta_assignments(args):
    pass


def read_contact_info(args):
    pass


commandList = [help, login, logout, create_course, create_account, edit_account, assign_instructor, assign_ta_to_course,
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