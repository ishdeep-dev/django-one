from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import Topic, Webpage, AccessRecord, FormData, UserProfileInfo
from django.contrib.auth.models import User
from . import forms
from first_app.forms import UserForm,UserProfileInfoForm



from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    my_dict={'insert_me':"Hellllllllooooooooooo Mooooo"}
    return render(request,'first_app/index.html',context=my_dict)


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))


def rel(request):
    return render(request,'first_app/linking.html')


def register(request):
    return render(request,'first_app/register.html')



def help(request):
    webpages_list=FormData.objects.order_by('name')
    date_dict={'access_records':webpages_list}
    return render(request,'first_app/index.html',context=date_dict)



def reg(request):
    form1=forms.FormName()
    if request.method=='POST':
        form1=forms.FormName(request.POST)

        if form1.is_valid():
            form1.save(commit=True)
            return help(request)
    return render(request,'first_app/forming.html',{'form':form1})



def register(request):

    registered = False


    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'picture' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.picture = request.FILES['picture']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'first_app/register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})




def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'first_app/login.html', {})
