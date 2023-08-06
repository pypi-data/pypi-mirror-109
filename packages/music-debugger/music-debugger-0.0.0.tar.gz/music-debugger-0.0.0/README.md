# Music debugger
##### ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ Makes debuging (2 music sites) much easier
___

###  SoundCloud ("Example")
```py
from music_debugger import SoundCloud as Sound

print(f'Title: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").title}')
print(f'Image url: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").image}')
print(f'description: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").description}')
print(f'Like count: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").like_count}')
print(f'play count: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").play_count}')
print(f'download count: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").download_count}')
print(f'Comments count: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").comments_count}')
print(f'Type: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").type}')
print(f'Comments count: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").comments_count}')
print(f'Author: {Sound(url="https://soundcloud.com/smilez/happy-ft-snoop-dogg-1").author}')
```

###  Deezer ("Example")
```py
from music_debugger import Deezer as Sound

print(f'Title: {Sound(url="https://www.deezer.com/us/track/1257838602").title}')
print(f'Image url: {Sound(url="https://www.deezer.com/us/track/1257838602").image}')
print(f'description: {Sound(url="https://www.deezer.com/us/track/1257838602").description}')
print(f'Audio: {Sound(url="https://www.deezer.com/us/track/1257838602").audio}')
print(f'Type: {Sound(url="https://www.deezer.com/us/track/1257838602").type}')
print(
    f'Author: {Sound(url="https://www.deezer.com/us/track/1257838602").author}')
```