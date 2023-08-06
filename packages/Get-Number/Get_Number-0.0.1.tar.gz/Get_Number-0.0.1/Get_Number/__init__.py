import random


def Get_Nr_Num(range, amount):
    ### 获得不重复随机数 ###
    ### (List)range 数字的范围；(int) 数字的数量 ###

    if isinstance(range, list):
        return "错误：range(minNumber, maxNumber)"
    if range[0] > range[1]:
        return "错误：范围错误"
    if range[1] - range[0] < amount:
        return "错误：范围过小"

    List = []
    i = 0
    while i < amount:
        Num = random.randint(range[0], range[1])
        if Num not in List:
            List.append(Num)
            i += 1
        else:
            continue

    return List
def Get_Prime_Num(number, all=False):
    ###(int)number为你要获得第几个质数###
    ###(Boolean)all 如果为True着返回数量为number的质数###
    i = 0
    List = []
    while len(List) < number:
        if i != 1 and i != 0:
            Bool = False
            Range = range(1, i + 1)
            for n in Range:
                if i % n == 0  and n != 1 and n != i:#如果为整除，且除数不为1或数字本身
                    List.remove(i)
                    break
                elif(i not in List):
                    List.append(i)

        i += 1

    if all:
        return List
    else:
        return List[number - 1]