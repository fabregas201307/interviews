"""
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

"""

class Solution:
    def twoSum(self, target: int, nums: list[int]) -> list[list[int]]:
        nums = sorted(nums)
        result = list()
        i, j = 0, len(nums)-1
        while i < j:
            cur_sum = nums[i] + nums[j]
            if cur_sum > target:
                j -= 1
            elif cur_sum < target:
                i += 1
            else:
                result.append([nums[i], nums[j]])
                j -= 1
        return result

        
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums = sorted(nums)
        result = set()
        ans = list()
        for i in range(len(nums)):
            target = (-1) * nums[i]
            cur_result = self.twoSum(target=target, nums=nums[i+1:])
            if len(cur_result) < 1:
                continue
            for cur_list in cur_result:
                print(cur_list)
                a, b, c = nums[i], cur_list[0], cur_list[1]
                result.add((a, b, c))
        
        for t in result:
            ans.append([t[0], t[1], t[2]])

        return ans

    

if __name__ == "__main__":
    solution = Solution()
    test_1 = [-1,0,1,2,-1,-4]
    test_2 = [0,1,1]
    test_3 = [0,0,0]
    ans = solution.threeSum(nums=test_3)
    print(ans)
 