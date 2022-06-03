# -*- coding: UTF-8 -*-
"""
Get general data from teh game.
"""
from ctypes import c_void_p

from pymem import Pymem
from pymem.memory import virtual_query


class GameProcess:
    name = 'hackGU.exe'
    _py_mem = None
    _process_handle = None

    @staticmethod
    def py_mem() -> Pymem:
        if not GameProcess._py_mem:
            GameProcess._py_mem = Pymem(GameProcess.name)

        return GameProcess._py_mem

    @staticmethod
    def process_handle() -> c_void_p:
        if not GameProcess._process_handle:
            GameProcess._process_handle = GameProcess.py_mem().process_handle
            print(f'Process id: {GameProcess.py_mem().process_id}')
            print('')

        return GameProcess._process_handle

    @staticmethod
    def get_base_addresses(region_size: int) -> list[tuple[int, int, int]]:
        next_region = 0x1
        max_address = 0x7fffffff0000
        addresses = []
        while next_region < max_address:
            mbi = virtual_query(GameProcess.process_handle(), next_region)
            next_region = mbi.BaseAddress + mbi.RegionSize
            if mbi.RegionSize == region_size:
                addresses.append((int(mbi.BaseAddress), int(next_region), int(mbi.RegionSize)))

        return addresses
