import math

import numpy as np

from scipy.io.wavfile import write
from typing import Final
from math import fabs

# Constant
VOLUME: Final[int] = 1
SAMPLE_RATE: Final[int] = 20000
FREQ: Final[int] = 2000
DURATION: Final[int] = 3

AMPLITUDE: Final[int] = 2


def make_sin() -> np.core.multiarray:
    t = np.arange(0, DURATION, 1 / SAMPLE_RATE)
    return VOLUME * np.sin(FREQ * 2 * np.pi * t)


def make_echantillon(val_signal: float, power_of_two: int) -> int:
    quantum = AMPLITUDE / (2 ** power_of_two - 1)
    nb_foi_quantum = val_signal // quantum
    list_quantum = [i * quantum for i in range(0, 2 ** power_of_two + 1)]
    list_quantum.append(val_signal)
    list_quantum.sort()

    index = list_quantum.index(val_signal)
    if math.fabs(list_quantum[index - 1] - val_signal) < math.fabs(list_quantum[index + 1] - val_signal):
        return list_quantum[index - 1]
    elif math.fabs(list_quantum[index - 1] - val_signal) > math.fabs(list_quantum[index + 1] - val_signal):
        return list_quantum[index + 1]
    else:
        return list_quantum[index - 1]


# Make echantillon
def make_encodage(signal: np.core.multiarray) -> None:
    nb_bit = [i for i in range(1, 9)]
    for k in nb_bit:
        a = list()
        for i in signal:
            a.append(make_echantillon(i, k))

        a = (np.array(a) - 1)
        write_wav(a, f"{k}bits")
    pass


def write_wav(sin: np.core.multiarray, file_name="main") -> None:
    write("audio/{0}.wav".format(file_name), SAMPLE_RATE, sin)


def main() -> None:
    main_sin = make_sin()

    # recording signal into file
    write_wav(main_sin)

    make_encodage(main_sin + 1)
    pass


if __name__ == '__main__':
    main()
    pass
