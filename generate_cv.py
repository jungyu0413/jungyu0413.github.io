#!/usr/bin/env python3
"""Generate JunGyu Lee CV PDF from homepage content."""

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "JunGyu_Lee_CV.pdf"

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
ACCENT = (9, 105, 218)  # homepage link blue
ME = "JunGyu Lee"  # bolded wherever it appears in an author list


class CV(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.left = 18
        self.right = 192
        self.content_w = self.right - self.left
        self.set_margins(self.left, 14, 210 - self.right)
        self.set_auto_page_break(auto=True, margin=13)
        self.add_font("cv", "", FONT_DIR / "Arial.ttf")
        self.add_font("cv", "B", FONT_DIR / "Arial Bold.ttf")
        self.add_font("cv", "I", FONT_DIR / "Arial Italic.ttf")
        self.add_font("cv", "BI", FONT_DIR / "Arial Bold Italic.ttf")

    def set_body(self, size=10):
        self.set_font("cv", "", size)

    def set_bold(self, size=10):
        self.set_font("cv", "B", size)

    def line_text(self, w, h, text, **kwargs):
        """multi_cell that always returns to the left margin and never justifies."""
        self.multi_cell(w, h, text, align="L", new_x="LMARGIN", new_y="NEXT", **kwargs)

    def section_title(self, title: str):
        self.ln(2)
        self.set_bold(11)
        self.set_text_color(35, 45, 60)
        self.cell(0, 7, title.upper(), new_x="LMARGIN", new_y="NEXT")
        y = self.get_y()
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.6)
        self.line(self.left, y, self.left + 34, y)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def body_text(self, text: str, size=10, bold=False):
        self.set_font("cv", "B" if bold else "", size)
        self.line_text(self.content_w, 4.8, text)

    def bullet_item(self, title: str, subtitle: str = "", meta: str = ""):
        self.set_bold(10)
        self.line_text(self.content_w, 4.8, f"• {title}")
        if subtitle:
            self.set_body(9.5)
            self.set_x(self.left + 3)
            self.set_text_color(90, 93, 105)
            self.line_text(self.content_w - 3, 4.5, subtitle)
            self.set_text_color(0, 0, 0)
        if meta:
            self.set_body(9)
            self.set_x(self.left + 3)
            self.set_text_color(120, 123, 135)
            self.line_text(self.content_w - 3, 4.2, meta)
            self.set_text_color(0, 0, 0)
        self.ln(1)

    def media_item(self, title: str, source: str, label: str, url: str):
        """Title on one line, then the outlet/date and a clickable label on the next."""
        self.set_bold(10)
        self.line_text(self.content_w, 4.8, f"• {title}")
        self.set_x(self.left + 3)
        self.set_body(9.5)
        self.set_text_color(90, 93, 105)
        self.write(4.5, f"{source}  ·  ")
        self.set_text_color(*ACCENT)
        self.write(4.5, label, link=url)
        self.set_text_color(0, 0, 0)
        self.ln(4.5)
        self.ln(1)

    def link_row(self, links, size=9, h=4.2, sep="  ·  "):
        """Short clickable labels instead of printing full URLs."""
        self.set_body(size)
        for i, (label, url) in enumerate(links):
            if i:
                self.set_text_color(120, 123, 135)
                self.write(h, sep)
            self.set_text_color(*ACCENT)
            self.write(h, label, link=url)
        self.set_text_color(0, 0, 0)
        self.ln(h)

    def year_heading(self, label: str):
        self.set_bold(10)
        self.cell(0, 5, label, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def authors_line(self, authors: str, size=9.5, h=4.5):
        for i, part in enumerate(authors.split(ME)):
            if i:
                self.set_bold(size)
                self.write(h, ME)
            self.set_body(size)
            self.write(h, part)
        self.ln(h)

    def publication(self, authors: str, title: str, venue: str, links=()):
        self.authors_line(authors)
        self.set_bold(10)
        self.line_text(self.content_w, 4.8, title)
        self.set_body(9.5)
        self.set_text_color(90, 93, 105)
        self.line_text(self.content_w, 4.5, venue)
        self.set_text_color(0, 0, 0)
        if links:
            self.link_row(links)
        self.ln(1.2)


def build_cv() -> CV:
    pdf = CV()
    pdf.add_page()

    # Header
    pdf.set_bold(22)
    pdf.cell(0, 10, "JunGyu Lee", new_x="LMARGIN", new_y="NEXT")
    pdf.set_body(11)
    pdf.set_text_color(90, 93, 105)
    pdf.cell(0, 6, "Ph.D. Student, Artificial Intelligence", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Graduate School of Artificial Intelligence, Yonsei University", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.link_row([
        ("jungyu.lee@yonsei.ac.kr", "mailto:jungyu.lee@yonsei.ac.kr"),
        ("jungyu0413.github.io", "https://jungyu0413.github.io/"),
        ("GitHub", "https://github.com/jungyu0413"),
        ("Google Scholar", "https://scholar.google.com/citations?user=fAaH1PIAAAAJ"),
        ("LinkedIn", "https://www.linkedin.com/in/jungyu-lee-0315sb/"),
    ], size=9.5, h=4.5, sep="   |   ")
    pdf.ln(2)

    # Research interests
    pdf.section_title("Research Interests")
    pdf.body_text(
        "Crowd Generation, Social Robot Navigation, World Models"
    )

    # Education
    pdf.section_title("Education")
    pdf.bullet_item(
        "Ph.D. in Engineering, Artificial Intelligence",
        "Yonsei University, Seoul, Korea",
        "Advisor: Prof. Hae-Gon Jeon · Visual AI Lab",
    )
    pdf.bullet_item(
        "M.S. in AI Robotics",
        "University of Science and Technology (UST), Korea Institute of Science and Technology (KIST) School",
        "Advisor: Prof. Gi Pyo Nam · Visual Intelligence Group (VIG)",
    )
    pdf.bullet_item(
        "B.S. in Big Data Analytics",
        "Kookmin University, Seoul, Korea",
    )

    # Experience
    pdf.section_title("Experience")
    pdf.bullet_item(
        "AI Researcher",
        "Seoul National University Hospital (SNUH)",
        "Jun 2025 – Nov 2025",
    )
    pdf.bullet_item(
        "AI Researcher",
        "Korea Institute of Science and Technology (KIST)",
        "Jan 2023 – Jun 2025",
    )
    pdf.bullet_item(
        "Research Internship",
        "Asan Medical Center (AMC)",
        "Aug 2021 – Nov 2021",
    )

    # Publications
    pdf.section_title("Publications")
    pdf.set_body(9)
    pdf.set_text_color(120, 123, 135)
    pdf.cell(0, 5, "* denotes equal contribution", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

    pdf.year_heading("Under Review")
    pdf.publication(
        "JunGyu Lee, Jisu Shin, Seunghyun Shin, Hae-Gon Jeon",
        "Controllable Crowd Generation through World-Model Planning",
        "arXiv preprint arXiv:2610.09438, 2026 (Under review)",
        [("Project", "https://jungyu0413.github.io/Ctrl-CWM/"), ("Paper", "https://arxiv.org/abs/2610.09438"), ("Code", "https://github.com/jungyu0413/Ctrl-CWM")],
    )
    pdf.publication(
        "JunGyu Lee, Inhwan Bae, Hae-Gon Jeon",
        "Revisiting Numerical Forecasting Models for Language-Based Trajectory Prediction",
        "arXiv preprint arXiv:2610.07954, 2026 (Under review)",
        [("Project", "https://jungyu0413.github.io/MoRE/"), ("Paper", "https://arxiv.org/abs/2610.07954"), ("Code", "https://github.com/jungyu0413/MoRE")],
    )
    pdf.publication(
        "Boa Jang*, JunGyu Lee*, Gwanho Lee, Jinwook Choi, Young-Gon Kim",
        "Skeleton-Guided Progressive Test-Time Adaptation for Thin Curvilinear Structures",
        "arXiv preprint arXiv:2610.11104, 2026 (Under review)",
        [("Project", "https://boa-jang.github.io/SGP-TTA/"), ("Paper", "https://arxiv.org/abs/2610.11104"), ("Code", "https://github.com/Boa-Jang/SGPTTA")],
    )

    pdf.year_heading("2026")
    pdf.publication(
        "Jisu Shin, Junoh Lee, JunGyu Lee, Inhwan Bae, Dohyeon Lee, Hokyun Im, "
        "Youngwoon Lee, Hae-Gon Jeon",
        "ComPose: When to Trust Hands for Object Pose Tracking",
        "NeurIPS 2026 — Conference on Neural Information Processing Systems (NeurIPS)",
        [("Project", "https://jsshin.com/ComPose/"), ("Paper", "https://arxiv.org/abs/2605.23523")],
    )
    pdf.publication(
        "Dong Yeong Kim*, JunGyu Lee*, Jaewon Choi, June Young Seo, Myeongseop Kim, "
        "Jinwook Choi, Taek Min Kim, Young-Gon Kim",
        "Distilling Temporal Coherence into 2D Networks for TRUS Prostate Video Segmentation",
        "MICCAI 2026 — Proceedings of the International Conference on Medical Image Computing "
        "and Computer-Assisted Intervention (MICCAI)",
        [("Project", "https://dydevelop.github.io/DTC-TRUS/"), ("Paper", "https://arxiv.org/abs/2606.31198"),
         ("Code", "https://github.com/DYDevelop/DTC-TRUS")],
    )
    pdf.publication(
        "Dong Yeong Kim, Jaewon Choi, Youmin Shin, JunGyu Lee, Myeongseop Kim, "
        "Jinwook Choi, Joo Whan Kim, Young-Gon Kim",
        "PSCT-Net: Geometry-Aware Pediatric Skull CT Reconstruction via Differentiable "
        "Back-Projection and Attention-Guided Refinement",
        "MICCAIW 2026 — Proceedings of the International Conference on Medical Image Computing "
        "and Computer-Assisted Intervention Workshop (MICCAIW)",
        [("Project", "https://dydevelop.github.io/PSCT-Net/"), ("Paper", "https://arxiv.org/abs/2606.19867"),
         ("Code", "https://github.com/DYDevelop/PSCT-Net")],
    )

    pdf.year_heading("2025")
    pdf.publication(
        "JunGyu Lee, Kunyoung Lee, Haesol Park, Ig-Jae Kim, Gi Pyo Nam",
        "V-NAW: Video-based Noise-aware Adaptive Weighting for Facial Expression Recognition",
        "CVPRW 2025 — Proceedings of the IEEE/CVF Conference on Computer Vision and "
        "Pattern Recognition Workshop (CVPRW)",
        [("Paper", "https://arxiv.org/abs/2503.15970"), ("Code", "https://github.com/jungyu0413/V-NAW")],
    )
    pdf.publication(
        "JunGyu Lee*, Yeji Choi*, Haksub Kim, Ig-Jae Kim, Gi Pyo Nam",
        "Navigating Label Ambiguity for Facial Expression Recognition in the Wild",
        "AAAI 2025 — Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)",
        [("Project", "https://jungyu0413.github.io/NLA/"), ("Paper", "https://arxiv.org/abs/2502.09993"), ("Code", "https://github.com/jungyu0413/NLA")],
    )

    pdf.year_heading("2024")
    pdf.publication(
        "JunGyu Lee, Sanghyun Alex Lee, Gi Pyo Nam",
        "Study on Facial Composite Feature Analysis for Determining Subject Anxiety Levels "
        "on Low-Power Computing Modules",
        "IEIE 2024 — Summer Annual Conference of IEIE",
        [("Project", "https://jungyu0413.github.io/Eye_Blink_Detection/"), ("Paper", "https://www.dbpia.co.kr/Journal/articleDetail?nodeId=NODE11890880"), ("Code", "https://github.com/jungyu0413/Eye_Blink_Detection")],
    )

    # Awards
    pdf.section_title("Honors & Awards")
    pdf.bullet_item(
        "Top 5 Placement, 8th ABAW Competition @ CVPR Workshop",
        meta="2025",
    )
    pdf.bullet_item(
        "Best Paper Award, KIST Convergence Conference",
        subtitle="Korea Institute of Science and Technology (KIST)",
        meta="2024",
    )
    pdf.bullet_item(
        "Outstanding Technology Award, AI-Robotics Research Division",
        subtitle="Korea Institute of Science and Technology (KIST)",
        meta="2024",
    )

    # Selected projects
    pdf.section_title("Selected Projects")
    pdf.bullet_item(
        "Expression Recognition App",
        "PyQt-based facial expression recognition from images, videos, or real-time webcam",
        "Python · PyQt",
    )
    pdf.bullet_item(
        "Realtime FER / VA Estimation / Eye Blink Detection / Face Detector",
        "Real-time facial analysis pipelines for expression, affect, and behavioral monitoring",
        "Python · Real-time · Embedded Systems",
    )

    # Media
    pdf.section_title("Media")
    pdf.media_item(
        "AI, Reading Inner Feelings",
        "Chosun Ilbo · Jul 2023",
        "Article", "https://www.chosun.com/economy/science/2023/07/27/CTQOEOWBRRFHBKFVO7P34P5QGM/",
    )
    pdf.media_item(
        "On-site Verification: Drugs, from Inflow to Distribution — Can They Be Stopped?",
        "MBC Newsdesk · May 2023",
        "Video", "https://www.youtube.com/watch?v=v42dA6POA84&t=144s",
    )
    pdf.media_item(
        "Customs' Cutting-Edge Detection Technology on the Front Line of the 'War on Drugs'",
        "JTBC News (D:Issue) · Apr 2023",
        "Video", "https://www.youtube.com/watch?v=Ey1pFt8AXhQ&t=31s",
    )

    return pdf


def main():
    pdf = build_cv()
    pdf.output(str(OUTPUT))
    print(f"Generated: {OUTPUT}")


if __name__ == "__main__":
    main()
