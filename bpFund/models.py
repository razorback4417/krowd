from django.db import models

# Create your models here.
class Cause(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    orgSchool = models.CharField(max_length=50)
    problem = models.CharField(max_length=500, null=True)
    sol = models.CharField(max_length=500, null=True)
    location = models.CharField(max_length=50)
    date = models.DateField(max_length=50)
    targetAmount = models.IntegerField()
    contribNum = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}: name: {self.name} email: {self.email} organization/school: {self.orgSchool} problem: {self.problem} solution: {self.sol} location: {self.location} date: {self.date} targetAmount: {self.targetAmount} contributionNum: {self.contributionNum}"

class User(models.Model):
    totalContributions = models.IntegerField(default=0)

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    slug = models.SlugField()
    def __str__(self):
        return f"{self.id}: name: {self.name} price: {self.price} description: {self.description} slug: {self.slug}"

class Order(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    postal_code = models.IntegerField()
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} name: {self.name} email: {self.email} postal_code: {self.postal_code} address: {self.address} date: {self.date} paid: {self.paid}"

class CartItem(models.Model):
    cart_id = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def __str__(self):
        return f"{self.id}: cart_id: {self.cart_id} price: {self.price} quantity: {self.quantity} date_added: {self.date_added} product: {self.product}"

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def total_cost(self):
        return self.quantity * self.price

