from RawSignal import RawSignal

class EEGSignal(RawSignal):

    def __init__(self, data, sfreq = 512, first_samp = 0, info = None, anotaciones=None):
        super().__init__(data, sfreq, first_samp, info, anotaciones)

        # self.
    