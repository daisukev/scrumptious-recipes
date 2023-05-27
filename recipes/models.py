from django.db import models
from PIL import Image
import os
from django.core.files import File
from io import BytesIO
# from django.forms import ModelForm




class Recipe(models.Model):
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="images/")
    thumbnail = models.ImageField(upload_to="images/", default ='https://placehold.co/300x225')
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def create_thumbnail(self):
        pass

    def save(self, *args, **kwargs):

        if not self.picture: # If there is no picture, there can't be a thumbnail, either
            self.thumbnail = None
        else:
            thumb_data = BytesIO() # create binary stream to store the thumbnail 
            thumb_img = Image.open(self.picture) #open a copy  of the picture

            # check dimensions of the picture
            print(thumb_img.width, thumb_img.height)
            if thumb_img.height >= thumb_img.width: # if it's a tall image, we want the thumbnail size  to adhere to the width, so the height is set arbitrarily large
                thumbnail_size = (400, 800)
            else:
                thumbnail_size = (400, 300)


            thumb_img.thumbnail(thumbnail_size) # shrink it


            # file formats 
            thumb_img.save(thumb_data, format=thumb_img.format)   # save the thumbnail same filetype as the original
            thumb_img.close() # close the image
            thumb_path = f"{self.picture}_thumbnail.{thumb_img.format.lower()}"
            thumb_file = File(thumb_data)
            file_path = os.path.join('media', thumb_path)
            with open(file_path, 'wb') as destination:
                for chunk in thumb_file.chunks():
                    destination.write(chunk)
            
            self.thumbnail.save(thumb_path, thumb_file, save=False)

        super(Recipe, self).save(*args, **kwargs, update_fields=['thumbnail'])
