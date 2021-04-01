# coding: utf-8

import random


def main():
    dinner = random.choices(['嘉旺',
                             '港岛记',
                             '食其家',
                             'KFC',
                             'McDonald',
                             '树熊',
                             '便利店',
                             '饭范',
                             '2楼选餐',
                             '1楼远选餐',
                             '1楼近选餐',
                             '膳予团餐',
                             '老上海',
                             '清补凉',
                             ], )
    print(f'Tonight, we get {dinner[0]}!')


if __name__ == "__main__":
    main()
