# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import bitarray
import datetime
import logging
import math
import mmh3
from struct import pack, unpack, calcsize

log = logging.getLogger(__name__)

# A simple-as-possible bloom filter implementation making use of version 3 of the 32-bit murmur
# hash function (for compat with multi-level-bloom-filter-js).
# mgoodwin 2018
class Bloomer:
    FILE_FMT = b'<III'

    def __init__(self, *, size, nHashFuncs, level):
        self.nHashFuncs = nHashFuncs
        self.size = size
        self.level = level

        self.bitarray = bitarray.bitarray(self.size, endian='little')
        self.bitarray.setall(False)

    def hash(self, seed, key):
        if not isinstance(key, bytes):
            if isinstance(key, str):
                key = key.encode('utf-8')
            else:
                key = str(key).encode('utf-8')
        hash_seed = ((seed << 16) + self.level) & 0xFFFFFFFF
        h = (mmh3.hash(key, hash_seed) & 0xFFFFFFFF) % self.size
        return h

    def add(self, key):
        for i in range(self.nHashFuncs):
            index = self.hash(i, key)
            self.bitarray[index] = True

    def __contains__(self, key):
        for i in range(self.nHashFuncs):
            index = self.hash(i, key)
            if not self.bitarray[index]:
                return False
        return True

    def clear(self):
        self.bitarray.setall(False)

    # Follows the bitarray.tofile parameter convention.
    def tofile(self, f):
        """Write the bloom filter to file object `f'. Underlying bits
        are written as machine values. This is much more space
        efficient than pickling the object."""
        f.write(pack(self.FILE_FMT, self.size, self.nHashFuncs, self.level))
        f.flush()
        self.bitarray.tofile(f)

    @classmethod
    def filter_with_characteristics(cls, elements, falsePositiveRate, level=1):
        nHashFuncs = Bloomer.calc_n_hashes(falsePositiveRate)
        size = Bloomer.calc_size(nHashFuncs, elements, falsePositiveRate)
        return Bloomer(size=size, nHashFuncs=nHashFuncs, level=level)

    @classmethod
    def calc_n_hashes(cls, falsePositiveRate):
        return math.ceil(math.log(1.0 / falsePositiveRate, 2))

    @classmethod
    def calc_size(cls, nHashFuncs, elements, falsePositiveRate):
        # From CRLite paper, https://cbw.sh/static/pdf/larisch-oakland17.pdf
        return math.ceil(1.44 * elements * math.log(1 / falsePositiveRate, 2))

    @classmethod
    def from_buf(cls, buf):
        filters = []
        while len(buf) > 0:
            log.debug(len(buf))
            size, nHashFuncs, level = unpack(Bloomer.FILE_FMT, buf[0:12])
            byte_count = math.ceil(size / 8)
            ba = bitarray.bitarray(endian="little")
            ba.frombytes(buf[12:12 + byte_count])
            buf = buf[12 + byte_count:]
            bloomer = Bloomer(size=1, nHashFuncs=nHashFuncs, level=level)
            bloomer.size = size
            log.debug("Size is {}, level {}, nHashFuncs, {}".format(
                size, level, nHashFuncs))
            bloomer.bitarray = ba
            filters.append(bloomer)
        return filters


