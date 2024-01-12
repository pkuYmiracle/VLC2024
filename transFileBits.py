def trans_file_to_bits(file_name): 
    file = open(file_name, 'rb') 
    file_data = file.read() 
    file.close() 
    file_bits = bin(int.from_bytes(file_data, byteorder='big'))
 
    return file_bits
def trans_bits_to_file(file_bits, new_file_name): 
    file_data = int(file_bits, 2)
 
    file_bytes = file_data.to_bytes((file_data.bit_length() + 7) // 8, byteorder='big')
 
    with open(new_file_name, 'wb') as file:
        file.write(file_bytes)

def are_files_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()
 
if __name__ == "__main__":
    # test for trans only
    filebits = trans_file_to_bits('test.txt')
    print(filebits)
    trans_bits_to_file(filebits, 'test2.txt')
    assert(are_files_equal('test.txt', 'test2.txt'))

    