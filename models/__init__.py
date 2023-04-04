# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
__models__ = ['OrderModel', 'SignatureLogModel']

from config import Config
from connect import connect_db, redis_cluster
from lib import DaoModel
from models.order import OrderDao
from models.signature import SignatureDao

NFTsModel = DaoModel(col=connect_db.db.nft, redis=redis_cluster)
NFTContractsModel = DaoModel(col=connect_db.db.nft_contracts, redis=redis_cluster)
UsersContractsModel = DaoModel(col=connect_db.db.users_contracts, redis=redis_cluster)
CryptoCurrenciesModel = DaoModel(col=connect_db.db.crypto_currencies, redis=redis_cluster)

OrderModel = OrderDao(col=connect_db.db.orders, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

SignatureLogModel = SignatureDao(col=connect_db.db.signature_log, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)