from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm,UserSearch
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

@login_required(login_url="signin") 
def home(request):
    user = request.user
    profile = Profile.objects.get(username=user)
    profiles=Profile.objects.all()
    friendship = Friendship.objects.filter(Q(user1=user) | Q(user2 = user))
    idCheck=0
    if UserStatus.objects.filter(user = user):
        stat = UserStatus.objects.get(user = user)
        stat.status = True
        stat.save()
    else:
        UserStatus.objects.create(user = user,status=True)
    
    if request.method == 'POST':
        if "postImage" in request.FILES:
            postImage = request.FILES['postImage']
            postContent = request.POST['postContent']
            Posts.objects.create(username=user,postImg=postImage,content=postContent)
            return redirect('home')
        if "create-story" in request.FILES:
            createStory = request.FILES['create-story']
            Stories.objects.create(user=user,story=createStory)
        if request.POST.get('btnId'):
            btnId = request.POST.get('btnId')
            print(btnId)
            inv =Profile.objects.get(id=btnId)
            print(inv)
            Invitations.objects.create(sent_by= user,sent_to= inv.username)
            
            ms = {'message': 'ok'}
            return JsonResponse(ms)
            
    postss=Posts.objects.all()
    my=[]
    for i in postss:
        for j in friendship:
            if i.username == j.user1 or i.username== j.user2:
                my.append(i)
    posts = list(set(my))
    posts.reverse()

    myStory = []
    if Stories.objects.filter(user=user):
        myStory=Stories.objects.get(user=user)
    else:
        myStory = "none"
    friendsStories=[]
    for i in friendship:
        if i.user1 == user:
            friendStory = Stories.objects.filter(user=i.user2)
            if friendStory:
                for j in friendStory:
                    friendsStories.append({"name":j.user.username,"img":j.story})
        if i.user2 == user:
            friendStory = Stories.objects.filter(user=i.user1)
            if friendStory:
                for j in friendStory:
                    friendsStories.append({"name":j.user.username,"img":j.story})
    suggestions=[]
    for i in profiles:
        name = i.username
        if Friendship.objects.filter(Q(user1=user) & Q(user2 = name)):
            pass
        elif Friendship.objects.filter(Q(user1=name) & Q(user2 = user)):
            pass
        elif Invitations.objects.filter(Q(sent_by=name) & Q(sent_to = user)):
            pass
        elif Invitations.objects.filter(Q(sent_to=name) & Q(sent_by = user)):
            pass
        elif name == user:
            pass
        else:
            suggestions.append({"name":name,"img":i.profileImg, "id":i.id})
   
    context = {
        "user":user,
        "profile":profile,
        "profiles":profiles,
        "friendship":friendship,
        "posts":posts,
        "friendsStories":friendsStories,
        "myStory":myStory,
        "suggestions":suggestions,
   
    }
    return render(request, 'appOne/home.html',context)

@login_required(login_url="signin") 
def messages(request):
    user = request.user
    profiles=Profile.objects.all()
    profile = Profile.objects.get(username=user)
    friendship = Friendship.objects.filter(Q(user1=user) | Q(user2 = user))
    for i in friendship:
        if Rooms.objects.filter(Q(userOne=i.user1) & Q(userTwo = i.user2) | Q(userOne=i.user2) & Q(userTwo = i.user1)).exists():
            pass
        else:
            Rooms.objects.create(userOne=i.user1,userTwo = i.user2)

    if request.method == 'POST':
        if "postImage" in request.FILES:
            postImage = request.FILES['postImage']
            postContent = request.POST['postContent']
            Posts.objects.create(username=user,postImg=postImage,content=postContent)
            return redirect('profile')
        
    context = {
        "user":user,
        "profile":profile,
        "profiles":profiles,
        "friendship":friendship,
    }
    return render(request, 'appOne/messages.html',context)

@login_required(login_url="signin") 
def notification(request):
    user = request.user
    profile = Profile.objects.get(username=user)
    myPosts = Posts.objects.filter(username=user)
    notifications = Notifications.objects.all()
    nf=[]
    
    for j in myPosts:
            if  Notifications.objects.filter(post = j.id):
                note = Notifications.objects.filter(post = j.id).order_by('-create_date')
                for i in note:
                    nf.append({"username":i.user.username,"img":i.user.profile.profileImg.url,"notification":i.notification})
            else:
                pass
    if request.method == 'POST':
        if "postImage" in request.FILES:
            postImage = request.FILES['postImage']
            postContent = request.POST['postContent']
            Posts.objects.create(username=user,postImg=postImage,content=postContent)
            return redirect('profile')
    context = {
        "user":user,
        "profile":profile,
        "notifications":nf
    }
    return render(request, 'appOne/notification.html',context)

