import ffmpeg

def compress_video(filename: str, output_filename: str):
    print("Видео Сжимается")
    input_stream = ffmpeg.input(filename)
    video_stream = input_stream.filter('eq', contrast=5.0)
    (
        ffmpeg.output(
            video_stream, input_stream.audio,
            output_filename,
            video_bitrate='2M',
            vcodec='libx264',
            acodec='aac',
        )
        .run()
    )
    print("Видео сжато")
