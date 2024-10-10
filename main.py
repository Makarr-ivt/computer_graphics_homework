from flask import Flask, request, send_file, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from video_compression import compress_video, analyze_video_compression

app = Flask(__name__)

# Конфигурация папок для загрузки видео, сжатого видео и графиков
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'
app.config['PLOTS_FOLDER'] = 'plots'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['PLOTS_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """ 
    Проверяет, допустимо ли расширение файла.
    Возвращает True, если расширение файла в списке допустимых.
    """
    valid_file_extensions = ("avi", "flv", "mov", "mp4", "mpeg", "vob", "wmv", "wmd", "gif")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in valid_file_extensions

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Обрабатывает загрузку файла пользователем.
    Если метод POST, проверяет наличие файла, его допустимость и сохраняет.
    Затем сжимает видео и анализирует его. Перенаправляет на страницу скачивания.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file(file.filename):
            # Обеспечивает безопасное имя файла
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Сжатие видео
            print("Видео сжимается, подождите.")
            compressed_filename = f"compressed_{filename}"
            compressed_path = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)
            compress_video(input_path, compressed_path)
            print("Видео сжато.")
            
            # Анализ и создание графика
            print("Запущен анализ потерь при сжатии.")
            print("Это может занять некоторое время, подождите.")
            plot_filename = f"plot_{filename}.png"
            plot_path = os.path.join(app.config['PLOTS_FOLDER'], plot_filename)
            analyze_video_compression(input_path, compressed_path, plot_path)
            
            # Перенаправление на страницу загрузки результатов
            return redirect(url_for('download_file', filename=compressed_filename, plot_filename=plot_filename))
    
    # Возвращает страницу загрузки, если метод GET
    return render_template('upload.html')

@app.route('/download/<filename>/<plot_filename>')
def download_file(filename, plot_filename):
    """
    Возвращает страницу, позволяющую скачать сжатый файл и график анализа.
    """
    return render_template('download.html', filename=filename, plot_filename=plot_filename)

@app.route('/get_file/<path:filename>')
def get_file(filename):
    """
    Позволяет скачать сжатое видео.
    """
    file_path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

@app.route('/get_plot/<path:plot_filename>')
def get_plot(plot_filename):
    """
    Позволяет скачать график анализа сжатия.
    """
    plot_path = os.path.join(app.config['PLOTS_FOLDER'], plot_filename)
    return send_file(plot_path, as_attachment=True)

if __name__ == "__main__":
    # Запуск приложения Flask в режиме отладки
    app.run(debug=True)
