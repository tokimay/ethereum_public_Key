
# This file is part of https://github.com/tokimay/ethereum_public_Key
# Copyright (C) 2016 https://github.com/tokimay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# This software is licensed under GPLv3. If you use or modify this project,
# you must include a reference to the original repository: https://github.com/tokimay/ethereum_public_Key

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


w3 = web3.Web3(web3.HTTPProvider('https://rpc.eth.gateway.fm'))
# Check Connection
t = w3.is_connected()
if not t:
    print('Check internet connection or change HTTPProvider in source code')
    exit(1)
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

print('recovered_public_key: ', recover_public_address.to_hex())
print('recovered_address   : ', recover_address)
