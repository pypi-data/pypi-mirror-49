from bc4py import __chain_version__
from bc4py.config import C, V, P, BlockChainError
from bc4py.bip32 import get_address
from bc4py.user import Balance
from bc4py.user.txcreation import *
from bc4py.database.account import *
from bc4py.database.create import create_db
from bc4py.database.tools import get_output_from_input
from bc4py.user.network.sendnew import send_newtx
from bc4py.user.api import utils
from bc4py.chain.tx import TX
from bc4py_extension import PyAddress
from multi_party_schnorr import PyKeyPair
from aiohttp import web
from binascii import a2b_hex
from time import time
import msgpack


def type2message(message_type, message):
    if message_type == C.MSG_NONE:
        return b''
    elif message_type == C.MSG_PLAIN:
        return message.encode()
    elif message_type == C.MSG_BYTE:
        return a2b_hex(message)
    elif message_type == C.MSG_MSGPACK:
        return msgpack.packb(message, use_bin_type=True)
    elif message_type == C.MSG_HASHLOCKED:
        return a2b_hex(message)
    else:
        raise Exception('Not found message type {}'.format(message_type))


async def create_raw_tx(request):
    # [version=1] [type=TRANSFER] [time=now] [deadline=now+10800]
    # [inputs:list()] [outputs:list()]
    # [gas_price=MINIMUM_PRICE] [gas_amount=MINIMUM_AMOUNT]
    # [message_type=None] [message=None]
    post = await utils.content_type_json_check(request)
    try:
        publish_time = post.get('time', int(time() - V.BLOCK_GENESIS_TIME))
        deadline_time = post.get('deadline', publish_time + 10800)
        message_type = post.get('message_type', C.MSG_NONE)
        message = type2message(message_type, post.get('message'))
        inputs = list()
        input_address = set()
        for txhash, txindex in post.get('inputs', list()):
            txhash = a2b_hex(txhash)
            inputs.append((txhash, txindex))
            pair = get_output_from_input(txhash, txindex)
            if pair is None:
                return web.Response(text="input is unknown or already used", status=400)
            address, coin_id, amount = pair
            input_address.add(address)
        outputs = list()
        for address, coin_id, amount in post.get('outputs', list()):
            outputs.append((PyAddress.from_string(address), coin_id, amount))
        tx = TX.from_dict(
            tx={
                'version': post.get('version', __chain_version__),
                'type': post.get('type', C.TX_TRANSFER),
                'time': publish_time,
                'deadline': deadline_time,
                'inputs': inputs,
                'outputs': outputs,
                'gas_price': post.get('gas_price', V.COIN_MINIMUM_PRICE),
                'gas_amount': 0,
                'message_type': message_type,
                'message': message
            })
        require_gas = tx.size + len(input_address) * C.SIGNATURE_GAS
        tx.gas_amount = post.get('gas_amount', require_gas)
        tx.serialize()
        return utils.json_res({'tx': tx.getinfo(), 'hex': tx.b.hex()})
    except Exception:
        return utils.error_res()


async def sign_raw_tx(request):
    post = await utils.content_type_json_check(request)
    try:
        binary = a2b_hex(post['hex'])
        other_pairs = dict()
        for sk in post.get('pairs', list()):
            sk = a2b_hex(sk)
            keypair: PyKeyPair = PyKeyPair.from_secret_key(sk)
            r, s = keypair.get_single_sign(binary)
            pk = keypair.get_public_key()
            ck = get_address(pk=pk, hrp=V.BECH32_HRP, ver=C.ADDR_NORMAL_VER)
            other_pairs[ck] = (pk, r, s)
        tx = TX.from_binary(binary=binary)
        async with create_db(V.DB_ACCOUNT_PATH) as db:
            cur = await db.cursor()
            for txhash, txindex in tx.inputs:
                pair = get_output_from_input(txhash, txindex)
                if pair is None:
                    return web.Response(text="input is unknown or already used", status=400)
                address, coin_id, amount = pair
                try:
                    sig = await sign_message_by_address(raw=tx.b, address=address, cur=cur)
                    tx.signature.append(sig)
                except BlockChainError:
                    if address not in other_pairs:
                        raise BlockChainError('Not found secret key "{}"'.format(address))
                    tx.signature.append(other_pairs[address])
        data = tx.getinfo()
        return utils.json_res({
            'hash': data['hash'],
            'signature': data['signature'],
            'hex': tx.b.hex(),
        })
    except Exception:
        return utils.error_res()


async def broadcast_tx(request):
    start = time()
    post = await utils.content_type_json_check(request)
    try:
        binary = a2b_hex(post['hex'])
        new_tx = TX.from_binary(binary=binary)
        new_tx.signature = [(a2b_hex(pk), a2b_hex(sig)) for pk, sig in post['signature']]
        if 'R' in post:
            new_tx.R = a2b_hex(post['R'])
        if not send_newtx(new_tx=new_tx):
            raise BlockChainError('Failed to send new tx')
        return utils.json_res({
            'hash': new_tx.hash.hex(),
            'gas_amount': new_tx.gas_amount,
            'gas_price': new_tx.gas_price,
            'fee': new_tx.gas_amount * new_tx.gas_price,
            'time': round(time() - start, 3)
        })
    except Exception:
        return utils.error_res()


