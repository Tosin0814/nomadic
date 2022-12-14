import uuid
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm, AvailabilityForm, PropertyReviewForm,LikeForm
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.contrib import messages
from .models import ProfilePicture, User, Property, PropertyFeature, Photo, Availability, Like, Review,Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

S3_BASE_URL = 'https://s3-ca-central-1.amazonaws.com/'
BUCKET = 'nomadic-leozhao'

# def choose_signup(request):
#   return render(request, 'registration/choose_signup.html')


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # Create a 'user' form object that includes the data from the browser
    form = NewUserForm(request.POST)
    if form.is_valid():
      # Add the user to the database
      user = form.save()
      # Login after signing up
      login(request, user)
      return redirect('profile_view', pk = user.id)
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = NewUserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

  

# class ProfilePage(LoginRequiredMixin, DetailView):
#   model = User
#   template_name = 'user/profile.html'

class ProfileView(LoginRequiredMixin, DetailView):
  model = User
  template_name = 'user/profile.html'

class ProfileUpdate(LoginRequiredMixin, UpdateView):
  model = User
  template_name = 'user/updateuser.html'
  fields = ['email']
  success_url = '/'

class ProfileDelete(LoginRequiredMixin, DeleteView):
  model = User
  template_name = 'user/confirm_delete.html'
  success_url = '/'

class PropertyList(ListView):
  model = Property
  template_name = 'property/index.html'

@login_required
def property_detail(request, property_id):
  user_like = Like.objects.filter(property=property_id, user=request.user)
  property = Property.objects.get(id=property_id)
  not_available = Reservation.objects.filter(property = property_id).values_list('availability', flat=True)
  reservation_user = Reservation.objects.filter(property = property_id, user=request.user).values_list('user', flat=True)
  property_review_form = PropertyReviewForm
  features_property_doesnt_have = PropertyFeature.objects.exclude(id__in = property.property_features.all().values_list('id'))
  features_property_doesnt_have_id = PropertyFeature.objects.exclude(id__in = property.property_features.all().values_list('id')).values_list("id", flat=True)
  availability_form = AvailabilityForm
  return render(request, 'property/detail.html',{
    'property': property,
    'features_property_doesnt_have': features_property_doesnt_have,
    'availability_form' : availability_form,
    'property_review_form' : property_review_form,
    'user_like': user_like,
    'not_available' : not_available,
    'reservation_user': reservation_user,
    'features_property_doesnt_have_id': features_property_doesnt_have_id
  })

class PropertyCreate(LoginRequiredMixin, CreateView):
  model = Property
  fields = ['title', 'description', 'location', 'price']
  template_name = 'property/createproperty.html'
  def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PropertyUpdate(LoginRequiredMixin, UpdateView):
  model = Property
  fields = ['title', 'description', 'location', 'price']
  template_name = 'property/createproperty.html'

class PropertyDelete(LoginRequiredMixin, DeleteView):
  model = Property
  template_name = 'property/confirm_delete.html'
  success_url = '/'

@login_required
def associate_property_feature(request, property_id, property_feature_id):
  Property.objects.get(id=property_id).property_features.add(property_feature_id)
  return redirect('property_detail', property_id=property_id)

@login_required
def dissociate_property_feature(request, property_id, property_feature_id):
  Property.objects.get(id=property_id).property_features.remove(property_feature_id)
  return redirect('property_detail', property_id=property_id)

@login_required
def add_photo(request, property_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          # build the full url string
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
          # we can assign to property_id or property (if you have a property object)
          photo = Photo(photo_url=url, property_id=property_id)
          photo.save()
      except:
          print('An error occurred uploading file to S3')
  return redirect('property_detail', property_id=property_id)

@login_required
def delete_photo_page(request, property_id):
  property = Property.objects.get(id=property_id)
  return render(request, 'property/property_photos.html',{
    'property': property,
  })

@login_required
def delete_photo(request, property_id, photo_id):
  Property.objects.get(id = property_id).photo_set.filter(id = photo_id).delete()
  return redirect('delete_photo_page', property_id = property_id)

@login_required
def add_profile_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        # First delete previous photo (Only one photo is allowed)
        existing_photos = ProfilePicture.objects.filter(user_id=user_id)
        if existing_photos:
            existing_photos.delete()
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to user_id or user (if you have a user object)
            profile_picture = ProfilePicture(url=url, user_id=user_id)
            profile_picture.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile_view', pk=user_id)

# Add Availability

@login_required
def add_availability(request, property_id):
  form = AvailabilityForm(request.POST)
  if form.is_valid():
    new_availbility = form.save(commit=False)
    new_availbility.property_id = property_id
    new_availbility.save()
  return redirect('property_detail', property_id = property_id)

@login_required
def delete_availability(request, property_id, availability_id):
  Property.objects.get(id = property_id).availability_set.filter(id = availability_id).delete()
  return redirect('property_detail', property_id = property_id)

class AvailabiblityUpdate(LoginRequiredMixin, UpdateView):
  model = Availability
  form_class = AvailabilityForm
  template_name = 'property/availability_form.html'


# Add Property Review
@login_required
def review_property(request, property_id):
    form = PropertyReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.user_name = request.user.username
        new_review.property_id = property_id
        new_review.save()
    return redirect('property_detail', property_id = property_id)


class HostProfileView(LoginRequiredMixin, DetailView):
  model = Property
  template_name = 'property/host_profile.html'

# Like
@login_required
def add_like(request, property_id):
    property = Property.objects.get(id = property_id)
    user = request.user
    if not Like.objects.filter(property = property, user = user).exists():
      new_like = Like(property = property, user = user)
      new_like.save()
    return redirect('property_detail', property_id = property_id)

@login_required
def remove_like(request,property_id):
  property = Property.objects.get(id = property_id)
  user = request.user
  if Like.objects.filter(property = property, user = user).exists():
     Like.objects.filter(property = property, user = user).delete()
  return redirect('property_detail', property_id = property_id)

@login_required
def make_reservation(request, property_id, availability_id):
  availability = Availability.objects.get(id = availability_id)
  user = request.user
  property = Property.objects.get(id = property_id)
  if not Reservation.objects.filter(availability = availability).exists():
    new_reservation = Reservation(availability = availability, user = user, property = property)
    new_reservation.save()
  return redirect('property_detail', property_id = property_id)

@login_required
def cancel_reservation(request, property_id, availability_id):
  if Reservation.objects.filter(availability = availability_id).exists():
     Reservation.objects.filter(availability = availability_id).delete()
  return redirect('property_detail', property_id = property_id)

@login_required
def reservation_list(request, user_id):
  reservation_list = Reservation.objects.all()
  context = {'reservation_list': reservation_list}
  return render(request, 'user/reservations.html', context)