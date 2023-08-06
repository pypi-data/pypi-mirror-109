"""这是  simple_tools 模块, 用于联系python 使用."""
def print_lol(the_list, level):
    """这里有一个位置参数，名为 the_list, 这可以是任何Python列表（包含或者不包含嵌套函数）
    所提供列表中的各个数据项会（递归的）打印到屏幕上，并且各占一行.
    level 用来在遇到 嵌套列表的时候插入制表符。"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level)
        else:
            for tab_step in range(level):
                print('\t', end='') 
            print(each_item)