from pathlib import Path

import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt
from scipy.signal import ShortTimeFFT


def compute_spectrogram(data, samplerate, frame_size, hop, db_ref):
    """Compute an amplitude spectrogram in decibels."""
    sft = ShortTimeFFT.from_window(
        "hann",
        fs=samplerate,
        nperseg=frame_size,
        noverlap=frame_size - hop,
        fft_mode="onesided2X",
        scale_to="magnitude",
    )

    # Compute the STFT and take the magnitude.
    # Frames extending beyond the recording are zero-padded.
    amplitude = np.abs(sft.stft(data))

    # Convert amplitude to decibels relative to db_ref.
    # Use a small positive floor to avoid log10(0).
    db = 20 * np.log10(np.maximum(amplitude / db_ref, 1e-12))

    # Get the frame-center times and frequency bins.
    time = sft.t(len(data))
    freq = sft.f

    return time, freq, db


def plot(time, freq, db, duration, max_frequency):
    """Display the spectrogram."""
    plt.rcParams["font.size"] = 14
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_ticks_position("both")

    # Keep the color range fixed for comparison with the slides.
    im = ax.pcolormesh(
        time,
        freq,
        db,
        shading="auto",
        cmap="jet",
        vmin=0,
        vmax=80,
    )

    ax.set_xlim(0, duration)
    ax.set_ylim(0, max_frequency)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Frequency [Hz]")
    fig.colorbar(im, ax=ax, label="Amplitude [dB]")

    fig.tight_layout()
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    # Read the bundled sample WAV file.
    filename = Path(__file__).resolve().parent / "wav" / "whistle.wav"

    audio, samplerate = sf.read(
        filename,
        dtype="float32",
        always_2d=True,
    )

    # Select the first channel and convert to a one-dimensional array.
    # For a stereo file, this selects the left channel without mixing.
    data = audio[:, 0]

    # STFT settings: 2,048 samples per frame and 75% overlap.
    frame_size = 2048
    hop = 512

    # Digital amplitude reference, not calibrated sound pressure.
    # The displayed values are not dB SPL.
    db_ref = 2e-5

    # ShortTimeFFT requires at least half a window of input samples.
    if len(data) < (frame_size + 1) // 2:
        raise ValueError(
            "The recording is too short. "
            "Use a longer recording or a smaller frame_size."
        )

    time, freq, db = compute_spectrogram(
        data, samplerate, frame_size, hop, db_ref
    )

    # Display the full recording and frequencies up to 3,000 Hz.
    # Do not exceed the Nyquist frequency.
    duration = len(data) / samplerate
    max_frequency = min(3000, samplerate / 2)

    plot(time, freq, db, duration, max_frequency)
