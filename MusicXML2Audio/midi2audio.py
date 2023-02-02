import argparse
import os
import subprocess
__all__ = ['FluidSynth']

DEFAULT_SOUND_FONT = os.path.join('../MusicXML2Audio/data/.fluidsynth/FluidR3Mono_GM.sf3')
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_GAIN = 0.2

class FluidSynth():
    def __init__(self, sound_font=DEFAULT_SOUND_FONT, sample_rate=DEFAULT_SAMPLE_RATE, gain=DEFAULT_GAIN):
        self.sample_rate = sample_rate
        self.sound_font = os.path.expanduser(sound_font)
        self.gain = gain

    def midi_to_audio(self, midi_file: str, audio_file: str, verbose=True):
        if verbose:
            stdout = None
        else:
            stdout = subprocess.DEVNULL
        subprocess.call(
            ['fluidsynth', '-ni', '-g', str(self.gain), self.sound_font, midi_file, '-F', audio_file, '-r', str(self.sample_rate)], 
            stdout=stdout, 
        )

    def play_midi(self, midi_file):
        subprocess.call(['fluidsynth', '-i', '-g', str(self.gain), self.sound_font, midi_file, '-r', str(self.sample_rate)])

def parse_args(allow_synth=True):
    parser = argparse.ArgumentParser(description='Convert MIDI to audio via FluidSynth')
    parser.add_argument('midi_file', metavar='MIDI', type=str)
    if allow_synth:
        parser.add_argument('audio_file', metavar='AUDIO', type=str, nargs='?')
    parser.add_argument('-s', '--sound-font', type=str,
        default=DEFAULT_SOUND_FONT,
        help='path to a SF2 sound font (default: %s)' % DEFAULT_SOUND_FONT)
    parser.add_argument('-r', '--sample-rate', type=int, nargs='?',
        default=DEFAULT_SAMPLE_RATE,
        help='sample rate in Hz (default: %s)' % DEFAULT_SAMPLE_RATE)
    return parser.parse_args()

def main(allow_synth=True):
    args = parse_args(allow_synth)
    fs = FluidSynth(args.sound_font, args.sample_rate)
    if allow_synth and args.audio_file:
        fs.midi_to_audio(args.midi_file, args.audio_file)
    else:
        fs.play_midi(args.midi_file)

def main_play():
    """
    A method for the `midiplay` entry point. It omits the audio file from args.
    """
    main(allow_synth=False)

if __name__ == '__main__':
    main()
