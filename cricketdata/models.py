from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class MatchRestApiData(models.Model):
    match_id = models.IntegerField(primary_key=True)
    status= models.CharField(max_length=100,null=True)
    details = models.CharField(max_length=200,null=True)
    team_1_flag = models.URLField()
    team_2_flag = models.URLField()
    match_link = models.CharField(max_length=300,null=True)
    slug = models.SlugField(allow_unicode=True,default=True)
    team_1_title = models.CharField(max_length=50,null=True)
    team_1_run = models.CharField(max_length=100,null=True)
    team_2_title = models.CharField(max_length=50,null=True)
    team_2_run = models.CharField(max_length=100,null=True)
    result = models.CharField(max_length=200,null=True)
    schedule = models.CharField(max_length=50,null=True)

    def __str__(self):
        return f"Match Id: {self.match_id},{self.team_1_title} vs {self.team_2_title}"

    def save(self,*args,**kwargs):
        self.slug = slugify(f"{self.team_1_title} vs {self.team_2_title}")
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('cricketdata:single',kwargs={'slug':self.slug})