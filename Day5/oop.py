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

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity):
        item = CartItem(product, quantity)
        self.items.append(item)

    def total_cost(self):
        total = 0
        for item in self.items:
            total =+ item.total_price()
        return total
    
    def show_cart(self):
        for item in self.items:
            print(f"{item.product.name} x{item.quantity}")

cart = ShoppingCart()

laptop = Product("Laptop", 15000)
mouse = Product("Mouse", 300)

cart.add_product(laptop, 1)
cart.add_product(mouse, 2)

cart.show_cart()
