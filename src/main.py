#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Entrypoint of the application which generate a 3D model which the characters and interactive objects.
"""
from multiprocessing import Process
from threading import Thread
from time import sleep

from matplotlib.pyplot import pause, subplots
from mplcursors import cursor

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
            'marker': 's',
            'color': '#B21111',
            'type': 'Vehicle',
        },
        3: {
            'marker': '.',
            'color': '#F000D066',
            'type': 'NPCs',
        },
        4: {
            'marker': 'P',
            'color': '#00FF5566',
            'type': 'Kiosks',
        },
        5: {
            'marker': 'd',
            'color': '#0035B235',
            'type': 'Monsters',
        },
        6: {
            'marker': '^',
            'color': '#0088FF66',
            'type': 'Places',
        },
        7: {
            'marker': '+',
            'color': '#00F1C232',
            'type': 'Chims',
        },
        8: {
            'marker': 'x',
            'color': '#00FFFF00',
            'type': 'Type 8',
        },
        9: {
            'marker': '2',
            'color': '#0000FFFF',
            'type': 'Type 9',
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
        'IGA', 'tres', 'MAXBURST', 'Lonely Wolf', ''
    )

    Vol1.GameObjects()

    figure, (axis_1_1, axis_1_2) = subplots(nrows=1, ncols=2, constrained_layout=False)
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

        if axis_1_1.has_data():
            axis_1_1.clear()

        if axis_1_2.has_data():
            axis_1_2.clear()

        axis_1_1.set_title('X, Y')
        axis_1_1.set_xlabel('X')
        axis_1_1.set_ylabel('Y')
        axis_1_2.set_title('X, Z')
        axis_1_2.set_xlabel('X')
        axis_1_2.set_ylabel('Z')

        for key in plots_by_type:
            plot = plots_by_type[key]
            axis_1_1.scatter(plot['x'], plot['y'], s=200, c=plot['color'], marker=plot['marker'], label=plot['label'])
            axis_1_2.scatter(plot['x'], plot['z'], s=200, c=plot['color'], marker=plot['marker'], label=plot['label'])
            for i, txt in enumerate(plot['name']):
                axis_1_1.annotate(txt, (plot['x'][i], plot['y'][i]))
        axis_1_2.legend(bbox_to_anchor=(1, 0.5), loc='center left', title='Objects in the World')

        cursor(hover=2)
        figure.canvas.draw_idle()
        pause(0.1)
        # exit(0)
