from pico2d import *

images = {}
wavs  = {}
musics = {}

def load(file):
    extention = file[-4:]
    if extention == '.png':
        global images
        if file in images:
            return images[file]

        image = load_image(file)
        images[file] = image
        return image

    elif extention == '.wav':
        global wavs
        if file in wavs:
            return wavs[file]
        wav = load_wav(file)
        wavs[file] = wav
        return wav

    elif extention == '.mp3':
        global musics
        if file in musics:
            return musics[file]
        music = load_music(file)
        musics[file] = music
        return music

def unload(file):
    extention = file[-4:]
    if extention == '.png':
        global images
        if file in images:
            del images[file]

    elif extention == '.wav':
        global wavs
        if file in wavs:
            del wavs[file]

    elif extention == '.mp3':
        global musics
        if file in musics:
            del musics[file]