@login_required(login_url="signin") 
def invitation(request):
    user = request.user
    profile = Profile.objects.get(username=user)
    invitations = Invitations.objects.filter(sent_to=user)
    if request.method == 'POST':
        if "postImage" in request.FILES:
            postImage = request.FILES['postImage']
            postContent = request.POST['postContent']
            Posts.objects.create(username=user,postImg=postImage,content=postContent)
            return redirect('profile')
    context = {
        "user":user,
        "profile":profile,
        "invitations":invitations,
    }
    return render(request, 'appOne/invitation.html',context)

@login_required(login_url="signin") 
def search(request):
    user = request.user
    profile = Profile.objects.get(username=user)
    friendship = Friendship.objects.filter(Q(user1=user) | Q(user2 = user))
    search_q = request.GET.get('search_query')
    form = UserSearch()
    results = form.filter_results(search_q)
    rs1=[]
    rs2=[]
    for i in results:
        if friendship.filter(Q(user1=i.id) | Q(user2=i.id)):
            rs1.append({"username":i.username,"img":i.profile.profileImg.url,"id":i.id})
        else:
            rs2.append({"username":i.username,"img":i.profile.profileImg.url,"id":i.id})
    if request.method == 'POST':
        if "postImage" in request.FILES:
            postImage = request.FILES['postImage']
            postContent = request.POST['postContent']
            Posts.objects.create(username=user,postImg=postImage,content=postContent)
            return redirect('profile')
    context = {
        "user":user,
        "profile":profile,
        "rs1":rs1,
        "rs2":rs2
    }
    return render(request, 'appOne/search.html',context)

@login_required(login_url="signin") 
def profile(request):
    user = request.user
    
    user_profile = Profile.objects.get(username=user)

    if request.method == 'POST':
        if "profileFileImg" in request.FILES:
            user_profile.profileImg = request.FILES["profileFileImg"]
        elif "cuvertureFileImag" in request.FILES:
            user_profile.cuvertureImg = request.FILES["cuvertureFileImag"]
        user_profile.save()
        if "postImage" in request.FILES:
            postImage = request.FILES['postImage']
            postContent = request.POST['postContent']
            Posts.objects.create(username=user,postImg=postImage,content=postContent)
            return redirect('profile')
    profile = Profile.objects.get(username = user)
    profiles = Profile.objects.all()
    myPosts = Posts.objects.filter(username = user).order_by('-create_date')
    friendship = Friendship.objects.filter(Q(user1=user) | Q(user2 = user))
    context = {
        "user":user,
        "profile":profile,
        "profiles":profiles,
        "myPosts":myPosts,
        "friendship":friendship
    }
    return render(request, 'appOne/profile.html',context)

@login_required(login_url="signin") 
def saves(request):
    user = request.user
    profile = Profile.objects.get(username=user)
    saves = Saves.objects.filter(username=user)
    allPosts = Posts.objects.all()
    posts=[]
    for i in saves:
        for j in allPosts:
            if i.post == j.id:
                posts.append({"username":j.username.username,"profileImg":j.username.profile.profileImg.url,"img":j.postImg.url,"id":j.id,
                "content":j.content})
    if request.method == 'POST':
        if "postImage" in request.FILES:
            postImage = request.FILES['postImage']
            postContent = request.POST['postContent']
            Posts.objects.create(username=user,postImg=postImage,content=postContent)
            return redirect('profile')
    context = {
        "user":user,
        "profile":profile,
        "posts":posts,
      
    }
    return render(request, 'appOne/saves.html',context)






