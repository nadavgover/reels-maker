from aubio import source, onset


def get_beat_timestamps(filename, sample_rate=0):
    win_s = 512  # fft size
    hop_s = win_s // 2  # hop size
    s = source(filename, sample_rate, hop_s)
    sample_rate = s.samplerate

    o = onset("default", win_s, hop_s, sample_rate)

    # list of onsets, in samples
    onsets = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        if o(samples):
            onsets.append(o.get_last_s())
        total_frames += read
        if read < hop_s:
            break
    return onsets


def get_beat_intervals_greater_than_threshold(beat_timestamps, threshold):
    beat_timestamps = beat_timestamps[:]
    beat_timestamps.insert(0, 0)
    beat_intervals = []
    last_used_i = 0
    for i, beat_timestamp in enumerate(beat_timestamps[1:], 1):
        for prev_timestamp in reversed(beat_timestamps[last_used_i:i]):
            interval = beat_timestamp - prev_timestamp
            if interval > threshold:
                beat_intervals.append(interval)
                last_used_i = i
                break
    return beat_intervals


if __name__ == '__main__':
    timestamps = get_beat_timestamps("audio/avengers_theme.mp3")
    beat_intervals = get_beat_intervals_greater_than_threshold(timestamps, 1)
