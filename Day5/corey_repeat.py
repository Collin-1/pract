# 1️⃣ Inheritance

# A class inherits properties from another class.

# This is called an "is-a relationship".

# Example:

class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def bark(self):
        print("Woof")

# Usage:

dog = Dog()

dog.speak()  # inherited
dog.bark()   # own method

# Output:

# Animal sound
# Woof


# 2️⃣ Polymorphism

# Different classes can use the same method name but behave differently.

# Example:

class Dog:
    def speak(self):
        print("Woof")

class Cat:
    def speak(self):
        print("Meow")

# Usage:

animals = [Dog(), Cat()]

for a in animals:
    a.speak()

# Output

# Woof
# Meow

# Interview explanation:

# Polymorphism allows different objects to respond to the same method in different ways.

# 3️⃣ Encapsulation

# Protecting internal data.

# Use private variables.

# Example:

class BankAccount:

    def __init__(self, balance):
        self.__balance = balance

# The __ makes it private.

# Access through methods:

def deposit(self, amount):
    self.__balance += amount


# 4️⃣ Abstraction

# Hiding complex logic and showing only what is necessary.

# Example:

# User only calls:

# cart.checkout()

# They do not see the internal calculation.

# 5️⃣ Class Variables vs Instance Variables
# Instance variables

# Unique per object.

# self.name
# self.price
# Class variables

# Shared across all objects.

# Example:

class Product:
    tax_rate = 0.15

# Every product shares this value.

# 6️⃣ Static Methods

# Methods that do not need the object.

# Example:

class MathUtils:

    @staticmethod
    def add(a, b):
        return a + b

# Usage:

MathUtils.add(3, 4)

# 7️⃣ Class Methods

# Operate on the class itself.

# Example:

class Product:
    count = 0

    def __init__(self):
        Product.count += 1

    @classmethod
    def total_products(cls):
        return cls.count
# 8️⃣ Method Overriding

# When a child class replaces a parent method.

# Example:

class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):

    def speak(self):
        print("Woof")

# Dog overrides speak.

# The 4 Core OOP Principles (Memorise for Interviews)

# 1️⃣ Encapsulation
# Hide internal data.

# 2️⃣ Inheritance
# Child classes reuse parent code.

# 3️⃣ Polymorphism
# Same method behaves differently.

# 4️⃣ Abstraction
# Hide complexity.

# What Junior Developer Interviews Usually Expect

# They expect you to know:

# ✅ Classes
# ✅ Constructors
# ✅ Inheritance
# ✅ Encapsulation
# ✅ Polymorphism
# ✅ Method overriding
# ✅ Composition
# ✅ __str__