def signup(request):
    if request.user.is_authenticated:
	    return redirect('home')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(username=username, email=email, password=password)
                Profile.objects.create(username=user)               
                return redirect('signin')
        else:
            form = SignUpForm()
    return render(request, 'appOne/signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            checkbox = request.POST.get('checkbox')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not checkbox:
                    request.session.set_expiry(0)
                return redirect('home')
            else:
                messages.error(request, 'Your username or password is incorrect') 
    return render(request, 'appOne/signIn.html')

def logoutUser (request):
    user=request.user
    stat = UserStatus.objects.get(user = user)
    stat.status = False
    stat.save()
    logout(request)
    return redirect('signin')


@login_required(login_url="signin") 
@csrf_exempt  
def my_view(request):
    lst = {}
    lstU={}
    lstImg={}
    if request.method == 'POST':
        postId = request.POST.get("id")
        allComments =Comments.objects.filter(post = postId)
        profiles = Profile.objects.all()
        for i in allComments:
            lstU[i.id]= i.username.username
            lst[i.id]= i.comment
            for j in profiles:
                if j.username.username == i.username.username:
                    lstImg[i.id]= j.profileImg.url
            
        data = {'message': lst,
        'users':lstU,
        'imgs':lstImg
        }
        return JsonResponse(data)
    return JsonResponse({'message': 'Error: Invalid request method.'})

@login_required(login_url="signin") 
def save_post(request):
    user = request.user
    lst = []
    if request.method == 'POST':
        data = json.loads(request.body)
        idNumber = data.get('idNumber')
        msg = data.get('msg')
        if msg == "save":
            if Saves.objects.filter(username = user,post = idNumber):
                pass
            else:
                Saves.objects.create(username = user,post = idNumber)
            return JsonResponse({'message': 'Saved'})
        if msg == "notSave":
            item = Saves.objects.filter(username = user,post = idNumber)
            item.delete()
            return JsonResponse({'message': 'deleted'})
        if msg == "saved!":
            items = Saves.objects.filter(username = user)
            for i in items:
                lst.append(i.post)
           
            return JsonResponse({'message': lst})
    return JsonResponse({'message': 'Error: Invalid request method.'})

@login_required(login_url="signin") 
def heart_post(request):
    user = request.user
    lst = []
    if request.method == 'POST':
        data = json.loads(request.body)
        idNumber = data.get('idNumber')
        msg = data.get('msg')
        msgg = data.get('msgg')

        if msg == "heart":
            if Hearts.objects.filter(username = user,post = idNumber):
                pass
            else:
                Hearts.objects.create(username = user,post = idNumber)
            return JsonResponse({'message': 'Saved'})
        if msg == "notHeart":
            item = Hearts.objects.filter(username = user,post = idNumber)
            item.delete()
            return JsonResponse({'message': 'deleted'})
        if msgg == "heart!":
            items = Hearts.objects.filter(username = user)
            for i in items:
                lst.append(i.post)
           
            return JsonResponse({'message': lst})
    return JsonResponse({'message': 'Error: Invalid request method.'})

@login_required(login_url="signin") 
def stat(request):
    user = request.user
    friendship = Friendship.objects.filter(Q(user1=user) | Q(user2 = user))
    lst = []
    lstImg=[]
    if request.method == "POST":
        
        for i in friendship:
            if i.user1 == user:
                us2 = i.user2
                if UserStatus.objects.filter(user=us2).exists():
                    
                    f = UserStatus.objects.get(user =us2) 
                    if f.status == True:
                        lst.append(f.user.username)
                        print(lst)
            elif i.user2 == user:
                us1 = i.user1
                if UserStatus.objects.filter(user=us1).exists():
                    d = UserStatus.objects.get(user =us1) 
                    if d.status == True:
                        lst.append(d.user.username)
                        
        profiles = Profile.objects.all()
        for i in profiles:
            for j in lst:
                if i.username.username == j:
                    lstImg.append(i.profileImg.url)
        return JsonResponse({'users': lst,
                            'usersImg':lstImg})
    return JsonResponse({'message': 'Error: Invalid request method.'})

@login_required(login_url="signin") 
def userStaff(request):
    if request.method == 'POST':
        messages=[]
        userId = request.POST.get("id")
        user = User.objects.get(id=userId)
        room = Rooms.objects.get(Q(userOne=user) & Q(userTwo = request.user) | Q(userOne=request.user) & Q(userTwo = user))
        for i in Messages.objects.filter(Q(user=user) & Q(room = room.id) | Q(user=request.user) & Q(room = room.id)).order_by('create_date'):
            messages.append({
                'id':i.user.id,
                'message':i.message
            })

        return JsonResponse({'user': user.username,'url':user.profile.profileImg.url,'room_id':room.id,'messages':messages})
    return JsonResponse({'message': 'Error: Invalid request method.'})

@login_required(login_url="signin") 
def createInvitation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sent_by=data.get("sent_by")
        sent_to=data.get("sent_to")
        fUser = User.objects.get(id=sent_by)
        lUser = User.objects.get(id=sent_to)

        if Invitations.objects.filter(Q(sent_by=fUser) & Q(sent_to = lUser) | Q(sent_by=lUser) & Q(sent_to = fUser)):
            pass
        else:
            Invitations.objects.create(sent_by=fUser ,sent_to = lUser)

        return JsonResponse({"message":"completed"})
    return JsonResponse({'message': 'Error: Invalid request method.'})

@login_required(login_url="signin") 
def createFriends(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        invId=data.get("invId")
        invParteners = Invitations.objects.get(id=invId)
        

        if Friendship.objects.filter(Q(user1=invParteners.sent_by) & Q(user2 = invParteners.sent_to) | Q(user1=invParteners.sent_to) & Q(user2 = invParteners.sent_by)):
            invParteners.delete()
        else:
            Friendship.objects.create(user1=invParteners.sent_by,user2=invParteners.sent_to)
            invParteners.delete()

        return JsonResponse({"message":"completed"})
    return JsonResponse({'message': 'Error: Invalid request method.'})

def pageNotFound(request, exception=None):
    return render(request, 'appOne/pageNotFound.html',status=404)
