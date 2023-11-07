from .forms import UserRegisterForm,profile_updation_form1,profile_updation_form2,profile_updation_form3,profile_updation_form4
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
import datetime
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q,F, ExpressionWrapper, fields
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import user_passes_test

def is_created1(user) :
    try :
        profile_personal_info.objects.get(user=user)
        return True
    except profile_personal_info.DoesNotExist:
        return False
def is_created2(user) :
    personal=profile_personal_info.objects.get(user=user)
    try :
        profile_educational_and_career_info.objects.get(profile_id=personal.id)
        return True
    except profile_educational_and_career_info.DoesNotExist:
        return False
def is_created3(user) :
    personal=profile_personal_info.objects.get(user=user)
    try :
        profile_family_details.objects.get(profile_id=personal.id)
        return True
    except profile_family_details.DoesNotExist:
        return False
def is_created4(user) :
    personal=profile_personal_info.objects.get(user=user)
    try :
        partner_preferences.objects.get(profile_id=personal.id)
        return True
    except partner_preferences.DoesNotExist:
        return False

# Create your views here.
def register(request):
    
    if request.method=='POST':
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account has been created succesfully for {username},now you can login')
            return redirect('login')
        else:
            messages.error(request,"Error Signing up")
            print(form.error_messages)
            return redirect("register")
    else:
        form =UserRegisterForm()
    return render(request,'users/register.html',{'form':form}) 
def landing(request):
    
    return render(request,'users/landing.html')
def about(request):
    return render(request,'users/about.html')


@login_required
@user_passes_test(is_created1, 'createform1')
@user_passes_test(is_created2, 'createform2')
@user_passes_test(is_created3, 'createform3')
@user_passes_test(is_created3, 'createform4')
def home(request):
    if request.user.is_authenticated:
    #try:
        x = request.user.username
        Gender=profile_personal_info.objects.get(user=User.objects.get(username=x)).gender
        
        # without usin select_related
        #preferences=partner_preferences.objects.get(profile_id=(profile_personal_info).objects.get(user=(User.objects.get(username=x))).id)
        
        # Use select_related to fetch the partner preferences and related profile_personal_info
        preferences = partner_preferences.objects.select_related('profile_id__user').get(profile_id__user__username=x)
        p_heigth=preferences.height
        
        p_income=preferences.income
        specific_income = p_income
        income_range = 5 
        min_income = specific_income - income_range
        max_income = specific_income + income_range
        with_p_income= profile_educational_and_career_info.objects.filter(income__gte=min_income, income__lte=max_income)[:1]

        h = profile_personal_info.objects.annotate(height_diff=ExpressionWrapper(F('height') - p_heigth,output_field=fields.IntegerField()))
        
        
        with_p_heigth=h.order_by('height_diff')[:1]
        prefered_family_details = profile_family_details.objects.filter(Q(religion__icontains=preferences.religion) | Q(mothertounge__icontains=preferences.mothertounge) |Q(caste__icontains=preferences.caste)  &(~Q(profile_id__gender=Gender)))
        prefered_personal_details=profile_personal_info.objects.filter( Q(marital_status=preferences.marital_status) & (~Q(gender=Gender)))
        prefered_career_details=profile_educational_and_career_info.objects.filter((Q(occupation__icontains=preferences.occupation) | Q(qualification__icontains=preferences.qualificaton)) &(~Q(profile_id__gender=Gender)))
        
        # contents={'firstname':profile_personal_info.objects.get(user=User.objects.get(username=x)).firstname,
        # 'lastname':profile_personal_info.objects.get(user=User.objects.get(username=x)).lastname,
        # 'city':profile_personal_info.objects.get(user=User.objects.get(username=x)).city,
        # 'state':profile_personal_info.objects.get(user=User.objects.get(username=x)).state,
        # 'occupation':profile_educational_and_career_info.objects.get(profile_id=(profile_personal_info).objects.get(user=(User.objects.get(username=x))).id).occupation,
        # 'caste':profile_family_details.objects.get(profile_id=(profile_personal_info).objects.get(user=(User.objects.get(username=x))).id).caste,
        # 'pic_url':profile_personal_info.objects.get(user=User.objects.get(username=x)).image_pic.url
        # }
        # print(with_p_income)
        # print( with_p_heigth)
        #print( prefered_career_details)
        return render(request,'users/home.html', {
            'prefered_personal_details': prefered_personal_details,
            'prefered_family_details': prefered_family_details,
            'prefered_career_details': prefered_career_details,
            'with_p_income': with_p_income,
            'with_p_heigth': with_p_heigth,
            'gender':Gender,
        })
        
    else:
        return render(request,'users/home.html')
    # except User.DoesNotExist:
    #     # Handling the case when the user does not exist
    #     return render(request, 'error.html', {'message': 'User not found'})
    # except (profile_personal_info.DoesNotExist, partner_preferences.DoesNotExist):
    #     # Handle the case when user profile or preferences do not exist
    #     return render(request, 'error.html', {'message': 'Profile or preferences not found'})

    # except Exception as e:
    #     # Handle other exceptions and show an error message
    #     return render(request, 'error.html', {'message': str(e)})





