from django.db import models
# from django.forms import ModelForm


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="images/")
    thumbnail = models.ImageField(upload_to="images/", default ='https://placehold.co/300x225')
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        thumb_width = 300
        thumb_height = 225
        super().save(*args, **kwargs)
        try: # maybe there's no image or it can't? 
            img_thumbnail = Image.open(self.picture).copy()
            img_thumbnail.thumbnail((thumb_width,thumb_height))
        except:
            pass

        # resize logic
        self.thumbnail = img_thumbnail

        self.save(update_fields=['thumbnail'])

