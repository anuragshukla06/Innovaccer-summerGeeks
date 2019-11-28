from django.shortcuts import render, redirect
from . import forms
from . import models
# from . import way2sms_api
import datetime
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template import loader
from twilio.rest import Client


# Create your views here.
account_sid = 'Enter Twilio sid'
auth_token = 'Enter Twilio Auth Token'
client = Client(account_sid, auth_token)


Meeting_Token = 0 # This has to be unique
Guest_Token = 0

def home(request):
    return render(request, 'main/homepage.html', {})

def host_registration(request):
    global Meeting_Token
    if request.method == 'POST':
        H_RegForm = forms.HostRegForm(request.POST or None)

        if (H_RegForm.is_valid()):
            host_name = H_RegForm.cleaned_data['host_name']
            phone = H_RegForm.cleaned_data['phone']
            meeting_name = H_RegForm.cleaned_data['meeting_name']
            address = H_RegForm.cleaned_data['address']
            email = H_RegForm.cleaned_data['email']

            try:
                existing_host = models.Host.objects.get(email=email)
                existing_meet = models.Meeting.objects.get(meeting_name=meeting_name, host=existing_host)
                return render(request, 'main/host_registration.html', {'EXISTING_MEET_FLAG': 1})
            except Exception as e:

                print(e)

                host = models.Host(host_name=host_name, phone=phone, email=email)
                host.save()
                meeting = models.Meeting(meeting_name=meeting_name, address=address, host=host, token=Meeting_Token)
                Meeting_Token += 1
                meeting.save()
                return render(request, 'main/hostPostRegistration.html', {'Token': meeting.token})
        else:
            return render(request, 'main/host_registration.html', {'EXISTING_MEET_FLAG': 2})
    else:
        return render(request, 'main/host_registration.html', {'EXISTING_MEET_FLAG': 0})

def showMeetings(request):
    meetings = models.Meeting.objects.all()
    return render(request, 'main/showMeetings.html', {'meetings': meetings})

def guestRegForm(request, meeting_pk):
    global Guest_Token
    if request.method == 'POST':
        G_RegForm = forms.GuestRegForm(request.POST or None)
        if (G_RegForm.is_valid()):
            guest_name = G_RegForm.cleaned_data['guest_name']
            guest_phone = G_RegForm.cleaned_data['guest_phone']
            guest_mail = G_RegForm.cleaned_data['guest_mail']
            meeting_id = G_RegForm.cleaned_data['meeting_id']

            meeting = models.Meeting.objects.get(pk = meeting_id)
            guest = None
            try:
                guest = models.Guest.objects.get(guest_mail=guest_mail)
                if guest.checked_in == True:
                    return render(request, 'main/guestRegForm.html', {'ALREADY_CHECKED_IN': 1})
                else:
                    guest.checked_in = True
                    guest.check_in_time = datetime.datetime.now()
                    guest.meeting = meeting
                    guest.token=Guest_Token
                    guest.save()
                    sendEmailHost(guest)
            except Exception as e:
                print(e)
                guest = models.Guest(guest_name=guest_name, guest_phone=guest_phone, guest_mail=guest_mail, meeting=meeting, token=Guest_Token)
                guest.save()
                sendEmailHost(guest)
            Guest_Token += 1
            return render(request, 'main/guestPostRegistration.html', {'Token': guest.token})
        else:
            print(G_RegForm.errors)
            return render(request, 'main/guestRegForm.html', {'ALREADY_CHECKED_IN': 3})

    else:

        meeting = None
        try:
            meeting = models.Meeting.objects.get(pk = meeting_pk)
        except:
            return HttpResponse("something went wrong.")
        return render(request, 'main/guestRegForm.html', {"meeting": meeting
            , "meeting_id": meeting_pk})



def check_out(request):

    if request.method == 'POST':
        CO_form = forms.CheckOutForm(request.POST or None)
        if (CO_form.is_valid()):
            guest_mail = CO_form.cleaned_data['guest_mail']
            token = CO_form.cleaned_data['token']

            try:
                guest = models.Guest.objects.get(guest_mail=guest_mail)
                if guest.token == token:
                    if guest.checked_in:
                        msg = 'You are successfully checked out from the meeting.'
                        checkoutGuestHelper(guest, msg)
                        return render(request, 'main/checkoutPage.html', {'Invalid': 0, "msg": "You are checked out"})
                    else:
                        return render(request, 'main/checkoutPage.html', {'Invalid': 0, "msg": "You were already checked out"})
                else:
                    return render(request, 'main/checkoutPage.html', {'Invalid': 1, "msg": "Invalid Token"})
            except Exception as e:
                print(e)
                return render(request, 'main/checkoutPage.html',
                              {'Invalid': 1, "msg": "Guest with given email doesn't exist."})
    else:
        return render(request, 'main/checkoutPage.html', {})

