from passport.wozimage import DiskImage, Track, WozError, raise_if
import bitarray

class EDDReader(DiskImage):
    def __init__(self, filename=None, stream=None):
        DiskImage.__init__(self, filename, stream)
        with stream or open(filename, 'rb') as f:
            for i in range(137):
                raw_bytes = f.read(16384)
                raise_if(len(raw_bytes) != 16384, WozError, "Bad EDD file (did you image by quarter tracks?)")
                bits = bitarray.bitarray(endian="big")
                bits.frombytes(raw_bytes)
                self.tracks.append(Track(bits, 131072))

    def seek(self, track_num):
        if type(track_num) != float:
            track_num = float(track_num)
        if track_num < 0.0 or \
           track_num > 35.0 or \
           track_num.as_integer_ratio()[1] not in (1,2,4):
            raise WozError("Invalid track %s" % track_num)
        trk_id = int(track_num * 4)
        return self.tracks[trk_id]

