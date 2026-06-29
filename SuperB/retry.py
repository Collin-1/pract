#q1
def anagrams(ls):
    ans = {}
    for i in ls:
        ow = "".join(sorted(i))
        if ow in ans:
            ans[ow].append(i)
        else:
            ans[ow] = [i]
    
    return [v for v in ans.values()]

print(anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))

#q2
def nonr(word):

    for i in word:
        if word.count(i) == 1:
            return i

print(nonr("superbalist"))

#q3
# i could not complete

#q4
# i could not complete


#q5
# i could not complete
