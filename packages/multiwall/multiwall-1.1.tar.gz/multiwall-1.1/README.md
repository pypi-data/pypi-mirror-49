# Wallpyper

Set your background on multiple monitors to random images from [Unsplash](https://unsplash.com/), [mikedrawsdota](http://wallpapers.mikedrawsdota.com/#_=_), and more.

## Installation

```bash
pip3 install multiwall
```

## Usage

```bash
pip3 install -r requirements.txt
python3 -m multiwall
```

The default source is [Unsplash](https://unsplash.com/), use the `--source` flag to change it.

```bash
python3 -m multiwall --source 'mikedrawsdota'
```

## Examples

```powershell
# 4k monitor + 1080p monitor (5760x2160 picture)
py -3 -m multiwall --monitors "3440x1440,1920x1080"
```

![5760x2160](https://i.imgur.com/huusFe8.jpg)


```powershell
# 4k monitor + portait monitor
py -3 -m multiwall --monitors "3440x1440,1440x2560"
```
![3440x1440,1440x2560](https://i.imgur.com/aNE8aYF.jpg)


## Planned Features

* [*] Automatic monitor size detection
* [*] Custom search parameters
* [*] Save images without setting wallpaper
* [ ] Favorite images
