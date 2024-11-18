import sys

def generate_crc16_table(polynomial=0x1021):
    table = []

    for byte in range(256):
        crc = byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF
        table.append(crc)

    return table

def calculate_crc16(data, table, initial_crc=0xFFFF, invert_result=False):
    crc = initial_crc
    for byte in data:
        crc = table[(crc >> 8) ^ byte] ^ ((crc & 0xFF) << 8)
        crc &= 0xFFFF
    return ~crc & 0xFFFF if invert_result else crc

def calculate_crc16_for_file(file_path, table, initial_crc=0xFFFF, invert_result=False):
    crc = initial_crc
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024):
                for byte in chunk:
                    crc = table[(crc >> 8) ^ byte] ^ ((crc & 0xFF) << 8)
                    crc &= 0xFFFF
        return ~crc & 0xFFFF if invert_result else crc
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

if __name__ == "__main__":
    polynomial = 0x1021
    initial_crc = 0xFFFF
    invert_result = False

    crc16_table = generate_crc16_table(polynomial)

    for i, value in enumerate(crc16_table):
        print(f"Byte {i:02X}: CRC = {value:04X}")

    test_data = b"123456789"
    crc_result = calculate_crc16(test_data, crc16_table, initial_crc, invert_result)
    print(f"CRC-16 for '{test_data.decode()}': {crc_result:04X}")

    file_path = "test_file.txt"
    crc_file_result = calculate_crc16_for_file(file_path, crc16_table, initial_crc, invert_result)
    if crc_file_result is not None:
        print(f"CRC-16 for file '{file_path}': {crc_file_result:04X}")
