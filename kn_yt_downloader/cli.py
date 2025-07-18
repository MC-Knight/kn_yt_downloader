import os
from rich.console import Console
from rich.prompt import Prompt
from yt_dlp import YoutubeDL

console = Console()


def welcome():
    console.clear()
    console.print("=======================================================")
    console.print(
        "             Knight Youtube Downloader CLI             ", style="bold green"
    )
    console.print("  A simple CLI tool to download YouTube videos/audio.  ")
    console.print("=======================================================")


def get_input():
    url = Prompt.ask("[green]Paste YouTube link[/green]").strip()
    if not url:
        console.print(
            "[red]Error:[/red] [bold red]You must provide a YouTube link.[/bold red]"
        )
        return get_input()
    return url


def download_video(url):
    try:
        console.print(f"[blue]Fetching resource info...[/blue]")
        ydl_opts = {
            "format": "best",
            "outtmpl": "%(title)s.%(ext)s",
            "noplaylist": True,
            "quiet": False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            console.print(f"[green]✅ Download completed: {info['title']}[/green]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


def main():
    welcome()
    url = get_input()
    download_video(url)


if __name__ == "__main__":
    main()
