from flask import Flask, send_file, redirect, url_for, render_template, request, session
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "520cfb052290f243fc5a1d12"

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session['link'] = request.form.get("url")
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template("error.html")
        else:
            return render_template("download.html",
                                   url=url,
                                   title=url.title,
                                   author=url.author,
                                   views=f"{url.views:,}",
                                   publish_date=url.publish_date.strftime("%d-%m-%Y"))
    return render_template("home.html")

@app.route("/download", methods=['GET', 'POST'])
def download_video():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer,
                         as_attachment=True,
                         download_name=f'{url.title}.mp4',
                         mimetype='video/mp4')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
