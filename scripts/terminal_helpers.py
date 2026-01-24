import click
import shutil
from wcwidth import wcswidth
from prompt_toolkit import prompt


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