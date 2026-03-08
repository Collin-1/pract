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

