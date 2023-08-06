# pylint: disable=locally-disabled, multiple-statements, unused-argument, no-value-for-parameter, no-member, invalid-name, too-many-function-args, unused-import, missing-function-docstring
"""
TBD
"""
from timeit import default_timer as timer
from numba import vectorize
import numpy as np
from entangle.logging.debug import logging
from entangle.process import process


@process(shared_memory=True)
def dopow(names, smm=None, sm=None):
    # pylint: disable=locally-disabled, unused-variable

    print("Names:", names)
    (namea, nameb, _, _, typea, typeb) = names

    start = timer()

    # Get named shared memory segments
    shma = sm(namea)
    shmb = sm(nameb)

    # Get prepopulated array buffers
    np_shma = np.frombuffer(shma.buf, dtype=typea)
    np_shmb = np.frombuffer(shmb.buf, dtype=typeb)

    @vectorize(['float32(float32, float32)'], target='cuda')
    def _pow(a, b):
        return a ** b

    _pow(np_shma, np_shmb)

    duration = timer() - start

    print("Powers Time: ", duration)


@process(shared_memory=True)
def createvectors(smm=None, sm=None):
    # pylint: disable=locally-disabled, unused-variable

    vec_size = 100000000

    start = timer()

    # Create random array of values
    a = b = np.array(np.random.sample(vec_size), dtype=np.float32)

    # write matrices to shared memory
    shma = smm.SharedMemory(a.nbytes)
    shmb = smm.SharedMemory(b.nbytes)

    names = (shma.name, shmb.name, a.shape, b.shape, a.dtype, b.dtype)

    duration = timer() - start
    print("Create Vectors Time: ", duration)

    return names


if __name__ == '__main__':
    dp = dopow(
        createvectors()
    )

    dp()
