from web3 import Web3
from typing import List, Any, Dict, Tuple, HexStr
import time
from database.models.Block import Block
from database.models.Receipt import Receipt
from database.models.Tx import Tx
from database.db import get_session
from sqlalchemy import desc
from tqdm import tqdm
from config import web3_rpc, fetch_balances


class Fetch_blocks:
    def __init__(self, every_block: int = 2) -> None:
        self._web3 = Web3(Web3.HTTPProvider(web3_rpc))
        self._session = get_session()
        self._every_block = every_block
        self._fetch_balances = fetch_balances

    def start_fetch(self, block_range: List = []) -> float:
        start_time = time.time()
        last_block = self._web3.eth.get_block("latest")["number"]
        with self._session as session:
            last_block_in_db_call = (
                session.query(Block.blockNumber).order_by(desc(Block.blockNumber)).first()
            )

            if (last_block_in_db_call) == None:
                last_block_in_db = 16203176
            else:
                last_block_in_db = last_block_in_db_call[0]

            all_blocks_in_db_query = session.query(Block.blockNumber).all()
            all_blocks_in_db = []
            for b in all_blocks_in_db_query:
                d = b._asdict()
                all_blocks_in_db.append(d["blockNumber"])
        receipts_list = []
        txs_list = []
        blocks_list = []
        count = 0

        if len(block_range) == 0 or len(block_range) == 1:
            start = last_block_in_db + 1
            end = last_block + 1
        elif len(block_range) == 2:
            start = block_range[0]
            end = block_range[1] + 1
        else:
            return 0

        for block_num in tqdm(range(start, end)):
            block_row, block_data = self.get_block_row(block_num)
            if block_num not in all_blocks_in_db:
                blocks_list.append(Block(**block_row))
            else:
                continue

            for tx_hash in tqdm(block_data["transactions"]):
                tx_row = self.get_tx_row(tx_hash)
                txs_list.append(Tx(**tx_row))

                receipt_row = self.get_receipt_row(block_num, tx_hash)
                receipts_list.append(Receipt(**receipt_row))

            count = count + 1

            if (count % self._every_block) == 0:
                with get_session() as session:
                    session.add_all(blocks_list)
                    session.add_all(txs_list)
                    session.add_all(receipts_list)
                    session.commit()
                    session.close()

                del blocks_list
                del txs_list
                del receipts_list
                blocks_list = []
                txs_list = []
                receipts_list = []

        return time.time() - start_time

    def get_block_row(self, block_num) -> Tuple[Dict[Any, HexStr], Any]:
        block_data = self._web3.eth.getBlock(block_num)
        block_row = {}
        to_hex = [
            "extraData",
            "logsBloom",
            "mixHash",
            "nonce",
            "parentHash",
            "receiptsRoot",
            "sha3Uncles",
            "stateRoot",
            "transactionsRoot",
        ]

        for key, value in block_data.items():
            if key in to_hex:
                block_row[key] = self._web3.toHex(value)
            elif key == "hash":
                block_row["blockHash"] = self._web3.toHex(value)
            elif key == "number":
                block_row["blockNumber"] = value
            elif key == "totalDifficulty":
                block_row[key] = str(value)
            elif key == "transactions":
                block_row[key] = str(value)
            elif key == "uncles":
                block_row[key] = str(value)
            else:
                block_row[key] = value

        return block_row, block_data

    def get_tx_row(self, tx_hash) -> dict:
        tx_data = self._web3.eth.getTransaction(tx_hash)
        tx_row = {}

        to_hex = ["blockHash", "r", "s"]

        for key, value in tx_data.items():
            if key in to_hex:
                tx_row[key] = self._web3.toHex(value)
            elif key == "hash":
                tx_row["tx_hash"] = self._web3.toHex(value)
            elif key == "from":
                tx_row["addressFrom"] = value
            elif key == "to":
                tx_row["addressTo"] = value
            elif key == "accessList":
                tx_row[key] = str(value)
            elif key == "value":
                tx_row[key] = str(value)
            else:
                tx_row[key] = value

        return tx_row

    def get_receipt_row(self, block_num, tx_hash) -> dict:
        receipt_data = self._web3.eth.getTransactionReceipt(tx_hash)
        receipt_row = {}
        if self._fetch_balances:
            balance_from = self._web3.eth.getBalance(
                receipt_data["from"], block_identifier=block_num
            )
            try:
                balance_to = self._web3.eth.getBalance(
                    receipt_data["to"], block_identifier=block_num
                )
            except TypeError:
                balance_to = -1
        else:
            balance_to = 0
            balance_from = 0

        for key, value in receipt_data.items():
            if key == "from":
                receipt_row["fromAddress"] = value
            elif key == "logs":
                receipt_row[key] = str(value)
            elif key == "logsBloom":
                receipt_row[key] = self._web3.toHex(value)
            elif key == "blockHash":
                receipt_row[key] = self._web3.toHex(value)
            elif key == "to":
                receipt_row["toAddress"] = value
            elif key == "transactionHash":
                receipt_row["tx_hash"] = self._web3.toHex(value)
            else:
                receipt_row[key] = value

        receipt_row["balanceFrom"] = str(balance_from)
        receipt_row["balanceTo"] = str(balance_to)

        return receipt_row
