import ffmpeg
import numpy as np
import matplotlib.pyplot as plt

def get_average_color(frame_data):
    array = np.frombuffer(frame_data, np.uint8)
    average_color = np.mean(array)  # среднее значение цвета по кадру
    return average_color

def analyze_video_compression(original_video, compressed_video, plot_path):
    print("Анализ потерь при сжатии видео (может занять некоторое время)")
    probe_original = ffmpeg.probe(original_video)
    num_frames = int(probe_original['streams'][0]['nb_frames'])
    # num_frames_original == num_frames_compressed
    # Иначе нет смысла в покадровом сравнении!
     
    a, b = map(int,probe_original['streams'][0]['r_frame_rate'].split("/"))
    # представляется в формате 25/1 
    fps = float(a / b)
    # fps_original == fps_compressed

    differences = []
    max_difference: int = 0
    max_difference_time: float = 0.0
    for i in range(num_frames):
        original_frame = (
            ffmpeg
            .input(original_video, ss=i/fps, t=1/fps)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True, capture_stderr=True)
        )
        
        compressed_frame = (
            ffmpeg
            .input(compressed_video, ss=i/fps, t=1/fps)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True, capture_stderr=True)
        )
        
        avg_color_original = get_average_color(original_frame[0])
        avg_color_compressed = get_average_color(compressed_frame[0])
        
        difference = abs(avg_color_compressed - avg_color_original)
        differences.append(difference)
        if difference > max_difference:
            max_difference = difference
            max_difference_time = i / fps

    plt.plot(range(num_frames), differences)
    plt.xlabel("Кадр")
    plt.ylabel("Разница среднего цвета")
    plt.title("Разница среднем цвете между оригинальным и сжатым видео")
    plt.grid()
    plt.scatter(max_difference_time * fps, max_difference, color='red', label=f'Макс. разница на {max_difference_time} секунде')
    plt.legend()
    plt.show()
    print("Построен график")



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