@login_required
def profile(request,id):
    # if request.method=='POST':
    #     button_action = request.POST.get('button_action')
    #     if button_action == 'bookmark':
    #         add_to_bookmarks(request,id)
            
            
    #x = request.user.username
    # contents={'firstname':profile_personal_info.objects.get(user=User.objects.get(username=x)).firstname,
    # 'lastname':profile_personal_info.objects.get(user=User.objects.get(username=x)).lastname,
    # 'city':profile_personal_info.objects.get(user=User.objects.get(username=x)).city,
    # 'state':profile_personal_info.objects.get(user=User.objects.get(username=x)).state,
    # 'occupation':profile_educational_and_career_info.objects.get(profile_id=(profile_personal_info).objects.get(user=(User.objects.get(username=x))).id).occupation,
    # 'caste':profile_family_details.objects.get(profile_id=(profile_personal_info).objects.get(user=(User.objects.get(username=x))).id).caste,
    # 'pic_url':profile_personal_info.objects.get(user=User.objects.get(username=x)).image_pic.url
    # }
    #id = request.GET.get(id)
    
    user=User.objects.get(pk=id)
    personal_info1=profile_personal_info.objects.get(user=user)
    career_details=profile_educational_and_career_info.objects.get(profile_id=personal_info1.id)
    family_details=profile_family_details.objects.get(profile_id=personal_info1.id)
    prefernces_details=partner_preferences.objects.get(profile_id=personal_info1.id)
    friendrequests=FriendRequest.objects.filter((Q(to_user=user) | Q(from_user=user)) ,Q(status='accepted'))
    z=friendrequests.first()
    print(friendrequests)
    print(z)
    return render(request,'users/profile.html',{'otheruser':user,'personal_info1':personal_info1,
                                                'career_details':career_details,'family_details':family_details,
                                                'prefernces_details':prefernces_details,
                                                'z':z})  
@login_required
def updateform1(request):
    if request.method == 'POST':
        form1=profile_updation_form1(request.POST,request.FILES,instance=request.user.profile_personal_info)
        if form1.is_valid():
            form1.save()
            messages.success(request,f'Your account has been Updated!')
            dynamic_url = f'/profile/{request.user.id}'
            return HttpResponseRedirect(dynamic_url)
    else:
        form1=profile_updation_form1(instance=request.user.profile_personal_info)
        context={
            'form1':form1
        }
        return render(request,'users/updateform1.html',context)
@login_required
def updateform2(request):
    if request.method == 'POST':
        form2=profile_updation_form2(request.POST,request.FILES,instance=request.user.profile_personal_info.profile_educational_and_career_info)
        if form2.is_valid():
            form2.save()
            messages.success(request,f'Your account has been Updated!')
            dynamic_url = f'/profile/{request.user.id}'
            return HttpResponseRedirect(dynamic_url)
    else:
        form2=profile_updation_form2(instance=request.user.profile_personal_info.profile_educational_and_career_info)
        context={
            'form2':form2
        }
        return render(request,'users/updateform2.html',context)
@login_required
def updateform3(request):
    if request.method == 'POST':
        form3=profile_updation_form3(request.POST,request.FILES,instance=request.user.profile_personal_info.profile_family_details)
        if form3.is_valid():
            form3.save()
            messages.success(request,f'Your account has been Updated!')
            dynamic_url = f'/profile/{request.user.id}'
            return HttpResponseRedirect(dynamic_url)
    else:
        form3=profile_updation_form3(instance=request.user.profile_personal_info.profile_family_details)
        context={
            'form3':form3
        }
        return render(request,'users/updateform3.html',context)
