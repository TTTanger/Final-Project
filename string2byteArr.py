def string_to_binary_array(input_string):
    """
    将字符串转换为二进制数组
    
    Args:
        input_string (str): 输入字符串
        
    Returns:
        list: 二进制数组，每个元素是一个字符的二进制表示
    """
    binary_array = []
    
    # 遍历字符串中的每个字符
    for char in input_string:
        # 将字符转换为ASCII值，然后转换为8位二进制，去掉'0b'前缀
        binary = format(ord(char), '08b')
        binary_array.append(binary)
    
    return binary_array

# 测试代码
if __name__ == "__main__":
    test_string = "Hello"
    result = string_to_binary_array(test_string)
    
    # 打印结果
    print(f"Original string: {test_string}")
    print("Binary array:")
    for i, binary in enumerate(result):
        print(f"Character '{test_string[i]}': {binary}")

    