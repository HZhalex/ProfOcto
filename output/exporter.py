"""
Exporter — xuất transcript ra Markdown và PDF.
PDF dùng thư viện reportlab (optional, cài thêm nếu cần).
"""
import os
from datetime import datetime
from debate.session import DebateSession


def export_markdown(session: DebateSession, directory: str = "transcripts") -> str:
    """Export transcript ra file Markdown đẹp có formatting đầy đủ."""
    os.makedirs(directory, exist_ok=True)
    slug = session.topic[:40].replace(" ", "_").replace("/", "-")
    filename = f"{directory}/debate_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    STATUS_EMOJI = {
        "VERIFIED":   "✅",
        "UNVERIFIED": "⚠️",
        "CONTESTED":  "🔴",
        "OPINION":    "💭",
    }

    lines = [
        "# 🎓 Academic Debate Arena",
        "",
        f"**Topic:** {session.topic}",
        f"**Field:** {session.field}",
        f"**Date:** {session.started_at[:19].replace('T', ' ')}",
        f"**Rounds:** {session.current_round} | **Turns:** {session.current_turn}",
        "",
        "---",
        "",
        "## 👥 Professors",
        "",
    ]

    for p in session.professors:
        lines += [
            f"### {p.name}",
            f"- **University:** {p.university}",
            f"- **Role:** {p.role}",
            f"- **Expertise:** {p.expertise}",
            f"- **Stance:** {p.stance}",
            "",
        ]

    lines += ["---", "", "## 💬 Debate Transcript", ""]

    for t in session.turns:
        if t.is_moderator:
            lines += [
                f"### 🎯 Moderator — Turn {t.turn_number}",
                "",
                f"> {t.content}",
                "",
            ]
        else:
            lines += [
                f"### {t.speaker_name} `{t.role}` — Turn {t.turn_number}",
                "",
                t.content,
                "",
            ]
            if t.fact_tags:
                lines.append("**Fact Check:**")
                for ft in t.fact_tags:
                    emoji = STATUS_EMOJI.get(ft["status"].upper(), "❓")
                    reason = f" — {ft['reason']}" if ft.get("reason") else ""
                    lines.append(f"- {emoji} `{ft['status'].upper()}` {ft['claim']}{reason}")
                    for src in ft.get("sources", []):
                        lines.append(f"  - 🔗 {src}")
                lines.append("")

    # Thêm stats cuối file
    lines += [
        "---",
        "",
        "## 📊 Stats",
        "",
    ]
    counts: dict[str, int] = {}
    for t in session.turns:
        if not t.is_moderator:
            counts[t.speaker_name] = counts.get(t.speaker_name, 0) + 1
    for name, count in counts.items():
        lines.append(f"- **{name}:** {count} turns")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filename


def export_pdf(session: DebateSession, directory: str = "transcripts") -> str:
    """
    Export transcript ra PDF.
    Yêu cầu: pip install reportlab
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
    except ImportError:
        raise ImportError(
            "reportlab chưa được cài. Chạy: pip install reportlab"
        )

    os.makedirs(directory, exist_ok=True)
    slug = session.topic[:40].replace(" ", "_").replace("/", "-")
    filename = f"{directory}/debate_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    style_title   = ParagraphStyle('Title2', parent=styles['Title'], fontSize=18, spaceAfter=6)
    style_h2      = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#4a4f6a'))
    style_h3      = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11, textColor=colors.HexColor('#333'))
    style_body    = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=15)
    style_mod     = ParagraphStyle('Mod', parent=styles['Normal'], fontSize=10,
                                   leading=14, leftIndent=12,
                                   borderPad=6, backColor=colors.HexColor('#f0f0ff'))
    style_meta    = ParagraphStyle('Meta', parent=styles['Normal'], fontSize=9,
                                   textColor=colors.gray)
    style_fact    = ParagraphStyle('Fact', parent=styles['Normal'], fontSize=9,
                                   textColor=colors.HexColor('#555'), leftIndent=16)

    story = []

    # Header
    story.append(Paragraph("🎓 Academic Debate Arena", style_title))
    story.append(Paragraph(f"<b>Topic:</b> {session.topic}", style_body))
    story.append(Paragraph(f"<b>Field:</b> {session.field} | <b>Date:</b> {session.started_at[:10]}", style_meta))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 0.3*cm))

    # Professors
    story.append(Paragraph("Professors", style_h2))
    for p in session.professors:
        story.append(Paragraph(f"<b>{p.name}</b> — {p.university} | {p.role}", style_body))
        story.append(Paragraph(f"Stance: {p.stance}", style_meta))
        story.append(Spacer(1, 0.2*cm))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#dddddd')))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Debate Transcript", style_h2))
    story.append(Spacer(1, 0.2*cm))

    # Turns
    for t in session.turns:
        if t.is_moderator:
            story.append(Paragraph(f"🎯 <b>Moderator</b> — Turn {t.turn_number}", style_h3))
            story.append(Paragraph(t.content, style_mod))
        else:
            story.append(Paragraph(f"<b>{t.speaker_name}</b> [{t.role}] — Turn {t.turn_number}", style_h3))
            story.append(Paragraph(t.content, style_body))
            for ft in t.fact_tags or []:
                story.append(Paragraph(
                    f"[{ft['status']}] {ft['claim']}", style_fact
                ))
        story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    return filename
