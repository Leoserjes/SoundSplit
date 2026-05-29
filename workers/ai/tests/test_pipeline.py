from worker.pipeline import AudioPipeline


def test_audio_pipeline_returns_expected_mock_artifacts() -> None:
    result = AudioPipeline().run(job_id="unit-test")

    assert result.job_id == "unit-test"
    assert result.artifacts == [
        "vocals.wav",
        "drums.wav",
        "bass.wav",
        "lead_melody.mid",
        "lead_melody.musicxml",
    ]
