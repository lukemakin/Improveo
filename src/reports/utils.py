import random


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z'] 

numbers = [0,1,2,3,4,5,6,7,9]


def create_problem_id():
    letts = [x.upper() for x in letters[:6]]
    nums = [str(x) for x in numbers[:6]]
    code = letts+nums
    random.shuffle(code)
    code = ''.join(x for x in code)
    return code
    