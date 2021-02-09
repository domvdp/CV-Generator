from django.shortcuts import render
from .models import Profile
from django.http import HttpResponse
from django.template import loader
import pdfkit
import io


config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")


# Create your views here.
def form(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        address = request.POST.get("address", "")
        postcode = request.POST.get("postcode", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        school = request.POST.get("school", "")
        job = request.POST.get("job", "")

        profile = Profile(first_name=first_name, last_name=last_name, address=address, postcode=postcode, phone=phone, email=email, school=school, job=job)

        profile.save()
    return render(request, "form.html")


def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template("resume.html")
    html = template.render({'user_profile': user_profile})

    pdf = pdfkit.from_string(html, False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content=Disposition'] = 'attachments'

    return response


def list(request):
    profile=Profile.objects.all()
    return render(request, "list.html", {'profile': profile})
