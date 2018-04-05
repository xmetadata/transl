# -*- coding: utf-8 -*-
from struct import pack, unpack, calcsize
from pypinyin import pinyin, lazy_pinyin, Style
import configparser
import chardet
import os

INI_PATH = r"D:/Code/transl/files"
CFG_PATH = r"D:/Code/transl/files"
BLK_PATH = r"D:/Code/transl/files"
if __name__ == '__main__':
    fmt = '50s70s'
    config = configparser.ConfigParser()
    config.read(r"%s/StockBlock.ini" % INI_PATH)
    map_table_name_list = []
    map_table_list = {}
    for opt in config.options('BLOCK_NAME_MAP_TABLE'):
        print('OPTION====>', opt)
        # BLOCK_NAME_MAP_TABLE
        print('BLOCK_NAME_MAP_TABLE====>', config['BLOCK_NAME_MAP_TABLE'][opt])
        map_table = ''
        for item in pinyin(config['BLOCK_NAME_MAP_TABLE'][opt], style=Style.FIRST_LETTER):
            map_table += item[0]
        map_table_upper = map_table.upper()
        map_table_upper_static = map_table_upper
        # repeat limit 1000
        for num in range(1000):
            if map_table_upper not in map_table_name_list:
                map_table_name_list.append(map_table_upper)
                break
            else:
                map_table_upper = map_table_upper_static + str(num)
        print(map_table_upper)
        map_table_list[map_table_upper] = config['BLOCK_NAME_MAP_TABLE'][opt]
        # BLOCK_STOCK_CONTEXT
        print('BLOCK_STOCK_CONTEXT====>', config['BLOCK_STOCK_CONTEXT'][opt])
        stock_context = []
        for item in config['BLOCK_STOCK_CONTEXT'][opt].split(','):
            if item:
                stock_context.append(
                    ('1' if int(item[3:][0]) == 6 else '0') + item[3:])
        stock_context_str = "\r\n".join(stock_context)
        print(stock_context_str)
        # BLOCK_STOCK_CONTEXT
        with open(r"%s/%s.blk" % (BLK_PATH, map_table_upper), "wb") as new_blk:
            new_blk.write(stock_context_str.encode('GB2312'))
            new_blk.close
    # BLOCK_NAME_MAP_TABLE
    if os.path.exists(r"%s/blocknew.cfg" % CFG_PATH):
        os.remove(r"%s/blocknew.cfg" % CFG_PATH)
    with open(r"%s/blocknew.cfg" % CFG_PATH, "ab") as new_cfg:
        for item in map_table_list:
            new_cfg.write(pack(fmt, map_table_list[item].encode(
                'GB2312'), item.encode('GB2312')))
        new_cfg.close
