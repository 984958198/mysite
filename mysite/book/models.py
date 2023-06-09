from django.db import models

class Douban(models.Model):
    id = models.BigIntegerField(primary_key=True)
    img = models.CharField(max_length=1024, help_text='图片地址')
    href = models.CharField(max_length=1024, help_text='书籍地址')
    title = models.CharField(max_length=128, help_text='标题')
    read = models.BooleanField(help_text='可试读')
    make = models.CharField(max_length=1024, help_text='制造说明')
    score = models.DecimalField(max_digits=2, decimal_places=1, help_text='评分')
    appraise = models.IntegerField(help_text='好评度')
    intro = models.CharField(max_length=1024, help_text='简介')
    update_time = models.DateTimeField(auto_created=True, auto_now_add=True, help_text='更新时间')