@login_required
def updatepreferences(request):
    if request.method == 'POST':
        form4=profile_updation_form4(request.POST,request.FILES,instance=request.user.profile_personal_info.partner_preferences)
        if form4.is_valid():
            form4.save()
            messages.success(request,f'Your account has been Updated!')
            dynamic_url = f'/profile/{request.user.id}'
            return HttpResponseRedirect(dynamic_url)
    else:
        form4=profile_updation_form4(instance=request.user.profile_personal_info.partner_preferences)
        context={
            'form4':form4
        }
        return render(request,'users/updatepreferences.html',context)
  
  
  
# class ProfileListView(ListView):
#     template_name = 'users/home.html'  # Set your desired template name here
#     def get_gender(self):
#         x = self.request.user.username
#         Gender=profile_personal_info.objects.get(user=User.objects.get(username=x)).gender
#         return Gender
#     def get_queryset_p(self):
        
#         x = self.request.user.username
#         # without usin select_related
#         #preferences=partner_preferences.objects.get(profile_id=(profile_personal_info).objects.get(user=(User.objects.get(username=x))).id)
            
#         # Use select_related to fetch the partner preferences and related profile_personal_info
#         preferences = partner_preferences.objects.select_related('profile_id__user').get(profile_id__user__username=x)
        
#         return preferences

#     def get_queryset_x(self):
#         preferences = self.get_queryset_p()
#         Gender=self.get_gender()  

        
#         prefered_personal_details=profile_personal_info.objects.filter( Q(marital_status=preferences.marital_status) & (~Q(gender=Gender)))
#         # prefered_personal_details = prefered_personal_details | with_p_heigth
#         return prefered_personal_details

#     def get_queryset_y(self):
#         preferences = self.get_queryset_p()
#         Gender=self.get_gender()  
       
#         prefered_career_details=profile_educational_and_career_info.objects.filter((Q(occupation__icontains=preferences.occupation) | Q(qualification__icontains=preferences.qualificaton)) &(~Q(profile_id__gender=Gender)))
#         # prefered_career_details = prefered_career_details | with_p_income
#         return prefered_career_details

#     def get_queryset_z(self):
#         preferences = self.get_queryset_p()
#         Gender=self.get_gender()  
#         prefered_family_details = profile_family_details.objects.filter(Q(religion__icontains=preferences.religion) | Q(mothertounge__icontains=preferences.mothertounge) |Q(caste__icontains=preferences.caste)  &(~Q(profile_id__gender=Gender)))
    
#         # Combine the querysets here if needed
#         return prefered_family_details
#     def get_queryset(self):
        
#         # x = self.request.user.username
#         # Gender=profile_personal_info.objects.get(user=User.objects.get(username=x)).gender
        
#         # # without usin select_related
#         # #preferences=partner_preferences.objects.get(profile_id=(profile_personal_info).objects.get(user=(User.objects.get(username=x))).id)
        
#         # # Use select_related to fetch the partner preferences and related profile_personal_info
#         # preferences = partner_preferences.objects.select_related('profile_id__user').get(profile_id__user__username=x)
#         # p_heigth=preferences.height
        
#         # p_income=preferences.income
#         # specific_income = p_income
#         # income_range = 5 
#         # min_income = specific_income - income_range
#         # max_income = specific_income + income_range
#         # with_p_income= profile_educational_and_career_info.objects.filter(income__gte=min_income, income__lte=max_income)[:10]

