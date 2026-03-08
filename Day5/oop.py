class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def __str__(self):
        return f"{self.name} - R{self.price}"
    


class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
    
    def total_price(self):
        return self.product.price * self.quantity

# composition is a design principle where a class contains objects of other classes as its attributes
# to build complex functionality, modeling a "has-a" relationship.

