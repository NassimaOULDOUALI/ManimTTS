"""
SSML Prosody Control for French TTS — ICNLSP 2025 Presentation
================================================================
Refactored Manim animation (target: 9 minutes)

Authors: Nassima Ould Ouali, Awais Hussain Sani, Ruben Bueno,
         Jonah Dauvet, Tim Luka Horstmann, Eric Moulines
Ref: https://aclanthology.org/2025.icnlsp-1.30/

TIMING SCRIPT - TARGET: 9min (540s)
====================================
SCENE 0: Introduction                                    0s   –  40s   (~40s)
SCENE 1: Audio Basics (waveform, spectrogram, F0)      40s  –  95s   (~55s)
SCENE 1bis: Prosody Primer                              95s  – 150s   (~55s)
SCENE 2A: TTS Expressivity Problem                     150s – 210s   (~60s)
SCENE 2B: SSML Challenges                              210s – 260s   (~50s)
SCENE 3A: Pipeline Interactive                         260s – 310s   (~50s)
SCENE 3B: Pipeline Diagram (Manim)                     310s – 350s   (~40s)
SCENE 4: Stage 1 – Break Prediction (QwenA)            350s – 400s   (~50s)
SCENE 5: Stage 2 – Prosody Prediction (QwenB)          400s – 450s   (~50s)
SCENE 6: Objective Evaluation                          450s – 490s   (~40s)
SCENE 7: Subjective Evaluation (AB Test)               490s – 530s   (~40s)
SCENE 8: Conclusions & Future Work                     530s – 560s   (~30s)
"""

from manim import *
import numpy as np
from pathlib import Path

# ============================================================================
# CONFIGURATION & THEME
# ============================================================================
config.text_backend = "pango"
config.disable_latex = False  # on garde LaTeX dispo pour les formules

BG_COLOR      = "#004178"
ACCENT_BLUE   = "#004178"
ACCENT_YELLOW = "#FF0049"
TEXT_COLOR    = "#F4F6FA"
ACCENT_PURPLE = "#FF0049"
ACCENT_CYAN   = "#14B8FF"
HI_GREY       = "#EFEFEF"

config.background_color = BG_COLOR
np.random.seed(7)

FONT_SANS = "DejaVu Sans"

# ============================================================================
# UTILITIES
# ============================================================================

ASSETS_DIR = Path(__file__).parent / "assets"

def load_img(stem: str, exts=(".png", ".jpg", ".jpeg", ".gif", ".ico")) -> ImageMobject:
    """Charge une image depuis assets/ avec fallback."""
    for ext in exts:
        p = ASSETS_DIR / f"{stem}{ext}"
        if p.exists():
            return ImageMobject(str(p))
    raise FileNotFoundError(f"Image introuvable pour '{stem}' dans assets/ ({exts})")


def T(s, **kw):
    """Wrapper Text : force la même police partout."""
    kw.setdefault("font", FONT_SANS)
    return Text(s, **kw)


def under_title(txt: str, color=ACCENT_BLUE, font_size=46, font: str = FONT_SANS):
    """Titre avec soulignement courbe (sans rectangle)."""
    t = Text(txt, font=font, weight=BOLD, font_size=font_size, color=color)
    underline = Line(
        t.get_bottom() + DOWN*0.06 + LEFT*0.1,
        t.get_bottom() + DOWN*0.06 + RIGHT*0.1,
        stroke_width=3
    ).set_color(color)
    return VGroup(t, underline).arrange(DOWN, buff=0.08)


