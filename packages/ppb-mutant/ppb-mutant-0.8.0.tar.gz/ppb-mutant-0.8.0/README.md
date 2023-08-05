ppb-mutant
==========

This library provides convenient support for the [Mutant Standard emoji](https://mutant.tech) for games using the [PursuedPyBear engine](https://github.com/ppb/pursuedpybear).

This version is for PursuedPyBear v0.6 and Mutant Standard v0.4.0.


Setup
=====
1. Install the `ppb-mutant` package through your preferred package management
   system. (pip, `requirements.txt`, pipenv, poetry, etc)


Usage
=====

Demo
----

A demo showing all emoji can be found by running `python -m ppb_mutant.index`.


`MutantSprite`
--------------

You can replace the use of `image` in your sprites with `emoji` like so:

```python
class SlimeSprite(ppb_mutant.MutantSprite):
    emoji = 'slime'
```

In addition, the formatting syntax with the variables `morph` and `skin` may be
used for Mutant's customization features:

```python
class PunchRightSprite(ppb_mutant.MutantSprite):
    emoji = 'fist_facing_right_{morph}_{skin}'
    morph = 'clw'
    tone = 'r2'  # "colour"
```

See the [modifier guide](https://mutant.tech/reference/0.3.0/mutstd_modifier_guide_0.3.0.png) for details on these.

Alternatively, most customizable emoji also have aliases defined:

```python
class PunchRightSprite(ppb_mutant.MutantSprite):
    emoji = 'fist_facing_right'
    morph = 'clw'
    tone = 'r2'  # "colour"
```


`SelectScene`
-------------

`SelectScene` is a base for  allowing you to handle mutant morph and tone
(color) customization. It can be used like:

```python
class CustomizeScene(SelectScene):
    class Sprite(SelectScene.Sprite): pass

    class BackSprite(Region, Sprite):
        emoji = 'tick'
        def on_button_pressed(self, mouse, signal):
            if self.contains(mouse.position) and mouse.button is ppb.buttons.Primary:
                signal(ppb.events.StopScene())

    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        left = self.main_camera.frame_left
        self.add(self.BackSprite(pos=(left + 2.5, 1.5)))

    def do_update_morphtone(self):
        print(self.morph, self.tone)
```

For a demo, run `python -m ppb_mutant.picker`.


Copyright Notice
================

This library uses [Mutant Standard emoji](https://mutant.tech), which are licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).


Development
===========
The compiled assets are not part of git.

If you just want a copy, pull them out of one of the PyPI packages and copy into
`ppb_mutant/_assets`

To compile them fresh, run `build.sh`, but it can take a while. This requires
[oxipng](https://github.com/shssoichiro/oxipng) and one of ImageMagick,
Inkscape, or rendersvg.
