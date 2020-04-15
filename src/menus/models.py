from django.db import models
from django.conf import settings
from restaurants.models import RestaurantLocation
from django.urls import reverse

class Item(models.Model):
	#associations
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	restaurant  	= models.ForeignKey(RestaurantLocation, on_delete=models.CASCADE)
	#item stuff
	name 			= models.CharField(max_length=120)
	contents		= models.TextField(help_text='seperate each item by comma')
	excludes		= models.TextField(blank=True, null=True, help_text='seperate each item by comma')
	public			= models.BooleanField(default=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	updated			= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		#return f"/restaurants/{self.slug}" # both the returns do the same
		return reverse('menus:detail', kwargs={'pk':self.pk})

	class Meta:
		ordering = ['-updated', '-timestamp'] # Most recently updated or timestamped first when we do Item.objects.all()

	def get_contents(self):
		return self.contents.split(",")

	def get_excludes(self):
		return self.excludes.split(",")
