#########################################################
# MABOSS Central Configuration (py)
# 
#
#########################################################
#webx / Flask

APP_NAME = 'webx'

VERSION = '1.3.0'

MABOSS_BASE = 'c:/MTP/AVL_dc/bli_monitor'

HOST = '127.0.0.1'
PORT = 6226
DEBUG = True

#api prefix
API = '/api'

ENDPOINT_JOBEXECUTOR_REQ = "tcp://127.0.0.1:62001"

#########################################################
#nginx
NGINX_CONF = ''
#########################################################
#mobile
WEIXIN_TOKEN = 'mabotech'

#########################################################
#Certificate Label Printing

#Engine serial model mapping
#please check  C:\MTP\mabotech\maboss1.2\var\html\maboss\certificate\js\config.js
SERIAL_MODEL_DICT = {'QSB6.7':'B','6LT9.3':'L'}

#production license
PRODUCTION_LICENSE = 'XK06-03-123456'

#lable template
#C:\MTP\mabotech\maboss1.2\maboss\repository\label2\templates

#LABEL_CFG = 'c:/mtp/mabotech/maboss1.1/kserver1.1/configuration/printers.json'

#########################################################
#logging

LOGGING_PATH = MABOSS_BASE+'/logs/'

LOGGING_CONFIG = MABOSS_BASE+'/conf/logging_config.py'

#########################################################
#DB

DB_TYPE = ['ORA', 'PG'] #

# oracle or postgresql
DEFAULT_DB = 'oracle'

ORA_URL = 'oracle+cx_oracle://flx:flx@MES'

#ORA_URL = 'oracle+cx_oracle://xxx:xxx@10.177.198.35:1521/gcicpmes?charset=utf8'

PG_URL = 'postgresql+psycopg2://postgres:pg@localhost:5432/maboss'

DB_URL = 'postgresql+psycopg2://postgres:pg@localhost:5432/maboss'

#DB_URL ='oracle+cx_oracle://xxx:xxx@localhost:1521/mesdb?charset=utf8'

DB_ECHO = True

#########################################################
#motorx server

#Endpoint
#JobExecutor
ENDPOINT_JOBEXECUTOR = "tcp://0.0.0.0:62001"

#JobScheduler
ENDPOINT_SCHEDULER = "tcp://127.0.0.1:62002"
#cron task config
#CRON_CONF = "C:/MTP/mabotech/maboss1.3.0/maboss/configuration/cron.csv"

#Machine Integrator
ENDPOINT_MACHINE = "tcp://127.0.0.1:62003"

#
ENDPOINT_PRINTING = "tcp://127.0.0.1:62004"

#Maintenance
ENDPOINT_MAINTENANCE = "tcp://127.0.0.1:62005"


#########################################################
# repository

REPOSITORIES = []

REPO_NAME = 'functions'

MODULE_PATH = MABOSS_BASE+'/maboss'

#########################################################
# label printing

WORKSTATIONS = ['62300']
SERIALNO_PREFIX = '90'
SERIALNO_STATUS = 3
DAY_OFFSET = 1041

LABEL_BASE = MABOSS_BASE+'/var/printing'

TEMPLATE_BASE = MABOSS_BASE+'/maboss/tasks/label2/templates'

LPR = 'C:/MTP/mabotech/bin/lpr'

LPQ = 'C:/MTP/mabotech/bin/lpq'



