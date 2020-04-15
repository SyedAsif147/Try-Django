from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail
from .utils import code_generator
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class ProfileManager(models.Manager):
	def toggle_follow(self, request_user , username_to_toggle):
		profile_=Profile.objects.get(user__username__iexact=username_to_toggle)
		user=request_user
		is_following = False
		if user in profile_.followers.all():
			profile_.followers.remove(user)
		else:
			profile_.followers.add(user)
			is_following=True
		return profile_, is_following


class Profile(models.Model):		#ForeignKey is replaced by one to one and many to many fields
	user 			= models.OneToOneField(User, on_delete=models.CASCADE) 	#user.profile.all()
	followers		= models.ManyToManyField(User, related_name='is_following', blank=True)	#user.is_following.all()
	#following		= models.ManyToManyField(User, related_name='following', blank=True)	#user.following.all()
	activation_key	= models.CharField(max_length=120, blank=True, null=True)
	activated		= models.BooleanField(default=False)	#for registration
	timestamp		= models.DateTimeField(auto_now_add=True)
	updated			= models.DateTimeField(auto_now=True)


	objects = ProfileManager()

	def __str__(self):
		return self.user.username

	def send_activation_email(self):
		if not self.activated:
			self.activation_key = code_generator() # utils.py #genkey
			self.save()
			path_ = reverse('activate', kwargs={"code":self.activation_key})
			subject = 'Activate Account'
			from_email = settings.DEFAULT_FROM_EMAIL
			message = f'Activate your account here: {path_}'
			recipient_list = [self.user.email]
			html_message = f'<p>Activate your account here: {path_}</p>'
			print(html_message)
			# sent_mail=send_mail(
			# 	subject,
			#  	message, 
			#  	from_email, 
			#  	recipient_list, 
			#  	fail_silently=False, 
			#  	html_message=html_message
			#  	)
			sent_mail = False
			return sent_mail

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
		profile, is_created = Profile.objects.get_or_create(user=instance)
		default_user_profile = Profile.objects.get_or_create(user__id=1)[0] #[0] because it returns a tuple  #user__username= or whatever field u want
		default_user_profile.followers.add(instance) #user__id=1 follows all new users
		profile.followers.add(default_user_profile.user) #user created will follow user__id=1
		profile.followers.add(2)	#user created will follow user with id 2
post_save.connect(post_save_user_receiver, sender=User)