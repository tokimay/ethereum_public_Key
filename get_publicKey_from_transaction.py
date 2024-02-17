from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from eth_account._utils.signing import to_standard_v, extract_chain_id
import web3
import sys

if len(sys.argv) > 1:
    my_transaction_hash = str(sys.argv[1])
else:
    print('usage:')
    print('python get_publicKey_from_transaction.py OUT_GOING_TRANSACTION_HASH')
    exit(1)


w3 = web3.Web3(web3.HTTPProvider('https://nodes.mewapi.io/rpc/eth'))
# Check Connection
t = w3.is_connected()
print('connection is: ', t)

tx = w3.eth.get_transaction(my_transaction_hash)
r = (tx.r).hex()
s = (tx.s).hex()
v = (to_standard_v(extract_chain_id(tx.v)[1]))

print('r: ', r)
print('s: ', s)
print('v: ', v)

sg = w3.eth.account._keys.Signature(vrs=(v, int(r, 16), int(s, 16)))

tt = {k: tx[k] for k in ["to", "nonce", "value", "gas", "chainId", "maxFeePerGas", "maxPriorityFeePerGas", "type", ]}
tt["data"] = tx["input"]
ut = serializable_unsigned_transaction_from_dict(tt)
recover_public_address = sg.recover_public_key_from_msg_hash(ut.hash())
recover_address = sg.recover_public_key_from_msg_hash(ut.hash()).to_checksum_address()

print('recover_public_address: ', recover_public_address.to_hex())
print('recover_address       : ', recover_address)
