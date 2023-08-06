#!/usr/bin/env python3

"""Document this method."""

from pygwin import Animation, Window, Box, Button, Gauge, Label, StyleClass
from pygwin import Frame, Table, Image, Media, HorizontalRule
from pygwin.animations import ScrollAnimation
from . import glob


TITLE = 'animations'.title()


def get_window(win_sys):
    """animations window"""
    #  pylint: disable=too-many-locals,too-many-statements

    elf = Media.get_image(glob.MONSTERS['elf'][0], scale=(64, 64))
    sc = StyleClass('anim_type').add(
        {'color': (255, 150, 150), 'valign': 'top'}
    )

    #  fill
    def handler(bound, update):
        def fun(prog):
            g.set_value(prog)
            return prog + update if prog != bound else None
        return fun

    def back():
        nonlocal anim_gauge
        stop()
        anim_gauge = Animation(g.value, 100, handler(0, -1), result)
        anim_gauge.start()

    def start():
        nonlocal anim_gauge
        stop()
        anim_gauge = Animation(g.value, 100, handler(100, 1), result)
        anim_gauge.start()

    def stop():
        nonlocal anim_gauge
        if anim_gauge is not None:
            anim_gauge.stop()
            anim_gauge = None
    g = Gauge(0, 100, 0, style={'halign': 'center', 'valign': 'center'})
    anim_gauge = None
    nav_links = Box(
        Label('back', link=back),
        Label('stop', link=stop),
        Label('go', link=start),
        style={
            'orientation': 'horizontal',
            'halign': 'center'
        }
    )
    fill_box = Box(nav_links, g, style={'halign': 'center'})

    #  glow animation
    StyleClass('glow').add(
        {'animation': 'glow'},
        context={'status': 'overed'}
    )
    button = Button('move over me', stc='glow')
    glow_box = Box(button, style={'halign': 'center'})

    #  grow animation
    animation_arguments = {
        'loop': False,
        'period': 50,
        'min_scale': 1.0,
        'max_scale': 1.2,
        'persistent': True
    }
    sc = StyleClass('grow')
    sc.add(
        {
            'animation': 'grow',
            'animation-arguments': {**animation_arguments, 'step': 0.02}
        },
        context={'event': 'on-clicked'}
    )
    sc.add(
        {
            'animation': 'grow',
            'animation-arguments': {**animation_arguments, 'step': -0.02}
        },
        context={'event': 'on-unclicked'}
    )
    label = Label('click on the image to make it grow')
    img = Image(elf, stc='grow', style={'halign': 'center'})
    grow_box = Box(label, img, style={'halign': 'center'})

    #  scroll animation
    def scroll_start(move):
        def fun():
            nonlocal scroll_anim
            if scroll_anim is not None:
                scroll_anim.stop()
            scroll_anim = ScrollAnimation(frame_scroll, move=move)
            scroll_anim.start()
            return True
        return fun

    def scroll_stop():
        nonlocal scroll_anim
        if scroll_anim is not None:
            scroll_anim.stop()
            scroll_anim = None
            return True
        return False
    scroll_anim = None
    link_up = Label('scroll up', link=scroll_start(-1))
    link_stop = Label('stop scrolling', link=scroll_stop)
    link_down = Label('scroll down', link=scroll_start(1))
    links_scroll = Box(
        link_up, link_stop, link_down,
        style={'halign': 'center', 'orientation': 'horizontal'}
    )
    board = glob.lorem_ipsum_textboard()
    frame_scroll = Frame(board, style={'size': (400, 800)})
    scroll_box = Box(links_scroll, frame_scroll, style={'halign': 'center'})

    #  fade out/fade in animation
    st = StyleClass('fade')
    st.add({'animation': 'fadeout'}, context={'event': 'on-over'})
    st.add({'animation': 'fadein'}, context={'event': 'on-unover'})
    label = Label('move over the image to make it disappear')
    img = Image(elf, stc='fade', style={'halign': 'center'})
    fade_box = Box(label, img, style={'halign': 'center'})

    tbl = Table(style={'halign': 'center'})
    tbl.new_row({0: Label('fill', stc='anim_type'), 1: fill_box})
    tbl.new_row({0: HorizontalRule()}, colspan={0: 2})
    tbl.new_row({0: Label('glow', stc='anim_type'), 1: glow_box})
    tbl.new_row({0: HorizontalRule()}, colspan={0: 2})
    tbl.new_row({0: Label('grow', stc='anim_type'), 1: grow_box})
    tbl.new_row({0: HorizontalRule()}, colspan={0: 2})
    tbl.new_row({0: Label('fade', stc='anim_type'), 1: fade_box})
    tbl.new_row({0: HorizontalRule()}, colspan={0: 2})
    tbl.new_row({0: Label('scroll', stc='anim_type'), 1: scroll_box})
    frame = Frame(tbl, style={'expand': True, 'size': ('100%', '100%')})
    result = Window(
        win_sys, frame, title=TITLE,
        style={'size': (600, '90%')}
    )
    result.set_style({'animation': 'fadeout'}, context={'event': 'on-close'})
    result.set_style({'animation': 'fadein'}, context={'event': 'on-open'})

    def close(_):
        del StyleClass['glow']
        del StyleClass['grow']
        del StyleClass['fade']
        del StyleClass['anim_type']
        return True
    result.add_processor('on-close', close)
    return result
