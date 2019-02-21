from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from contacts.models import Contact
from django.conf import settings

def contact(request):

    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, 'You have already contacted this realtor concerning this property')
                return redirect('/listings/' + listing_id)

        contact = Contact(
            listing_id = listing_id,
            listing = listing,
            name = name,
            email = email,
            phone = phone, 
            message = message,
            user_id = user_id
        )

        contact.save()

        # send_mail(
        #     'Property listing inquiry',
        #     'There has been an enquiry for ' + listing + '. Sign into admin panel for more info',
        #     settings.EMAIL_HOST_USER,
        #     [realtor_email,],
        #     fail_silently=False
        # )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you shortly')
        return redirect('/listings/' + listing_id)