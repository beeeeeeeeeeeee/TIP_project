from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info in ["/login/", "/image/code/"]:
            return
        # print("M1 middle ware in")
        info_dict = request.session.get("info")
        if info_dict:
            return

        # return HttpResponse("No authority to visit")
        return redirect("/login/")
