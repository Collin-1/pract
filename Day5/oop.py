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

class User:
    def __init__(self, username):
        self.username = username
        self.cart = ShoppingCart()

    def add_to_cart(self, product, quantity):
        self.cart.add_product(product, quantity)
    
    def checkout(self):
        total = self.cart.total_cost()
        print(f"{self.username} checked out. Total: R{total}")

user = User("Collin")

laptop = Product("Laptop", 15000)
keyboard = Product("Keyboard", 800)

user.add_to_cart(laptop, 1)
user.add_to_cart(keyboard, 1)

user.cart.show_cart()

user.checkout()