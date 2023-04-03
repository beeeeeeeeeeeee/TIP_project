import random
import googlemaps
from openpyxl import load_workbook
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from django.db.models import Q

from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from app01.utilis.encrypt import md5
from app01.utilis.code import check_code
from django.utils.safestring import mark_safe
from io import BytesIO
import json
from app01.utilis.pagination import Pagination
from django.http import JsonResponse
from datetime import datetime


# Create your views here.

class AddressModelForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = "__all__"
        # exclude = ("lat", "long")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def address_list(request):
    search_value = request.POST.get("q", "")

    if search_value:
        queryset = models.Address.objects.filter(
            Q(address__icontains=search_value) | Q(suburb__icontains=search_value) | Q(
                postcode__icontains=search_value)).order_by("-aid")
        # queryset = models.Address.objects.filter(
        #     Q(address__icontains=search_value) & Q(suburb__icontains=search_value)).order_by("-aid")
        form = AddressModelForm()
        content = {
            "form": form,
            "queryset": queryset,
            "search_value": search_value
        }
        return render(request, "address_list.html", content)

    queryset = models.Address.objects.all().order_by("-aid")
    page_object = Pagination(request, queryset)

    form = AddressModelForm()
    content = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_value": search_value

    }
    return render(request, "address_list.html", content)


def address_add(request):
    title = "Add New Address"
    if request.method == "GET":
        form = AddressModelForm()
        return render(request, "address_add.html", {"form": form, "title": title})

    form = AddressModelForm(data=request.POST)
    if form.is_valid():
        address = request.POST.get("address")
        suburb = request.POST.get("suburb")
        postcode = request.POST.get("postcode")
        lat = request.POST.get("lat")
        long = request.POST.get("long")
        print(address)

        exists = models.Address.objects.filter(address=address, suburb=suburb, postcode=postcode).exists()
        if exists:
            address_id = models.Address.objects.filter(address=address, suburb=suburb, postcode=postcode).first().aid
            form = AddressModelForm()
            alert = f"The address is exist, and the Address ID is {address_id}, please double check"
            return render(request, "address_add.html", {"form": form, "alert": alert})

        print(address, suburb, postcode, lat, long)
        form.save()
        return redirect("/address/list/")
    return render(request, "address_add.html", {"form": form, "title": title})


def address_multi(request):
    # "bulk upload"
    file_object = request.FILES.get("exc")
    # print(type(file_object))
    wb = load_workbook(file_object)
    sheet = wb.worksheets[1]
    # from the second rows min_row=2
    for row in sheet.iter_rows(min_row=2):
        aid = row[0].value
        address = row[1].value
        suburb = row[2].value
        postcode = row[3].value
        latitude = row[4].value
        longitude = row[5].value
        models.Address.objects.create(aid=aid, address=address, suburb=suburb, postcode=postcode,
                                      lat=latitude, long=longitude)
        # print(aid, address, suburb, postcode, latitude,longitude)

    return redirect("/address/list/")


def address_edit(request, nid):
    row_object = models.Address.objects.filter(aid=nid).first()
    title = "Edit Address"

    if request.method == "GET":
        form = AddressModelForm(instance=row_object)
        return render(request, "address_add.html", {"form": form, "title": title})

    form = AddressModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/address/list/")
    else:
        return render(request, "address_add.html", {"form": form, "title": title})


class PianoModelForm(forms.ModelForm):
    class Meta:
        model = models.Piano
        fields = "__all__"
        # exclude = ("lat", "long")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def piano_list(request):
    search_value = request.POST.get("q", "")

    if search_value:
        queryset = models.Piano.objects.filter(
            Q(brand__icontains=search_value) | Q(model__icontains=search_value) | Q(
                sub_model__icontains=search_value) | Q(colour__icontains=search_value)).order_by("-pid")
        # queryset = models.Address.objects.filter(
        #     Q(address__icontains=search_value) & Q(suburb__icontains=search_value)).order_by("-aid")
        form = PianoModelForm()
        content = {
            "form": form,
            "queryset": queryset,
            "search_value": search_value
        }
        return render(request, "piano_list.html", content)
    queryset = models.Piano.objects.all().order_by("-pid")
    page_object = Pagination(request, queryset)

    form = PianoModelForm()
    content = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()

    }
    return render(request, "piano_list.html", content)


def piano_multi(request):
    # "bulk upload"
    file_object = request.FILES.get("exc")
    # print(type(file_object))
    wb = load_workbook(file_object)
    sheet = wb.worksheets[2]
    # from the second rows min_row=2
    for row in sheet.iter_rows(min_row=2):
        pid = row[0].value
        brand = row[1].value
        model = row[2].value
        sub_model = row[3].value
        colour = row[4].value
        piano_type = row[5].value
        models.Piano.objects.create(pid=pid, brand=brand, model=model, sub_model=sub_model,
                                    colour=colour, type=piano_type)
        # print(pid, brand, model, sub_model, colour, piano_type)

    return redirect("/piano/list/")


