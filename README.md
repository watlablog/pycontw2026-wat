# pycontw2026-wat
Sample code for my PyCon Taiwan 2026 talk: record audio and visualize sound with Python using waveforms, FFTs, and spectrograms.

## Setup

Use Python 3.12. Run these commands from the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, create the environment with `py -3.12 -m venv .venv` and
activate it in PowerShell with `.venv\Scripts\Activate.ps1`.

## View the sample spectrogram

```bash
python src/spectrogram.py
```

This displays a spectrogram of the bundled `src/wav/kuchibue.wav` sample.
No microphone recording is needed.

## Record audio

```bash
python src/record.py
```

This records five seconds of mono audio at 44,100 Hz using the default input
device, then displays the waveform. Close the plot window to save the recording
to `src/wav/recorded.wav`. Microphone access is required.

To visualize your recording, change `"kuchibue.wav"` to `"recorded.wav"` in the
`filename` assignment in `src/spectrogram.py`, then run the spectrogram command
again.

Both scripts resolve WAV paths relative to their own location, so they also work
when run from inside `src`. The sample WAV is included in version control;
recordings and the virtual environment are ignored.
