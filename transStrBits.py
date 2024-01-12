def trans_str_to_bits(input_str : str) -> str:  
    binary_list = [bin(ord(char))[2:].zfill(8) for char in input_str] 
    binary_str = ''.join(binary_list)
    
    return binary_str
def trans_bits_to_str(input_bits : str) -> str: 
    binary_list = [input_bits[i:i+8] for i in range(0, len(input_bits), 8)] 
    char_list = [chr(int(binary, 2)) for binary in binary_list] 
    char_str = ''.join(char_list)
    
    return char_str

if __name__ == "__main__":
    test = trans_str_to_bits("--12 ads")
    print(test,len(test))
    ans = trans_bits_to_str(test)
    print(ans)