def piano_add(request):
    title = "Add New Piano"
    if request.method == "GET":
        form = PianoModelForm()
        return render(request, "add.html", {"form": form, "title": title})

    form = PianoModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/piano/list/")
    return render(request, "add.html", {"form": form, "title": title})


def piano_edit(request, nid):
    row_object = models.Piano.objects.filter(pid=nid).first()
    title = "Edit Piano"

    if request.method == "GET":
        form = PianoModelForm(instance=row_object)
        return render(request, "add.html", {"form": form, "title": title})

    form = PianoModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/piano/list/")
    else:
        return render(request, "add.html", {"form": form, "title": title})


class CPAModelForm(forms.ModelForm):
    class Meta:
        model = models.CPA
        fields = "__all__"
        # fields = ["aid","pid]
        # exclude = ("lat", "long")
        # widgets = {"aid": forms.TextInput(),"pid":forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def cpa_list(request):
    queryset = models.CPA.objects.all().order_by("-cid")
    page_object = Pagination(request, queryset)

    form = CPAModelForm()
    content = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()

    }
    return render(request, "cpa_list.html", content)


def cpa_multi(request):
    # "bulk upload"
    file_object = request.FILES.get("exc")
    # print(type(file_object))
    wb = load_workbook(file_object)
    sheet = wb.worksheets[0]
    # from the second rows min_row=2
    for row in sheet.iter_rows(min_row=2):
        cid = row[0].value
        uid = row[1].value
        aid = row[2].value
        pid = row[3].value
        sn = row[4].value
        sales = row[5].value
        co_sales = row[6].value
        sold_date = row[7].value
        active = row[8].value
        directly_sold = row[9].value
        models.CPA.objects.create(cid=cid, uid=uid, aid_id=aid, pid_id=pid, sn=sn, sales=sales, co_sales=co_sales,
                                  sold_date=sold_date, active=active, directly_sold=directly_sold)
        # print(cid, uid, aid, pid, sn, sales, co_sales, sold_date, active, directly_sold)

    return redirect("/cpa/list/")


def cpa_add(request):
    title = "Add New CPA Information"
    if request.method == "GET":
        form = CPAModelForm()
        return render(request, "add.html", {"form": form, "title": title})

    form = CPAModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/cpa/list/")
    return render(request, "add.html", {"form": form, "title": title})


def cpa_edit(request, nid):
    row_object = models.CPA.objects.filter(cid=nid).first()
    title = "Edit CPA Information"

    if request.method == "GET":
        form = CPAModelForm(instance=row_object)
        return render(request, "add.html", {"form": form, "title": title})

    form = CPAModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/cpa/list/")
    else:
        return render(request, "add.html", {"form": form, "title": title})


class TuningModelForm(forms.ModelForm):
    class Meta:
        model = models.Tuning
        fields = "__all__"
        # fields = ["aid","pid]
        # exclude = ("lat", "long")
        # widgets = {"aid": forms.TextInput(),"pid":forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def tuning_list(request):
    queryset = models.Tuning.objects.all().order_by("-tid")
    page_object = Pagination(request, queryset)

    form = TuningModelForm()
    content = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()

    }
    return render(request, "tuning_list.html", content)


def tuning_multi(request):
    # "bulk upload"
    file_object = request.FILES.get("exc")
    # print(type(file_object))
    wb = load_workbook(file_object)
    sheet = wb.worksheets[3]
    # from the second rows min_row=2
    for row in sheet.iter_rows(min_row=2):
        tid = row[0].value
        mid = row[1].value
        cid = row[2].value
        tuning_date = row[3].value
        piano_condition = row[4].value
        models.Tuning.objects.create(tid=tid, mid=mid, cid_id=cid, tuning_date=tuning_date,
                                     piano_condition=piano_condition)

        # print(cid, uid, aid, pid, sn, sales, co_sales, sold_date, active, directly_sold)

    return redirect("/tuning/list/")


def tuning_add(request):
    title = "Add New Tuning Information"
    if request.method == "GET":
        form = TuningModelForm()
        return render(request, "add.html", {"form": form, "title": title})

    form = TuningModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/tuning/list/")
    return render(request, "add.html", {"form": form, "title": title})


def tuning_edit(request, nid):
    row_object = models.Tuning.objects.filter(tid=nid).first()
    title = "Edit Tuning Information"

    if request.method == "GET":
        form = TuningModelForm(instance=row_object)
        return render(request, "add.html", {"form": form, "title": title})

    form = TuningModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/tuning/list/")
    else:
        return render(request, "add.html", {"form": form, "title": title})