class FilterCascade:
    DIFF_FMT = b'<III'

    def __init__(self, filters, error_rates=[0.02, 0.5], growth_factor=1.1,
                 min_filter_length=10000, version=0):
        self.filters = filters
        self.error_rates = error_rates
        self.growth_factor = growth_factor
        self.min_filter_length = min_filter_length
        self.version = version

    def initialize(self, *, include, exclude):
        log.debug("{} include and {} exclude".format(
            len(include), len(exclude)))
        depth = 1

        while len(include) > 0:
            starttime = datetime.datetime.utcnow()
            er = self.error_rates[-1]
            if depth < len(self.error_rates):
                er = self.error_rates[depth - 1]

            if depth > len(self.filters):
                self.filters.append(
                    # For growth-stability reasons, we force all layers to be at least
                    # min_filter_length large. This is important for the deep layers near the end.
                    Bloomer.filter_with_characteristics(
                        max(
                            int(len(include) * self.growth_factor),
                            self.min_filter_length), er, depth))
            else:
                # Filter already created for this layer. Check size and resize if needed.
                required_size = Bloomer.calc_size(
                    self.filters[depth - 1].nHashFuncs, len(include), er)
                if self.filters[depth - 1].size < required_size:
                    # Resize filter
                    self.filters[depth -
                                 1] = Bloomer.filter_with_characteristics(
                                     int(len(include) * self.growth_factor),
                                     er, depth)
                    log.info("Resized filter at {}-depth layer".format(depth))
            filter = self.filters[depth - 1]
            log.debug(
                "Initializing the {}-depth layer. err={} include={} exclude={} size={} hashes={}"
                .format(depth, er, len(include), len(exclude), filter.size,
                        filter.nHashFuncs))
            # loop over the elements that *should* be there. Add them to the filter.
            for elem in include:
                filter.add(elem)

            # loop over the elements that should *not* be there. Create a new layer
            # that *includes* the false positives and *excludes* the true positives
            log.debug("Processing false positives")
            false_positives = set()
            for elem in exclude:
                if elem in filter:
                    false_positives.add(elem)

            endtime = datetime.datetime.utcnow()
            log.debug(
                "Took {} ms to process layer {} with bit count {}".format(
                    (endtime - starttime).seconds * 1000 +
                    (endtime - starttime).microseconds / 1000, depth,
                    len(filter.bitarray)))
            # Sanity check layer growth.  Bit count should be going down
            # as false positive rate decreases.
            if depth > 2:
                if len(filter.bitarray) > len(
                        self.filters[depth - 3].bitarray):
                    log.error(
                        "Increase in false positive rate detected. depth {} has {} bits and depth {} has {} bits"
                        .format(depth, len(filter.bitarray), depth - 3,
                                len(self.filters[depth - 3].bitarray)))
                    self.filters.clear()
                    return
            include, exclude = false_positives, include
            if len(include) > 0:
                depth = depth + 1
        # Filter characteristics loaded from meta file may result in unused layers.
        # Remove them.
        if depth < len(self.filters):
            del self.filters[depth:]

    def __contains__(self, elem):
        for layer, filter in [(idx + 1, self.filters[idx])
                              for idx in range(len(self.filters))]:
            even = layer % 2 == 0
            if elem in filter:
                if layer == len(self.filters):
                    return True != even
            else:
                return False != even

    def check(self, *, entries, exclusions):
        for entry in entries:
            assert entry in self, "oops! false negative!"
        for entry in exclusions:
            assert not entry in self, "oops! false positive!"

    def bitCount(self):
        total = 0
        for filter in self.filters:
            total = total + len(filter.bitarray)
        return total

    def layerCount(self):
        return len(self.filters)

    def saveDiffMeta(self, f):
        for filter in self.filters:
            f.write(
                pack(FilterCascade.DIFF_FMT, filter.size, filter.nHashFuncs,
                     filter.level))

    # Follows the bitarray.tofile parameter convention.
    def tofile(self, f):
        NO_VERSION_FMT = "<III"
        VERSION_FMT = "<HIII"

        for filter in self.filters:
            """Write the bloom filter to file object `f'. Underlying bits
            are written as machine values. This is much more space
            efficient than pickling the object."""
            if self.version == 0:
                f.write(pack(NO_VERSION_FMT, filter.size, filter.nHashFuncs, filter.level))
            else:
                f.write(pack(VERSION_FMT, self.version, filter.size, filter.nHashFuncs, filter.level))
            filter.bitarray.tofile(f)
            f.flush()

    @classmethod
    def loadDiffMeta(cls, f):
        filters = []
        size = calcsize(FilterCascade.DIFF_FMT)
        data = f.read()
        while len(data) >= size:
            filtersize, nHashFuncs, level = unpack(FilterCascade.DIFF_FMT,
                                                   data[:size])
            filters.append(
                Bloomer(size=filtersize, nHashFuncs=nHashFuncs, level=level))
            data = data[size:]
        return FilterCascade(filters)

    @classmethod
    def cascade_with_characteristics(cls, capacity, error_rates, layer=0):
        return FilterCascade(
            [Bloomer.filter_with_characteristics(capacity, error_rates[0])],
            error_rates=error_rates)
