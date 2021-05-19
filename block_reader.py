# simple bitcoin block reading script by Charles Recaido
# Central Washington University - Masters in Computational Science

import datetime


# get the header information of a block
def getblockheader(block_header):
    print('-----------------Block header')
    block_header = bytearray(block_header)

    # block version
    block_version = block_header[:4]
    block_version.reverse()
    print('Current block number: 0x' + str(block_version.hex()))

    # hash of previous block
    prev_block_hash = block_header[4:36]
    prev_block_hash.reverse()
    print('Previous block hash: 0x' + str(prev_block_hash.hex()))

    # Merkle Root (a hash of the tx data in the block to prove a tx and save time when there is many tx)
    merkle_root = block_header[36:68]
    merkle_root.reverse()
    print('Merkle root hash: 0x' + str(merkle_root.hex()))

    # The time in which the block header is hashed
    time_mined = block_header[68:72]
    time_mined.reverse()
    print('Time of block: ' + str(datetime.datetime.fromtimestamp(int(time_mined.hex(), 16))))

    # short hand of the target hash for the block (mining purposes to reward a block)
    bits_block = block_header[72:76]
    bits_block.reverse()
    print('Hash target of block: 0x' + str(bits_block.hex()))

    # nonce of block (what miners change to try to find the target hash)
    nonce_block = block_header[76:80]
    nonce_block.reverse()
    print('Nonce of block: ' + str(int(nonce_block.hex(), 16)))
    print('-----------------End Block header')


