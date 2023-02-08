# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
__models__ = ['OrderModel']

from config import Config
from connect import connect_db, redis_cluster
from lib import DaoModel
from models.order import OrderDao

NFTsModel = DaoModel(col=connect_db.db.nfts, redis=redis_cluster)

OrderModel = OrderDao(col=connect_db.db.orders, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
