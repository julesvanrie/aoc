with open('input.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

message_coded = lines[0]
length = len(message_coded)

hex_dict = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }

def hex_to_bin(message):
    message = ''.join([hex_dict[h] for h in message])
    return message

def bin_to_int(message):
    message = '0b' + message
    return int(message, 2)

def get_packets(message, main=False):
    i = 0
    while i < len(message):
        jump = get_packet(message[i:])
        i += jump
        print(jump, i)
        if main:
            while i < len(message):
                if i % 4 != 0:
                    if message[i] == '0':
                        i += 1
                    print(i)
                elif message[i:i+4] == '0000':
                    i += 4
                    print(i)
                else:
                    break
    return i

def get_packet(message):
    print(message)
    version = bin_to_int(message[0:3])
    type_id = bin_to_int(message[3:6])
    i = 6
    if type_id == 4:
        jump, literal = get_literal(message[6:])
        packets.append((version, type_id, literal))
        i += jump
    else:
        length_type_id = message[i]
        packets.append((version, type_id, 'operater ' + length_type_id))
        if length_type_id == '0':
            p_length = bin_to_int(message[i + 1:i + 16])
            i += 16
            i += get_packets(message[i:i+p_length])
        else:
            p_number = bin_to_int(message[i + 1:i + 12])
            i += 12
            for j in range(p_number):
                i += get_packet(message[i:])
    return i

def get_literal(message):
    literal = ''
    i = 0
    while message[i] == '1':
        literal = literal + message[i+1:i+5]
        i += 5
    literal = literal + message[i+1:i+5]
    i += 5
    return i, bin_to_int(literal)

# Main loop
message_coded = hex_to_bin(message_coded)
print(message_coded)
packets = []
get_packets(message_coded, main=True)
print(len(packets))

# Result for part 1
count = 0
for packet in packets:
    count += packet[0]
    print(packet)

result = count

print(f"Result for part 1 is {result}")

# Result for part 2
