from idcard_generator.id_card_utils import random_card_no, IdentityCard


def test():
    code = random_card_no()  # 17位身份证
    print(code)
    if IdentityCard.check(code):
        print("你的校验位为:%s" % IdentityCard.calculate(code))


if __name__ == '__main__':
    test()
