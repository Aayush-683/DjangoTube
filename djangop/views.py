# Import necessary modules and classes
from django.shortcuts import render, redirect
from django.http import HttpResponse
from db.models import User, Videos, Likes, Subscriptions
from db.forms import LoginForm, RegisterForm, VideoForm

# Create your views here.

# Define a view for the homepage
def home(request):
    # Retrieve all videos from the database
    videos = Videos.objects.all()
    videos = list(videos)
    # Get the username from the session
    username = request.session.get("username")
    subs = None
    if username:
        try:
            # Try to fetch the user object based on the username
            user = User.objects.get(name=username)
            # Get the user's subscriptions
            subs = Subscriptions.objects.filter(user=user)
            subs = list(subs)
        except:
            subs = None
    return render(request, "home.html", {"videos": videos, "subn": subs})


# Define a view for user login
def login(request):
    # Check if the user is already logged in
    if request.session.get("username"):
        return redirect("/")
    form = LoginForm()
    return render(request, "login.html", {"authtype": "Login", "form": form})


# Define a view for user registration
def register(request):
    # Check if the user is already logged in
    if request.session.get("username"):
        return redirect("/")
    form = RegisterForm()
    return render(request, "login.html", {"authtype": "Register", "form": form})


# Define a view for user authentication
def authenticate(request):
    if request.method == "GET":
        # If the request method is GET, return an "Invalid Request" response
        return HttpResponse("Invalid Request")
    else:
        if request.POST["authtype"] == "Login":
            # Check if the authentication type is "Login"
            form = LoginForm(request.POST)
            if form.is_valid():
                # If the form is valid, extract the username and password from the form
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                try:
                    user = User.objects.get(name=username)
                    # Attempt to retrieve a user with the provided username
                    if user.password == password:
                        # If the password matches, set the session username and redirect to the homepage
                        request.session["username"] = username
                        return redirect("/")
                    else:
                        # If the password is incorrect, render the login page with an error message
                        return render(
                            request,
                            "login.html",
                            {
                                "authtype": "Login",
                                "form": form,
                                "error": "Invalid Password",
                            },
                        )
                except:
                    # If the user does not exist, render the login page with an error message
                    return render(
                        request,
                        "login.html",
                        {
                            "authtype": "Login",
                            "form": form,
                            "error": "User does not exist",
                        },
                    )
            else:
                # If the form is not valid, render the login page with an error message
                return render(
                    request,
                    "login.html",
                    {"authtype": "Login", "form": form, "error": "Invalid Credentials"},
                )
        elif request.POST["authtype"] == "Register":
            form = RegisterForm(request.POST)
            if form.is_valid():
                # If the authentication type is "Register" and the form is valid, proceed to registration
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                confirm_password = form.cleaned_data["confirm_password"]
                if password == confirm_password:
                    # If the passwords match, attempt to retrieve a user with the provided username
                    try:
                        user = User.objects.get(name=username)
                        # If the user already exists, render the registration page with an error message
                        return render(
                            request,
                            "login.html",
                            {
                                "authtype": "Register",
                                "form": form,
                                "error": "User already exists",
                            },
                        )
                    except:
                        # If the user does not exist, create a new user, set the session username, and redirect to the homepage
                        user = User(name=username, password=password)
                        user.save()
                        request.session["username"] = username
                        return redirect("/")
                else:
                    # If the passwords do not match, render the registration page with an error message
                    return render(
                        request,
                        "login.html",
                        {
                            "authtype": "Register",
                            "form": form,
                            "error": "Passwords do not match",
                        },
                    )
            else:
                # If the form is not valid, render the registration page with an error message
                return render(
                    request,
                    "login.html",
                    {
                        "authtype": "Register",
                        "form": form,
                        "error": "Invalid Credentials",
                    },
                )


def logout(request):
    # Clear the session username and redirect to the login page
    request.session["username"] = None
    return redirect("/login")

