from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from . models import Contact


def contact(request):
	if request.method == "POST":
		listing_id = request.POST['listing_id']
		listing = request.POST['listing']
		name = request.POST['name']
		email = request.POST['email']
		phone = request.POST['phone']
		message = request.POST['message']
		user_id = request.POST['user_id']
		realtor_email = request.POST['realtor_email']

		#check if user has alredy made an enquiry
		if request.user.is_authenticated:
			user_id = request.user.id
			has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
			if has_contacted:
				messages.error(request, "You have already made an enquiry for this listing.")
				return redirect('/listings/'+listing_id)

		contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
		contact.save()

		#Send Email
		msg = "Name : " + name + "\nPhone Number : " + phone + "\nEmail ID : " + email + "\nMessage : " + message

		send_mail(
			'You have a new enquiry for property listing: ' + listing, # subject
			'There is new enquiry for the property \n'+ listing +'\n Sign in to the admin area for more info. \n' + msg, # message
			email, # from mail
			['<email-id>', realtor_email], # to mail
			)

		messages.success(request, 'Your request has been submitted and the realtor will get back to you soon.')

		return redirect('/listings/'+listing_id)