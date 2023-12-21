"""
Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.

"""

class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        my_dict = dict()
        my_dict["2"] = ['a', 'b', 'c']
        my_dict["3"] = ['d', 'e', 'f']
        my_dict["4"] = ['g', 'h', 'i']
        my_dict["5"] = ['j', 'k', 'l']
        my_dict["6"] = ['m', 'n', 'o']
        my_dict["7"] = ['p', 'q', 'r', 's']
        my_dict["8"] = ['t', 'u', 'v']
        my_dict["9"] = ['w', 'x', 'y', 'z']

        result = my_dict.get(digits[0])

        for digit in digits[1:]:
            result = [old+new for old in result for new in my_dict.get(digit)]

        return result

    

if __name__ == "__main__":
    solution = Solution()
    test_1 = "23"
    test_2 = ""
    test_3 = "2"
    ans = solution.letterCombinations(digits=test_1)
    print(ans)
 