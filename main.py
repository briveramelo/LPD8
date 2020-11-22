import sys

from lpd8.lpd8 import LPD8
from lpd8.programs import Programs
from lpd8.pads import Pads
from lpd8.knobs import Knobs
from consummer import Consummer
from time import sleep
from audioMappings import AudioMappings
import json
from os import path


def main(argv):
    sound_map_path = argv[0]
    if not path.exists(sound_map_path):
        raise FileNotFoundError("sound map not found at %s" % sound_map_path)
    if not sound_map_path.endswith(".json"):
        raise TypeError("sound map file not json file at %s" % sound_map_path)

    lpd8 = LPD8()
    lpd8.start()

    # load config for sound map and format
    with open(sound_map_path) as sound_map_file:
        sound_map_json = json.load(sound_map_file)

        keys = sound_map_json.keys()
        if not len(keys) == 4:
            raise TypeError("sound map json should use exactly 4 keys named: '1','2','3',4'")
        for i in range(1, 5):
            if not str(i) in keys:
                raise TypeError("sound map json should use exactly 4 keys named: '1','2','3',4'")
            if not len(sound_map_json[str(i)]) == 8:
                raise TypeError("sound map json keys should be exactly 8 items long")

        for i in range(1, 5):
            sound_map_json[i] = sound_map_json.pop(str(i))
            for j in range(0, 8):
                sound_file_path = sound_map_json[i][j]
                if not path.exists(sound_file_path):
                    raise FileNotFoundError("file not found at %s" % sound_file_path)

    audio_mappings = AudioMappings(sound_map_json)
    consummer = Consummer(audio_mappings)

    for PGM in Programs.ALL_PGMS:
        lpd8.subscribe(consummer, consummer.ctrl_value, PGM, LPD8.CTRL, Knobs.ALL_KNOBS)
        lpd8.subscribe(consummer, consummer.note_on_value, PGM, LPD8.NOTE_ON, Pads.PAD_INDICES[PGM].ALL_PADS)
        lpd8.subscribe(consummer, consummer.note_off_value, PGM, LPD8.NOTE_OFF, Pads.PAD_INDICES[PGM].ALL_PADS)
        lpd8.subscribe(consummer, consummer.pgm_change, PGM, LPD8.PGM_CHG, PGM)

    print('ready to play sounds')
    # We loop as long as test class allows it
    while consummer.is_running():

        # Every loop, we update pads status (blink, ON or OFF)
        # This method returns True if LPD8 pad is still running, False otherwise
        if lpd8.pad_update():
            sleep(.5)
        else:

            # If LPD8 pad is not running anymore, we leave the loop
            consummer.stop()

    # We tidy up things and kill LPD8 process
    lpd8.stop()


if __name__ == "__main__":
    main(sys.argv[1:])
