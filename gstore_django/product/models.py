from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.contrib.auth.models import User

#nesrine
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    #nesrine
    def save(self, *args, **kwargs): # Auto Slug Field
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)
    @property
    def created_at_read(self):
        return self.created_at
    @property
    def modified_at_read(self):
        return self.modified_at

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    #nesrine
    def save(self, *args, **kwargs): # Auto Slug Field
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    @property
    def created_at_read(self):
        return self.created_at
    @property
    def modified_at_read(self):
        return self.modified_at

class Product(models.Model):
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    price_sale = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    #to check if product is in stock
    quantity = models.IntegerField(default=1, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/category-product/{self.category.slug}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    #nesrine
    def save(self, *args, **kwargs): # Auto Slug Field
        self.slug = slugify(self.name)
        if not self.id: #new product
            self.thumbnail = self.make_thumbnail(self.image)
        else: # if updating existing instance
            self.thumbnail = self.make_thumbnail(self.image)
        super(Product, self).save(*args, **kwargs)
    
    @property
    def category_name(self):
        return self.category.name
    @property
    def brand_name(self):
        return self.brand.name
    @property
    def created_at_read(self):
        return self.created_at
    @property
    def modified_at_read(self):
        return self.modified_at
    @property
    def slug_at_read(self):
        return self.slug
    

class Wish(models.Model):
    user = models.ForeignKey(User, related_name='wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
   

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.product.name
    
    def get_absolute_url(self):
        return f'/{self.product}/'
    
    @property
    def product_name(self):
        return self.product.name

#nesrine    
class Sale(models.Model):
    sale_value = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.sale_value)
    @property
    def created_at_read(self):
        return self.created_at
    @property
    def modified_at_read(self):
        return self.modified_at