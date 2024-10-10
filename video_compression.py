import ffmpeg
import numpy as np
import matplotlib.pyplot as plt

def get_average_color(frame_data):
    """Вычисляет средний цвет из кадрового изображения."""
    array = np.frombuffer(frame_data, np.uint8)
    # array -- одномерный массив из всех пикселей кадра
    average_color = np.mean(array)  # среднее значение цвета по кадру
    return average_color

def analyze_video_compression(original_video, compressed_video, plot_path):
    """Сравнивает оригинальное и сжатое видео по кадрам, строит график разницы"""
    # Получаем информацию о видео
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
        # Извлечение кадра из оригинального видео
        original_frame = (
            ffmpeg
            .input(original_video, ss=i/fps, t=1/fps)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True, capture_stderr=True)
        )
        
        # то же из сжатого видео
        compressed_frame = (
            ffmpeg
            .input(compressed_video, ss=i/fps, t=1/fps)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True, capture_stderr=True)
        )
        
        # Получаем средние цвета
        avg_color_original = get_average_color(original_frame[0])
        avg_color_compressed = get_average_color(compressed_frame[0])
        
        # Вычисляем разницу (потерю качества)
        difference = abs(avg_color_compressed - avg_color_original)
        differences.append(difference)
        # поиск кадра с максимальными потерями
        if difference > max_difference:
            max_difference = difference
            max_difference_time = i / fps

    # Построение графика потерь
    plt.plot(range(num_frames), differences)
    plt.xlabel("Кадр")
    plt.ylabel("Разница среднего цвета")
    plt.title("Разница среднем цвете между оригинальным и сжатым видео")
    plt.grid()
    # точка для выделения кадра с наибольшей потерей качества
    plt.scatter(max_difference_time * fps, max_difference, color='red', label=f'Макс. разница на {max_difference_time} секунде')
    plt.legend()
    plt.savefig(plot_path)

import ffmpeg

def compress_video(filename: str, output_filename: str):
    """
    Из видеофайла filename делает сжатое видео output_filename 
    с пониженным битрейтом до 2 Мбит/сек
    """
    try:
        # Пробуем прочитать информацию о видеофайле
        probe = ffmpeg.probe(filename)
        
        # Проверяем наличие аудиопотока (audio stream)
        has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
        
        # Поток видео
        input_video = ffmpeg.input(filename)
        video_stream = input_video.video.filter('eq', contrast=5.0)

        # Настройка параметров вывода
        output_params = {'video_bitrate': '2M', 'vcodec': 'libx264'}
        
        if has_audio:
            # Если есть аудио, добавляем аудиопоток в выходной файл
            output_params['acodec'] = 'aac'
            output_process = ffmpeg.output(video_stream, input_video.audio, output_filename, **output_params)
        else:
            # Если аудио нет, выводим только видео
            output_process = ffmpeg.output(video_stream, output_filename, **output_params)
        
        # Запускаем процесс ffmpeg
        output_process.run(overwrite_output=True)
    
    except ffmpeg.Error as e:
        print('ffmpeg error:', e.stderr.decode())
