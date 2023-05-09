import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import scipy.signal

s, Fs = sf.read("klavir.wav")

def get_all_tones():
    MIDIFROM = 24
    MIDITO = 108
    SKIP_SEC = 0.25
    HOWMUCH_SEC = 0.5
    WHOLETONE_SEC = 2
    tones = np.arange(MIDIFROM, MIDITO+1)
    N = int(Fs * HOWMUCH_SEC)
    Nwholetone = int(Fs * WHOLETONE_SEC)
    xall = np.zeros((MIDITO+1, N)) # matrix with all tones - first signals empty,
    # but we have plenty of memory ...
    samplefrom = int(SKIP_SEC * Fs)
    sampleto = samplefrom + N
    for tone in tones:
        x = s[samplefrom:sampleto]
        x = x - np.mean(x) # safer to center ...
        xall[tone,:] = x
        samplefrom += Nwholetone
        sampleto += Nwholetone
    return xall

xall = get_all_tones()

tones_names = [27, 79, 82]
freqs = [38.89, 783.99, 932.33]
midilow = 24
toneSamples = 2 * Fs
tone_periods = []
spektrums = []

fig, ax = plt.subplots(3, 2, figsize=(20, 8))

# -----------------------------------------------------------------------------
#               1 TASK - PLOT 3 PERIODS OF TONE AND SPECTRUM
# -----------------------------------------------------------------------------

# 1 TASK, 1.1 PLOT 3 PERIODS OF TONE
for index, tone in enumerate(tones_names):
    start = toneSamples*(tone - midilow) + 12000        # find start of tone and skip first 0.25s of tone
    start_no_skip = toneSamples*(tone - midilow)        # find start of tone
    spektrums.append(s[start:start+24000])
    period = int(1 / freqs[index] * Fs)					# period of tone in samples
    x = s[start:start+period*3]                         # 3 periods
    tone_periods.append(x - np.mean(x))                 # center signal
    ax[index, 0].set_title(f"Signál {tone}")
    ax[index, 0].set_xlabel('Čas $[s]$', labelpad=10)
    ax[index, 0].set_ylabel('amplituda', labelpad=10)
    ax[index, 0].plot(np.linspace(0, 1/freqs[index]*3, len(s[start:start+period*3])), tone_periods[index])

