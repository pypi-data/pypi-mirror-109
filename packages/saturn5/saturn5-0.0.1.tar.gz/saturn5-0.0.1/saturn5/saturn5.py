'''
description:
author: ['Felipe Sá']
version: 1.0.0
created: 2021-06-14
last modified date: 2021-06-14
'''

import time

def launch():

    rocket = '''
                  !
                  !
                  ^  
                 / \\
                |===|
                |   |
                |   |
                |   |
               /_____\\
               |     |
               |     |
               |     |
               |     |
              /| |   |\\
             / | |   | \\
            /__|_|___|__\\
               /_\/_\\
               ######
              ########
               ######
                ####
                ####
                 ##
                 ##   
                 ##
                 ##

    '''

    for i in range(9, 0, -1):
        print(f'{i}...')
        time.sleep(1)
    print('Booster ignition and lifoff...a new era of Clicksign date lake exploration!!!')
    time.sleep(1)
    print(rocket)

