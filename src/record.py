import sounddevice as sd
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path


def record(index, samplerate, duration):
    """Record audio and return the audio data and time axis."""
    audio = sd.rec(
        frames=int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32",
        device=index,
        blocking=True,
    )

    # Convert the shape from (num_samples, 1) to (num_samples,).
    data = audio[:, 0]

    # Create the time axis from the actual number of samples.
    t = np.arange(len(data)) / samplerate

    return data, t


def plot(t, data):
    """Display the waveform."""
    plt.rcParams["font.size"] = 14
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"

    fig, ax = plt.subplots()
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_ticks_position("both")

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    ax.plot(t, data, lw=1, color="red")

    fig.tight_layout()
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    duration = 3
    samplerate = 44100
    index = None  # Use the default input device.
    data, t = record(index, samplerate, duration)

    plot(t, data)

    out_dir = Path(__file__).resolve().parent / "wav"
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = out_dir / "recorded.wav"
    sf.write(filename, data, samplerate, subtype="PCM_16")

    print(f"Saved: {filename.resolve()}")
