from django.forms import ModelForm, IntegerField
from django.contrib.auth.forms import UserCreationForm
from .models import User, Testimonial


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class TestimonialForm(ModelForm):
    stars = IntegerField(required=False)

    class Meta:
        model = Testimonial
        fields = ['text', "stars"]