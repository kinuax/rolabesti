from rich import print


class Logger:
    @staticmethod
    def log(msg: str) -> None:
        print(f"[green]├─[/green] {msg}")
