from worker.pipeline import AudioPipeline


def main() -> None:
    pipeline = AudioPipeline()
    pipeline.run(job_id="local-dev")


if __name__ == "__main__":
    main()