# create wavs
sf.write(f"audio/a_orig.wav", s[toneSamples*(27 - midilow):toneSamples*(27 - midilow)+Fs//2], Fs)
sf.write(f"audio/b_orig.wav", s[toneSamples*(79 - midilow):toneSamples*(79 - midilow)+Fs//2], Fs)
sf.write(f"audio/c_orig.wav", s[toneSamples*(82 - midilow):toneSamples*(82 - midilow)+Fs//2], Fs)


# 1 TASK, 1.2 PLOT SPECTRUM OF TONE
for index, spektrum in enumerate(spektrums):
    N = spektrum.size
    seg_spec = np.abs(np.fft.fft(spektrum))
    G = np.log(seg_spec + 10**-5)                    # spectrum, 10^-5 to avoid log(0)
    freq = np.arange(G.size) * Fs / N                # frequency (x-axis)

    # create spectrum from signals
    half = freq.size//2
    ax[index, 1].plot(freq[:half], G[:half])  # <= spectrum
    ax[index, 1].set_title(f"Spektrum signál {tones_names[index]}")
    ax[index, 1].set_xlabel('Frequency $[Hz]$')
    ax[index, 1].set_ylabel('logPSD $[dB]$')

plt.tight_layout()
plt.savefig("task_1.pdf")



# -----------------------------------------------------------------------------
#               2 TASK - FIND BASE FREQUENCY OF TONES
# -----------------------------------------------------------------------------

tone27 = sf.read("audio/a_orig.wav")[0]
tone79 = sf.read("audio/b_orig.wav")[0]
tone82 = sf.read("audio/c_orig.wav")[0]

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size // 2:]

def find_base_frequency_using_autocorr(signal, sample_rate):
    autocorr_signal = autocorr(signal)
    peaks, _ = scipy.signal.find_peaks(autocorr_signal)
    best_peak = peaks[0]
    for peak in peaks:
        if autocorr_signal[peak] > autocorr_signal[best_peak]:
            best_peak = peak

    base_frequency = sample_rate / best_peak
    return base_frequency


def find_base_frequency_using_fft(signal, sample_rate):
    fft = np.fft.fft(signal)
    fft = fft[:len(fft)//2]
    max_freq = np.argmax(np.abs(fft))
    base_frequency = max_freq * sample_rate / len(signal)
    return base_frequency


def base_freq_for_midis():
    """calculate base frequency for all midis and output to freqs.txt"""

    freqs = np.zeros(109)
    # find base frequency of all tones and print to file
    with open("freqs.txt", "w") as f:
        f.write(f"{'tone': <10}{'frequency': <15}\n")
        for tone in range(24, 50):
            freq = find_base_frequency_using_autocorr(xall[tone], Fs)
            f.write(f"{tone: <10}{freq: <15}\n")
            freqs[tone] = freq
        for tone in range(50, 109):
            freq = find_base_frequency_using_fft(xall[tone], Fs)
            f.write(f"{tone: <10}{freq: <15}\n")
            freqs[tone] = freq

    return freqs

all_freqs = base_freq_for_midis()
freq_27 = find_base_frequency_using_autocorr(tone27, Fs)
freq_79 = find_base_frequency_using_fft(tone79, Fs)
freq_82 = find_base_frequency_using_fft(tone82, Fs)

print(f"Base frequency of tone 27 is {freq_27} Hz, should be 38.89 Hz")
print(f"Base frequency of tone 79 is {freq_79} Hz, should be 783.99 Hz")
print(f"Base frequency of tone 82 is {freq_82} Hz, should be 932.33 Hz")

tones = [(tone27, freq_27), (tone79, freq_79), (tone82, freq_82)]
fig, ax = plt.subplots(3, 1, figsize=(15, 8))

for index, tone in enumerate(tones):
    N = tone[0].size
    seg_spec = np.abs(np.fft.fft(tone[0]))
    G = np.log(seg_spec**2 + 10**-5)
    freq = np.arange(G.size) * Fs / N
    half = freq.size//2
    ax[index].plot(freq[:half], G[:half])
    ax[index].axvline(x=tone[1], color='r', alpha=0.5)
    ax[index].set_title(f"Spektrum signál {tones_names[index]}")
    ax[index].set_xlabel('Frequency $[Hz]$')
    ax[index].set_ylabel('logPSD $[dB]$')
    plt.tight_layout()
plt.savefig(f"task_2.pdf")



# -----------------------------------------------------------------------------
#                  3 TASK - APPROXIMATION OF REAL BASE FREQUENCY
# -----------------------------------------------------------------------------


def precise_dtft(x,fmax,FREQRANGE,FREQPOINTS):
    n = np.arange(0, x.size)
    fsweep = np.linspace(fmax-FREQRANGE,fmax+FREQRANGE,FREQPOINTS)

    A = np.zeros([FREQPOINTS, x.size],dtype=complex)   
    for k in np.arange(0,FREQPOINTS):
        A[k,:] = np.exp(-1j * 2 * np.pi * fsweep[k] / Fs * n)     # norm. omega = 2 * pi * f / Fs ... 
    Xdtft = np.matmul(A,x.T)
    precisefmax = fsweep[np.argmax(np.abs(Xdtft))]
    return precisefmax

def find_base_frequency(base_frequency, signal):
    FREQRANGE = 100 / 1200 * base_frequency
    FREQPOINTS = 200
    val = precise_dtft(signal, base_frequency, FREQRANGE, FREQPOINTS)
    return np.abs(val)

freq_27_better = find_base_frequency(freq_27, xall[27])
freq_79_better = find_base_frequency(freq_79, xall[79])
freq_82_better = find_base_frequency(freq_82, xall[82])

freqs_better = np.zeros(109)
for tone in range(24, 109):
    freqs_better[tone] = find_base_frequency(all_freqs[tone], xall[tone])

print(f"Base frequency of tone 27 is {freq_27_better} Hz, should be 38.89 Hz")
print(f"Base frequency of tone 79 is {freq_79_better} Hz, should be 783.99 Hz")
print(f"Base frequency of tone 82 is {freq_82_better} Hz, should be 932.33 Hz")

with open("freqs_dtft.txt", "w") as f:
    f.write(f"{'tone': <10}{'frequency': <15}\n")
    for tone in range(24, 109):
        print(f"Finding base frequency of tone {tone}...{all_freqs[tone]}" )
        freq = find_base_frequency(all_freqs[tone], xall[tone])
        f.write(f"{tone: <10}{freq: <15}\n")



# -----------------------------------------------------------------------------
#               4 TASK - Represent each note using Fourier series 
# -----------------------------------------------------------------------------


def represent_tone(tone, freq):
    N = tone.size
    coeffs = []
    FREQRANGE = 100 / 1200 * freq
    FREQPOINTS = 200
    for k in range(5):
        precise_freq = precise_dtft(tone, (k+1)*freq, FREQRANGE, FREQPOINTS)
        X = np.fft.fft(tone)
        coeffs.append(X[int(precise_freq * N / Fs)])
    return coeffs

def transform_to_log_space(values):
    return np.log10(values + 10**-5)

coeffs_27 = represent_tone(tone27, freq_27_better)
coeffs_79 = represent_tone(tone79, freq_79_better)
coeffs_82 = represent_tone(tone82, freq_82_better)

coeffs_27 = np.abs(coeffs_27)
coeffs_79 = np.abs(coeffs_79)
coeffs_82 = np.abs(coeffs_82)

fig, ax = plt.subplots(3, 1, figsize=(15, 8))
N = tone27.size
seg_spec = np.abs(np.fft.fft(tone27))
G = transform_to_log_space(seg_spec)
freq = np.arange(G.size) * Fs / N
half = freq.size//2

ax[0].plot(freq[:half], G[:half])
ax[0].set_title(f"Spektrum signál 27")
ax[0].set_xlabel('Frequency $[Hz]$')
ax[0].set_ylabel('logPSD $[dB]$')
plt.xlim(0, 11*freq_27_better)
for k in range(5):
    ax[0].scatter((k+1)*freq_27_better, transform_to_log_space(np.abs(coeffs_27[k])), color='red')

N = tone79.size
seg_spec = np.abs(np.fft.fft(tone79))
G = transform_to_log_space(seg_spec)
freq = np.arange(G.size) * Fs / N
half = freq.size//2

ax[1].plot(freq[:half], G[:half])
ax[1].set_title(f"Spektrum signál 27")
ax[1].set_xlabel('Frequency $[Hz]$')
ax[1].set_ylabel('logPSD $[dB]$')
plt.xlim(0, 11*freq_79_better)
for k in range(5):
    ax[1].scatter((k+1)*freq_79_better, transform_to_log_space(np.abs(coeffs_79[k])), color='red')

N = tone82.size
seg_spec = np.abs(np.fft.fft(tone82))
G = transform_to_log_space(seg_spec)
freq = np.arange(G.size) * Fs / N
half = freq.size//2

ax[2].plot(freq[:half], G[:half])
ax[2].set_title(f"Spektrum signál 27")
ax[2].set_xlabel('Frequency $[Hz]$')
ax[2].set_ylabel('logPSD $[dB]$')
plt.xlim(0, 11*freq_82_better)
for k in range(5):
    ax[2].scatter((k+1)*freq_82_better, transform_to_log_space(np.abs(coeffs_82[k])), color='red')

plt.tight_layout()
plt.savefig('task_4.pdf')



# -----------------------------------------------------------------------------
#                    5 TASK - Synthesis of tone using FR 
# -----------------------------------------------------------------------------


fig, ax = plt.subplots(3, 1, figsize=(15, 8))

def synthesis_tone(coeffs, freq, amplitude, Length=1):
    """synthesis of tone using FR and given coefficients"""
    N = Fs * Length
    tone = np.zeros(N)
    for k in range(5):
        tone += np.real(coeffs[k] * np.exp(2j * np.pi * k * freq * np.arange(N) / Fs))

    tone = tone / np.max(np.abs(tone)) * amplitude
    return tone


# save tones
sf.write('audio/a.wav', synthesis_tone(coeffs_27, freq_27, np.max(np.abs(xall[27]))), Fs)
sf.write('audio/b.wav', synthesis_tone(coeffs_79, freq_79, np.max(np.abs(xall[79]))), Fs)
sf.write('audio/c.wav', synthesis_tone(coeffs_82, freq_82, np.max(np.abs(xall[82]))), Fs)

synth_27 = synthesis_tone(coeffs_27, freq_27, np.max(np.abs(xall[27])))
synth_79 = synthesis_tone(coeffs_79, freq_79, np.max(np.abs(xall[79])))
synth_82 = synthesis_tone(coeffs_82, freq_82, np.max(np.abs(xall[82])))


def compare_tones(real, synth, freq):
    """compare real signal with synthesized, aligned to the beginning of the signal"""
    corr = np.correlate(real, synth, mode='full')
    pos = np.argmax(corr)
    synth = np.roll(synth, pos - synth.size)
    period = int(1 / freq * Fs)

    return real, synth, period

# plot first 10 periods of real and synthesized signal
real, synth, period = compare_tones(xall[27], synth_27, freq_27)
ax[0].plot(np.linspace(0, 1/freq_27*10, len(real[:10*period])), real[:10*period], label='real')
ax[0].plot(np.linspace(0, 1/freq_27*10, len(real[:10*period])), synth[:10*period], label='synth')
ax[0].set_title(f"Syntéza signálu 27")
ax[0].set_xlabel('Čas $[s]$')
ax[0].set_ylabel('Amplituda')

real, synth, period = compare_tones(xall[79], synth_79, freq_79)
ax[1].plot(np.linspace(0, 1/freq_79*10, len(real[:10*period])), real[:10*period], label='real')
ax[1].plot(np.linspace(0, 1/freq_79*10, len(real[:10*period])), synth[:10*period], label='synth')
ax[1].set_title(f"Syntéza signálu 79")
ax[1].set_xlabel('Čas $[s]$')
ax[1].set_ylabel('Amplituda')

real, synth, period = compare_tones(xall[82], synth_82, freq_82)
ax[2].plot(np.linspace(0, 1/freq_82*10, len(real[:10*period])), real[:10*period], label='real')
ax[2].plot(np.linspace(0, 1/freq_82*10, len(real[:10*period])), synth[:10*period], label='synth')
ax[2].set_title(f"Syntéza signálu 82")
ax[2].set_xlabel('Čas $[s]$')
ax[2].set_ylabel('Amplituda')

plt.tight_layout()
fig.subplots_adjust(bottom=0.12)
fig.legend(labels=["real", "synth"], loc="lower center", ncol=4)

plt.savefig(f"task_5.pdf")



# -----------------------------------------------------------------------------
#   6 TASK - Create a new song using the synthesized tones from skladba.txt 
# -----------------------------------------------------------------------------


coeffs = np.zeros((109, 5), dtype=complex)

# calculate coefficients for all tones and save them to file
for i in range(24, 109):
    coeffs[i] = represent_tone(xall[i], all_freqs[i])
    np.save(f'coeffs_{i}.npy', coeffs[i])


# use this if calculated coefficients are already saved
for i in range(24, 109):
    coeffs[i] = np.load(f'coeffs_{i}.npy')


synth = np.zeros((109, Fs))
for i in range(24, 109):
    synth[i] = synthesis_tone(coeffs[i], freqs_better[i], np.max(np.abs(xall[i])))


with open('skladba.txt', 'r') as f:
    lines = f.read().splitlines()

# get length of song find max time
max_to = 0
for line in lines:
    parts = line.split()
    to = float(parts[1])
    if to > max_to:
        max_to = to

# get length of song in seconds
song_length = max_to / 1000

Fs = 48000                          # 48k or 8k depending on what we want to generate
song = np.zeros(int(song_length * Fs))
for i, line in enumerate(lines):
    print(f"Processing line {i+1}/{len(lines)}")
    # split line into parts
    parts = line.split()

    fr = float(parts[0])            # time from
    to = float(parts[1])            # time to
    note = int(float((parts[2])))   # MIDI note
    vol = int(float((parts[3])))    # volume

    # get frequency of note
    best_freq = freqs_better[note]
    coeff = coeffs[note]
    tone = synthesis_tone(coeff, best_freq, vol, 10)

    # add tone to song
    ffrom = int(fr / 1000 * Fs)
    tto = int(to / 1000 * Fs)
    song[ffrom:tto] += tone[:tto-ffrom]

song = np.convolve(song, np.hamming(100), mode='same')
song = song / np.max(np.abs(song))
song = song * 0.5

# make attack and decay
attack = np.linspace(0, 1, int(0.1 * Fs))
decay = np.linspace(1, 0, int(0.1 * Fs))
song[:int(0.1 * Fs)] *= attack
song[-int(0.1 * Fs):] *= decay

sf.write('audio/out_48k.wav', song, Fs)



# -----------------------------------------------------------------------------
#                       7 TASK - Create spectrogram
# -----------------------------------------------------------------------------


fig, ax = plt.subplots(1, 1, figsize=(15, 8))

def plot_spectrogram(f, t, sgr, name='', vmin=-160, ax=None):
    # Transfer to PSD 
    sgr_log = 10 * np.log10(sgr + 1e-20)  # log(0) is undefined -> +1e-20 (add small value)

    if ax == None:
        fig = plt.figure(figsize=(20, 6))
        ax = fig.add_subplot(111)
    
    ax.set_title(f"Spectogram {name}", pad=10)
    ax.set_xlabel('$t\ [s]$')
    ax.set_ylabel('$f\ [Hz]$', rotation=0, labelpad=42)
    ax.set_xlim(0, 10)

    # pcolormesh of spectogram:
    cmesh = ax.pcolormesh(t, f, sgr_log, shading="gouraud", cmap=plt.cm.inferno, vmin=vmin)
    cbar = plt.colorbar(cmesh, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('PSD\n$[dB]$', rotation=0, labelpad=30)
    plt.tight_layout()
    plt.savefig(f'spectrogram_{name}.png')


song, Fs = sf.read('audio/out_8k.wav')
_freq, _time, _sgr = scipy.signal.spectrogram(song, Fs)
plot_spectrogram(_freq, _time, _sgr[:10*Fs], name='10s z out_8k.wav')

song, Fs = sf.read('audio/out_48k.wav')
_freq, _time, _sgr = scipy.signal.spectrogram(song, Fs)
plot_spectrogram(_freq, _time, _sgr[:10*Fs], name='10s z out_48k.wav')
