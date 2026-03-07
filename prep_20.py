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

# 8. Sum of List
def add(numbers:list)->int:
    total = 0
    for number in numbers:
        total += number
    return total

# 9. Count Characters
def count_characters(word:str)->dict:
    word_count = {}
    for letter in word:
        word_count[letter] = word_count.get(letter, 0) + 1
    return word_count

# 10. Two Sum
def two_sum(numbers:list, target:int)-> tuple:
    pos = []
    for i in range(len(numbers)):
        if (target - numbers[i]) in numbers:
            pos.append(i)
    return pos

# 11. Find Second Largest Number
def second_largest(numbers:list)->int:
    largest = numbers[0]
    s_largest = numbers[0]
    for number in numbers:
        if number >largest:
            s_largest = largest
            largest = number
    return s_largest

# 12. Merge Two Lists
def merge(list1:list, list2:list)->list:
    list1.extend(list2)
    return list1


# 13. Remove Even Numbers
def remove_even(numbers:list)->list:
    return[number for number in numbers if number%2 != 0]

# 14. Find Missing Number
def missing_number(numbers):
    for number in range(len(numbers)):
        if numbers[number] != number+1:
            return number+1
        
# 15. Sort Words Alphabetically
def sort_words(words:list):
    return sorted(words)

# 16. Longest Word
def longest(words:str):
    words_list = words.split()
    longest_word = words_list[0]
    for word in words_list:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word


