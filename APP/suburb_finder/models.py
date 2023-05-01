from django.db import models

# Create your models here.

class Suburb(models.Model):
    suburb_name = models.CharField(max_length=60)
    post_code = models.CharField(max_length=4)
    num_cust = models.IntegerField()
    
    def set_num_cust():
        ## querry db for number of customers in suburb
        return 5 # test value
    
    def get_distance(origin):
        # google maps api call get route dist and time
        #
        # return dist, time
        pass

    def __str__(self):
        return self.suburb_name