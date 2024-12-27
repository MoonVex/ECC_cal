def hex_to_bin(hex_str, length):
    return bin(int(hex_str, 16))[2:].zfill(length)

def compute_ecc(prgdata, x_adr, y_adr, reden=0, ifren=1):
    # Convert inputs to binary strings
    prgdata_bin = f'{int(prgdata, 16):0128b}'
    x_adr_bin = f'{int(x_adr, 16):011b}'
    y_adr_bin = f'{int(y_adr, 16):06b}'

    # Concatenate address components
    prgadr_bin = f'{reden}{ifren}{x_adr_bin}{y_adr_bin}'
    
    # Define masks
    dpick_masks = [
        hex_to_bin('06524a0a889643db0884bdde092d1357', 128),
        hex_to_bin('08a25116112a96cd111275ef125125ab', 128),
        hex_to_bin('52346120a24c666a202b59b7249a4a3d', 128),
        hex_to_bin('2cc48244c471350c424daeba40e68cce', 128),
        hex_to_bin('b00703870781b9900471cf3c8703f0f0', 128),
        hex_to_bin('c0f80407f801c1e08781f03ff804ff00', 128),
        hex_to_bin('ff0007f80001fe00f801ffc0fff80000', 128),
        hex_to_bin('fffff8000001fffffffe000000000000', 128),
        hex_to_bin('fffffffffffe00000000000000000000', 128)
    ]

    apick_masks = [
        hex_to_bin('2555b', 20),
        hex_to_bin('49a6d', 20),
        hex_to_bin('8e38e', 20),
        hex_to_bin('f03f0', 20),
        hex_to_bin('ffc00', 20)
    ]
    
    # Compute ECC
    ecc = [0] * 16
    
    for i in range(9):
        dpick_mask = int(dpick_masks[i], 2)
        ecc[i] = bin(int(prgdata_bin, 2) & dpick_mask).count('1') % 2
    
    for i in range(5):
        apick_mask = int(apick_masks[i], 2)
        ecc[i + 9] = bin(int(prgadr_bin, 2) & apick_mask).count('1') % 2

    ecc[1] ^= 1
    ecc[2] ^= 1
    ecc[3] ^= 1
    ecc[4] ^= 1
    ecc[9] ^= 1

    ecc[14] = 0
    ecc[15] = 0
    
    # Convert ECC to hexadecimal
    ecc_hex = ''.join(str(bit) for bit in ecc[::-1])
    ecc_hex = hex(int(ecc_hex, 2))[2:].upper().zfill(4)
    
    return ecc_hex

def verify_ecc(data):
    prgdata, ecc_received = data[:-4], data[-4:]
    ecc_calculated = compute_ecc(prgdata, '0', '0', 0, 1)
    return ecc_received == ecc_calculated

# Example usage
data_128 = '0000000000000036305942365002E363'
data_128 = '0000007d0020bae824a26ee8000004fd'
x_adr = 'A'
x_adr = '9'
y_adr = '0'
y_adr = '2'
reden = 0
ifren = 1

# Compute ECC
ecc_result = compute_ecc(data_128, x_adr, y_adr, reden, ifren)
print(f"Computed ECC: {ecc_result}")

# Verify ECC for 144-bit data
data_144 = '00000000036305942365002E363' + ecc_result
is_ecc_valid = verify_ecc(data_144)
print(f"ECC Verification: {is_ecc_valid}")
