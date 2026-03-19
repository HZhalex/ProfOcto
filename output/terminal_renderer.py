from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.table import Table
from rich import box
from debate.session import ProfessorProfile, Turn

console = Console()

PROFESSOR_COLORS = ["cyan", "green", "yellow", "magenta", "blue"]
MODERATOR_COLOR = "bright_white"

STATUS_COLORS = {
    "VERIFIED":   ("✓", "green"),
    "UNVERIFIED": ("?", "yellow"),
    "CONTESTED":  ("✗", "red"),
    "OPINION":    ("◈", "dim white"),
}

_color_map: dict[str, str] = {}


def _get_color(prof_key: str, professors: list) -> str:
    if prof_key not in _color_map:
        idx = len(_color_map) % len(PROFESSOR_COLORS)
        _color_map[prof_key] = PROFESSOR_COLORS[idx]
    return _color_map[prof_key]


def print_header(topic: str, field: str):
    console.print()
    console.print(Rule(f"[bold]🐙 ProfOcto[/bold]", style="bright_blue"))
    console.print(f"[dim]Field:[/dim] {field}")
    console.print(f"[bold]Topic:[/bold] {topic}")
    console.print()


def print_professors_table(professors: list[ProfessorProfile]):
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim")
    table.add_column("Professor", style="bold")
    table.add_column("University", style="dim")
    table.add_column("Role")
    table.add_column("Stance", style="italic")

    for i, p in enumerate(professors):
        color = PROFESSOR_COLORS[i % len(PROFESSOR_COLORS)]
        table.add_row(
            f"[{color}]{p.name}[/{color}]",
            p.university,
            p.role,
            p.stance[:60] + "..." if len(p.stance) > 60 else p.stance,
        )

    console.print(table)
    console.print()


def print_round_header(round_num: int):
    console.print(Rule(f"[bold yellow]Round {round_num}[/bold yellow]", style="yellow"))
    console.print()


def print_moderator_turn(content: str, turn_num: int, label: str = "Moderator"):
    panel = Panel(
        Text(content, style="white"),
        title=f"[bold bright_white]🎯 {label}[/bold bright_white]",
        subtitle=f"[dim]Turn {turn_num}[/dim]",
        border_style="bright_blue",
        padding=(0, 2),
    )
    console.print(panel)
    console.print()


def print_professor_header(prof: ProfessorProfile, turn_num: int, professors: list):
    color = _get_color(prof.key, professors)
    console.print(
        f"[bold {color}]{prof.name}[/bold {color}]"
        f"[dim] — {prof.role} | Turn {turn_num}[/dim]"
    )


def print_streaming_start():
    """Called before streaming professor's response text."""
    pass


def print_fact_tags(fact_tags: list[dict]):
    if not fact_tags:
        return
    console.print()
    for ft in fact_tags:
        status = ft.get("status", "OPINION").upper()
        symbol, color = STATUS_COLORS.get(status, ("?", "white"))

        # Dòng chính: tag + claim
        console.print(
            f"  [{color}]{symbol} {status}[/{color}]"
            f"[dim] — {ft.get('claim', '')}[/dim]"
        )

        # Reason (if available - from web search)
        reason = ft.get("reason", "")
        if reason:
            console.print(f"    [dim italic]{reason}[/dim italic]")

        # Nguồn web (nếu có)
        sources = ft.get("sources", [])
        for src in sources:
            console.print(f"    [dim blue]↳ {src}[/dim blue]")


def print_turn(turn: Turn, professors: list):
    if turn.is_moderator:
        print_moderator_turn(turn.content, turn.turn_number)
        return

    prof = next((p for p in professors if p.key == turn.speaker_key), None)
    if prof:
        color = _get_color(prof.key, professors)
        header = (
            f"[bold {color}]{prof.name}[/bold {color}]"
            f"[dim] — {prof.role} | Turn {turn.turn_number}[/dim]"
        )
        panel = Panel(
            Text(turn.content),
            title=header,
            border_style=color,
            padding=(0, 2),
        )
        console.print(panel)
        print_fact_tags(turn.fact_tags)
        console.print()


def print_final_summary(content: str):
    console.print(Rule("[bold green]Key Insights[/bold green]", style="green"))
    console.print()
    console.print(content)
    console.print()


def print_saved(filename: str):
    console.print(f"[dim]Transcript saved → [underline]{filename}[/underline][/dim]")
    console.print()


def stream_write(text: str):
    """Gọi trong stream callback để in text real-time."""
    console.print(text, end="", highlight=False)
