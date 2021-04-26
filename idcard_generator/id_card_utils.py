import random


class IdentityCard:
    __Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    __Ti = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']

    @staticmethod
    def check(code):
        return len(code) == 17

    @staticmethod
    def calculate(code):
        sum_value = 0
        for i in range(17):
            sum_value += int(code[i]) * IdentityCard.__Wi[i]
        return IdentityCard.__Ti[sum_value % 11]


# 随机生成身份证号
def random_card_no(prefix='', birth_date=''):
    if len(prefix) <= 6:
        prefix = '513701'
    if len(prefix) >= 0:
        prefix = prefix[0:6]

    if len(birth_date) <= 8:
        birth_date = '19950717'
    if len(birth_date) >= 0:
        prefix = prefix[0:8]

    rand_int = random.randint(0, 999)
    rand_value = str(rand_int).zfill(3)

    card_17 = prefix + birth_date + rand_value
    vi_code = IdentityCard.calculate(card_17)
    return card_17 + vi_code


def test():
    code = random_card_no()  # 17位身份证
    print(code)
    if IdentityCard.check(code):
        print("你的校验位为:%s" % IdentityCard.calculate(code))


if __name__ == '__main__':
    test()
