from django.db import models
from djangoldp.models import Model
from django.conf import settings
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

class Language (Model):
    code = models.CharField(max_length=2, verbose_name="ISO Code")
    name = models.CharField(max_length=64, verbose_name="Language name")

    def __str__(self):
        return self.name

class Organisation (Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    website = models.CharField(max_length=4096, verbose_name="Website")

    def __str__(self):
        return self.name

class Entrepreneur(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="entrepreneur_profile")
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

class Mentor(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="mentor_profile")
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name='Phone number')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    country = CountryField(blank=True)
    language = models.ForeignKey(Language, blank=True)
    profile = models.ImageField(upload_to="mentors", blank=True, verbose_name="Profile picture")

    headline = models.CharField(max_length=256, blank=True, verbose_name='Headline or current position')
    city = models.CharField(max_length=256, blank=True, verbose_name='City')

    biography = models.TextField(blank=True, verbose_name="Tell us more about your activities")
    skills = models.TextField(blank=True, verbose_name="What skills can you share with our entrepreneurs ?")

    linkedin = models.CharField(max_length=256, blank=True, verbose_name='Linkedin account')
    twitter = models.CharField(max_length=256, blank=True, verbose_name='Twitter account')

    class Meta:
        permission_classes=[]
        serializer_fields=["@id", "phone", "headline", "biography", "skills"]
        nested_fields=["user", "organisation"]
        container_path = 'mentors/'
        rdf_type = 'coopstarter:mentor'
        depth = 0

    def __str__(self):
        return self.user.get_full_name()

class Step (Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    order = models.IntegerField(verbose_name="Order", blank=True, null=True, default=0)

    def __str__(self):
        return self.name

class Format (Model):
    name = models.CharField(max_length=128, verbose_name="Title")

    def __str__(self):
        return self.name

class Field (Model):
    name = models.CharField(max_length=128, verbose_name="Title")

    def __str__(self):
        return self.name

class Type (Model):
    name = models.CharField(max_length=128, verbose_name="Title")

    def __str__(self):
        return self.name


class Resource (Model):
    # Mandatory Fields
    name = models.CharField(max_length=32, verbose_name="Title")

    format = models.ManyToManyField(Format, blank=True)
    publication_year = models.IntegerField(verbose_name="Publication Year")
    language = models.ForeignKey(Language, blank=True, verbose_name="Language")
    field = models.ManyToManyField(Field, blank=True)
    country = CountryField(verbose_name="Country of publication", blank=True)
    uri = models.CharField(max_length=4086, verbose_name="Location/weblink")
    author = models.CharField(max_length=32, verbose_name="Author")
    skills = models.TextField(verbose_name="Learning outcomes/skills")

    # Complementary fields
    #toto =  models.DateTimeField(verbose_name="Date et heure de fin")
    #booleanTest = models.BooleanField(default=False, verbose_name="Porteur de cellule")
    description = models.TextField(verbose_name="Description")
    iframe_link = models.TextField(verbose_name="Iframe link", blank=True)
    image = models.ImageField(upload_to="resources", blank=True, verbose_name="Photo")

    #Classification Fields
    target = models.CharField(max_length=32, choices=(('mentor', 'Mentor'), ('entrepreneur', 'Entrepreneur'), ('public', 'public')), verbose_name="Target audience", blank=True)
    type = models.ForeignKey(Type, blank=True, verbose_name="Type of content")
    
    steps = models.ManyToManyField(Step, blank=True)
    sharing = models.CharField(max_length=32, choices=(('private', 'Private (nobody)'), ('public', 'Public (everybody)')), verbose_name="Sharing profile", blank=True, null=True)

    related = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.name

class Request (Model):
    # Mandatory Fields
    name = models.CharField(max_length=32, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    
    language = models.ForeignKey(Language, blank=True, verbose_name="Language")
    field = models.ManyToManyField(Field, blank=True)
    country = CountryField(verbose_name="Country of publication", blank=True)
    
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    skills = models.TextField(verbose_name="Learning outcomes/skills")

    def __str__(self):
        return self.name

class Review (Model):
    resource = models.ForeignKey(Resource,  verbose_name="Associated resource", blank=True)
    comment =  models.TextField(verbose_name="Comment")

    status = models.CharField(max_length=32, choices=(('inappropriate', 'Inappropriate'), ('validated', 'Validated'), ('to_improve', 'Improvement required')), verbose_name="Resource status", blank=True, null=True)

    def __str__(self):
        return self.comment


# user_model = get_user_model()
# djangoldp_modules = list(filter(lambda app: app.startswith('djangoldp_'), settings.INSTALLED_APPS))
# user_fields = ['@id', 'first_name', 'groups', 'last_name', 'username', 'email']
# user_nested_fields = ['mentor_profile', 'entrepreneur_profile']
# for dldp_module in djangoldp_modules:
#     try:
#         user_fields += import_module(dldp_module + '.settings').USER_NESTED_FIELDS
#         user_nested_fields += import_module(dldp_module + '.settings').USER_NESTED_FIELDS
#     except:
#         pass

# s_fields = []
# s_fields.extend(user_fields)
# s_fields.extend(user_nested_fields)
# user_model._meta.serializer_fields = s_fields