#         # h = profile_personal_info.objects.annotate(height_diff=ExpressionWrapper(F('height') - p_heigth,output_field=fields.IntegerField()))
        
        
#         # with_p_heigth=h.order_by('height_diff')[:10]
#         # prefered_family_details = profile_family_details.objects.filter(Q(religion__icontains=preferences.religion) | Q(mothertounge__icontains=preferences.mothertounge) |Q(caste__icontains=preferences.caste)  &(~Q(profile_id__gender=Gender)))
#         # prefered_personal_details=profile_personal_info.objects.filter( Q(marital_status=preferences.marital_status) & (~Q(gender=Gender)))
#         # prefered_career_details=profile_educational_and_career_info.objects.filter((Q(occupation__icontains=preferences.occupation) | Q(qualification__icontains=preferences.qualificaton)) &(~Q(profile_id__gender=Gender)))
#         combined_queryset=list(self.get_queryset_x()) + list(self.get_queryset_y()) + list(self.get_queryset_z())
#         return combined_queryset
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # In the get_context_data method
#         preferences=self.get_queryset_p()
#         p_heigth=preferences.height
            
        
#         h = profile_personal_info.objects.annotate(height_diff=ExpressionWrapper(F('height') - p_heigth,output_field=fields.IntegerField()))
            
            
#         with_p_heigth=h.order_by('height_diff')[:10]
        
#         p_income=preferences.income
#         specific_income = p_income
#         income_range = 5 
#         min_income = specific_income - income_range
#         max_income = specific_income + income_range
#         with_p_income= profile_educational_and_career_info.objects.filter(income__gte=min_income, income__lte=max_income)[:10]
#         # Add the querysets to the context
#         context['prefered_personal_details'] = self.get_queryset_x()
#         context['prefered_career_details'] = self.get_queryset_y()
#         context['prefered_family_details'] = self.get_queryset_z()
#         context['with_p_heigth'] = with_p_heigth
        
#         # You can also add other context data if needed
#         context['gender'] = self.get_gender()
#         context['with_p_income'] = with_p_income
        
#         return context 
    
class ProfileDetailedView(DetailView):
    model=profile_personal_info
    template_name='users/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve data from ModelX
        profile_x = profile_personal_info.objects.get(pk=self.object.pk)

        # Retrieve related data from ModelY and ModelZ
        profile_y = profile_educational_and_career_info.objects.get(profile_id=profile_x)  # Replace related_field_x with the actual field name
        profile_z = profile_family_details.objects.get(profile_id=profile_x)  # Replace related_field_x with the actual field name

        context['profile_personal_info'] = profile_x
        context['profile_educational_and_career_info'] = profile_y
        context['profile_family_details'] = profile_z

        return context
    
@login_required
def add_to_bookmarks(request, id):
        # Retrieve specific attributes from ProfilePersonalInfo
    if request.method=='POST':
        
        personal_info = profile_personal_info.objects.get(user=User.objects.get(pk=id))
        firstname = personal_info.firstname  # Replace with the specific attribute name
        lastname = personal_info.lastname  # Replace with the specific attribute name
        # image = personal_info.image_pic  # Replace with the specific attribute name
        city = personal_info.city  # Replace with the specific attribute name
        state = personal_info.state  # Replace with the specific attribute name

        # Retrieve specific attributes from ProfileEducation
        profile_education = profile_educational_and_career_info.objects.get(profile_id=personal_info.id)
        occupation = profile_education.occupation  # Replace with the specific attribute name

        # Retrieve specific attributes from ProfileFamily
        profile_family = profile_family_details.objects.get(profile_id=personal_info.id)
        religion = profile_family.religion  # Replace with the specific attribute name
        caste = profile_family.caste  # Replace with the specific attribute name

        # Create a Shortlist entry with the specific attributes
        bookmark,created=Bookmark.objects.get_or_create(user=request.user, firstname=firstname, lastname=lastname, state=state,city=city,
                                occupation=occupation,religion=religion,caste=caste,no=id)
        if created:
            # Bookmark added successfully
            bookmark.image=personal_info.image_pic
            bookmark.save()
            messages.success(request, 'Profile added to bookmarks!')
        else:
            # Profile was already in bookmarks
            messages.info(request, 'Profile is already in bookmarks.')
            
        # Redirect back to the profile or a success page
        return redirect('profile',id=id)
@login_required
def bookmarks(request):
    # Retrieve the profiles in the user's shortlist
    shortlisted_profiles = Bookmark.objects.filter(user=request.user)

    return render(request, 'users/shortlist.html', {'shortlisted_profiles': shortlisted_profiles})
    