# Define a view for handling video uploads
def upload(request):
    if request.method == "GET":
        # If the request method is GET (i.e., accessing the upload page), check if the user is authenticated
        username = request.session.get("username")
        if username is None:
            # If the user is not authenticated, redirect to the login page
            return redirect("/login/")
        else:
            # If the user is authenticated, render the upload page with a VideoForm
            return render(request, "upload.html", {"form": VideoForm()})
    else:
        # If the request method is not GET (i.e., submitting the upload form), check if the user is authenticated
        username = request.session.get("username")
        if username is None:
            # If the user is not authenticated, redirect to the login page
            return redirect("/login/")
        else:
            # If the user is authenticated, retrieve the user object
            user = User.objects.get(name=username)
            # Create a VideoForm with the POST data and uploaded files
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                # If the form is valid, extract the video title, video file, and thumbnail file
                title = form.cleaned_data["title"]
                video = form.cleaned_data["video"]
                thumbnail = form.cleaned_data["thumbnail"]
                # Create a new Videos object with the extracted data and link it to the user
                video = Videos(title=title, video=video, thumbnail=thumbnail, user=user)
                video.save()
                # Redirect to the user's page with a success message
                return redirect("/user?name=" + username + "&upload=success")
            else:
                # If the form is not valid, print form errors and render the upload page with the form and errors
                print(form.errors)
                print(form.non_field_errors)
                print(form)
                return render(request, "upload.html", {"form": form})

# Define a view for handling video deletion
def delete(request):
    if request.method == "GET":
        # If the request method is GET (i.e., accessing the delete page), check if the user is authenticated
        username = request.session.get("username")
        if username is None:
            # If the user is not authenticated, redirect to the login page
            return redirect("/login/")
        else:
            # If the user is authenticated, render the delete page
            return render(request, "delete.html")
    else:
        # If the request method is not GET (i.e., submitting the delete form), check if the user is authenticated
        username = request.session.get("username")
        id = request.POST.get("id")
        if username is None or id is None:
            # If either the user or video ID is missing, return a 404 response
            return HttpResponse(status=404)
        try:
            # Try to retrieve the video object with the given ID
            vidObj = Videos.objects.get(id=id)
            if vidObj.user.name == username:
                # If the video belongs to the authenticated user, delete it
                vidObj.delete()
            else:
                # If the video does not belong to the user, render the delete page with an error message
                return render(
                    request,
                    "delete.html",
                    {"error": "That video does not belong to you!"},
                )
            # Render the delete page with a success message
            return render(
                request, "delete.html", {"error": "Video was deleted successfully!"}
            )
        except:
            # If there's an exception (e.g., video not found), render the delete page with an error message
            return render(
                request,
                "delete.html",
                {"error": "Unable to find a video with id: " + id},
            )

# Define a view to display user videos
def myvideos(request):
    # Get the 'name' and 'upload' parameters from the request's GET data
    username = request.GET.get("name")
    success = request.GET.get("upload")

    chk = False  # Initialize a flag variable 'chk' as False

    if success == "success":
        # If the 'success' parameter is equal to the string "success", set 'chk' to True
        chk = True
    else:
        chk = False

    if username is None:
        # If the 'username' is not provided in the request, redirect to the login page
        return redirect("/login/")
    else:
        try:
            # Try to retrieve the user object with the provided 'username'
            user = User.objects.get(name=username)

            # Retrieve the current user using the session 'username'
            u2 = User.objects.get(name=request.session.get("username"))

            # Fetch the subscriptions for the current user 'u2'
            subs = Subscriptions.objects.filter(user=u2)
            subs = list(subs)

            # Retrieve videos uploaded by the user with 'username'
            videos = Videos.objects.filter(user=user)
            videos = list(videos)

            if len(videos) == 0:
                # If there are no videos, set 'videos' to None
                videos = None

            # Render the home page with user videos, the 'chk' flag, and subscription information
            return render(
                request, "home.html", {"videos": videos, "chk": chk, "subn": subs}
            )
        except:
            # If there's an exception (e.g., user not found), return a 404 response
            return HttpResponse(status=404)

# Define a view to display a video and its details
def video(request):
    # Get the 'id' parameter from the request's GET data
    id = request.GET["id"]

    # Retrieve the video object with the provided 'id'
    try:
        video = Videos.objects.get(id=id)
    except:
        # If there's an exception (e.g., video not found), return a 404 response
        return HttpResponse(status=404)

    # Fetch the likes for the video
    likes = Likes.objects.filter(video=video)

    if likes is None:
        # If there are no likes, set 'likes' to 0
        likes = 0
    else:
        # Calculate the number of likes
        likes = len(likes)

    subscribed = False  # Initialize a flag variable 'subscribed' as False
    liked = False  # Initialize a flag variable 'liked' as False

    username = request.session.get("username")

    subs = None  # Initialize a variable 'subs' as None

    if username is not None:
        # If a user is logged in, retrieve their user object
        user = User.objects.get(name=username)

        # Fetch all the user's subscriptions
        subs = Subscriptions.objects.filter(user=user)
        subs = list(subs)

        try:
            # Check if the user is subscribed to the channel of the video
            sub = Subscriptions.objects.get(user=user, channel=video.user)
            # Set the 'subscribed' flag to True
            subscribed = True
        except:
            pass

        try:
            # Check if the user has liked the video
            like = Likes.objects.get(user=user, video=video)
            # Set the 'liked' flag to True
            liked = True
        except:
            pass

    # Render the 'video.html' template with video details, likes, subscription, and like information
    return render(
        request,
        "video.html",
        {
            "video": video,
            "likes": likes,
            "subscribed": subscribed,
            "liked": liked,
            "subn": subs,
        },
    )

