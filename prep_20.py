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