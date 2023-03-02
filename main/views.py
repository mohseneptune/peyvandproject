from django.shortcuts import render


def home_view(request):
    template_name = 'main/home.html'
    template_title = 'صفحه اصلی'


    context = {
        'template_title': template_title
    }
    return render(request, template_name, context)



def contact_view(request):
    template_name = 'main/contact.html'
    template_title = 'تماس با ما'


    context = {
        'template_title': template_title
    }
    return render(request, template_name, context)


def about_view(request):
    template_name = 'main/about.html'
    template_title = 'درباره ما'


    context = {
        'template_title': template_title
    }
    return render(request, template_name, context)