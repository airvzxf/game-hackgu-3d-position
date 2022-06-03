# -*- coding: UTF-8 -*-
"""
Contain the information of the Offsets.
"""
from struct import pack

from pymem.memory import read_string, read_int, read_float
from pymem.pattern import pattern_scan_module, scan_pattern_page
from pymem.process import module_from_name
from pymem.ressources.structure import MODULEINFO

from core.game_process import GameProcess


class Vol1:
    """
    The base programming classes in the game.
    """
    dll_name = 'hackGU_vol1.dll'
    _dll_module = None

    @staticmethod
    def dll_module() -> MODULEINFO:
        if not Vol1._dll_module:
            Vol1._dll_module = module_from_name(GameProcess.process_handle(), Vol1.dll_name)

        return Vol1._dll_module

    @staticmethod
    def print_dll_module():
        size_total = Vol1.dll_module().lpBaseOfDll + Vol1.dll_module().SizeOfImage
        print(f'Name: {Vol1.dll_module().name}'
              f' | Base: : {Vol1.dll_module().lpBaseOfDll:x}'
              f' | Entrypoint: : {Vol1.dll_module().EntryPoint:x}'
              f' | Size: : {Vol1.dll_module().SizeOfImage:x}'
              f' | Total: {size_total:x}')
        print('')

    class GameObjects:
        """
        The information about the definition of the classes in the game.
        """
        region_size = 0x5001000
        array_init = None
        offset_next_array = 0x80
        offset_next_element = 0x18
        offset_name = 0x48
        offset_type_id = 0x20
        offset_x_position = 0xE0
        offset_y_position = 0xE4
        offset_z_position = 0xE8
        objects_information = None
        _object_addresses = None

        @classmethod
        def __init__(cls):
            memory = GameProcess.py_mem()
            pattern = b'\x4D\x48\x4C\x50\x5F\x4F\x50\x54\x49\x4F\x4E\x5F\x47\x41\x4D\x45\x5F\x43\x54\x52\x4C\x5F\x50' \
                      b'\x43\x00\x00\x00\x00\x4F\x50\x54\x49\x4F\x4E\x00\x00\x00\x00\x00\x00'
            memory_address = pattern_scan_module(memory.process_handle, Vol1.dll_module(), pattern)
            init_array_reference = memory_address + 8 * 6
            init_array_pattern = pack('<Q', init_array_reference)

            for base_address, _, _ in GameProcess.get_base_addresses(cls.region_size):
                found = scan_pattern_page(GameProcess.process_handle(), base_address, init_array_pattern)
                if found[1]:
                    cls.array_init = found[1]
                    print(f'Vol1.GameObjects.array_init: {hex(cls.array_init)}\n')
                    break

            if not cls.array_init:
                error_message = 'Error: Not found the base address of the array which contains the objects in the game.'
                raise Exception(error_message)

        @classmethod
        def _get_main_address_by_type(cls) -> list:
            memory = GameProcess.py_mem()
            array_pointer = cls.array_init
            found = []
            while True:
                next_array = array_pointer + 8 * 2
                element_init = array_pointer + 8 * 3
                next_array_long = memory.read_longlong(next_array)
                element_init_long = memory.read_longlong(element_init)
                array_pointer += 0x80

                if element_init_long != 0:
                    found.append(element_init_long)

                if next_array_long == 0:
                    break

            return found

        @classmethod
        def _get_elements_from_main_class(cls, addresses: list) -> list:
            memory = GameProcess.py_mem()
            found = []
            for address in addresses:
                while True:
                    found.append(address)
                    next_element = memory.read_longlong(address + cls.offset_next_element)
                    address = next_element
                    if next_element == 0:
                        break

            return found

        @classmethod
        def object_addresses(cls):
            main_address_by_type = cls._get_main_address_by_type()
            elements_from_main = cls._get_elements_from_main_class(main_address_by_type)
            cls._object_addresses = elements_from_main

        @classmethod
        def set_objects_information(cls):
            if not cls._object_addresses:
                print('Not exists _object_addresses, it will be created.')
                Vol1.GameObjects.object_addresses()
                print('Created: _object_addresses')

            cls.objects_information = []
            for object_address in cls._object_addresses:
                type_id = read_int(GameProcess.process_handle(), object_address + cls.offset_type_id)
                if type_id < 1:
                    print(f'Warning! Type id: {type_id}')
                    continue
                try:
                    name = read_string(GameProcess.process_handle(), object_address + cls.offset_name) or 'UNKNOWN NAME'
                except UnicodeDecodeError:
                    print(f'Warning: UnicodeDecodeError. Type id: {type_id}')
                    continue
                x_position = round(read_float(GameProcess.process_handle(), object_address + cls.offset_x_position))
                y_position = round(read_float(GameProcess.process_handle(), object_address + cls.offset_y_position))
                z_position = round(read_float(GameProcess.process_handle(), object_address + cls.offset_z_position))

                cls.objects_information.append({
                    'name': name,
                    'type_id': type_id,
                    'x_position': x_position,
                    'y_position': y_position,
                    'z_position': z_position,
                })
            cls.objects_information = sorted(cls.objects_information, key=lambda x: (x['type_id'], x['name']))

            return True
