from django.db import models

class pointtb(models.Model):
    team = models.CharField(max_length=5, null=False, primary_key=True)
    matches = models.IntegerField(null=False)
    win = models.IntegerField(null=False)
    loss = models.IntegerField(null=False)
    tie = models.IntegerField(default=0)
    point = models.IntegerField(null=False)
    runscored = models.IntegerField(null=True,default=0)
    runconceded = models.IntegerField(null=True,default=0)
    oversfaced = models.FloatField(null=True,default=0)
    oversbowled = models.FloatField(null=True,default=0)   
    nrr = models.FloatField(null=False)

    def save(self,*args,**kwargs):
        try:
            if self.oversfaced>0 and self.oversbowled>0:
                self.nrr = (self.runscored/self.oversfaced) - (self.runconceded/self.oversbowled)
            else:
                self.nrr = 0
        except ZeroDivisionError:
            self.nrr = 0
        super().save(*args,**kwargs)
    
    class Meta:
        db_table = "pointtb"
        ordering = ["-point","-nrr"]        

class matches(models.Model):
    no = models.AutoField(primary_key=True)
    home = models.CharField(max_length=5, null=False)
    away = models.CharField(max_length=5, null=False)
    winner = models.CharField(max_length=5, null=True)
    looser = models.CharField(max_length=5, null=True)
    tie = models.CharField(max_length=5, default='No')

    class Meta:
        db_table = "matches"

class playoff(models.Model):
    no = models.IntegerField(primary_key=True,null=False)
    team1 = models.CharField(max_length=5, null=False)
    team2 = models.CharField(max_length=5, null=False)
    winner = models.CharField(max_length=5, null=True)
    looser = models.CharField(max_length=5, null=True)

    class Meta:
        db_table = "playoff"