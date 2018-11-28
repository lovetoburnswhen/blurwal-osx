# BlurWal

A background application that smoothly blurs your wallpaper when a given
number of windows is opened.


## Example

![A before/after screenshot showing the wallpaper being blurred](https://gitlab.com/BVollmerhaus/blurwal/raw/master/example.png)\
*[dotfiles](https://gitlab.com/BVollmerhaus/dotfiles) used in this example*
| *Wallpaper by [Ian Valerio](https://unsplash.com/@iangvalerio)*


## Feature(s)

BlurWal will first generate transition frames for the current wallpaper,
with each of them being an increasingly blurred version. When you then open
a given number of windows, these frames will be set as your wallpaper in
quick succession, giving the effect of a smooth blur transition. When the
number of open windows goes below the threshold again, the transition will
run in reverse and consequently unblur the wallpaper.

**tl;dr:** A sleek-looking blur effect for your minimal desktop's wallpaper.


## Installation

### Requirements

* `Python 3.6+`
* `ImageMagick` (*for generating transition frames*)
* `feh` (*for setting the wallpaper*)

### From PyPI repository

```shell
pip install --user blurwal
```

### Manually via Git clone

```shell
git clone https://gitlab.com/BVollmerhaus/blurwal
cd blurwal
pip install --user .
```


## Usage

Simply run `blurwal` and it will regenerate its transition frames and blur
on the appropriate window events.


### Options

This list includes only the interesting options – run `blurwal -h` for a
complete list and further information.

| Option | Description |
| ------ | ----------- |
| `-m`, `--min`    | The minimum number of windows to blur the wallpaper (default: 2)
| `-s`, `--steps`  | The number of steps in a blur transition (default: 10, minimum: 2)
| `-b`, `--blur`   | The blur strength (sigma) to use when fully blurred (default: 10)
| `-i`, `--ignore` | A space-separated list of window classes to exclude


## Additional thanks to

* [Matthias Bräuer](https://gitlab.com/Braeuer) (Testing and Feedback)
