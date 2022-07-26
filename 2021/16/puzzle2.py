import math

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
    tmp_packets = []
    while i < len(message):
        jump, packet = get_packet(message[i:])
        tmp_packets.append(packet)
        i += jump
        if main:
            while i < len(message):
                if i % 4 != 0:
                    if message[i] == '0':
                        i += 1
                elif message[i:i + 4] == '0000':
                    i += 4
                else:
                    break
    return i, tmp_packets


def get_packet(message):
    version = bin_to_int(message[0:3])
    type_id = bin_to_int(message[3:6])
    i = 6
    if type_id == 4:
        jump, literal = get_literal(message[6:])
        packet = (version, type_id, literal)
        i += jump
    else:
        length_type_id = message[i]
        if length_type_id == '0':
            p_length = bin_to_int(message[i + 1:i + 16])
            i += 16
            jump, tmp_packets = get_packets(message[i:i + p_length])
            i += jump
        else:
            p_number = bin_to_int(message[i + 1:i + 12])
            i += 12
            tmp_packets = []
            for j in range(p_number):
                jump, tmp_p = get_packet(message[i:])
                tmp_packets.append(tmp_p)
                i += jump
        packet = (version, type_id, tmp_packets)
    return i, packet


def get_literal(message):
    literal = ''
    i = 0
    while message[i] == '1':
        literal = literal + message[i + 1:i + 5]
        i += 5
    literal = literal + message[i + 1:i + 5]
    i += 5
    return i, bin_to_int(literal)


# Main loop
message_coded = hex_to_bin(message_coded)
packets = get_packets(message_coded, main=True)[1]

# Result for part 1

def sum_versions(packets):
    sum_v = 0
    for packet in packets:
        sum_v += packet[0]
        if type(packet[2]) != int:
            sum_v += sum_versions(packet[2])
    return sum_v

result = sum_versions(packets)

print(f"Result for part 1 is {result}")


# Result for part 2
def calc_value(packets):
    values = []
    for packet in packets:
        if packet[1] == 4:
            value = packet[2]
        elif packet[1] == 0:
            value = sum(calc_value(packet[2]))
        elif packet[1] == 1:
            value = math.prod(calc_value(packet[2]))
        elif packet[1] == 2:
            value = min(calc_value(packet[2]))
        elif packet[1] == 3:
            value = max(calc_value(packet[2]))
        elif packet[1] == 5:
            compare = calc_value(packet[2])
            value = 1 if compare[0] > compare[1] else 0
        elif packet[1] == 6:
            compare = calc_value(packet[2])
            value = 1 if compare[0] < compare[1] else 0
        elif packet[1] == 7:
            compare = calc_value(packet[2])
            value = 1 if compare[0] == compare[1] else 0
        values.append(value)
    return values

result = calc_value(packets)[0]

print(f"Result for part 2 is {result}")
