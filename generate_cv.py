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
        self.set_margins(self.left, 16, 210 - self.right)
        self.set_auto_page_break(auto=True, margin=18)
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
        self.ln(3)
        self.set_bold(11)
        self.set_text_color(35, 45, 60)
        self.cell(0, 7, title.upper(), new_x="LMARGIN", new_y="NEXT")
        y = self.get_y()
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.6)
        self.line(self.left, y, self.left + 34, y)
        self.ln(4)
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

    def contact_lines(self, items, size=9.5, sep="   |   "):
        """Pack contact items into as few lines as fit the content width."""
        self.set_body(size)
        max_w = self.content_w - 2 * self.c_margin  # multi_cell pads both sides
        lines, current = [], ""
        for item in items:
            candidate = f"{current}{sep}{item}" if current else item
            if current and self.get_string_width(candidate) > max_w:
                lines.append(current)
                candidate = item
            current = candidate
        lines.append(current)
        for line in lines:
            self.line_text(self.content_w, 4.5, line)

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

    def publication(self, authors: str, title: str, venue: str, links: str = ""):
        self.authors_line(authors)
        self.set_bold(10)
        self.line_text(self.content_w, 4.8, title)
        self.set_body(9.5)
        self.set_text_color(90, 93, 105)
        self.line_text(self.content_w, 4.5, venue)
        if links:
            self.set_body(9)
            self.line_text(self.content_w, 4.2, links)
        self.set_text_color(0, 0, 0)
        self.ln(2)


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
    pdf.contact_lines([
        "Email: jungyu.lee@yonsei.ac.kr",
        "Web: jungyu0413.github.io",
        "GitHub: github.com/jungyu0413",
        "Google Scholar: scholar.google.com/citations?user=fAaH1PIAAAAJ",
        "LinkedIn: linkedin.com/in/jungyu-lee-0315sb",
    ])
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Research interests
    pdf.section_title("Research Interests")
    pdf.body_text(
        "Robotics, Crowd Generation, World Models, Facial Expression Recognition, "
        "Medical Image/Video Analysis, Human-Centric AI"
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
        "JunGyu Lee, Inhwan Bae, Hae-Gon Jeon",
        "Revisiting Numerical Forecasting Models for Language-Based Human Trajectory Prediction",
        "Under review",
        "Project: jungyu0413.github.io/MoRE/",
    )

    pdf.year_heading("2026")
    pdf.publication(
        "Jisu Shin, Junoh Lee, JunGyu Lee, Inhwan Bae, Dohyeon Lee, Hokyun Im, "
        "Youngwoon Lee, Hae-Gon Jeon",
        "ComPose: When to Trust Hands for Object Pose Tracking",
        "NeurIPS 2026 — Conference on Neural Information Processing Systems (NeurIPS)",
        "Project: jsshin.com/ComPose/   Paper: arxiv.org/abs/2605.23523",
    )
    pdf.publication(
        "Dong Yeong Kim*, JunGyu Lee*, Jaewon Choi, June Young Seo, Myeongseop Kim, "
        "Jinwook Choi, Taek Min Kim, Young-Gon Kim",
        "Distilling Temporal Coherence into 2D Networks for TRUS Prostate Video Segmentation",
        "MICCAI 2026 — Proceedings of the International Conference on Medical Image Computing "
        "and Computer-Assisted Intervention (MICCAI)",
        "Project: dydevelop.github.io/DTC-TRUS/   Paper: arxiv.org/abs/2606.31198   "
        "Code: github.com/DYDevelop/DTC-TRUS",
    )
    pdf.publication(
        "Dong Yeong Kim, Jaewon Choi, Youmin Shin, JunGyu Lee, Myeongseop Kim, "
        "Jinwook Choi, Joo Whan Kim, Young-Gon Kim",
        "PSCT-Net: Geometry-Aware Pediatric Skull CT Reconstruction via Differentiable "
        "Back-Projection and Attention-Guided Refinement",
        "MICCAIW 2026 — Proceedings of the International Conference on Medical Image Computing "
        "and Computer-Assisted Intervention Workshop (MICCAIW)",
        "Project: dydevelop.github.io/PSCT-Net/   Paper: arxiv.org/abs/2606.19867   "
        "Code: github.com/DYDevelop/PSCT-Net",
    )

    pdf.year_heading("2025")
    pdf.publication(
        "JunGyu Lee, Kunyoung Lee, Haesol Park, Ig-Jae Kim, Gi Pyo Nam",
        "V-NAW: Video-based Noise-aware Adaptive Weighting for Facial Expression Recognition",
        "CVPRW 2025 — Proceedings of the IEEE/CVF Conference on Computer Vision and "
        "Pattern Recognition Workshop (CVPRW)",
        "Paper: arxiv.org/abs/2503.15970   Code: github.com/jungyu0413/V-NAW",
    )
    pdf.publication(
        "JunGyu Lee*, Yeji Choi*, Haksub Kim, Ig-Jae Kim, Gi Pyo Nam",
        "Navigating Label Ambiguity for Facial Expression Recognition in the Wild",
        "AAAI 2025 — Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)",
        "Paper: arxiv.org/abs/2502.09993   Code: github.com/jungyu0413/NLA",
    )

    pdf.year_heading("2024")
    pdf.publication(
        "JunGyu Lee, Sanghyun Alex Lee, Gi Pyo Nam",
        "Study on Facial Composite Feature Analysis for Determining Subject Anxiety Levels "
        "on Low-Power Computing Modules",
        "IEIE 2024 — Summer Annual Conference of IEIE",
        "Paper: dbpia.co.kr/Journal/articleDetail?nodeId=NODE11890880",
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
    pdf.bullet_item(
        "AI, Reading Inner Feelings (Chosun Ilbo feature)",
        "Jul 2023",
    )

    return pdf


def main():
    pdf = build_cv()
    pdf.output(str(OUTPUT))
    print(f"Generated: {OUTPUT}")


if __name__ == "__main__":
    main()
