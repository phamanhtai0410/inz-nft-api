# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG")
    PROJECT = "inz-nft-api"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')

    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')

    # Authentication
    TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXP_TIME', default='864000'))

    # Config celery worker
    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    BROKER_USE_SSL = True
    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.create_domain': {'queue': 'inz-smc-queue'},
        'worker.create_contract_smc': {'queue': 'inz-smc-queue'},
        'worker.insert_new_contract': {'queue': 'inz-smc-queue'},
        'worker.send_task_import_contract': {'queue': 'inz-smc-queue'},
    }

    TASKS_NAME = {
        'IMPORT_CONTRACT': 'worker.task_scan_import_nft'
    }

    PUBLIC_PATH = os.getenv('PUBLIC_PATH')

    # Redis
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER'))
    REDLOCK_REDIS = json.loads(os.getenv('REDLOCK_REDIS', '[]'))

    # Blockchain
    BSC_RPC_URI = os.getenv('BSC_RPC_URI')
    ETH_RPC_URI = os.getenv('ETH_RPC_URI')
    CHAIN_ID = int(os.getenv('CHAIN_ID'))

    IPFS_TOKEN = os.getenv('IPFS_TOKEN')
    WALLET_IAPI = os.getenv('WALLET_IAPI')
    CONFIRM_BLOCK = 1
    ASSETS = json.loads(os.getenv('ASSETS', '{}'))

    AUTH_PRIVATE_KEY = os.getenv('AUTH_PRIVATE_KEY')

    #  Simplex config
    SIMPLEX_URI = os.getenv('SIMPLEX_URI')

    # ANOTHER SERVICE URL
    INZ_DAPP_BASE_URL = os.getenv('INZ_DAPP_BASE_URL')
    INZ_IAPI_BASE_URL = os.getenv('INZ_IAPI_BASE_URL')

    # Innovaz SMC
    # INZ_COIN_TOKEN_ADDRESS = {
    #     'BSC': os.getenv('INZ_COIN_TOKEN_ADDRESS_BSC'),
    #     'ETHEREUM': os.getenv('INZ_COIN_TOKEN_ADDRESS_ETH'),
    #     'POLYGON': os.getenv('INZ_COIN_TOKEN_ADDRESS_POLYGON'),
    # }
    # INZ_MARKET_ADDRESS = {
    #     'BSC': os.getenv('INZ_MARKET_ADDRESS_BSC'),
    #     'ETHEREUM': os.getenv('INZ_MARKET_ADDRESS_ETH'),
    #     'POLYGON': os.getenv('INZ_MARKET_ADDRESS_POLYGON'),
    # }
    # INZ_FACTORY_ADDRESS = {
    #     'BSC': os.getenv('INZ_FACTORY_ADDRESS_BSC'),
    #     'ETHEREUM': os.getenv('INZ_FACTORY_ADDRESS_ETH'),
    #     'POLYGON': os.getenv('INZ_FACTORY_ADDRESS_POLYGON'),
    # }

    # Constants Config
    SIGNATURE_EXPIRE_TIME = 60 * 60
