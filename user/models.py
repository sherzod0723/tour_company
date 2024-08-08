from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from cart.models import Cart, CartItem
from .managers import UserManager


# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
        null=True,
    )
    photo = models.ImageField(upload_to='user_image/', default='/static/user_image/default.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def count_cart_items(self):
        count = 0
        user_cart = Cart.objects.filter(user_id=self.id)
        if user_cart:
            count = CartItem.objects.filter(cart_id=user_cart.first().id).count()
        return count

    objects = UserManager()

    def __str__(self):
        if self.username:
            return self.username
        return f"{self.first_name} {self.last_name}"


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    text = models.TextField()
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.stars}"



