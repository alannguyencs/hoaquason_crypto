from pathlib import Path
import os

CWF = Path(__file__)

# LOCAL_PATH = "/home/alan/GoogleDrive/investment/hoaquason_crypto/hoaquason_crypto/"
# IS_LOCAL = os.path.isdir(LOCAL_PATH)
DRIVE_PATH = str(CWF.parent) + '/'
# if IS_LOCAL \
#                     else '/content/drive/MyDrive/investment/hoaquason_crypto/hoaquason_crypto/'
# if not os.path.isdir(DRIVE_PATH):
#     DRIVE_PATH = "C:/Users/Alan/Documents/hoaquason_crypto/hoaquason_crypto/"
print ('DRIVE_PATH:', DRIVE_PATH)
BINANCE_LISTING_PATH = DRIVE_PATH + 'binance_listing.json'

