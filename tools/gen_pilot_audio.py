"""Colonna sonora ORIGINALE (sintetizzata con numpy: nessuna musica di terzi, nessuna licenza da gestire).
16 s, stereo, 48 kHz. Drone + pad (La min - Fa - Do - La min/Mi), polso, pizzicati, riser/whoosh sui tagli.
Uso previsto: Reel Instagram/Facebook di AUTO EVO STORE. Se si preferisce un brano licenziato, basta sostituire la traccia."""
import numpy as np, sys, os
from scipy.io import wavfile
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000; DUR = 16.0; N = int(SR * DUR)
CUTS = [3.2, 7.2, 11.2, 14.4]
rng = np.random.default_rng(7)
t = np.arange(N) / SR


def env_ad(n, a, d):
    e = np.ones(n); na = int(a * SR); e[:na] = np.linspace(0, 1, max(1, na)); e[na:] = np.exp(-np.arange(n - na) / (d * SR)); return e


def saw_pad(f, dur, det=(0.997, 1.0, 1.003), bright=6.0):
    n = int(dur * SR); tt = np.arange(n) / SR; y = np.zeros(n)
    for d in det:
        for h in range(1, 24):
            fh = f * d * h
            if fh > 9000: break
            y += np.sin(2 * np.pi * fh * tt + h) * (1.0 / h) * np.exp(-h / bright)
    return y / len(det)


def midi(m): return 440.0 * 2 ** ((m - 69) / 12)


L = np.zeros(N); R = np.zeros(N)


def add(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[:j - i] * gain
    L[i:j] += s * (1 - max(0, pan)); R[i:j] += s * (1 + min(0, pan))


# --- pad a 4 accordi (4 s ciascuno)
chords = [(57, 60, 64), (53, 57, 60), (48, 55, 60), (57, 64, 68)]
for k, ch in enumerate(chords):
    for m in ch:
        p = saw_pad(midi(m), 4.8)
        e = np.minimum(1, np.arange(len(p)) / (SR * 1.4)) * np.exp(-np.maximum(0, np.arange(len(p)) / SR - 3.6) / 0.5)
        add(p * e, k * 4.0 - 0.4 if k else 0, pan=(-0.3 if m % 2 else 0.3), gain=0.11)
# --- drone sub
sub = np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 110 * t) * 0.18
sub *= np.minimum(1, t / 2.5) * np.minimum(1, (DUR - t) / 1.2)
L += sub * 0.22; R += sub * 0.22
# --- polso sub sui battiti (96 bpm) dal secondo shot
beat = 60 / 96
for b in np.arange(CUTS[0], 14.4, beat):
    f = 55 if b < 7.2 else (43.65 if b < 11.2 else 49)
    k = np.sin(2 * np.pi * f * np.arange(int(0.5 * SR)) / SR) * env_ad(int(0.5 * SR), 0.004, 0.16)
    add(k, b, gain=0.30)
# --- pizzicati (ottavi) con riverbero
arp = [(0, 69, 72, 76, 72), (4, 65, 69, 72, 69), (8, 60, 64, 67, 64), (12, 69, 73, 76, 73)]
for (st, *notes) in arp:
    for q in range(8):
        at = st + q * beat / 2
        if at < CUTS[0] - 0.01 and st == 0 and at < 1.6: continue
        m = notes[q % 4] + (12 if q % 8 == 7 else 0)
        n = int(0.9 * SR); tt = np.arange(n) / SR
        p = (np.sin(2 * np.pi * midi(m) * tt) + 0.35 * np.sin(2 * np.pi * midi(m) * 2 * tt)) * env_ad(n, 0.003, 0.22)
        add(p, at, pan=(-0.45 if q % 2 else 0.45), gain=0.075)
# --- hi-hat leggero dal secondo shot
for b in np.arange(CUTS[0], 14.4, beat / 2):
    n = int(0.05 * SR); h = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (0.012 * SR))
    sos = butter(2, 7000 / (SR / 2), 'high', output='sos'); add(sosfilt(sos, h), b, gain=0.035)
# --- riser + impatto sui tagli
for c in [0.0] + CUTS:
    dur = 1.6 if c else 0.0
    if dur:
        n = int(dur * SR); x = rng.normal(0, 1, n)
        sw = np.linspace(300, 6000, n); ph = np.cumsum(sw) / SR
        # rumore filtrato con taglio crescente (approssimazione con somma di bande)
        sos = butter(2, [900 / (SR / 2), 5200 / (SR / 2)], 'band', output='sos'); y = sosfilt(sos, x)
        y *= np.linspace(0, 1, n) ** 2.2
        add(y, c - dur, gain=0.18)
    n = int(1.2 * SR); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (46 - 10 * np.minimum(1, tt / 0.5)) * tt) * env_ad(n, 0.002, 0.35)
    ns = rng.normal(0, 1, n) * env_ad(n, 0.001, 0.12); sos = butter(2, 2200 / (SR / 2), 'low', output='sos')
    add(boom * 0.8 + sosfilt(sos, ns) * 0.25, c, gain=0.34)
# --- riverbero (coda di rumore) sul mix
n = int(2.2 * SR); ir = rng.normal(0, 1, (2, n)) * np.exp(-np.arange(n) / (0.55 * SR))[None, :]
sos = butter(2, 5200 / (SR / 2), 'low', output='sos'); ir = sosfilt(sos, ir, axis=1)
wet = np.stack([fftconvolve(L, ir[0])[:N], fftconvolve(R, ir[1])[:N]])
wet /= (np.abs(wet).max() + 1e-9)
mix = np.stack([L, R]); mix = mix / (np.abs(mix).max() + 1e-9)
mix = mix * 0.82 + wet * 0.20
# --- master: fade, normalizzazione ~ -16 dBFS RMS, limitatore morbido
fade = np.minimum(1, t / 0.4) * np.minimum(1, (DUR - t) / 1.3)
mix *= fade[None, :]
rms = np.sqrt((mix ** 2).mean()); mix *= (10 ** (-16 / 20)) / rms
mix = np.tanh(mix * 1.15) / 1.15
mix *= 0.89 / np.abs(mix).max()
out = (mix.T * 32767).astype(np.int16)
dst = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/pacchetto_pilota_v1/03_reel/AEV_reel-identita_audio_originale_v1.wav'
os.makedirs(os.path.dirname(dst), exist_ok=True)
wavfile.write(dst, SR, out)
print('ok', dst, 'rms_dbfs', 20 * np.log10(np.sqrt(((mix) ** 2).mean())), 'peak', 20 * np.log10(np.abs(mix).max()))
