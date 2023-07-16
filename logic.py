import keyboard

#key combos paired with strings to be written
key_combos = {
    'alt+n': 'Vasvári Botond',
    'alt+e': 'botyware@gmail.com',
    'alt+t': '+36205172585',
    'alt+p': 'Korhelyleves333@',
    'alt+c': 'Kazincbarcika',
    'alt+s': 'Mikszáh Kálmán str. 7. ground floor/1.',
}

def m():
    #start a loop on a thread that globally listens for key combinations
    while(True):
        for key_combo in key_combos:
            if keyboard.is_pressed(key_combo):
                keyboard.write(key_combos[key_combo])
            elif keyboard.is_pressed('esc'):
                break

if __name__ == '__main__':
    m()

