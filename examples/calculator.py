class SolutionA:
    def calculate(self, s: str) -> int:
        s = list(s)
        ops = []
        nums = []
        i = 0

        while i < len(s):
            if s[i] in "+-(":
                ops.append(s[i])
            else:
                if s[i].isnumeric():
                    end = i
                    while end < len(s) and s[end].isnumeric():
                        end += 1
                    num2 = int("".join(s[i:end]))
                    i = end - 1
                    nums.append(num2)
                elif s[i] == ')':
                    ops.pop()

                if len(nums) > 1 and len(ops) > 0 and ops[-1] != '(':
                    op = ops.pop()
                    num2 = nums.pop()
                    num1 = nums.pop()
                    num = num1 + num2 if op == '+' else num1 - num2
                    nums.append(num)

            i += 1

        return nums[0]

class SolutionB:
    def calculate(self, s: str) -> int:
        number = 0
        sign_value = 1
        result = 0
        operations_stack = []

        for c in s:
            if c.isdigit():
                number = number * 10 + int(c)
            elif c in "+-":
                result += number * sign_value
                sign_value = -1 if c == '-' else 1
                number = 0
            elif c == '(':
                operations_stack.append(result)
                operations_stack.append(sign_value)
                result = 0
                sign_value = 1
            elif c == ')':
                result += sign_value * number
                result *= operations_stack.pop()
                result += operations_stack.pop()
                number = 0

        return result + number * sign_value


s = SolutionB()
res = s.calculate("1+( 9-(3 + 1 ))")
print(res)