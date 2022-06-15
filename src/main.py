#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Entrypoint of the application which generate a 3D model which the characters and interactive objects.
"""
from multiprocessing import Process
from threading import Thread
from time import sleep

from matplotlib.pyplot import pause, subplots

from core.vol1.vol_1 import Vol1

if __name__ == '__main__':
    Vol1.print_dll_module()

    references = {
        1: {
            'marker': '*',
            'color': '#FFA20066',
            'type': 'Party Player',
        },
        2: {
            'marker': '|',
            'color': '#B2111166',
            'type': 'Vehicle',
        },
        3: {
            'marker': '.',
            'color': '#FF00D066',
            'type': 'NPCs',
        },
        4: {
            'marker': 'P',
            'color': '#77F0A366',
            'type': 'Kiosks',
        },
        5: {
            'marker': 'd',
            'color': '#00FF5566',
            'type': 'Monsters',
        },
        6: {
            'marker': '^',
            'color': '#0088FF66',
            'type': 'Places',
        },
        7: {
            'marker': '+',
            'color': '#F1C23266',
            'type': 'Type 7',
        },
        8: {
            'marker': 'x',
            'color': '#FFFF0066',
            'type': 'Chims',
        },
        9: {
            'marker': '2',
            'color': '#00FFFF66',
            'type': 'Cinematic',
        },
    }

    ignore_names = (
        'Eddie', 'Rudolph', 'Nogmung', 'Oimatsu', 'Vergilius', 'Midnight-Head', 'DOMINATOR', 'Corporal Yano',
        'Ookami Itto', 'SideWinder', 'Ubadama', 'Heretic', 'Kunio', 'Encephalon', 'Boltz', 'Aryosha', 'Kazuki',
        'Blue Eye Samurai', 'Mark', 'Wise Dragon', 'Nagare', 'Colt 31', 'NonBE', 'Great Leo', 'JJ', 'Schrodinger',
        'Trigger', 'NAOO', 'Isolde', 'Wang Lin', 'dr. D', 'Henako', 'Syake', 'Senion', 'Olive', 'Heavenly Flower',
        '-COOH', 'Mile', 'Moonlight Dance', 'Alice', 'Pen Pen', '1/2', 'meruru', 'Sapphire', 'Pale', 'Nuada', 'Tanu',
        'Vanguard', 'Sky', 'TomCat', 'Sagittarius', 'GATES', 'b1u3', 'Watson', 'Tiphereth', 'Ingrid', 'Inui', 'Mikatan',
        'Dimitri', 'Ninjato', 'angel hair', 'Aralagi', 'Chobi', 'Mihirogi', 'Nagi', 'Abcinian', 'Barson', 'Rider Chyob',
        'IGA', 'tres', 'MAXBURST', 'Lonely Wolf', 'William=G', 'Ryotaku', 'Amber', 'Battery Tomekichi', 'Fang',
        'Evil Woman', 'Chamee', 'Cecile', 'Suzuki Pig', 'Jade', 'Quasar', 'Towa', 'Lieutenant Okada', 'Phelix', 'Jill',
        'Osamu', 'Agnes', 'Telese', 'Seisaku', 'Ougai', 'Rintaro', 'Kanko', 'Lettuce Taro', 'EXILE', 'Ayuo',
        'Dragonfly', 'Flamberge', 'Pokuri', 'Yoshio', 'Rental Daughter', 'Ishikari Cat', 'Menou', 'Hiira', 'Pochi',
        'Yatsufusa', 'Shirochan', 'Eteman', 'Chrysanthemum', 'Heart in Brocade', 'Yoko', 'Madame Insane', 'Onyx',
        'Punisher Mitch', 'Aleneor', 'Joanna', '', '', '', '', '', '', '', '', '', '', '', '', ''
    )

    Vol1.GameObjects()

    figure, (axis_1_1, axis_1_2, axis_1_3) = subplots(nrows=1, ncols=3, constrained_layout=False)
    figure.suptitle('HackGU')

    p = Thread(target=Vol1.GameObjects.object_addresses())
    p.start()

    while True:
        if not p.is_alive():
            p.join()
            p = Process(target=Vol1.GameObjects.object_addresses())
            p.start()

        if not Vol1.GameObjects.set_objects_information():
            sleep(1)
            continue

        plots_by_type = {}
        for object_information in Vol1.GameObjects.objects_information:
            type_id = object_information.get('type_id')
            if type_id == 3:
                if object_information.get('name') in ignore_names:
                    continue
                print(object_information.get('name'))
            if type_id not in plots_by_type.keys():
                if type_id not in references.keys():
                    color = '#000088'
                    marker = 'x'
                    label = 'UNKNOWN'
                else:
                    color = references.get(type_id).get('color')
                    marker = references.get(type_id).get('marker')
                    label = references.get(type_id).get('type') or 'UNKNOWN TYPE'

                plots_by_type[type_id] = {
                    'x': [],
                    'y': [],
                    'z': [],
                    'name': [],
                    'color': color,
                    'marker': marker,
                    'label': label
                }
            plots_by_type[type_id]['x'].append(object_information.get('x_position'))
            plots_by_type[type_id]['y'].append(object_information.get('y_position'))
            plots_by_type[type_id]['z'].append(object_information.get('z_position'))
            plots_by_type[type_id]['name'].append(object_information.get('name'))

        axis_1_1.clear()
        axis_1_1.set_title('X, Y')
        axis_1_1.set_xlabel('X')
        axis_1_1.set_ylabel('Y')
        axis_1_2.clear()
        axis_1_2.set_title('X, Z')
        axis_1_2.set_xlabel('X')
        axis_1_2.set_ylabel('Z')
        axis_1_3.clear()
        axis_1_3.set_title('Game Information')
        axis_1_3.set_xlabel('X')
        axis_1_3.set_ylabel('Y')

        for key in plots_by_type:
            plot = plots_by_type[key]
            axis_1_1.scatter(plot['x'], plot['y'], s=200, c=plot['color'], marker=plot['marker'], label=plot['label'])
            axis_1_2.scatter(plot['x'], plot['z'], s=200, c=plot['color'], marker=plot['marker'], label=plot['label'])
            for i, name in enumerate(plot['name']):
                axis_1_1.annotate(name, (plot['x'][i], plot['y'][i]))
                axis_1_2.annotate(name, (plot['x'][i], plot['z'][i]))
        axis_1_1.legend(bbox_to_anchor=(0, 0.5), loc='center right', title='Objects in the World')

        dungeon_info = Vol1.Dungeon()
        axis_1_3.text(0.1, 0.90, 'Dungeon', fontsize=20)
        axis_1_3.text(0.1, 0.85, f'Enemy Parties: {dungeon_info.enemy_party}'
                                 f' | {hex(dungeon_info.enemy_party_address)}', fontsize=12)
        axis_1_3.text(0.1, 0.80, f'Surprise Attack: {dungeon_info.surprise_attack}'
                                 f' | {hex(dungeon_info.surprise_attack_address)}', fontsize=12)
        axis_1_3.text(0.1, 0.75, f'Destroyed objects: {dungeon_info.destroyed_objects}'
                                 f'/{dungeon_info.max_destroyed_objects}'
                                 f' | {hex(dungeon_info.destroyed_objects_address)}', fontsize=12)
        axis_1_3.text(0.1, 0.70, f'Chim spheres: {dungeon_info.chim_spheres}'
                                 f' | {hex(dungeon_info.chim_spheres_address)}', fontsize=12)

        figure.canvas.draw_idle()
        pause(0.1)
        # exit(0)