def manage(request, email, token):
    NO_GUESTS = 0
    meeting = models.Meeting.objects.get(token=token)
    guests = models.Guest.objects.filter(meeting=meeting, checked_in=True)
    if len(guests) == 0: NO_GUESTS = 1

    return render(request, 'main/managePage.html', {'guests': guests, 'email': email, 'token':token, 'NO_GUESTS': NO_GUESTS})



def manageForm(request):

    if request.method == 'POST':
        HD_form = forms.HostDetailsForm(request.POST or None)
        if (HD_form.is_valid()):
            host_mail = HD_form.cleaned_data['host_mail']
            token = HD_form.cleaned_data['token']
            try:
                if models.Meeting.objects.get(token=token).host.email == host_mail:
                    return redirect(manage, host_mail, token)
                else:
                    return render(request, 'main/manageForm.html', {'Invalid': 1})
            except Exception as e:
                print(e)
                return render(request, 'main/manageForm.html', {'Invalid': 1})
        else:
            return render(request, 'main/manageForm.html', {'Invalid': 1})
    else:
        return render(request, 'main/manageForm.html', {'Invalid': 0})

def kickoutGuest(request, email, token, guest_pk):
    guest = models.Guest.objects.get(pk=guest_pk)
    msg = "You are checked out by the Host."
    checkoutGuestHelper(guest, msg)
    return redirect(manage, email, token)

def checkoutGuestHelper(guest, msg):
    guest.checked_in = False
    guest.checked_out_time = datetime.datetime.now()

    check_in_time = guest.check_in_time
    check_out_time = guest.checked_out_time
    address = guest.meeting.address
    host_name = guest.meeting.host.host_name
    meeting_name = guest.meeting.meeting_name
    # zerosms.sms('9399151865', 'E9366Q', str(guest.guest_phone), 'hello there!')

    details = {'guest_name': guest.guest_name, 'check_in_time': check_in_time,
               'check_out_time': check_out_time, 'address': address,
               'host_name': host_name, 'meeting_name': meeting_name}
    # zerosms.sms(phno=9399151865,passwd='E9366Q',message='helloworld!!',receivernum='9653088794')


    html_text = loader.render_to_string('main/guest_email.html', {'msg': msg,
                                                            'details': details})
    subject = "Your Meeting Details"


    plain_text_msg = "Dear " + guest.guest_name+ ",\n" + "Thank You for using the application. " + msg +"Here are your details: \n Meeting Name:" +  meeting_name + "\n Host: " + host_name + "\n Address: " + address + "Check-In Time: " + str(check_in_time) + "Check-Out Time: " + str(check_out_time)

    send_mail(subject, plain_text_msg, guest.guest_mail, [guest.guest_mail], html_message=html_text)

    message = client.messages.create(
        from_='+12055579239',
        body=plain_text_msg,
        to='+917526812579'
    )

    print(message.sid)

    guest.save()

def sendEmailHost(guest):
    check_in_time = guest.check_in_time
    guest_name = guest.guest_name
    guest_email = guest.guest_mail
    guest_phone = guest.guest_phone
    host_mail = guest.meeting.host.email
    host_name = guest.meeting.host.host_name

    plain_text_msg = "Dear " + host_name+ ",\n" +"A guest hust signed in!: \n Guest Name:" +  guest_name + "\n Guest Phone: " + str(guest_phone) + "\n Email: " + guest_email + "Check-In Time: " + str(check_in_time)


    try:
        message = client.messages.create(
            from_='Enter Your Phone Here',
            body=plain_text_msg,
            to=host_mail
        )
    except Exception as e:
        print(e)

    print(message.sid)

    print(guest_name, "This is the statement")
    details = {'guest_name': guest_name, 'check_in_time': check_in_time,
                   'guest_email': guest_email, 'guest_phone': guest_phone, "host_name": host_name}

    html_text = loader.render_to_string('main/host_email.html', {'details': details})
    subject = "Guest Details"
    send_mail(subject, 'plain_text', host_mail, [host_mail], html_message=html_text)


