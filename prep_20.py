# Question 1
# Reverse a string.
def reverse_string(s):
    return s[::-1]

# Question 2
# Find duplicates in a list.
def find_duplicates(nums):
    seen = set()
    duplicates = set()

    for n in nums:
        if n in seen:
            duplicates.add(n)
        else:
            seen.add(n)

    return list(duplicates)

# Question 3
# Count vowels in a string.

def count_vowels(s):
    vowels = "aeiou"
    count = 0

    for c in s.lower():
        if c in vowels:
            count += 1

    return count

# Question 4
# Find Maximum Number.

def find_max(numbers:list)->int:
    largest = numbers[0]
    for number in numbers:
        if number >largest:
            largest = number

    return largest


# 4 Remove Duplicates From List

def remove_duplicate(numbers:list)->list:
    seen = set()
    no_duplicates = []
    for number in numbers:
        if number not in seen:
            seen.add(number)
            no_duplicates.append(number)
    return no_duplicates

# 5. FizzBuzz
def fizz_buzz(number:int)->str:
    for number in range(1, number+1):
        if (number%3 == 0) and (number%5==0):
            print("FizzBuzz")
        elif number%3 == 0:
            print("Fizz")
        elif number%5 == 0:
            print("Buzz")
        else:
            print(number)

# 6. Find Duplicates
def find_duplicate(numbers:list)->list:
    seen = set()
    duplicates = []
    for number in numbers:
        if number in seen:
            duplicates.append(number)
        else:
            seen.add(number)
    return duplicates

# 7. Check Palindrome
def check_palindrome(word:str)->bool:
    return word == word[::-1] if word else False

