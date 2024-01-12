import transStrBits
def trans_file_to_bits(file_name): 
    with open(file_name, 'rb') as file:
        content = file.read()
    binary_data = ''.join(format(byte, '08b') for byte in content)
    return binary_data

def trans_bits_to_file(file_bits, new_file_name): 
    
    file = transStrBits.binary_to_bytes(file_bits)
    with open(new_file_name, 'w') as f:
            f.write(file.decode('utf-8')) 

def are_files_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()
 
if __name__ == "__main__":
    # test for trans only
    filebits = trans_file_to_bits('test.txt')
    print(filebits)
    trans_bits_to_file(filebits, 'test2.txt')
    assert(are_files_equal('test.txt', 'test2.txt'))

    