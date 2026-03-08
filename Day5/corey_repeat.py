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


