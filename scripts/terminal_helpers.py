import click
import shutil
from wcwidth import wcswidth
from prompt_toolkit import prompt

# from prompt_toolkit.application import Application
# from prompt_toolkit.buffer import Buffer
# from prompt_toolkit.key_binding import KeyBindings
# from prompt_toolkit.layout import Layout
# from prompt_toolkit.layout.containers import Window, HSplit, VSplit
# from prompt_toolkit.layout.controls import BufferControl
# from prompt_toolkit.layout.dimension import Dimension

def display_width(s: str) -> int:
    w = wcswidth(s)
    return w if w >= 0 else len(s)

def center_display(s: str, width: int, fillchar: str = " ") -> str:
    s_w = display_width(s)
    if s_w >= width:
        return s

    total_pad = width - s_w
    left = total_pad // 2
    right = total_pad - left
    return (fillchar * left) + s + (fillchar * right)

def term_center(s: str, fallback_cols: int = 80) -> str:
    cols = shutil.get_terminal_size(fallback=(fallback_cols, 20)).columns
    return center_display(s, cols)

def click_center(text: str, **style_kwargs) -> None:
    click.echo(click.style(term_center(text), **style_kwargs))

def centered_prompt(label: str = "") -> str:
    width = shutil.get_terminal_size(fallback=(80, 20)).columns
    pad = width // 2

    prompt_text = " " * pad + label
    return prompt(prompt_text)

# def centered_input(width: int = 40) -> str:
#     buf = Buffer()
#     kb = KeyBindings()

#     @kb.add("enter")
#     def _enter(event):
#         event.app.exit(result=buf.text)

#     input_window = Window(
#         BufferControl(buffer=buf),
#         height=1,
#         width=Dimension(preferred=width),
#         wrap_lines=False,
#     )

#     row = VSplit(
#         [
#             Window(width=Dimension(weight=1)),   # left filler
#             input_window,                        # fixed-width input
#             Window(width=Dimension(weight=1)),   # right filler
#         ],
#         height=1,
#         width=Dimension(weight=1),              # IMPORTANT: span full terminal width
#     )

#     root = HSplit(
#         [row],
#         width=Dimension(weight=1),              # IMPORTANT: span full terminal width
#     )

#     app = Application(
#         layout=Layout(root),
#         key_bindings=kb,
#         full_screen=False,
#     )
#     return app.run()