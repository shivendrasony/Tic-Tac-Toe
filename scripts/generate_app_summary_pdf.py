from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "classic-snake-app-summary.pdf"


def build_pdf() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch,
        title="Classic Snake App Summary",
        author="Codex",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=22,
        textColor=colors.HexColor("#17313E"),
        spaceAfter=8,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#17313E"),
        spaceAfter=4,
        spaceBefore=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=10.6,
        textColor=colors.HexColor("#1F2933"),
        spaceAfter=2,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-6,
        bulletIndent=0,
        spaceAfter=1,
    )
    note_style = ParagraphStyle(
        "Note",
        parent=body_style,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#5B6670"),
    )

    left_column = [
        Paragraph("Classic Snake", title_style),
        Paragraph("What It Is", section_style),
        Paragraph(
            "A lightweight browser implementation of the classic Snake arcade game, "
            "served by a minimal Node.js HTTP server. The UI presents a 16x16 game "
            "board, score display, game status text, restart control, and on-screen "
            "direction/pause buttons.",
            body_style,
        ),
        Paragraph("Who It's For", section_style),
        Paragraph(
            "Primary persona: <b>Not found in repo.</b> Inferred from the UI and controls: "
            "people who want a simple, no-login Snake game that works with keyboard input "
            "and touch/click controls.",
            body_style,
        ),
        Paragraph("What It Does", section_style),
        Paragraph("• Renders a 16x16 game grid in the browser.", bullet_style),
        Paragraph("• Starts movement from arrow keys, WASD, or touch/click controls.", bullet_style),
        Paragraph("• Tracks score and updates status text during play.", bullet_style),
        Paragraph("• Supports pause/resume via Space key or a Pause button.", bullet_style),
        Paragraph("• Lets players restart the game without reloading the page.", bullet_style),
        Paragraph("• Detects wall collisions and self-collisions as game-over states.", bullet_style),
        Paragraph("• Places food on unoccupied cells and grows the snake after eating.", bullet_style),
    ]

    right_column = [
        Paragraph("How It Works", section_style),
        Paragraph(
            "<b>Static server:</b> <font name='Courier'>server.js</font> uses Node's "
            "<font name='Courier'>http</font>, <font name='Courier'>fs</font>, and "
            "<font name='Courier'>path</font> modules to serve files from the repo root, "
            "mapping <font name='Courier'>/</font> to <font name='Courier'>index.html</font>.",
            body_style,
        ),
        Paragraph(
            "<b>Frontend shell:</b> <font name='Courier'>index.html</font> defines the panel, "
            "board container, score, status, restart action, and touch controls; "
            "<font name='Courier'>styles.css</font> supplies layout and visuals.",
            body_style,
        ),
        Paragraph(
            "<b>UI controller:</b> <font name='Courier'>src/game.js</font> builds the board DOM, "
            "binds keyboard/button events, runs a 140 ms game loop, and renders state to cells/text.",
            body_style,
        ),
        Paragraph(
            "<b>Game logic:</b> <font name='Courier'>src/snakeLogic.js</font> owns state creation, "
            "direction queuing, pause toggling, movement ticks, collision checks, scoring, "
            "and random food placement.",
            body_style,
        ),
        Paragraph(
            "<b>Tests:</b> <font name='Courier'>test/snakeLogic.test.js</font> verifies movement, "
            "growth, wall/self collisions, safe food placement, and reverse-direction prevention.",
            body_style,
        ),
        Paragraph(
            "<b>Data flow:</b> user input updates queued direction or pause state; the interval loop "
            "advances game state; render logic maps state to board cells, score text, and status text.",
            body_style,
        ),
        Paragraph("How To Run", section_style),
        Paragraph("1. In the repo root, run <font name='Courier'>npm install</font> if your environment needs dependencies.", body_style),
        Paragraph("2. Start the app with <font name='Courier'>npm run dev</font> or <font name='Courier'>npm start</font>.", body_style),
        Paragraph("3. Open <font name='Courier'>http://127.0.0.1:3000</font> in a browser.", body_style),
        Paragraph("4. Optional: run <font name='Courier'>npm test</font> to execute the Node test suite.", body_style),
        Spacer(1, 4),
        Paragraph(
            "Repo notes: dependency installation details beyond the built-in Node runtime are "
            "<b>Not found in repo</b>; there is no README or deployment documentation present.",
            note_style,
        ),
    ]

    table = Table(
        [[left_column, right_column]],
        colWidths=[3.45 * inch, 3.45 * inch],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFDF8")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#C9D3DA")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D9E1E6")),
            ]
        )
    )

    doc.build([table])


if __name__ == "__main__":
    build_pdf()
