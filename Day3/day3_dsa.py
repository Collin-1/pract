from __future__ import annotations
from collections import Counter, deque
from typing import Dict, List, Tuple, Optional


# ============================================================
# Problem 1: Count product frequency in a cart (Hash Map)
# ============================================================
def count_cart_items(cart_product_ids: List[int]) -> Dict[int, int]:
    """
    Given a list of product IDs in a cart, return a map of product_id -> count.

    Example:
    [1,1,2,3,3,3] -> {1:2, 2:1, 3:3}

    Time: O(n)
    Space: O(k) where k = unique products
    """
    counts: Dict[int, int] = {}
    for pid in cart_product_ids:
        counts[pid] = counts.get(pid, 0) + 1
    return counts


# ============================================================
# Problem 2: First non-repeating character (Hash Map)
# ============================================================
def first_unique_char(s: str) -> int:
    """
    Return index of first non-repeating character, or -1.

    Example: "leetcode" -> 0
             "loveleetcode" -> 2 ('v')

    Time: O(n)
    Space: O(1) effectively (limited charset) / O(k) general
    """
    freq = Counter(s)
    for i, ch in enumerate(s):
        if freq[ch] == 1:
            return i
    return -1


# ============================================================
# Problem 3: Two Sum (Hash Map)
# ============================================================
def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Return indices of two numbers that add up to target, or None.

    Time: O(n)
    Space: O(n)
    """
    seen: Dict[int, int] = {}  # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return (seen[need], i)
        seen[x] = i
    return None


# ============================================================
# Problem 4: Remove duplicates from a sorted array (Two pointers)
# ============================================================
def remove_duplicates_sorted(nums: List[int]) -> int:
    """
    Given a sorted list, remove duplicates in-place.
    Return the length of the unique prefix.

    Example:
    [1,1,2,2,3] becomes [1,2,3,?,?] and returns 3

    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0

    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write


# ============================================================
# Problem 5: Valid parentheses (Stack)
# ============================================================
def is_valid_parentheses(s: str) -> bool:
    """
    Return True if parentheses are valid.

    Time: O(n)
    Space: O(n)
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: List[str] = []

    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0


# ============================================================
# Problem 6: Sliding window - Longest substring without repeating chars
# ============================================================
def longest_unique_substring(s: str) -> int:
    """
    Return length of the longest substring without repeating chars.

    Example: "abcabcbb" -> 3 ("abc")

    Time: O(n)
    Space: O(k)
    """
    last_seen: Dict[str, int] = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)

    return best


# ============================================================
# Problem 7: Inventory check (Ecommerce-style)
# ============================================================
def can_fulfill_order(stock: Dict[int, int], order: Dict[int, int]) -> bool:
    """
    stock: product_id -> available quantity
    order: product_id -> requested quantity

    Return True if order can be fulfilled.

    Time: O(m) where m = number of unique products in order
    Space: O(1)
    """
    for pid, qty in order.items():
        if stock.get(pid, 0) < qty:
            return False
    return True


# ============================================================
# Problem 8: BFS shortest path in a grid (very light graph)
# ============================================================
def shortest_path_grid(grid: List[List[int]]) -> int:
    """
    0 = free cell, 1 = blocked cell
    Find shortest path from top-left (0,0) to bottom-right (r-1,c-1)
    using BFS. Return steps count, or -1 if not possible.

    Time: O(R*C)
    Space: O(R*C)
    """
    if not grid or not grid[0]:
        return -1

    R, C = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[R - 1][C - 1] == 1:
        return -1

    q = deque([(0, 0, 0)])  # (row, col, steps)
    seen = set([(0, 0)])

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        r, c, steps = q.popleft()
        if r == R - 1 and c == C - 1:
            return steps

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc, steps + 1))

    return -1


# ============================================================
# Quick Tests (run this file directly)
# ============================================================
if __name__ == "__main__":
    print("Running Day 3 tests...")

    assert count_cart_items([1, 1, 2, 3, 3, 3]) == {1: 2, 2: 1, 3: 3}
    assert first_unique_char("leetcode") == 0
    assert first_unique_char("aabb") == -1
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 2, 4], 6) == (1, 2)

    nums = [1, 1, 2, 2, 3]
    k = remove_duplicates_sorted(nums)
    assert k == 3
    assert nums[:k] == [1, 2, 3]

    assert is_valid_parentheses("()[]{}") is True
    assert is_valid_parentheses("(]") is False
    assert longest_unique_substring("abcabcbb") == 3
    assert longest_unique_substring("bbbbb") == 1

    stock = {1: 5, 2: 0, 3: 10}
    order_ok = {1: 2, 3: 5}
    order_bad = {2: 1}
    assert can_fulfill_order(stock, order_ok) is True
    assert can_fulfill_order(stock, order_bad) is False

    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]
    assert shortest_path_grid(grid) == 4

    print("✅ All Day 3 tests passed!")