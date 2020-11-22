from lpd8.pgm_chg import Pgm_Chg


class Consummer:

    def __init__(self, audios):
        self._running = True
        self.audios = audios

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False

    def ctrl_value(self, data):
        print('CTRL : ' + str(data))

    def note_on_value(self, data):
        # print('NOTE ON : ' + str(data))
        max_velocity = 127
        normalized_volume = data[2] / max_velocity
        audio = self.audios.get(data[0], data[1])
        audio.channel.set_volume(normalized_volume)
        audio.channel.play(audio.sound)

    def note_off_value(self, data):
        # print('NOTE OFF : ' + str(data))
        audio = self.audios.get(data[0], data[1])
        audio.channel.stop()

    def pgm_change(self, data):
        print('PGM CHG : ' + str(data))
        if data[1] == Pgm_Chg.PGM_CHG_4:
            self._running = False
