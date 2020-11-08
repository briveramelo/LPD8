import pygame

from lpd8.pgm_chg import Pgm_Chg


class Consummer:

    def __init__(self):
        self._running = True
        pygame.mixer.init(channels=8)
        self.sndA = pygame.mixer.Sound("./sounds/special_explosion.wav")
        self.soundChannelA = pygame.mixer.Channel(1)

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False

    def ctrl_value(self, data):
        print('CTRL : ' + str(data))

    def note_on_value(self, data):
        print('NOTE ON : ' + str(data))
        maxVelocity = 127
        normalizedVolume = data[2] / maxVelocity
        self.soundChannelA.set_volume(normalizedVolume)
        self.soundChannelA.play(self.sndA)

    def note_off_value(self, data):
        self.soundChannelA.stop()
        print('NOTE OFF : ' + str(data))

    def pgm_change(self, data):
        print('PGM CHG : ' + str(data))
        if data[1] == Pgm_Chg.PGM_CHG_4:
            self._running = False
