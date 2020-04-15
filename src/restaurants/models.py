from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.db.models import Q
from .validators import validate_category
from .utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.query.QuerySet):
	def search(self, query): 
		if query:	
			query=query.strip()  #RestaurantLocation.objects.all().search(query) ##RestaurantLocation.objects.filter(something).search(query)
			return self.filter(
			Q(name__icontains=query)|
			Q(location__icontains=query)|
			Q(category__icontains=query)|
			Q(item__name__icontains=query)|
			Q(item__contents__icontains=query)	
			).distinct() #.distinct() is used to show only one search o/p...otherwise u get the same thing multiple times due to those various queries...
		return self

class RestaurantLocationManager(models.Manager):
	def get_queryset(self):
		return RestaurantLocationQuerySet(self.model, using=self._db)

	def search(self, query):   #RestaurantLocation.objects.search()
		return self.get_query_set().search(query)

class RestaurantLocation(models.Model):
	owner 			= models.ForeignKey(User, on_delete=models.CASCADE) #Django Models Unleashed JOINCFE.com
	name 			= models.CharField(max_length=120)
	location		= models.CharField(max_length=120, null=True, blank=True)
	category 		= models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])		
	timestamp		= models.DateTimeField(auto_now_add=True)
	updated			= models.DateTimeField(auto_now=True)
	slug			= models.SlugField(null=True, blank=True)
	#my_date_field	= models.DateTimeField(auto_now=False, auto_now_add=False)
	#creates and displays RestaurantLocation objects in admin


	objects = RestaurantLocationManager() #add Model.objects.all()

	#to display it as its name in admin page
	def __str__(self):
	 	return self.name

	def get_absolute_url(self):
		#return f"/restaurants/{self.slug}" # both the returns do the same
		return reverse('restaurants:detail', kwargs={'slug':self.slug})

	#linking the name to title....since we dont have a title parameter as above
	@property
	def title(self):
		return self.name

def rl_pre_save_reciever(sender, instance, *args, **kwargs):
	instance.category = instance.category.capitalize()
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

# def rl_post_save_reciever(sender, instance, *args, **kwargs):
# 	print("saved")
# 	print(instance.timestamp)
	# if not instance.slug:
	# 	instance.slug = unique_slug_generator(instance)
	# 	instance.save()

pre_save.connect(rl_pre_save_reciever, sender = RestaurantLocation)



# post_save.connect(rl_post_save_reciever, sender = RestaurantLocation)
