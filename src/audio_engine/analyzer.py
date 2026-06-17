import os
from typing import Dict, Any


def analyze_audio(wav_path: str) -> Dict[str, Any]:
    if not wav_path or not os.path.exists(wav_path):
        return {}

    try:
        import librosa
        import numpy as np
    except ImportError as e:
        print(f"[ANALYZER] librosa/numpy not available: {e}")
        return {}

    try:
        y, sr = librosa.load(wav_path, sr=None, mono=True)

        if len(y) == 0:
            return {}

        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        rms = librosa.feature.rms(y=y)[0]
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        return {
            "spectral_centroid_mean": float(np.mean(spectral_centroids)),
            "spectral_centroid_std": float(np.std(spectral_centroids)),
            "rms_mean": float(np.mean(rms)),
            "rms_std": float(np.std(rms)),
            "rms_energy_variance": float(np.var(rms)),
            "zero_crossing_rate_mean": float(np.mean(zcr)),
            "tempo_bpm": float(tempo),
            "duration_sec": float(len(y) / sr),
        }
    except Exception as e:
        print(f"[ANALYZER] Analysis failed: {e}")
        return {}


def _get_wav_path(state):
    track_spec = state.get("track_specification", {})
    track_id = track_spec.get("track_id", "track_001")
    output_root = track_spec.get("output_dir", "warehouse")
    return os.path.join(output_root, "gold_outputs", track_id, "master_output.wav")


def analyze_audio_node(state: Dict[str, Any]) -> Dict[str, Any]:
    wav_path = _get_wav_path(state)
    print(f"[ANALYZER] Analyzing {wav_path or '(no WAV)'}")

    if not wav_path:
        return {"analysis_metrics": {}}

    metrics = analyze_audio(wav_path)
    if metrics:
        print(f"[ANALYZER] tempo={metrics.get('tempo_bpm', 0):.1f}, "
              f"centroid={metrics.get('spectral_centroid_mean', 0):.0f}, "
              f"rms={metrics.get('rms_mean', 0):.4f}, "
              f"zcr={metrics.get('zero_crossing_rate_mean', 0):.4f}")
    else:
        print(f"[ANALYZER] No metrics extracted")

    return {"analysis_metrics": metrics}
