import os
import platform
import shutil
from rich.console import Console
from rich.prompt import Prompt
from yt_dlp import YoutubeDL

console = Console()

IS_WINDOWS = platform.system() == "Windows"


def welcome():
    console.clear()
    console.print("=======================================================")
    console.print(
        "             Knight Youtube Downloader CLI             ", style="bold green"
    )
    console.print("  A simple CLI tool to download YouTube videos/audio.  ")
    console.print("=======================================================")


def get_ffmpeg_path():
    if IS_WINDOWS:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "ffmpeg", "bin")
    return None


def check_ffmpeg_linux():
    if not IS_WINDOWS:
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            console.print("[red]❌ FFmpeg is not installed on your system.[/red]")
            console.print("Please install it using:")
            console.print("[green]sudo apt install ffmpeg[/green] (Debian/Ubuntu)")
            console.print("[green]brew install ffmpeg[/green] (macOS/Homebrew)")
            raise FileNotFoundError("Missing ffmpeg and/or ffprobe.")


def get_input():
    url = Prompt.ask("[green]Paste YouTube link[/green]").strip()
    if not url:
        console.print(
            "[red]Error:[/red] [bold red]You must provide a YouTube link.[/bold red]"
        )
        return get_input()
    return url


def get_format_choice():
    format_map = {"1": "video", "2": "audio", "3": "best"}

    console.print(
        "[yellow]Choose format:[/yellow] [1] Video [2] Audio [3] Best [4] Custom (default: 3)"
    )
    choice = Prompt.ask("[green]Enter choice[/green]", default="3").strip()

    if choice not in format_map:
        console.print("[red]Invalid choice. Please try again.[/red]")
        return get_format_choice()

    return format_map[choice]


def download_video(url, file_format):
    console.print(f"\n[cyan]Downloading in format: {file_format}[/cyan]")
    ffmpeg_location = get_ffmpeg_path()

    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
    }

    if file_format == "audio":
        ydl_opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
    elif file_format == "video":
        ydl_opts["format"] = "bestvideo+bestaudio/best"
    else:  # best
        ydl_opts["format"] = "best"

    if ffmpeg_location:
        ydl_opts["ffmpeg_location"] = ffmpeg_location

    try:
        console.print(f"[blue]Fetching resource info...[/blue]")
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            console.print(f"[green]✅ Download completed: {info['title']}[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")


def main():
    welcome()
    url = get_input()
    file_format = get_format_choice()
    download_video(url, file_format)


if __name__ == "__main__":
    main()