def step_box(title: str, lines: list[str], color=ACCENT_BLUE, title_size=28, body_size=20):
    """Boîte arrondie pour un step de pipeline ou architecture."""
    head = T(title, font_size=title_size, color=color, weight=BOLD)
    body = VGroup(*[
        T(line, font_size=body_size, color=TEXT_COLOR)
        for line in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
    content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    rect = RoundedRectangle(corner_radius=0.20, stroke_color=color, stroke_width=3)
    rect.surround(content, buff=0.25)
    return VGroup(rect, content)


# ============================================================================
# SCENE 0: Introduction (~28–30 s, sans padding)
# ============================================================================
class SceneIntro(Scene):
    def construct(self):
        # --- Titre sans ombre ni fond noir ---
        title = T(
            "Improving French Synthetic Speech Quality\nvia SSML Prosody Control",
            font_size=44,
            color=ACCENT_YELLOW,   # ton rouge Hi! PARIS
            weight=BOLD,
        )
        title.scale_to_fit_width(min(config.frame_width * 0.9, title.width))
        title.to_edge(UP, buff=0.55)
        # ⛔ On supprime ceci :
        # title.set_stroke(BLACK, width=2.2, opacity=0.75)
        # title.add_background_rectangle(color=BLACK, opacity=0.18, buff=0.12)
        title.set_z_index(10)

        # Titre un peu plus lent
        self.play(Write(title), run_time=2.5)
        self.wait(1.5)

        # --- Auteurs (plus lent) ---
        authors_text = [
            "Nassima Ould Ouali, Awais Hussain Sani, Ruben Bueno,",
            "Jonah Dauvet, Tim Luka Horstmann, Eric Moulines",
        ]
        authors_lines = VGroup(*[
            T(line, font_size=26, color=TEXT_COLOR)
            for line in authors_text
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        authors_lines.next_to(title, DOWN, buff=0.55).set_z_index(9)

        self.play(
            LaggedStart(
                *[FadeIn(line, shift=UP * 0.1) for line in authors_lines],
                lag_ratio=0.45,
            ),
            run_time=4.0,  # apparition plus lente des deux lignes
        )
        self.wait(1.5)

        # --- Affiliations (plus basses + plus lente) ---
        affiliations = T(
            "École Polytechnique, Hi! PARIS Research Center, McGill University",
            font_size=22,
            color=HI_GREY,
            slant=ITALIC,
        )
        # on les "baisse" en augmentant le buff
        affiliations.next_to(authors_lines, DOWN, buff=0.9).set_z_index(9)

        self.play(FadeIn(affiliations, shift=UP * 0.1), run_time=3.0)
        self.wait(1.5)

        # --- Conférence (plus lente, laisse le temps de lire) ---
        conference = T(
            "ICNLSP 2025",
            font_size=28,
            color=ACCENT_YELLOW,   # bleu Hi! PARIS
            weight=BOLD,
        ).next_to(affiliations, DOWN, buff=0.5).set_z_index(9)

        self.play(FadeIn(conference, shift=UP * 0.1), run_time=3.0)
        self.wait(3.0)

        # --- Petit effet sur le titre ---
        self.play(Flash(title, flash_radius=0.32), run_time=1.2)
        self.wait(2.0)

        # --- Sortie sans padding artificiel ---
        self.play(
            LaggedStart(
                FadeOut(conference),
                FadeOut(affiliations),
                *[FadeOut(l) for l in authors_lines],
                lag_ratio=0.12,
            ),
            run_time=2.5,
        )
        self.play(FadeOut(title), run_time=2.0)



# ============================================================================
# SCENE 1: Audio Basics (~40 s, sans padding)
# ============================================================================
class SceneBasics(Scene):
    """
    Waveform → Spectrogram → Pitch/F0
    Même style que SceneIntro (T = DejaVu Sans, palette Hi! PARIS).
    """
    def construct(self):
        # --- Titre principal ---
        title = T(
            "Audio Signal Basics",
            font_size=48,
            color=ACCENT_YELLOW,   # bleu Hi! PARIS
            weight=BOLD,
        ).to_edge(UP, buff=0.5)

        self.play(Write(title), run_time=2.0)
        self.wait(1.0)

        # =====================================================================
        # 1) WAVEFORM
        # =====================================================================
        waveform_title = T(
            "Waveform: Amplitude vs Time",
            font_size=32,
            color=ACCENT_YELLOW,   # rouge Hi! PARIS pour les sous-titres
            weight=BOLD,
        ).next_to(title, DOWN, buff=0.6)

        self.play(Write(waveform_title), run_time=1.2)

        wf = load_img("waveform").scale(1.0)
        if wf.width > config.frame_width * 1.05:
            wf.width = config.frame_width * 1.05
        wf.shift(DOWN * 0.3)

        wf_desc = T(
            "Loudness ≈ RMS amplitude (average energy)\n"
            "Temporal variation of the audio signal.",
            font_size=22,
            color=TEXT_COLOR,
            line_spacing=1.0,
        ).next_to(wf, DOWN, buff=0.4)

        wf_cite = T(
            "Databootcamp TTS Course",
            font_size=16,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(wf, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(wf_desc), FadeIn(wf_cite), run_time=0.8)
        self.wait(5.0)

        self.play(
            FadeOut(waveform_title),
            FadeOut(wf),
            FadeOut(wf_desc),
            FadeOut(wf_cite),
            run_time=0.8,
        )
        self.wait(0.3)

        # =====================================================================
        # 2) SPECTROGRAM
        # =====================================================================
        spect_title = T(
            "Spectrogram: Frequency Energy over Time",
            font_size=32,
            color=ACCENT_YELLOW,
            weight=BOLD,
        ).next_to(title, DOWN, buff=0.6)

        self.play(Write(spect_title), run_time=1.2)

        sp = load_img("spectrogramme").scale(0.7)
        if sp.width > config.frame_width * 1.05:
            sp.width = config.frame_width * 1.05
        sp.shift(DOWN * 0.2)

        sp_desc = T(
            "Short-Time Fourier Transform (STFT):\n"
            "• Window: 20–30 ms, Hop: ≈10 ms, Hann window\n"
            "• FFT: decomposes the signal into frequency bands\n"
            "→ Time–frequency representation of speech.",
            font_size=20,
            color=TEXT_COLOR,
            line_spacing=1.1,
        ).next_to(sp, DOWN, buff=0.35)

        sp_cite = T(
            "Databootcamp TTS Course",
            font_size=16,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(sp, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(sp_desc), FadeIn(sp_cite), run_time=0.8)
        self.wait(7.0)

        self.play(
            FadeOut(spect_title),
            FadeOut(sp),
            FadeOut(sp_desc),
            FadeOut(sp_cite),
            run_time=0.8,
        )
        self.wait(0.3)

        # =====================================================================
        # 3) PITCH / F0
        # =====================================================================
        pitch_title = T(
            "Pitch & Fundamental Frequency (F0)",
            font_size=32,
            color=ACCENT_YELLOW,
            weight=BOLD,
        ).next_to(title, DOWN, buff=0.6)

        self.play(Write(pitch_title), run_time=1.2)

        f0img = load_img("f0").scale(1.0)
        if f0img.width > config.frame_width * 1.05:
            f0img.width = config.frame_width * 1.05
        f0img.shift(DOWN * 0.2)

        pitch_desc = VGroup(
            T(
                "Perceived pitch ↔ F0 (fundamental frequency)",
                font_size=26,
                color=TEXT_COLOR,
            ),
            T(
                "Typical extraction: pyworld, Praat, with outlier post-processing",
                font_size=22,
                color=HI_GREY,
                slant=ITALIC,
            ),
        ).arrange(DOWN, buff=0.25).next_to(f0img, DOWN, buff=0.45)

        pitch_cite = T(
            "Databootcamp TTS Course",
            font_size=16,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(f0img, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(pitch_desc), FadeIn(pitch_cite), run_time=0.8)
        self.wait(8.0)

        self.play(
            FadeOut(title),
            FadeOut(pitch_title),
            FadeOut(f0img),
            FadeOut(pitch_desc),
            FadeOut(pitch_cite),
            run_time=1.2,
        )
        self.wait(0.3)


# ============================================================================
# SCENE 1bis: Prosody Primer (SSML example + 4 paramètres, 2 "pages")
# ============================================================================
class SceneProsodyPrimer(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # SLIDE 1 : Prosody & SSML + exemple de code
        # ------------------------------------------------------------------
        title_text = T(
            "Prosody & SSML",
            font_size=44,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        underline = Line(
            title_text.get_bottom() + DOWN * 0.06 + LEFT * 0.1,
            title_text.get_bottom() + DOWN * 0.06 + RIGHT * 0.1,
            stroke_width=3,
        ).set_color(ACCENT_BLUE)

        title = VGroup(title_text, underline).arrange(DOWN, buff=0.08)
        title.to_edge(UP, buff=0.6)

        subtitle = T(
            "SSML example and prosodic controls",
            font_size=22,
            color=HI_GREY,
        ).next_to(title, DOWN, buff=0.25)

        self.play(
            FadeIn(title, shift=DOWN * 0.2),
            FadeIn(subtitle, shift=DOWN * 0.2),
            run_time=2.0,
        )
        self.wait(1.0)

        # -- Label à gauche
        ssml_label = T(
            "SSML example",
            font_size=28,
            color=ACCENT_YELLOW,
            weight=BOLD,
        ).next_to(subtitle, DOWN, buff=0.5)

        # -- Code SSML (monospace)
        line1 = Text(
            "<speak>",
            font="DejaVu Sans Mono",
            font_size=24,
            color=HI_GREY,
        )
        line2 = Text(
            '  Bonjour, <break time="250ms"/> je m\'appelle Alice.',
            font="DejaVu Sans Mono",
            font_size=24,
            color=HI_GREY,
        )
        line3 = Text(
            '  <prosody rate="slow" pitch="+5%">Je vous souhaite la bienvenue !</prosody>',
            font="DejaVu Sans Mono",
            font_size=24,
            color=HI_GREY,
        )
        line4 = Text(
            "</speak>",
            font="DejaVu Sans Mono",
            font_size=24,
            color=HI_GREY,
        )

        code_group = VGroup(line1, line2, line3, line4).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12
        )
        code_group.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        self.play(FadeIn(ssml_label, shift=DOWN * 0.1), run_time=0.9)
        self.play(
            LaggedStart(
                *[FadeIn(l, shift=RIGHT * 0.1) for l in code_group],
                lag_ratio=0.22,
            ),
            run_time=3.0,
        )
        self.wait(1.5)  # temps pour lire le code complet

        # -- Focus 1 : <break time="250ms"/>
        br_rect = SurroundingRectangle(
            line2,
            color=ACCENT_YELLOW,
            buff=0.18,
            stroke_width=3,
        )
        br_caption = T(
            '<break time="250ms"/> → explicit pause between syntagms.',
            font_size=22,
            color=TEXT_COLOR,
        ).next_to(code_group, DOWN, buff=0.55).align_to(code_group, LEFT)

        self.play(Create(br_rect), run_time=0.8)
        self.play(FadeIn(br_caption, shift=UP * 0.1), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(br_rect), run_time=0.5)

        # -- Focus 2 : <prosody rate="slow" pitch="+5%">
        pr_rect = SurroundingRectangle(
            line3,
            color=ACCENT_CYAN,
            buff=0.18,
            stroke_width=3,
        )
        pr_caption = T(
            '<prosody rate="slow" pitch="+5%"> → local control of tempo & pitch.',
            font_size=22,
            color=TEXT_COLOR,
        ).next_to(br_caption, DOWN, buff=0.30).align_to(code_group, LEFT)

        self.play(Create(pr_rect), run_time=0.8)
        self.play(FadeIn(pr_caption, shift=UP * 0.1), run_time=0.9)
        self.wait(2.5)

        # -- Légende colorée en bas
        def legend_item(label: str, color):
            dot = Dot(radius=0.06, color=color)
            txt = T(label, font_size=18, color=HI_GREY)
            return VGroup(dot, txt).arrange(RIGHT, buff=0.15)

        legend = VGroup(
            legend_item("Pitch (F0)", ACCENT_YELLOW),
            legend_item("Volume", ACCENT_YELLOW),
            legend_item("Rate", ACCENT_YELLOW),
            legend_item("Breaks", ACCENT_YELLOW),
        ).arrange(RIGHT, buff=0.7)
        legend.to_edge(DOWN, buff=0.6)

        self.play(FadeIn(legend, shift=UP * 0.1), run_time=0.9)
        self.wait(1.8)

        # ------------------------------------------------------------------
        # CLEAR PAGE : on efface tout le premier slide
        # ------------------------------------------------------------------
        self.play(
            FadeOut(legend),
            FadeOut(br_caption),
            FadeOut(pr_caption),
            FadeOut(pr_rect),
            FadeOut(ssml_label),
            FadeOut(code_group),
            FadeOut(subtitle),
            FadeOut(title),
            run_time=1.4,
        )
        self.wait(0.2)

        # ------------------------------------------------------------------
        # SLIDE 2 : "How SSML controls prosody" + définitions des 4 paramètres
        # ------------------------------------------------------------------
        big_title_text = T(
            "How SSML controls prosody ?",
            font_size=44,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        big_underline = Line(
            big_title_text.get_bottom() + DOWN * 0.06 + LEFT * 0.1,
            big_title_text.get_bottom() + DOWN * 0.06 + RIGHT * 0.1,
            stroke_width=3,
        ).set_color(ACCENT_BLUE)

        big_title = VGroup(big_title_text, big_underline).arrange(DOWN, buff=0.08)
        big_title.to_edge(UP, buff=0.7)

        self.play(FadeIn(big_title, shift=DOWN * 0.2), run_time=1.6)
        self.wait(0.8)

        params_data = [
            ("Pitch (F0)", ACCENT_YELLOW,
             "Perceived height of the voice.",
             "Intonation, questions, emphasis."),
            ("Volume (Loudness)", ACCENT_YELLOW,
             "Perceived intensity of speech.",
             "Prominence, emotional strength."),
            ("Rate (Tempo)", ACCENT_YELLOW,
             "Speed of articulation.",
             "Urgency vs clarity, rhythm."),
            ("Breaks (Pauses)", ACCENT_YELLOW,
             "Short silences between phrases.",
             "Structure, emphasis, comprehension."),
        ]

        cards = []
        for label, color, l1, l2 in params_data:
            head = T(label, font_size=26, color=color, weight=BOLD)
            line_a = T(l1, font_size=22, color=TEXT_COLOR)
            line_b = T(l2, font_size=20, color=HI_GREY)
            card = VGroup(head, line_a, line_b).arrange(
                DOWN, aligned_edge=LEFT, buff=0.16
            )
            cards.append(card)

        # ORGANISATION EN 2 COLONNES
        left_column = VGroup(cards[0], cards[1]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        right_column = VGroup(cards[2], cards[3]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)

        # Positionner les colonnes côte à côte
        columns_group = VGroup(left_column, right_column).arrange(RIGHT, buff=1.5, aligned_edge=UP)
        columns_group.next_to(big_title, DOWN, buff=0.8)

        # Apparition interactive : première colonne puis deuxième colonne
        self.play(
            LaggedStartMap(FadeIn, left_column, shift=RIGHT * 0.2, lag_ratio=0.4),
            run_time=1.5
        )
        self.wait(0.3)

        self.play(
            LaggedStartMap(FadeIn, right_column, shift=LEFT * 0.2, lag_ratio=0.4),
            run_time=1.5
        )

        # Indicate chaque élément
        for card in cards:
            self.play(Indicate(card[0], scale_factor=1.03), run_time=0.4)
            self.wait(0.3)

        self.wait(1.0)

        # Sortie propre
        self.play(
            FadeOut(columns_group),
            FadeOut(big_title),
            run_time=2.3,
        )

# ============================================================================
# SCENE 2A: TTS Expressivity Problem (60s)
# ============================================================================
class SceneProblemTTS(Scene):
    TARGET_SECONDS = 60.0

    def construct(self):
        start = 0.0

        title = under_title("The TTS Expressivity Problem", color=ACCENT_YELLOW, font_size=46)
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title, shift=DOWN*0.2), run_time=1.2); start += 1.2
        self.wait(0.4); start += 0.4

        # Baromètre
        lbl_intel = T("Intelligibility", font_size=22, color=HI_GREY)
        lbl_expr  = T("Expressivity",  font_size=22, color=HI_GREY)
        bar_w = 4.8

        bar_i_bg = Line(ORIGIN, RIGHT*bar_w, stroke_width=8).set_color(HI_GREY).set_opacity(0.25)
        bar_i_fg = Line(ORIGIN, RIGHT*(bar_w*0.86), stroke_width=10).set_color(ACCENT_YELLOW)
        g_i = VGroup(lbl_intel, VGroup(bar_i_bg, bar_i_fg).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.16)

        bar_e_bg = Line(ORIGIN, RIGHT*bar_w, stroke_width=8).set_color(HI_GREY).set_opacity(0.25)
        bar_e_fg = Line(ORIGIN, RIGHT*(bar_w*0.28), stroke_width=10).set_color(ACCENT_PURPLE)
        g_e = VGroup(lbl_expr, VGroup(bar_e_bg, bar_e_fg).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.16)

        meter = VGroup(g_i, g_e).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.8).shift(DOWN*0.2)
        self.play(FadeIn(meter, shift=UP*0.1), run_time=1.2); start += 1.2

        # SLIDE 1
        heading = T("Current State", font_size=32, color=ACCENT_YELLOW, weight=BOLD)
        bullet_items = [
            "• Commercial TTS prioritizes clarity",
            "• Prosodic variation is limited",
            "• Leads to monotonous speech",
            "• French prosody particularly affected",
        ]
        bullets = VGroup(*[
            T(item, font_size=26, color=TEXT_COLOR)
            for item in bullet_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        col_state = VGroup(heading, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.42)

        heading2 = T("Consequences", font_size=32, color=ACCENT_CYAN, weight=BOLD)
        cons_items = [
            "↓ Engagement & naturalness",
            "↓ Perceived speaker intent",
            "↑ Listening fatigue",
        ]
        cons = VGroup(*[
            T(s, font_size=24, color=TEXT_COLOR) for s in cons_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        col_cons = VGroup(heading2, cons).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        col_state.next_to(meter, RIGHT, buff=1.2).align_to(meter, UP)
        sep = Line(ORIGIN, DOWN*3.8, stroke_width=2).set_color(HI_GREY).set_opacity(0.20)
        sep.next_to(col_state, RIGHT, buff=0.7).align_to(col_state, UP)
        col_cons.next_to(sep, RIGHT, buff=0.7).align_to(col_state, UP)

        slide1 = VGroup(col_state, sep, col_cons)

        self.play(
            FadeIn(col_state, shift=UP*0.12),
            FadeIn(sep,       shift=UP*0.05),
            FadeIn(col_cons,  shift=UP*0.12),
            run_time=1.2
        ); start += 1.2
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.08) for b in bullets], lag_ratio=0.22), run_time=2.5); start += 2.5
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in cons],    lag_ratio=0.22), run_time=2.0); start += 2.0
        self.wait(2.0); start += 2.0

        # TRANSITION : on nettoie TOUT ce qui appartient à la première "page"
        self.play(
            FadeOut(slide1),
            FadeOut(meter),
            run_time=1.0
        ); start += 1.0

        # On enlève aussi le titre de la première page avant d'afficher le nouveau
        self.play(FadeOut(title), run_time=0.8); start += 0.8

        # ------------------------------------------------------------------
        # SLIDE 2 : "Prosody control" (gros titre) + définitions
        # ------------------------------------------------------------------
        big_title_text = T(
            "Prosody control",
            font_size=44,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        big_underline = Line(
            big_title_text.get_bottom() + DOWN * 0.06 + LEFT * 0.1,
            big_title_text.get_bottom() + DOWN * 0.06 + RIGHT * 0.1,
            stroke_width=3,
        ).set_color(ACCENT_BLUE)

        big_title = VGroup(big_title_text, big_underline).arrange(DOWN, buff=0.08)
        big_title.to_edge(UP, buff=0.7)

        self.play(FadeIn(big_title, shift=DOWN * 0.2), run_time=1.6)
        self.wait(0.8)

        # Petit sous-titre explicatif sous "Prosody control"
        prosody_subtitle = T(
            "Pitch, volume, rate and pauses",
            font_size=22,
            color=HI_GREY,
        ).next_to(big_title, DOWN, buff=0.5)

        self.play(FadeIn(prosody_subtitle, shift=DOWN * 0.1), run_time=1.0)
        self.wait(0.6)

        params_data = [
            ("Pitch (F0)", ACCENT_YELLOW,
             "Perceived height of the voice.",
             "Intonation, questions, emphasis."),
            ("Volume (Loudness)", ACCENT_YELLOW,
             "Perceived intensity of speech.",
             "Prominence, emotional strength."),
            ("Rate (Tempo)", ACCENT_YELLOW,
             "Speed of articulation.",
             "Urgency vs clarity, rhythm."),
            ("Breaks (Pauses)", ACCENT_YELLOW,
             "Short silences between phrases.",
             "Structure, emphasis, comprehension."),
        ]

        cards = []
        for label, color, l1, l2 in params_data:
            head = T(label, font_size=26, color=color, weight=BOLD)
            line_a = T(l1, font_size=22, color=TEXT_COLOR)
            line_b = T(l2, font_size=20, color=HI_GREY)
            card = VGroup(head, line_a, line_b).arrange(
                DOWN, aligned_edge=LEFT, buff=0.16
            )
            cards.append(card)

        # ORGANISATION EN 2 COLONNES
        left_column = VGroup(cards[0], cards[1]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        right_column = VGroup(cards[2], cards[3]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)

        columns_group = VGroup(left_column, right_column).arrange(
            RIGHT, buff=1.5, aligned_edge=UP
        )
        columns_group.next_to(prosody_subtitle, DOWN, buff=0.8)

        # Apparition interactive
        self.play(
            LaggedStartMap(FadeIn, left_column, shift=RIGHT * 0.2, lag_ratio=0.4),
            run_time=1.5
        )
        self.wait(0.3)

        self.play(
            LaggedStartMap(FadeIn, right_column, shift=LEFT * 0.2, lag_ratio=0.4),
            run_time=1.5
        )

        for card in cards:
            self.play(Indicate(card[0], scale_factor=1.03), run_time=0.4)
            self.wait(0.3)

        self.wait(1.0)

        # Sortie propre
        self.play(
            FadeOut(columns_group),
            FadeOut(prosody_subtitle),
            FadeOut(big_title),
            run_time=2.3,
        )

# ============================================================================
# SCENE 2B: SSML Challenges (clair, interactif, sans padding)
# ============================================================================
class SceneProblemSSML(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # TITRE
        # ------------------------------------------------------------------
        title_text = T(
            "SSML challenges",
            font_size=44,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        underline = Line(
            title_text.get_bottom() + DOWN * 0.06 + LEFT * 0.1,
            title_text.get_bottom() + DOWN * 0.06 + RIGHT * 0.1,
            stroke_width=3,
        ).set_color(ACCENT_BLUE)

        title = VGroup(title_text, underline).arrange(DOWN, buff=0.08)
        title.to_edge(UP, buff=0.55)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=1.4)
        self.wait(0.6)

        # ------------------------------------------------------------------
        # SLIDE 1 : "Why SSML is hard"
        # ------------------------------------------------------------------
        heading = T(
            "Why SSML is hard in practice ?",
            font_size=32,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        heading.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=1.2)

        bullet_texts = [
            "Manual tags do not scale",
            "LLMs often break XML syntax",
            "Engines handle SSML differently",
        ]
        bullets = VGroup(*[
            T(f"• {txt}", font_size=26, color=TEXT_COLOR)
            for txt in bullet_texts
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        bullets.next_to(heading, DOWN, buff=0.45)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=1.2)

        # Apparition interactive des bullets
        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.15), run_time=0.7)
            self.play(Indicate(b, scale_factor=1.03), run_time=0.35)
            self.wait(0.3)

        self.wait(0.8)

        # Petite synthèse visuelle : encadrer la liste
        box = SurroundingRectangle(
            bullets,
            color=ACCENT_YELLOW,
            buff=0.25,
            stroke_width=3,
        )
        self.play(Create(box), run_time=0.8)
        self.wait(0.7)

        # Transition vers le slide 2 : on garde le titre, on efface le reste
        self.play(
            FadeOut(box),
            FadeOut(heading),
            FadeOut(bullets),
            run_time=1.0,
        )
        self.wait(0.4)


        # ------------------------------------------------------------------
        # SLIDE 2 : "Typical failure patterns"
        # ------------------------------------------------------------------
        heading2 = T(
            "Typical failure patterns",
            font_size=32,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        heading2.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=1.2)
        self.play(FadeIn(heading2, shift=UP * 0.1), run_time=1.0)
        self.wait(0.4)

         # 4 cartes avec sauts de ligne pour que le texte tienne
        def pattern_card(title_str: str, line1: str, line2: str = ""):
            head = T(title_str, font_size=28, color=ACCENT_YELLOW, weight=BOLD)
            line1_text = T(line1, font_size=24, color=TEXT_COLOR)
            if line2:
                line2_text = T(line2, font_size=22, color=TEXT_COLOR)
                card = VGroup(head, line1_text, line2_text).arrange(
                    DOWN, aligned_edge=LEFT, buff=0.16
                )
            else:
                card = VGroup(head, line1_text).arrange(
                    DOWN, aligned_edge=LEFT, buff=0.18
                )
            return card

        card_syntax = pattern_card(
            "Syntax",
            "Unclosed tags, bad nesting,",
            "escaping issues."
        )
        card_sem = pattern_card(
            "Semantics", 
            "Unsupported attributes or units,",
            "clipped ranges."
        )
        card_ctrl = pattern_card(
            "Control",
            "Conflicting <prosody>,",
            "unclear global vs local."
        )
        card_eval = pattern_card(
            "Evaluation",
            "MOS only, no automatic",
            "SSML validation."
        )
        # ORGANISATION EN 2 COLONNES ÉQUILIBRÉES
        left_col = VGroup(card_syntax, card_sem).arrange(
            DOWN, buff=0.4, aligned_edge=LEFT
        )
        right_col = VGroup(card_ctrl, card_eval).arrange(
            DOWN, buff=0.4, aligned_edge=LEFT
        )
        
        # Centrer le groupe des colonnes
        columns_group = VGroup(left_col, right_col).arrange(
            RIGHT, buff=1.7, aligned_edge=UP
        )
        columns_group.next_to(heading2, DOWN, buff=1.2)
        
        # Centrer horizontalement
        columns_group.move_to(ORIGIN).align_to(heading2, UP).shift(DOWN * 0.9)

        # On pose la grille mais invisible au départ
        for card in [card_syntax, card_sem, card_ctrl, card_eval]:
            card.set_opacity(0.0)
        self.add(columns_group)

        # Apparition interactive des 4 cartes avec encadrement léger
        cards_order = [card_syntax, card_sem, card_ctrl, card_eval]
        for card in cards_order:
            self.play(card.animate.set_opacity(1.0), run_time=0.7)
            rect = SurroundingRectangle(
                card,
                color=ACCENT_YELLOW,
                buff=0.15,
                stroke_width=2,
            )
            self.play(Create(rect), run_time=0.4)
            self.play(Indicate(card[0], scale_factor=1.03), run_time=0.35)
            self.wait(0.4)
            self.play(FadeOut(rect), run_time=0.4)

        self.wait(1.1)

        # ------------------------------------------------------------------
        # Citation + sortie propre
        # ------------------------------------------------------------------
        citation = T(
            "Ref: ICNLSP 2025 (pp. 1–2)",
            font_size=18,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=0.8)
        self.wait(1.0)

        self.play(
            FadeOut(citation),
            FadeOut(columns_group),
            FadeOut(heading2),
            FadeOut(title),
            run_time=1.6,
        )
        self.wait(0.5)

# ============================================================================
# SCENE 3: Proposed SSML pipeline (figure + zones mises en avant)
# ============================================================================
class ScenePipelineInteractive(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # 1) Titre harmonisé
        # ------------------------------------------------------------------
        title = under_title(
            "Proposed SSML pipeline",
            color=ACCENT_YELLOW,
            font_size=46,
        )
        title.to_edge(UP, buff=0.75)

        self.play(FadeIn(title, shift=DOWN * 0.4), run_time=1.6)
        self.wait(0.9)

        # ------------------------------------------------------------------
        # 2) Image du pipeline
        # ------------------------------------------------------------------
        pipeline_img = ImageMobject("assets/pipeline.png")
        pipeline_img.scale_to_fit_width(config.frame_width * 0.9)
        pipeline_img.next_to(title, DOWN, buff=0.8)

        self.play(FadeIn(pipeline_img, shift=UP * 0.2), run_time=2.0)
        self.wait(2.0)  # vue globale

        # ------------------------------------------------------------------
        # 3) Définition des 3 zones avec rectangles *vides*
        # ------------------------------------------------------------------
        w = pipeline_img.width
        h = pipeline_img.height

        left_box = Rectangle(
            width=w * 0.32,
            height=h * 0.9,
            stroke_color=ACCENT_YELLOW,
            stroke_width=3,
            fill_opacity=0.0,   # aucune couleur de fond
        )
        center_box = Rectangle(
            width=w * 0.32,
            height=h * 0.9,
            stroke_color=ACCENT_YELLOW,
            stroke_width=3,
            fill_opacity=0.0,
        )
        right_box = Rectangle(
            width=w * 0.32,
            height=h * 0.9,
            stroke_color=ACCENT_YELLOW,
            stroke_width=3,
            fill_opacity=0.0,
        )

        # Positionnement relatif à l'image
        left_box.move_to(pipeline_img.get_left() + RIGHT * (w * 0.16))
        center_box.move_to(pipeline_img.get_center())
        right_box.move_to(pipeline_img.get_right() + LEFT * (w * 0.16))

        # ------------------------------------------------------------------
        # 4) Labels sous CHAQUE rectangle, avec de l'air
        # ------------------------------------------------------------------
        lbl_left = T(
            "Input & preprocessing",
            font_size=24,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        lbl_center = T(
            "Prosody analysis\n& features",
            font_size=24,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        lbl_right = T(
            "SSML generation\n& improved TTS",
            font_size=24,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        # On les place sous chaque box, avec un buff assez large
        lbl_left.next_to(left_box, DOWN, buff=0.4)
        lbl_center.next_to(center_box, DOWN, buff=0.4)
        lbl_right.next_to(right_box, DOWN, buff=0.4)

        # ------------------------------------------------------------------
        # 5) CORRECTION : On ajoute seulement l'image au départ
        # ------------------------------------------------------------------
        self.add(pipeline_img)  # Seulement l'image au début

        # ------------------------------------------------------------------
        # 6) Mise en avant zone par zone (sans masquer l'image)
        # ------------------------------------------------------------------

        # ---- Zone gauche : audio + baseline ----
        # Ajouter la box et le label en même temps qu'on les anime
        self.play(
            FadeIn(left_box),
            FadeIn(lbl_left, shift=UP * 0.1),
            run_time=1.0,
        )
        self.play(Indicate(left_box, scale_factor=1.02), run_time=0.8)
        self.wait(1.6)

        # Laisser le contour légèrement visible, moins fort
        self.play(left_box.animate.set_stroke(opacity=0.6), run_time=0.6)

        # ---- Zone centrale : syntagmes + features ----
        self.play(
            FadeIn(center_box),
            FadeIn(lbl_center, shift=UP * 0.1),
            run_time=1.0,
        )
        self.play(Indicate(center_box, scale_factor=1.02), run_time=0.7)
        self.wait(1.6)
        self.play(center_box.animate.set_stroke(opacity=0.6), run_time=0.6)

        # ---- Zone droite : SSML + output ----
        self.play(
            FadeIn(right_box),
            FadeIn(lbl_right, shift=UP * 0.1),
            run_time=1.1,
        )
        self.play(Indicate(right_box, scale_factor=1.02), run_time=0.7)
        self.wait(1.8)

        # ------------------------------------------------------------------
        # 7) Récap global : tous les contours légèrement visibles
        # ------------------------------------------------------------------
        self.play(
            left_box.animate.set_stroke(opacity=0.6),
            center_box.animate.set_stroke(opacity=0.6),
            right_box.animate.set_stroke(opacity=0.6),
            run_time=0.8,
        )
        self.wait(1.5)

        # ------------------------------------------------------------------
        # 8) Citation + sortie propre
        # ------------------------------------------------------------------
        citation = T(
            "Ref: Ouali et al., ICNLSP 2025 – Section 3, Figure 1",
            font_size=18,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(citation), run_time=0.8)
        self.wait(1.5)

        self.play(
            FadeOut(citation),
            FadeOut(left_box),
            FadeOut(center_box),
            FadeOut(right_box),
            FadeOut(lbl_left),
            FadeOut(lbl_center),
            FadeOut(lbl_right),
            FadeOut(pipeline_img),
            FadeOut(title),
            run_time=1.6,
        )
        self.wait(0.4)

# ============================================================================
# SCENE X: Two-stage SSML cascade (image seule, sans interaction)
# ============================================================================
class SceneCascadeInteractive(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # 1) Titre harmonisé
        # ------------------------------------------------------------------
        title = under_title(
            "Two-stage SSML cascade",
            color=ACCENT_YELLOW,
            font_size=46,
        )
        title.to_edge(UP, buff=0.65)

        self.play(FadeIn(title, shift=DOWN * 0.4), run_time=1.6)
        self.wait(0.8)

        # ------------------------------------------------------------------
        # 2) Image de la cascade (sans encadrement, juste affichée)
        # ------------------------------------------------------------------
        cascade_img = ImageMobject("assets/cascade.png")

        # On contrôle largeur / hauteur pour que ça tienne bien sous le titre
        max_w = config.frame_width * 0.9
        max_h = config.frame_height * 0.65   # laisse de l’air en bas
        cascade_img.scale_to_fit_width(max_w)
        if cascade_img.height > max_h:
            cascade_img.scale_to_fit_height(max_h)

        cascade_img.next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(cascade_img, shift=UP * 0.2), run_time=2.0)
        self.wait(8.0)  # durée d’affichage de la figure (à ajuster si besoin)

        # ------------------------------------------------------------------
        # 3) Sortie propre
        # ------------------------------------------------------------------
        self.play(
            FadeOut(cascade_img),
            FadeOut(title),
            run_time=1.6,
        )
        self.wait(0.4)

# ============================================================================
# SCENE 4: Stage 1 – Break Prediction (QwenA)
# ============================================================================
class SceneStage1(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # 1) Titre harmonisé
        # ------------------------------------------------------------------
        title = under_title(
            "Stage 1: Break Prediction (QwenA)",
            color=ACCENT_YELLOW,
            font_size=46,
        )
        title.to_edge(UP, buff=0.55)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.6)
        self.wait(0.6)

        # ------------------------------------------------------------------
        # 2) Bloc gauche : modèle & tâche
        # ------------------------------------------------------------------
        heading_model = T(
            "QwenA: text → breaks",
            font_size=32,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        b1 = T("Qwen 2.5–7B, QLoRA 4-bit", font_size=26, color=TEXT_COLOR)
        b2 = T("Input: ≤ 200-word French paragraph", font_size=24, color=TEXT_COLOR)
        b3 = T("Output: <break> tag placement", font_size=24, color=TEXT_COLOR)

        bullets_model = VGroup(b1, b2, b3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22
        )

        left_panel = VGroup(heading_model, bullets_model).arrange(
            DOWN, aligned_edge=LEFT, buff=0.40
        )
        left_panel.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=0.9)

        # Apparition progressive
        self.play(FadeIn(heading_model, shift=UP * 0.1), run_time=1.0)
        for b in bullets_model:
            self.play(FadeIn(b, shift=RIGHT * 0.15), run_time=0.6)
            self.play(Indicate(b, scale_factor=1.02), run_time=0.3)
            self.wait(0.2)

        self.wait(0.6)

        # ------------------------------------------------------------------
        # 3) Bloc droit : performance (positionné AVANT de créer le cadre)
        # ------------------------------------------------------------------
        heading_perf = T(
            "Performance (dev set)",
            font_size=30,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        f1_text = T(
            "F₁ score: 99.24%",
            font_size=30,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        ppl_text = T(
            "Perplexity: 1.001",
            font_size=26,
            color=TEXT_COLOR,
        )
        baseline_text = T(
            "BERT baseline: 92.06% F₁",
            font_size=22,
            color=HI_GREY,
        )

        perf_box = VGroup(
            heading_perf,
            f1_text,
            ppl_text,
            baseline_text,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)

        # On place d'abord le bloc à sa position finale
        perf_box.next_to(left_panel, RIGHT, buff=1.4).align_to(left_panel, UP)

        # Maintenant seulement on crée le cadre autour
        perf_frame = SurroundingRectangle(
            perf_box,
            color=ACCENT_YELLOW,
            buff=0.30,
            stroke_width=3,
        )

        # Apparition interactive du bloc de performance
        self.play(
            FadeIn(perf_box, shift=UP * 0.1),
            Create(perf_frame),
            run_time=1.4,
        )
        self.wait(0.4)

        # Mise en avant des chiffres clés
        self.play(Indicate(f1_text, scale_factor=1.05), run_time=0.6)
        self.wait(0.3)
        self.play(Indicate(ppl_text, scale_factor=1.03), run_time=0.5)
        self.wait(0.3)
        self.play(Indicate(baseline_text, scale_factor=1.03), run_time=0.5)
        self.wait(0.8)

        # ------------------------------------------------------------------
        # 4) Citation + sortie propre
        # ------------------------------------------------------------------
        citation = T(
            "Ref: ICNLSP 2025 – Table 4 (Stage 1: QwenA)",
            font_size=18,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(citation), run_time=0.7)
        self.wait(1.0)

        self.play(
            FadeOut(citation),
            FadeOut(perf_frame),
            FadeOut(perf_box),
            FadeOut(left_panel),
            FadeOut(title),
            run_time=1.6,
        )
        self.wait(0.4)


# ============================================================================
# SCENE 5: Stage 2 – Prosody Prediction (QwenB)
# ============================================================================
class SceneStage2(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # 1) Titre harmonisé, même style que Stage 1
        # ------------------------------------------------------------------
        title = under_title(
            "Stage 2: Prosody Prediction (QwenB)",
            color=ACCENT_YELLOW,
            font_size=42,  # Légèrement réduit
        )
        title.to_edge(UP, buff=0.55)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.6)
        self.wait(0.6)

        # ------------------------------------------------------------------
        # 2) ORGANISATION EN 2 COLONNES AVEC POLICE RÉDUITE
        # ------------------------------------------------------------------

        # Colonne gauche : Modèle QwenB
        heading_model = T(
            "QwenB: SSML → prosody values",
            font_size=28,  # Réduit
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        b1 = T(
            "Qwen 2.5–7B (second instance)",
            font_size=22,  # Réduit
            color=TEXT_COLOR,
        )
        b2 = T(
            "QLoRA adapter fine-tuning",
            font_size=22,
            color=TEXT_COLOR,
        )
        b3 = T(
            "Input: SSML skeleton from QwenA",
            font_size=22,
            color=TEXT_COLOR,
        )
        b4 = T(
            "Output: numeric prosodic attributes",
            font_size=22,
            color=TEXT_COLOR,
        )

        bullets_model = VGroup(b1, b2, b3, b4).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.18,  # Espacement réduit
        )

        left_column = VGroup(heading_model, bullets_model).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.30,  # Espacement réduit
        )

        # Colonne droite : Features prosodiques
        heading_feat = T(
            "Prosodic features",
            font_size=28,  # Réduit
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        f_pitch = T(
            "Pitch: f₀ → semitone → %",
            font_size=22,  # Réduit et texte raccourci
            color=TEXT_COLOR,
        )
        f_vol = T(
            "Volume: LUFS → gain %",
            font_size=22,
            color=TEXT_COLOR,
        )
        f_rate = T(
            "Rate: words/sec → tempo %",
            font_size=22,
            color=TEXT_COLOR,
        )
        f_break = T(
            "Breaks: 250-500 ms silence",
            font_size=22,  # Texte simplifié
            color=TEXT_COLOR,
        )

        features_list = VGroup(f_pitch, f_vol, f_rate, f_break).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.18,  # Espacement réduit
        )

        right_column = VGroup(heading_feat, features_list).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.30,  # Espacement réduit
        )

        # Positionner les deux colonnes plus centrées
        columns_group = VGroup(left_column, right_column).arrange(
            RIGHT, 
            buff=0.8,  # Espacement réduit entre colonnes
            aligned_edge=UP
        )
        columns_group.next_to(title, DOWN, buff=0.6).shift(LEFT * 0.3)  # Décalé vers la gauche

        # ------------------------------------------------------------------
        # 3) ANIMATION DES DEUX COLONNES
        # ------------------------------------------------------------------

        # Apparition de la colonne gauche
        self.play(FadeIn(heading_model, shift=UP * 0.1), run_time=0.9)
        self.wait(0.2)
        
        for b in bullets_model:
            self.play(FadeIn(b, shift=RIGHT * 0.15), run_time=0.4)
            self.play(Indicate(b, scale_factor=1.02), run_time=0.2)
            self.wait(0.1)

        self.wait(0.3)

        # Apparition de la colonne droite
        self.play(FadeIn(heading_feat, shift=UP * 0.1), run_time=0.7)
        self.wait(0.2)

        # Animation groupée des features
        features_animations = []
        for feat in features_list:
            features_animations.append(FadeIn(feat, shift=RIGHT * 0.15))
        
        self.play(LaggedStart(*features_animations, lag_ratio=0.2), run_time=1.0)
        
        # Indicate chaque feature
        for feat in features_list:
            self.play(Indicate(feat, scale_factor=1.03), run_time=0.3)
            self.wait(0.1)

        self.wait(0.5)

        # ------------------------------------------------------------------
        # 4) Cadre autour de la colonne droite
        # ------------------------------------------------------------------
        features_frame = SurroundingRectangle(
            right_column,
            color=ACCENT_BLUE,
            buff=0.20,  # Buff réduit
            stroke_width=2,
        )

        self.play(Create(features_frame), run_time=0.6)
        self.wait(0.6)

        # ------------------------------------------------------------------
        # 5) Citation + sortie propre
        # ------------------------------------------------------------------
        citation = T(
            "Ref: ICNLSP 2025 – Section 4",
            font_size=16,  # Réduit
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(citation), run_time=0.6)
        self.wait(0.8)

        self.play(
            FadeOut(citation),
            FadeOut(features_frame),
            FadeOut(columns_group),
            FadeOut(title),
            run_time=1.4,
        )
        self.wait(0.4)

# ============================================================================
# SCENE 6: Objective Evaluation (F1 + MAE, clair et interactif)
# ============================================================================
class SceneEvalObj(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # 1) Titre harmonisé
        # ------------------------------------------------------------------
        title = under_title(
            "Objective evaluation",
            color=ACCENT_YELLOW,
            font_size=46,
        )
        title.to_edge(UP, buff=0.55)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.4)
        self.wait(0.6)

        # ------------------------------------------------------------------
        # 2) Bloc gauche : Break prediction accuracy (F1)
        # ------------------------------------------------------------------
        f1_heading = T(
            "Break prediction accuracy",
            font_size=30,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        f1_qwen = T(
            "QwenA (ours): 99.24% F₁",
            font_size=26,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        f1_bert = T(
            "BERT baseline: 92.06% F₁",
            font_size=24,
            color=HI_GREY,
        )

        f1_block = VGroup(
            f1_heading,
            f1_qwen,
            f1_bert,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )

        # Position du panneau gauche
        f1_block.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=0.9)

        # Cadre autour du bloc, créé APRÈS positionnement
        f1_frame = SurroundingRectangle(
            f1_block,
            color=ACCENT_YELLOW,
            buff=0.30,
            stroke_width=3,
        )

        # Apparition interactive bloc F1
        self.play(
            FadeIn(f1_block, shift=UP * 0.1),
            Create(f1_frame),
            run_time=1.4,
        )
        self.wait(0.4)

        self.play(Indicate(f1_qwen, scale_factor=1.03), run_time=0.5)
        self.wait(0.3)
        self.play(Indicate(f1_bert, scale_factor=1.03), run_time=0.5)
        self.wait(0.5)

        # ------------------------------------------------------------------
        # 3) Bloc droit : MAE prosodique (Pitch, Volume, Rate)
        # ------------------------------------------------------------------
        mae_heading = T(
            "Prosody MAE (Stage 2 – QwenB)",
            font_size=30,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        mae_pitch = T(
            "Pitch: 0.97% vs 1.68% (BiLSTM)",
            font_size=24,
            color=TEXT_COLOR,
        )
        mae_vol = T(
            "Volume: 1.09% vs 6.04% (BiLSTM)",
            font_size=24,
            color=TEXT_COLOR,
        )
        mae_rate = T(
            "Rate: 1.10% vs 0.84% (BiLSTM)",
            font_size=24,
            color=TEXT_COLOR,
        )
        mae_key = T(
            "≈25–40% MAE reduction vs baselines",
            font_size=24,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        mae_block = VGroup(
            mae_heading,
            mae_pitch,
            mae_vol,
            mae_rate,
            mae_key,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.18,
        )

        # Position panneau droit (après avoir posé le bloc gauche)
        mae_block.next_to(f1_block, RIGHT, buff=1.4).align_to(f1_block, UP)

        mae_frame = SurroundingRectangle(
            mae_block,
            color=ACCENT_YELLOW,
            buff=0.30,
            stroke_width=3,
        )

        # Apparition bloc MAE
        self.play(
            FadeIn(mae_block, shift=UP * 0.1),
            Create(mae_frame),
            run_time=1.6,
        )

        for m in [mae_pitch, mae_vol, mae_rate]:
            self.play(Indicate(m, scale_factor=1.03), run_time=0.4)
            self.wait(0.2)

        self.play(Indicate(mae_key, scale_factor=1.04), run_time=0.5)
        self.wait(0.8)

        # ------------------------------------------------------------------
        # 4) Citation + sortie propre
        # ------------------------------------------------------------------
        citation = T(
            "Ref: Ouali et al., ICNLSP 2025 – Table 4–5",
            font_size=18,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(citation), run_time=0.7)
        self.wait(1.0)

        self.play(
            FadeOut(citation),
            FadeOut(f1_frame),
            FadeOut(mae_frame),
            FadeOut(f1_block),
            FadeOut(mae_block),
            FadeOut(title),
            run_time=1.6,
        )
        self.wait(0.4)

# ============================================================================
# SCENE 7: Subjective evaluation (AB test, clair et interactif, sans padding)
# ============================================================================
class SceneEvalSubj(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # 1) Titre harmonisé
        # ------------------------------------------------------------------
        title = under_title(
            "Subjective evaluation (AB test)",
            color=ACCENT_YELLOW,
            font_size=46,
        )
        title.to_edge(UP, buff=0.55)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.4)
        self.wait(0.6)

        # ------------------------------------------------------------------
        # 2) Panneau gauche : Study design
        # ------------------------------------------------------------------
        design_heading = T(
            "Study design",
            font_size=30,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        d_n = T("18 participants", font_size=24, color=TEXT_COLOR)
        d_pairs = T("30 AB pairs (≈1 min)", font_size=24, color=TEXT_COLOR)
        d_cond = T("Baseline vs SSML-enhanced", font_size=24, color=TEXT_COLOR)

        design_block = VGroup(
            design_heading,
            d_n,
            d_pairs,
            d_cond,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )

        design_block.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=0.9)

        design_frame = SurroundingRectangle(
            design_block,
            color=ACCENT_YELLOW,
            buff=0.30,
            stroke_width=3,
        )

        self.play(
            FadeIn(design_block, shift=UP * 0.1),
            Create(design_frame),
            run_time=1.5,
        )
        self.wait(0.4)

        for line in [d_n, d_pairs, d_cond]:
            self.play(Indicate(line, scale_factor=1.03), run_time=0.4)
            self.wait(0.2)

        # ------------------------------------------------------------------
        # 3) Panneau droit : MOS + préférence
        # ------------------------------------------------------------------
        mos_heading = T(
            "Listening results",
            font_size=30,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        mos_base = T("Baseline: 3.20 MOS", font_size=24, color=HI_GREY)
        mos_enh = T(
            "Enhanced: 3.87 (+0.67, +20%)",
            font_size=24,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        mos_p = T(
            "p < 0.005 (significant)",
            font_size=22,
            color=ACCENT_YELLOW,
            slant=ITALIC,
        )
        mos_pref = T(
            "15 / 18 listeners prefer enhanced",
            font_size=24,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        mos_block = VGroup(
            mos_heading,
            mos_base,
            mos_enh,
            mos_p,
            mos_pref,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.18,
        )

        mos_block.next_to(design_block, RIGHT, buff=1.4).align_to(design_block, UP)

        mos_frame = SurroundingRectangle(
            mos_block,
            color=ACCENT_YELLOW,
            buff=0.30,
            stroke_width=3,
        )

        self.play(
            FadeIn(mos_block, shift=UP * 0.1),
            Create(mos_frame),
            run_time=1.6,
        )

        self.play(Indicate(mos_enh, scale_factor=1.04), run_time=0.5)
        self.wait(0.2)
        self.play(Indicate(mos_p, scale_factor=1.03), run_time=0.5)
        self.wait(0.2)
        self.play(Indicate(mos_pref, scale_factor=1.04), run_time=0.5)
        self.wait(0.8)

        # ------------------------------------------------------------------
        # 4) Citation + sortie propre
        # ------------------------------------------------------------------
        citation = T(
            "Ref: Ouali et al., ICNLSP 2025 – Section 5",
            font_size=18,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(citation), run_time=0.7)
        self.wait(1.0)

        self.play(
            FadeOut(citation),
            FadeOut(design_frame),
            FadeOut(mos_frame),
            FadeOut(design_block),
            FadeOut(mos_block),
            FadeOut(title),
            run_time=1.6,
        )
        self.wait(0.4)

# ============================================================================
# SCENE 8: Conclusions & Future Work (clair, interactif, sans padding)
# ============================================================================
class SceneOutro(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # 1) Titre harmonisé
        # ------------------------------------------------------------------
        title = under_title(
            "Conclusions & future work",
            color=ACCENT_YELLOW,
            font_size=46,
        )
        title.to_edge(UP, buff=0.55)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.4)
        self.wait(0.6)

        # ------------------------------------------------------------------
        # 2) Panneau gauche : Key achievements
        # ------------------------------------------------------------------
        ach_heading = T(
            "Key achievements",
            font_size=30,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        ach1 = T("✓ 99.2% F₁ break placement", font_size=24, color=TEXT_COLOR)
        ach2 = T("✓ 25–40% MAE reduction",     font_size=24, color=TEXT_COLOR)
        ach3 = T("✓ MOS 3.20 → 3.87 (+20%)",   font_size=24, color=TEXT_COLOR)
        ach4 = T("✓ First French SSML pipeline", font_size=24, color=TEXT_COLOR)

        ach_block = VGroup(
            ach_heading,
            ach1,
            ach2,
            ach3,
            ach4,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )

        ach_block.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=0.9)

        ach_frame = SurroundingRectangle(
            ach_block,
            color=ACCENT_YELLOW,
            buff=0.30,
            stroke_width=3,
        )

        self.play(
            FadeIn(ach_block, shift=UP * 0.1),
            Create(ach_frame),
            run_time=1.6,
        )
        self.wait(0.4)

        for line in [ach1, ach2, ach3, ach4]:
            self.play(Indicate(line, scale_factor=1.03), run_time=0.35)
            self.wait(0.15)

        # ------------------------------------------------------------------
        # 3) Panneau droit : Future work
        # ------------------------------------------------------------------
        fw_heading = T(
            "Future work",
            font_size=30,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        fw1 = T("→ Unified end-to-end model",         font_size=24, color=TEXT_COLOR)
        fw2 = T("→ Richer multimodal embeddings",     font_size=24, color=TEXT_COLOR)
        fw3 = T("→ Extension to more languages",      font_size=24, color=TEXT_COLOR)

        fw_block = VGroup(
            fw_heading,
            fw1,
            fw2,
            fw3,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )

        fw_block.next_to(ach_block, RIGHT, buff=1.6).align_to(ach_block, UP)

        fw_frame = SurroundingRectangle(
            fw_block,
            color=ACCENT_YELLOW,
            buff=0.30,
            stroke_width=3,
        )

        self.play(
            FadeIn(fw_block, shift=UP * 0.1),
            Create(fw_frame),
            run_time=1.6,
        )
        self.wait(0.6)

        for line in [fw1, fw2, fw3]:
            self.play(Indicate(line, scale_factor=1.03), run_time=0.35)
            self.wait(0.15)

        # ------------------------------------------------------------------
        # 4) Lien GitHub en bas
        # ------------------------------------------------------------------
        github = T(
            "github.com/hi-paris/Prosody-Control-French-TTS",
            font_size=20,
            color=ACCENT_YELLOW,
            slant=ITALIC,
        )
        github.to_edge(DOWN, buff=1.2)

        self.play(FadeIn(github, shift=UP * 0.1), run_time=1.0)
        self.wait(0.8)

        # ------------------------------------------------------------------
        # 5) Citation + sortie vers “Merci / Thank you”
        # ------------------------------------------------------------------
        citation = T(
            "Ref: Ouali et al., ICNLSP 2025 – Conclusions",
            font_size=18,
            color=HI_GREY,
            slant=ITALIC,
        ).to_corner(DR)

        self.play(FadeIn(citation), run_time=0.8)
        self.wait(1.0)

        thanks = T(
            "Merci / Thank you",
            font_size=48,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )

        self.play(
            FadeOut(citation),
            FadeOut(github),
            FadeOut(ach_frame),
            FadeOut(fw_frame),
            FadeOut(ach_block),
            FadeOut(fw_block),
            FadeOut(title),
            run_time=1.6,
        )
        self.play(FadeIn(thanks, shift=UP * 0.2), run_time=1.4)
        self.wait(2.0)


# ============================================================================
# VIDEO COMPLET (enchaîne toutes les scènes avec transitions)
# ============================================================================
class VideoComplet(Scene):
    def construct(self):
        # 0) Introduction
        intro = SceneIntro()
        intro.renderer = self.renderer
        intro.construct()
        self._transition("Audio signal basics")

        # 1) Audio Basics
        basics = SceneBasics()
        basics.renderer = self.renderer
        basics.construct()
        self._transition("Prosody & SSML")

        # 1bis) Prosody Primer
        pros = SceneProsodyPrimer()
        pros.renderer = self.renderer
        pros.construct()
        self._transition("The TTS expressivity problem")

        # 2A) TTS Expressivity Problem
        problem_tts = SceneProblemTTS()
        problem_tts.renderer = self.renderer
        problem_tts.construct()
        self._transition("SSML challenges")

        # 2B) SSML Challenges
        problem_ssml = SceneProblemSSML()
        problem_ssml.renderer = self.renderer
        problem_ssml.construct()
        self._transition("Proposed SSML pipeline")

        # 3A) Pipeline – Interactive overview
        pipe_int = ScenePipelineInteractive()
        pipe_int.renderer = self.renderer
        pipe_int.construct()
        self._transition("Two-stage SSML cascade")

        # 3B) Two-stage SSML cascade (image)
        cascade = SceneCascadeInteractive()
        cascade.renderer = self.renderer
        cascade.construct()
        self._transition("Stage 1: break prediction (QwenA)")

        # 4) Stage 1 – Break prediction (QwenA)
        stage1 = SceneStage1()
        stage1.renderer = self.renderer
        stage1.construct()
        self._transition("Stage 2: prosody prediction (QwenB)")

        # 5) Stage 2 – Prosody prediction (QwenB)
        stage2 = SceneStage2()
        stage2.renderer = self.renderer
        stage2.construct()
        self._transition("Objective evaluation")

        # 6) Objective evaluation
        evalobj = SceneEvalObj()
        evalobj.renderer = self.renderer
        evalobj.construct()
        self._transition("Subjective evaluation (AB test)")

        # 7) Subjective evaluation (AB test)
        evalsubj = SceneEvalSubj()
        evalsubj.renderer = self.renderer
        evalsubj.construct()
        self._transition("Conclusions & future work")

        # 8) Outro
        outro = SceneOutro()
        outro.renderer = self.renderer
        outro.construct()

    def _transition(self, next_scene_name: str):
        """
        Petit écran intermédiaire sobre entre deux scènes.
        """
        t = T(
            next_scene_name,
            font_size=40,
            color=ACCENT_YELLOW,
            weight=BOLD,
        )
        t.move_to(ORIGIN)
        self.play(FadeIn(t, scale=1.1), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(t, scale=0.9), run_time=1.0)
        self.wait(0.4)
