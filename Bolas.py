import random
def bolas(number,deck_num,n):
    # 用来测试卡组数量为deck_num时投入number张该类卡牌
    # 在选择n张牌时能选到的概率（波拉斯卜算师）
    count=0
    decks=range(deck_num)
    for i in range(100000):
        num=random.sample(decks,n)
        for j in range(len(num)):
            if num[j]<=number-1:
                count=count+1
                break
    print(count/1000,"%")

if __name__ == '__main__':
    flag=True
    while flag:
        print('以下输入均为整数')
        deck_number=int(input("请输入卡组数量："))
        need_number=int(input("请输入可检索的卡牌投入数量："))
        deep=int(input("请输入检索卡的检索深度："))
        bolas(need_number, deck_number, deep)
        f2=input("是否继续？(Y/N)")
        print(f2)
        if f2 == 'N':
            flag=False