async def send_from_user(request):
    start = time()
    if P.F_NOW_BOOTING:
        return web.Response(text='Now booting', status=403)
    post = await utils.content_type_json_check(request)
    async with create_db(V.DB_ACCOUNT_PATH, strict=True) as db:
        cur = await db.cursor()
        try:
            from_name = post.get('from', C.account2name[C.ANT_UNKNOWN])
            from_id = await read_name2userid(from_name, cur)
            to_address = PyAddress.from_string(post['address'])
            coin_id = int(post.get('coin_id', 0))
            amount = int(post['amount'])
            coins = Balance(coin_id, amount)
            if 'hex' in post:
                msg_type = C.MSG_BYTE
                msg_body = a2b_hex(post['hex'])
            elif 'message' in post:
                msg_type = post.get('message_type', C.MSG_PLAIN)
                msg_body = type2message(msg_type, post['message'])
            else:
                msg_type = C.MSG_NONE
                msg_body = b''
            new_tx = await send_from(from_id, to_address, coins, cur, msg_type=msg_type, msg_body=msg_body)
            if 'R' in post:
                new_tx.R = a2b_hex(post['R'])
            if not await send_newtx(new_tx=new_tx):
                raise BlockChainError('Failed to send new tx')
            await db.commit()
            return utils.json_res({
                'hash': new_tx.hash.hex(),
                'gas_amount': new_tx.gas_amount,
                'gas_price': new_tx.gas_price,
                'fee': new_tx.gas_amount * new_tx.gas_price,
                'time': round(time() - start, 3)
            })
        except Exception as e:
            await db.rollback()
            return utils.error_res()


async def send_many_user(request):
    start = time()
    if P.F_NOW_BOOTING:
        return web.Response(text='Now booting', status=403)
    post = await utils.content_type_json_check(request)
    async with create_db(V.DB_ACCOUNT_PATH, strict=True) as db:
        cur = await db.cursor()
        try:
            user_name = post.get('from', C.account2name[C.ANT_UNKNOWN])
            user_id = await read_name2userid(user_name, cur)
            send_pairs = list()
            for address, coin_id, amount in post['pairs']:
                send_pairs.append((PyAddress.from_string(address), int(coin_id), int(amount)))
            if 'hex' in post:
                msg_type = C.MSG_BYTE
                msg_body = a2b_hex(post['hex'])
            elif 'message' in post:
                msg_type = post.get('message_type', C.MSG_PLAIN)
                msg_body = type2message(msg_type, post['message'])
            else:
                msg_type = C.MSG_NONE
                msg_body = b''
            new_tx = await send_many(user_id, send_pairs, cur, msg_type=msg_type, msg_body=msg_body)
            if not await send_newtx(new_tx=new_tx):
                raise BlockChainError('Failed to send new tx')
            await db.commit()
            return utils.json_res({
                'hash': new_tx.hash.hex(),
                'gas_amount': new_tx.gas_amount,
                'gas_price': new_tx.gas_price,
                'fee': new_tx.gas_amount * new_tx.gas_price,
                'time': round(time() - start, 3)
            })
        except Exception as e:
            await db.rollback()
            return utils.error_res()


async def issue_mint_tx(request):
    start = time()
    post = await utils.content_type_json_check(request)
    async with create_db(V.DB_ACCOUNT_PATH, strict=True) as db:
        cur = await db.cursor()
        try:
            user_name = post.get('from', C.account2name[C.ANT_UNKNOWN])
            sender = await read_name2userid(user_name, cur)
            mint_id, tx = await issue_mint_coin(
                name=post['name'],
                unit=post['unit'],
                digit=post.get('digit', 8),
                amount=post['amount'],
                cur=cur,
                description=post.get('description', None),
                image=post.get('image', None),
                additional_issue=post.get('additional_issue', True),
                sender=sender)
            if not await send_newtx(new_tx=tx):
                raise BlockChainError('Failed to send new tx')
            await db.commit()
            return utils.json_res({
                'hash': tx.hash.hex(),
                'gas_amount': tx.gas_amount,
                'gas_price': tx.gas_price,
                'fee': tx.gas_amount * tx.gas_price,
                'time': round(time() - start, 3),
                'mint_id': mint_id
            })
        except Exception:
            return utils.error_res()


async def change_mint_tx(request):
    start = time()
    post = await utils.content_type_json_check(request)
    async with create_db(V.DB_ACCOUNT_PATH, strict=True) as db:
        cur = await db.cursor()
        try:
            user_name = post.get('from', C.account2name[C.ANT_UNKNOWN])
            sender = await read_name2userid(user_name, cur)
            tx = await change_mint_coin(
                mint_id=post['mint_id'],
                cur=cur,
                amount=post.get('amount'),
                description=post.get('description'),
                image=post.get('image'),
                setting=post.get('setting'),
                new_address=post.get('new_address'),
                sender=sender)
            if not await send_newtx(new_tx=tx):
                raise BlockChainError('Failed to send new tx')
            await db.commit()
            return utils.json_res({
                'hash': tx.hash.hex(),
                'gas_amount': tx.gas_amount,
                'gas_price': tx.gas_price,
                'fee': tx.gas_amount * tx.gas_price,
                'time': round(time() - start, 3)
            })
        except Exception:
            return utils.error_res()


__all__ = [
    "create_raw_tx",
    "sign_raw_tx",
    "broadcast_tx",
    "send_from_user",
    "send_many_user",
    "issue_mint_tx",
    "change_mint_tx",
]