# get the transaction information of the block
def gettxdata(block_tx):
    print('-----------------Block Transaction')
    block_tx = bytearray(block_tx)
    current_byte = 0

    # transaction count for the block
    current_byte += 1
    tx_cnt = block_tx[:current_byte]
    if 'fd' == tx_cnt.hex():
        current_byte += 2
        tx_cnt = block_tx[(current_byte - 2):current_byte]
        tx_cnt.reverse()
    elif 'fe' == tx_cnt.hex():
        current_byte += 4
        tx_cnt = block_tx[(current_byte - 4):current_byte]
        tx_cnt.reverse()

    tx_cnt = int(tx_cnt.hex(), 16)
    print('Transaction count: ' + str(tx_cnt))

    # loop through transactions
    for i in range(tx_cnt):
        # version of transaction structure
        current_byte += 4
        tx_struct_version = block_tx[(current_byte - 4):current_byte]
        tx_struct_version.reverse()
        print('Tx version: ' + str(int(tx_struct_version.hex(), 16)))

        # number of tx inputs
        current_byte += 1
        tx_input_cnt = block_tx[(current_byte - 1):current_byte]
        if 'fd' == tx_input_cnt.hex():
            current_byte += 2
            tx_input_cnt = block_tx[(current_byte - 2):current_byte]
            tx_input_cnt.reverse()
        elif 'fe' == tx_input_cnt.hex():
            current_byte += 4
            tx_input_cnt = block_tx[(current_byte - 4):current_byte]
            tx_input_cnt.reverse()

        tx_input_cnt = int(tx_input_cnt.hex(), 16)
        print('# of Tx inputs: ' + str(tx_input_cnt))

        # loop through inputs
        for j in range(tx_input_cnt):
            # transaction ID
            current_byte += 32
            tx_id = block_tx[(current_byte - 32):current_byte]
            tx_id.reverse()
            print('Tx ID: 0x' + str(tx_id.hex()))

            # output index (there can be multiple outputs that the input needs to know which one)
            current_byte += 4
            tx_vout = block_tx[(current_byte - 4):current_byte]
            tx_vout.reverse()
            print('Output for input #' + str(j+1) + ': ' + str(tx_vout.hex()))

            # unlocking code size
            current_byte += 1
            tx_scriptsig_size = block_tx[(current_byte - 1):current_byte]
            if 'fd' == tx_scriptsig_size.hex():
                current_byte += 2
                tx_scriptsig_size = block_tx[(current_byte - 2):current_byte]
                tx_scriptsig_size.reverse()
            elif 'fe' == tx_scriptsig_size.hex():
                current_byte += 4
                tx_scriptsig_size = block_tx[(current_byte - 4):current_byte]
                tx_scriptsig_size.reverse()

            tx_scriptsig_size = int(tx_scriptsig_size.hex(), 16)
            print('Size of unlocking code: ' + str(tx_scriptsig_size) + ' bytes.')

            # unlocking script
            current_byte += tx_scriptsig_size
            tx_scriptsig = block_tx[(current_byte - tx_scriptsig_size):current_byte]
            print('Unlocking script 0x' + str(tx_scriptsig.hex()))

            # ending sequence for input
            current_byte += 4
            tx_input_end = block_tx[(current_byte - 4):current_byte]
            tx_input_end.reverse()
            print('End of input #' + str(j+1) + ': ' + str(tx_input_end.hex()))

        # number of tx outputs
        current_byte += 1
        tx_output_cnt = block_tx[(current_byte - 1):current_byte]
        if 'fd' == tx_output_cnt.hex():
            current_byte += 2
            tx_output_cnt = block_tx[(current_byte - 2):current_byte]
            tx_output_cnt.reverse()
        elif 'fe' == tx_output_cnt.hex():
            current_byte += 4
            tx_output_cnt = block_tx[(current_byte - 4):current_byte]
            tx_output_cnt.reverse()

        tx_output_cnt = int(tx_output_cnt.hex(), 16)
        print('# of tx outputs: ' + str(tx_output_cnt))

        # loop through outputs
        for k in range(tx_output_cnt):
            # tx value
            current_byte += 8
            tx_value = block_tx[(current_byte - 8):current_byte]
            tx_value.reverse()
            tx_value = int(tx_value.hex(), 16)
            print('Value of tx: ' + str(tx_value) + ' satoshis (' + str(tx_value/100000000) + ' BTC)')

            # tx script public key size
            current_byte += 1
            scriptpubkey_size = block_tx[(current_byte - 1):current_byte]
            if 'fd' == scriptpubkey_size.hex():
                current_byte += 2
                scriptpubkey_size = block_tx[(current_byte - 2):current_byte]
                scriptpubkey_size.reverse()
            elif 'fe' == scriptpubkey_size.hex():
                current_byte += 4
                scriptpubkey_size = block_tx[(current_byte - 4):current_byte]
                scriptpubkey_size.reverse()

            scriptpubkey_size = int(scriptpubkey_size.hex(), 16)
            print('Public key size: ' + str(scriptpubkey_size))

            # tx script public key
            current_byte += scriptpubkey_size
            scriptpubkey = block_tx[(current_byte - scriptpubkey_size):current_byte]
            print('Output address: 0x' + str(scriptpubkey.hex()))

        # unix time to lock tx or min block height
        current_byte += 4
        locktime = block_tx[(current_byte - 4):current_byte]
        locktime.reverse()
        print('Locktime value: ' + str(locktime.hex()))


    print('-----------------End Block Transaction')


if __name__ == '__main__':
    # file location of blockchain
    # note that bitcoin core blk.dat files contain many "blocks" (so a block of blocks)
    # anytime blocks is mentioned in this script it's referring to the many blocks found in a blk.dat file
    ##filename = 'D:/bitcoin_core/blocks/blk00000.dat'
    filename = 'blktest.dat'

    # open file
    file = open(filename, 'rb')
    cnt = 1

    # the magic bytes designate the start of a new "block" object
    while magic_bytes := file.read(4):
        print('===================================Block ' + str(cnt) + '==============================')
        cnt += 1
        # the size of the header + transaction data of the block
        # this doesn't include the preceding magic bytes and size bytes
        block_size = file.read(4)
        block_size = bytearray(block_size)

        # majority of the blockchain is in big-endian but should be read in little-endian thus the need for reverse
        block_size.reverse()
        # human readable form
        block_size = int(block_size.hex(), 16)
        print('Size of current block: ' + str(block_size) + ' bytes.')

        # get block header information (header is 80 bytes)
        current_block_header = file.read(80)
        getblockheader(current_block_header)

        # get block transaction data
        current_block_tx = file.read(block_size - 80)
        gettxdata(current_block_tx)

    file.close()
    print('Program Finished')



