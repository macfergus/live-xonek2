from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SliderElement import SliderElement


g_logger = None

CHANNEL = 0

NUM_TRACKS = 4
NUM_SCENES = 4

ENCODERS = [0, 1, 2, 3]
PUSH_ENCODERS = [52, 53, 54, 55]
KNOBS1 = [4, 5, 6, 7]
BUTTONS1 = [48, 49, 50, 51]
KNOBS2 = [8, 9, 10, 11]
BUTTONS2 = [44, 45, 46, 47]
KNOBS3 = [12, 13, 14, 15]
BUTTONS3 = [40, 41, 42, 43]
FADERS = [16, 17, 18, 19]
GRID = [
    [36, 37, 38, 39],
    [32, 33, 34, 35],
    [28, 29, 30, 31],
    [24, 25, 26, 27],
]


def button(notenr, name=None):
    rv = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL, notenr)
    if name is not None:
        rv.name = name
    return rv


def fader(notenr):
    rv = SliderElement(MIDI_CC_TYPE, CHANNEL, notenr)
    return rv


class XoneK2(ControlSurface):
    def __init__(self, instance):
        global g_logger
        g_logger = self.log_message
        super(XoneK2, self).__init__(instance, False)
        with self.component_guard():
            self._set_suppress_rebuild_requests(True)
            self.init_session()
            self.init_mixer()
            self.init_matrix()
            self.init_tempo()

            # connect mixer to session
            self.session.set_mixer(self.mixer)
            self.session.update()
            self.set_highlighting_session_component(self.session)
            self._set_suppress_rebuild_requests(False)

    def init_session(self):
        self.session = SessionComponent(NUM_TRACKS, NUM_SCENES)
        self.session.name = 'Session'
        self.session.update()

    def init_mixer(self):
        self.mixer = MixerComponent(num_tracks=NUM_TRACKS)
        self.mixer.id = 'Mixer'

        self.song().view.selected_track = self.mixer.channel_strip(0)._track

        for i in range(NUM_TRACKS):
            self.mixer.channel_strip(i).set_volume_control(fader(FADERS[i]))

        self.mixer.update()

    def init_matrix(self):
        self.matrix = ButtonMatrixElement()

        for scene_index in range(NUM_SCENES):
            scene = self.session.scene(scene_index)
            scene.name = 'Scene ' + str(scene_index)
            button_row = []
            for track_index in range(NUM_TRACKS):
                note_nr = GRID[scene_index][track_index]
                b = button(note_nr, 'Clip %d, %d button' % (scene_index, track_index))
                button_row.append(b)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = 'Clip slot %d, %d' % (scene_index, track_index)
                clip_slot.set_stopped_value(0)
                clip_slot.set_started_value(64)
                clip_slot.set_launch_button(b)
            self.matrix.add_row(tuple(button_row))

    def init_tempo(self):
        pass
