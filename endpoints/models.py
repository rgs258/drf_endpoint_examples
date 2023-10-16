from django.db import models


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        """

        :return: The name of the customer
        """
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=100)

    def __str__(self):
        """

        :return: The name of the product
        """
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        """

        :return: The name of the customer and the product they ordered
        """

        return self.customer.name + " " + self.product.name


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

    def __str__(self):
        """

        :return: The name of the customer and their address
        """

        return self.customer.name + " " + self.address


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=100)

    def __str__(self):
        """
        :return: The name of the customer and the product they reviewed
        """

        return self.customer.name + " " + self.product.name