# Define a view for subscribing to channels and displaying subscribed content
def sub(request):
    if request.method == "GET":
        # Check if the request method is GET
        username = request.session.get("username")
        if username is None:
            # If the user is not logged in, redirect to the login page
            return redirect("/login/")
        else:
            user = User.objects.get(name=username)
            # Get the user object of the logged-in user

            subs = Subscriptions.objects.filter(user=user)
            if subs is None:
                # If there are no subscriptions, render a page with no subscriptions
                return render(request, "home.html", {"subs": None})
            else:
                subs2 = Subscriptions.objects.filter(user=user)
                subs2 = list(subs)
                channels = []
                for sub in subs:
                    channels.append(sub.channel)
                # Get a list of subscribed channels

                # Initialize a list to store videos from subscribed channels
                videos = []
                for channel in channels:
                    videos.append(Videos.objects.filter(user=channel))
                # Retrieve videos from the subscribed channels

                subs = []
                for video in videos:
                    subs += list(video)
                subs = list(subs)
                if len(subs) == 0:
                    subs = None
                # Combine videos from channels and check if there are any

                # Render a page with subscribed content and subscriptions
                return render(request, "home.html", {"subs": subs, "subn": subs2})
    else:
        # If the request method is not GET, it's likely a POST request
        channelName = request.POST["channel"]
        username = request.session.get("username")
        if username is None:
            # If the user is not logged in, redirect to the login page
            return redirect("/login/")
        elif channelName == username:
            # If a user tries to subscribe to their own channel, redirect to their profile
            return redirect("/user?name=" + username)
        else:
            try:
                user = User.objects.get(name=username)
                # Get the user object of the logged-in user
                Channel = User.objects.get(name=channelName)
                # Get the user object of the channel to be subscribed to

                subChk = Subscriptions.objects.filter(user=user, channel=Channel)
                if len(subChk) == 0:
                    # If the user is not already subscribed, create a subscription and save it
                    sub = Subscriptions(user=user, channel=Channel)
                    sub.save()
                else:
                    # If the user is already subscribed, delete the subscription
                    sub = Subscriptions.objects.get(user=user, channel=Channel)
                    sub.delete()
            except:
                return HttpResponse(status=204)
                # If there's an error, respond with a status code 204 (No Content)

        return HttpResponse(status=204)
        # Respond with a status code 204 (No Content)

# Define a view for managing likes on videos
def like(request):
    if request.method == "GET":
        # Check if the request method is GET
        username = request.session.get("username")
        if username is None:
            # If the user is not logged in, redirect to the login page
            return redirect("/login/")
        else:
            user = User.objects.get(name=username)
            # Get the user object of the logged-in user

            subs = Subscriptions.objects.filter(user=user)
            subs = list(subs)
            likes = Likes.objects.filter(user=user)
            if likes is None:
                # If the user has no likes, render a page with no likes
                return render(request, "home.html", {"likes": None, "subn": subs})
            else:
                likes = list(likes)
                if len(likes) == 0:
                    likes = None
                # If the user has likes, render a page with the liked content

                # Render a page with the user's likes and subscriptions
                return render(request, "home.html", {"likes": likes, "subn": subs})
    else:
        # If the request method is not GET, it's likely a POST request
        videoId = request.POST["videoId"]
        username = request.session.get("username")
        if username is None:
            # If the user is not logged in, redirect to the login page
            return redirect("/login/")
        else:
            try:
                user = User.objects.get(name=username)
                # Get the user object of the logged-in user
                video = Videos.objects.get(id=videoId)
                # Get the video object to be liked

                likeChk = Likes.objects.filter(user=user, video=video)
                if len(likeChk) == 0:
                    # If the user has not liked this video, create a like and save it
                    like = Likes(user=user, video=video)
                    like.save()
                else:
                    # If the user has already liked this video, delete the like
                    like = Likes.objects.get(user=user, video=video)
                    like.delete()
            except:
                print("Error")
                return HttpResponse(status=204)
                # If there's an error, respond with a status code 204 (No Content)

        return HttpResponse(status=204)
        # Respond with a status code 204 (No Content)