import pygame
from lpd8.programs import Programs
from lpd8.pads import Pads


class AudioMappings:

    def __init__(self, pad_sound_map):
        pygame.mixer.init(channels=32)
        self.Sounds = {1: {}, 2: {}, 3: {}, 4: {}}

        # map soundMaps to pad indices
        # distribute channels as much as possible
        max_channels = pygame.mixer.get_num_channels()
        current_pad = 0
        for PGM in Programs.ALL_PGMS:
            for pad in Pads.PAD_INDICES[PGM].ALL_PADS:
                channel_num = current_pad % max_channels
                channel = pygame.mixer.Channel(channel_num)
                file_path = pad_sound_map[PGM][channel_num]
                sound = pygame.mixer.Sound(file_path)
                self.Sounds[PGM][pad] = Audio(channel, sound)
                current_pad += 1

    def set_mapping_easy(self, program, pad_1_to_8, file_name):
        pad = Pads.PAD_INDICES[program][pad_1_to_8 - 1]
        self.set_mapping(program, pad, file_name)

    def set_mapping(self, program, pad, file_name):
        self.Sounds[program][pad].sound = pygame.mixer.Sound(file_name)

    def get(self, program, pad):
        return self.Sounds[program][pad]


class Audio:
    def __init__(self, channel, sound):
        self.channel = channel
        self.sound = sound
