import transStrBits
def trans_file_to_bits(file_name): 
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        
    return transStrBits.trans_str_to_bits(content)

def trans_bits_to_file(file_bits, new_file_name): 
    file_str = transStrBits.trans_bits_to_str(file_bits)
    with open(new_file_name, 'w', encoding='utf-8') as file:
        file.write(file_str)

def are_files_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()
 
if __name__ == "__main__":
    # test for trans only
    filebits = trans_file_to_bits('test.txt')
    print(filebits)
    trans_bits_to_file(filebits, 'test2.txt')
    assert(are_files_equal('test.txt', 'test2.txt'))

    