@login_required
def send_friend_request(request, to_user_id):
    if request.user.is_authenticated:
        to_user = User.objects.get(id=to_user_id)
        
        friend_request,created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if created:
            friend_request.save()
            messages.success(request, f'friend request is sent to {to_user.profile_personal_info.firstname}!')
        
        else:
            # Profile was already in bookmarks
            messages.info(request, f'you had already sent request to {to_user.profile_personal_info.firstname}')
        return redirect('sent_requests')
    else:
        pass
    
        # Handle unauthorized user
@login_required
def received_requests(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    
    
    return render(request, 'users/received_requests.html', {'received_requests': received_requests})
@login_required
def accepted_requests(request):
    accepted_requests = FriendRequest.objects.filter(Q(from_user=request.user, status='accepted') | Q(to_user=request.user, status='accepted'))
    return render(request, 'users/accepted_requests.html', {'accepted_requests': accepted_requests})

@login_required
def sent_requests(request):
    sent_requests_pending = FriendRequest.objects.filter(from_user=request.user, status='pending')    
    sent_requests_declined = FriendRequest.objects.filter(from_user=request.user, status='declined')    
    
    return render(request, 'users/sent_requests.html', { 'sent_requests_pending': sent_requests_pending,
                                                          'sent_requests_declined':sent_requests_declined})


@login_required
def accept_friend_request(request, request_id):
    
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id=request_id)
        if friend_request.to_user == request.user:
            friend_request.status = 'accepted'
            friend_request.save()
            messages.success(request,f'You had accepted {friend_request.from_user.profile_personal_info.firstname} friend request')
        return redirect('accepted_requests')
    
@login_required
def decline_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id=request_id)
        if friend_request.to_user == request.user:
            friend_request.status = 'declined'
            friend_request.save()
        return redirect('received_requests')
@login_required   
def unbookmark(request, item_id):
    if request.method == 'POST':
        bookmark = Bookmark.objects.filter(user=request.user, no=item_id).first()
        name=bookmark.firstname
        bookmark.delete()
        messages.success(request, f'you have UnBookmarked the {name} profile !')

    return redirect('bookmarks')

@login_required
def createform1(request):
    if request.method == 'POST':
        form1=profile_updation_form1(request.POST,request.FILES)
       
        if form1.is_valid():
            profile_info = form1.save(commit=False)  # Don't save to the database yet
            profile_info.user = request.user  # Set the user
            profile_info.save()
            messages.success(request,f'Your personal account has been created!')
            
            return redirect('createform2')
    else:
        form1=profile_updation_form1()
        context={
            'form1':form1
        }
        return render(request,'users/updateform1.html',context)
@login_required
def createform2(request):
    if request.method == 'POST':
        form2=profile_updation_form2(request.POST,request.FILES)
        personal=profile_personal_info.objects.get(user=request.user)
        if form2.is_valid():
            profile_info = form2.save(commit=False)  # Don't save to the database yet
            profile_info.profile_id = personal  # Set the user
            profile_info.save()
            messages.success(request,f'Your educational account has been created!')
            
            return redirect('createform3')
    else:
        form2=profile_updation_form2()
        context={
            'form2':form2
        }
        return render(request,'users/updateform2.html',context)
@login_required
def createform3(request):
    if request.method == 'POST':
        form3=profile_updation_form3(request.POST,request.FILES)
        personal=profile_personal_info.objects.get(user=request.user)
        if form3.is_valid():
            profile_info = form3.save(commit=False)  # Don't save to the database yet
            profile_info.profile_id = personal # Set the user
            profile_info.save()
            messages.success(request,f'Your family background details has been created!')
            return redirect('createform4')
    else:
        form3=profile_updation_form3()
        context={
            'form3':form3
        }
        return render(request,'users/updateform3.html',context)
@login_required
def createform4(request):
    if request.method == 'POST':
        form4=profile_updation_form4(request.POST,request.FILES)
        personal=profile_personal_info.objects.get(user=request.user)
        if form4.is_valid():
            profile_info = form4.save(commit=False)  # Don't save to the database yet
            profile_info.profile_id = personal  # Set the user
            profile_info.save()
            messages.success(request,f'Your partner preferences been created!')
            messages.success(request,f'here are your preferences!')
            return redirect('home')
    else:
        form4=profile_updation_form4()
        context={
            'form4':form4
        }
        return render(request,'users/updatepreferences.html',context)
    