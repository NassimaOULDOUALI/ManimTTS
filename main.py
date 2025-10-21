"""
Manim Community v0.18+ Video Project: TTS & SSML Prosody Control
10-minute video (600s ± 15s) about French TTS improvement via SSML
"""

from manim import *
import numpy as np
import os

# --- Durées standardisées (équilibre lisibilité / rythme) ---
DUR_IN   = 0.95   # apparition titre/éléments principaux
DUR_ELT  = 0.85   # apparition d'éléments secondaires
DUR_OUT  = 0.63   # disparition (fade-out) compacte
PAUSE    = 0.38   # petite respiration entre actions

# --- Déterminisme visuel pour la partie spectrogramme ---
np.random.seed(0)

def slide_break(scene: Scene, keep: Mobject | None = None, intertitle: str | None = None):
    """
    Coupe 'propre' entre deux segments dans la MÊME Scene.
    - Efface tout ce qui est à l'écran SAUF 'keep' (p.ex. le titre persistant).
    - Optionnel: affiche un intertitre bref puis le retire.
    """
    # 1) Effacer tout sauf 'keep'
    to_clear = [m for m in scene.mobjects if (keep is None or m is not keep)]
    if to_clear:
        scene.play(FadeOut(Group(*to_clear)), run_time=DUR_OUT)  # CORRECTION: Group au lieu de VGroup

    # 2) Intertitre optionnel
    if intertitle is not None:
        t = Text(intertitle, font_size=44, color=ACCENT_YELLOW, weight=BOLD)
        scene.play(FadeIn(t, scale=1.05), run_time=DUR_ELT)
        scene.wait(PAUSE)
        scene.play(FadeOut(t, scale=0.95), run_time=DUR_OUT)


# CONFIGURATION SANS LATEX - Force Pango backend
config.text_backend = "pango"
config.disable_latex = True

# Theme colors
BG_COLOR = "#0b0f17"
ACCENT_BLUE = "#7cc5ff"
ACCENT_YELLOW = "#ffd166"
TEXT_COLOR = WHITE

config.background_color = BG_COLOR

# ============================================================================
# SCENE 0: Introduction (30s)
# ============================================================================
class SceneIntro(Scene):
    """
    Scene 0: Title, authors, paper reference
    Duration: 30 seconds
    Sources: PDF page 1
    """
    def construct(self):
        # Title
        title = Text(
            "Improving French Synthetic Speech Quality\nvia SSML Prosody Control",
            font_size=42,
            color=ACCENT_BLUE,
            weight=BOLD
        ).to_edge(UP, buff=0.8)
        
        # CORRECTION: Liste d'auteurs corrigée
        authors = Text(
            "Nassima Ould Ouali, Awais Hussain Sani,\n"
            "Ruben Bueno, Jonah Dauvet, Tim Luka Horstmann, Eric Moulines",
            font_size=26,
            color=TEXT_COLOR
        ).next_to(title, DOWN, buff=0.5)
        
        # Affiliations
        affiliations = Text(
            "École Polytechnique, Hi! PARIS Research Center, McGill University",
            font_size=22,
            color=ACCENT_YELLOW,
            slant=ITALIC
        ).next_to(authors, DOWN, buff=0.3)
        
        # Conference
        conference = Text(
            "ICNLSP 2025",
            font_size=28,
            color=ACCENT_BLUE,
            weight=BOLD
        ).next_to(affiliations, DOWN, buff=0.8)

        
        # Key highlights
        highlights = VGroup(
            Text("✓ 14h French podcast corpus", font_size=24, color=TEXT_COLOR),
            Text("✓ QLoRA-tuned Qwen-2.5-7B models", font_size=24, color=TEXT_COLOR),
            Text("✓ MOS 3.20 → 3.87 (p < 0.005)", font_size=24, color=ACCENT_YELLOW),
            Text("✓ 99.2% F1 for break placement", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(conference, DOWN, buff=0.8)
        
        # CORRECTION: Citation définie et utilisée
        citation = Text(
            "Données : ICNLSP 2025, p. 1",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        # Animations - CORRECTION: utilisation de Group au lieu de VGroup
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeIn(Group(authors, affiliations)), run_time=2)  # CORRECTION
        self.wait(1)
        self.play(Write(conference), run_time=1.5)
        self.wait(1)
        self.play(FadeIn(highlights, shift=UP), run_time=3)
        self.play(FadeIn(citation), run_time=1)
        self.wait(10)

# ============================================================================
# SCENE 1: Audio Basics - Waveform, Spectrogram, Pitch/F0
# ============================================================================
class SceneBasics(Scene):
    """
    Scene 1: Waveform, spectrogram, pitch/F0 animations
    Sources: PPT slides 9, 12, 13, 16, 22
    """
    def construct(self):
        # --- Titre persistant en haut de la scène ---
        title = Text("Audio Signal Basics", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=DUR_IN)
        self.wait(PAUSE)

        # ===================== WAVEFORM (Slide 1) =====================
        waveform_title = Text("Waveform: Amplitude vs. Time", font_size=32, color=ACCENT_YELLOW)
        waveform_title.next_to(title, DOWN, buff=0.5)

        axes_waveform = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-1, 1, 0.5],
            x_length=10, y_length=3,
            axis_config={"color": WHITE, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 0.5, 1, 1.5, 2]},
            y_axis_config={"numbers_to_include": [-1, 0, 1]},
        ).scale(0.7).shift(DOWN * 0.5)

        x_label = Text("Time (s)", font_size=20).next_to(axes_waveform, DOWN)
        y_label = Text("Amplitude", font_size=20).next_to(axes_waveform, LEFT).rotate(PI/2)

        def waveform_func(t):
            return 0.5 * np.sin(2 * np.pi * 5 * t) + 0.3 * np.sin(2 * np.pi * 10 * t)

        waveform_graph = axes_waveform.plot(waveform_func, color=ACCENT_BLUE)

        waveform_citation = Text(
            "D'après le cours (slide 9)",
            font_size=16, color=TEXT_COLOR, slant=ITALIC
        ).to_corner(DR)

        waveform_desc = Text(
            "Loudness: higher RMS amplitude → higher perceived loudness",
            font_size=22, color=TEXT_COLOR
        ).next_to(axes_waveform, DOWN, buff=0.8)

        # Animations - CORRECTION: utilisation de Group
        self.play(Write(waveform_title), run_time=DUR_ELT)
        self.play(Create(axes_waveform), Write(x_label), Write(y_label), run_time=DUR_ELT)
        self.play(Create(waveform_graph), run_time=DUR_IN)
        self.play(FadeIn(Group(waveform_desc, waveform_citation)), run_time=DUR_ELT)  # CORRECTION
        self.wait(PAUSE + 0.2)

        # ---- Slide break -> garde le titre, nettoie le reste, intertitre bref
        slide_break(self, keep=title, intertitle="Spectrogram")

        # ===================== SPECTROGRAM (Slide 2) =====================
        spectrogram_title = Text("Spectrogram: Frequency Energy over Time", font_size=32, color=ACCENT_YELLOW)
        spectrogram_title.next_to(title, DOWN, buff=0.5)

        axes_spectro = Axes(
            x_range=[0, 2, 0.5],
            y_range=[0, 8000, 2000],
            x_length=10, y_length=4,
            axis_config={"color": WHITE, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 0.5, 1, 1.5, 2]},
            y_axis_config={"numbers_to_include": [0, 2000, 4000, 6000, 8000]},
        ).scale(0.6).shift(DOWN * 0.3)

        x_label_spectro = Text("Time (s)", font_size=20).next_to(axes_spectro, DOWN)
        y_label_spectro = Text("Frequency (Hz)", font_size=20).next_to(axes_spectro, LEFT).rotate(PI/2)

        # Grille compacte (16x8) pour réduire le coût de rendu
        spectrogram_rects = Group()  # CORRECTION: Group au lieu de VGroup
        for i in range(16):
            for j in range(8):
                x = i * 0.125
                y = j * 1000
                intensity = 0.3 + 0.5 * np.random.random()
                rect = Rectangle(
                    width=0.55, height=0.35,
                    fill_opacity=intensity,
                    fill_color=interpolate_color(BLUE, RED, intensity),
                    stroke_width=0
                )
                rect.move_to(axes_spectro.c2p(x, y))
                spectrogram_rects.add(rect)

        spectro_citation = Text(
            "D'après le cours (slide 12)",
            font_size=16, color=TEXT_COLOR, slant=ITALIC
        ).to_corner(DR)

        spectro_desc = Text(
            "Window: 20–30 ms | Hop: ~10 ms | Hann window + FFT",
            font_size=22, color=TEXT_COLOR
        ).next_to(axes_spectro, DOWN, buff=0.8)

        self.play(Write(spectrogram_title), run_time=DUR_ELT)
        self.play(Create(axes_spectro), Write(x_label_spectro), Write(y_label_spectro), run_time=DUR_ELT)
        self.play(FadeIn(spectrogram_rects), run_time=DUR_IN)
        self.play(FadeIn(Group(spectro_desc, spectro_citation)), run_time=DUR_ELT)  # CORRECTION
        self.wait(PAUSE + 0.2)

        # ---- Slide break -> garde le titre, nettoie le reste, intertitre bref
        slide_break(self, keep=title, intertitle="Pitch & F0")

        # ===================== PITCH / F0 (Slide 3) =====================
        pitch_title = Text("Pitch & Fundamental Frequency (F0)", font_size=32, color=ACCENT_YELLOW)
        pitch_title.next_to(title, DOWN, buff=0.5)

        pitch_desc = VGroup(
            Text("Pitch is strongly related to F0", font_size=26, color=TEXT_COLOR),
            Text("(physical measure of vocal fold vibration)", font_size=22, color=TEXT_COLOR, slant=ITALIC),
        ).arrange(DOWN, buff=0.2).shift(UP * 0.5)

        f0_formula = VGroup(
            Text("s_i = 12 × log2(f0(i) / f0_ref)", font_size=32, color=ACCENT_BLUE),
            Text("(semitone offset)", font_size=20, color=TEXT_COLOR, slant=ITALIC),
            Text("p_i = (2^(s_i/12) - 1) × 100", font_size=32, color=ACCENT_BLUE),
            Text("(percentage pitch change)", font_size=20, color=TEXT_COLOR, slant=ITALIC),
        ).arrange(DOWN, buff=0.3).shift(DOWN * 0.5)

        tools_text = Text(
            "Tools: librosa (spectrogram), pyworld (F0), Praat (verification)",
            font_size=22, color=ACCENT_YELLOW
        ).to_edge(DOWN, buff=1)

        pitch_citation = Text(
            "D'après le cours (slides 13, 16) + ICNLSP 2025, p. 4",
            font_size=16, color=TEXT_COLOR, slant=ITALIC
        ).to_corner(DR)

        self.play(Write(pitch_title), run_time=DUR_ELT)
        self.play(FadeIn(pitch_desc, shift=UP), run_time=DUR_IN)
        self.play(Write(f0_formula), run_time=1.2)
        self.play(FadeIn(Group(tools_text, pitch_citation)), run_time=DUR_ELT)  # CORRECTION
        self.wait(PAUSE + 0.2)

        # --- Nettoyage final (y compris le titre persistant)
        self.play(
            FadeOut(Group(  # CORRECTION: Group au lieu de VGroup
                title, pitch_title, pitch_desc, f0_formula, tools_text, pitch_citation
            )),
            run_time=DUR_OUT
        )

# ============================================================================
# SCENE 2: TTS Expressivity Problem
# ============================================================================
class SceneProblem(Scene):
    """
    Scene 2: TTS expressivity problem
    Sources: PDF page 1, Section 1
    """
    def construct(self):
        # --- Titre persistant ---
        title = Text("The TTS Expressivity Problem", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=DUR_IN)
        self.wait(PAUSE)

        # ===================== Slide 1 — Current State =====================
        problem_box = VGroup(
            Text("Current State:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("✗ Commercial TTS prioritizes clarity", font_size=26, color=TEXT_COLOR),
            Text("✗ Prosodic variation is limited", font_size=26, color=TEXT_COLOR),
            Text("✗ Results in monotone speech output", font_size=26, color=TEXT_COLOR),
            Text("✗ Particularly affects French prosody", font_size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(problem_box, shift=UP), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # Transition propre vers la slide suivante (on garde le titre)
        slide_break(self, keep=title, intertitle="SSML Challenges")

        # ===================== Slide 2 — SSML Challenges =====================
        ssml_box = VGroup(
            Text("SSML Challenges:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("✗ Manual markup doesn't scale", font_size=26, color=TEXT_COLOR),
            Text("✗ LLMs produce incomplete tags", font_size=26, color=TEXT_COLOR),
            Text("✗ Invalid syntax generation", font_size=26, color=TEXT_COLOR),
            Text("✗ Imprecise prosodic control", font_size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(ssml_box, shift=UP), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # ===================== Référence (slide courte dédiée) =====================
        slide_break(self, keep=title)  # on efface tout sauf le titre
        citation = Text(
            "Données : ICNLSP 2025, p. 1–2",
            font_size=18, color=TEXT_COLOR, slant=ITALIC
        ).to_corner(DR)

        self.play(FadeIn(citation), run_time=DUR_ELT)
        self.wait(PAUSE + 0.2)

        # Nettoyage final (y compris titre et citation) — pas de trainage d'objets
        self.play(FadeOut(Group(title, citation)), run_time=DUR_OUT)  # CORRECTION

# ============================================================================
# SCENE 3: Pipeline Overview
# ============================================================================
class ScenePipeline(Scene):
    """
    Scene 3: Text → pauses → SSML → TTS pipeline
    Sources: PDF p.3, Slide 26
    """
    PIPELINE_IMG_PATHS = [
        "assets/pipeline.svg",
        "assets/pipeline.png",
        "assets/pipeline.jpg",
    ]

    def construct(self):
        # --- Titre persistant ---
        title = Text("The Proposed Pipeline", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=DUR_IN)
        self.wait(PAUSE)

        # ===================== Slide 1 — Corpus info =====================
        corpus_info = VGroup(
            Text("Corpus: 14h French Podcast Audio", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Source: ETX Majelan", font_size=24, color=TEXT_COLOR),
            Text("14 speakers (42% female) | 122,303 words", font_size=24, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(corpus_info, shift=DOWN), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # Transition propre vers la slide 2 (on garde le titre)
        slide_break(self, keep=title, intertitle="Pipeline Overview")

        # ===================== Slide 2 — Image + étapes (2 colonnes) =====================
        # 1) Image du pipeline (si disponible)
        pipeline_img = self._load_pipeline_image()
        img_caption = Text("Overall pipeline diagram", font_size=18, color=TEXT_COLOR, slant=ITALIC)

        if pipeline_img is not None:
            # ratio 2:3 de la largeur utilisable
            max_w = config.frame_width * 0.52
            max_h = config.frame_height * 0.60
            pipeline_img.scale_to_fit_width(max_w)
            if pipeline_img.height > max_h:
                pipeline_img.scale_to_fit_height(max_h)

            left_col = Group(pipeline_img, img_caption).arrange(DOWN, buff=0.25, aligned_edge=CENTER)  # CORRECTION: Group
        else:
            # Fallback = encart placeholder si aucune image n'est trouvée
            ph = Rectangle(width=6.2, height=3.8, color=GREY_B)
            ph_text = Text("Pipeline image not found", font_size=22, color=GREY_B)
            left_col = Group(ph, ph_text).arrange(DOWN, buff=0.25)  # CORRECTION: Group

        # 2) Étapes synthétiques (colonne droite)
        steps_compact = VGroup(
            self._create_step_box("1. Audio Preprocessing",
                                  "Demucs source sep.\nWhisperTS alignment (WER 5.95%)", ACCENT_BLUE),
            self._create_step_box("2. Baseline Generation",
                                  "MS Azure TTS (Henri)\nReference for deltas", ACCENT_YELLOW),
            self._create_step_box("3. Syntagm Segmentation",
                                  "Prosodic units\nPause detection", ACCENT_BLUE),
            self._create_step_box("4. Feature Extraction",
                                  "Pitch, Volume, Rate, Breaks\nNormalized deltas", ACCENT_YELLOW),
            self._create_step_box("5. SSML Generation",
                                  "QwenA: Break insertion\nQwenB: Prosody values", ACCENT_BLUE),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        # Mise en page 2 colonnes
        two_cols = Group(left_col, steps_compact).arrange(RIGHT, buff=0.8, aligned_edge=TOP).next_to(title, DOWN, buff=0.5)  # CORRECTION: Group

        # Animation d'arrivée
        self.play(
            FadeIn(left_col, shift=LEFT, lag_ratio=0.05),
            FadeIn(steps_compact, shift=RIGHT, lag_ratio=0.05),
            run_time=DUR_IN
        )
        self.wait(PAUSE + 0.2)

        # Citation (slide courte dédiée)
        slide_break(self, keep=title)
        citation = Text(
            "Données : ICNLSP 2025, p. 3 (Section 3) + slide 26",
            font_size=18, color=TEXT_COLOR, slant=ITALIC
        ).to_corner(DR)
        
        self.play(FadeIn(citation), run_time=DUR_ELT)
        self.wait(PAUSE + 0.2)

        # Nettoyage final
        self.play(FadeOut(Group(title, citation)), run_time=DUR_OUT)  # CORRECTION

    # ---------- Helpers ----------
    def _load_pipeline_image(self):
        """Essaie de charger un SVG ou une image raster du pipeline."""
        for p in self.PIPELINE_IMG_PATHS:
            if os.path.exists(p):
                try:
                    if p.lower().endswith(".svg"):
                        svg = SVGMobject(p, stroke_width=1)
                        return svg
                    img = ImageMobject(p)
                    return img
                except Exception:
                    continue
        return None

    def _create_step_box(self, step_title: str, step_desc: str, color):
        """Boîte d'étape robuste."""
        header = Text(step_title, font_size=22, color=color, weight=BOLD)
        body   = Text(step_desc, font_size=18, color=TEXT_COLOR, line_spacing=0.8)
        box    = VGroup(header, body).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        rect = RoundedRectangle(corner_radius=0.15, color=color, stroke_width=2)
        rect.surround(box, buffer_factor=1.15)

        return VGroup(rect, box)

# ... (les autres scènes suivent le même pattern de correction)

# ============================================================================
# SCENE 4: Stage 1 - Break Insertion (QwenA)
# ============================================================================
class SceneStage1(Scene):
    """
    Scene 4: Stage 1 - Break insertion (QwenA)
    """
    ARCH_IMG_CANDIDATES = [
        "assets/qwena_arch.svg",
        "assets/qwena_arch.png",
        "assets/stage1_architecture.svg",
        "assets/stage1_architecture.png",
        "assets/model_arch_stage1.jpg",
    ]

    def construct(self):
        # --- Titre persistant ---
        title = Text("Stage 1: Break Prediction (QwenA)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=DUR_IN)
        self.wait(PAUSE)

        # ===================== Slide 1 — Image d'architecture + résumé =====================
        arch = self._load_arch_image()
        caption = Text("Architecture (Stage 1 / QwenA)", font_size=18, color=TEXT_COLOR, slant=ITALIC)

        if arch is not None:
            max_w = config.frame_width * 0.52
            max_h = config.frame_height * 0.60
            arch.scale_to_fit_width(max_w)
            if arch.height > max_h:
                arch.scale(max_h / arch.height)
            left_col = VGroup(arch, caption).arrange(DOWN, buff=0.2, aligned_edge=CENTER)
        else:
            ph = Rectangle(width=6.2, height=3.8, color=GREY_B)
            ph_text = Text("Architecture image not found", font_size=22, color=GREY_B)
            left_col = VGroup(ph, ph_text).arrange(DOWN, buff=0.2)

        model_info = VGroup(
            Text("Model: Qwen 2.5-7B", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Fine-tuning: QLoRA (4-bit, r=8, α=16)", font_size=24, color=TEXT_COLOR),
            Text("Input: French paragraphs ≤ 200 words", font_size=24, color=TEXT_COLOR),
            Text("Output: <break> tag positions", font_size=24, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        layout = VGroup(left_col, model_info).arrange(RIGHT, buff=0.8, aligned_edge=TOP).next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(left_col, shift=LEFT), FadeIn(model_info, shift=RIGHT), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # ===================== Slide 2 — Métriques =====================
        slide_break(self, keep=title, intertitle="Performance")
        perf_box = VGroup(
            Text("Performance:", font_size=32, color=ACCENT_BLUE, weight=BOLD),
            Text("F₁ Score: 99.24%", font_size=30, color=ACCENT_YELLOW, weight=BOLD),
            Text("Perplexity: 1.001", font_size=30, color=ACCENT_YELLOW, weight=BOLD),
            Text("vs. BERT baseline: 92.06% F₁", font_size=24, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.8)

        self.play(FadeIn(perf_box, shift=UP), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # ===================== Slide 3 — Référence =====================
        slide_break(self, keep=title)
        citation = Text("Données : ICNLSP 2025, p. 7 (Table 4)", font_size=18, color=TEXT_COLOR, slant=ITALIC).to_corner(DR)
        self.play(FadeIn(citation), run_time=DUR_ELT)
        self.wait(PAUSE + 0.2)

        # Nettoyage final
        self.play(FadeOut(VGroup(title, citation)), run_time=DUR_OUT)

    # ---------- Helpers ----------
    def _load_arch_image(self):
        """Charge l'image/SVG d'architecture si disponible (sans écraser la scène en cas d'échec)."""
        for p in self.ARCH_IMG_CANDIDATES:
            try:
                if p.lower().endswith(".svg"):
                    return SVGMobject(p, stroke_width=1)
                return ImageMobject(p)
            except Exception:
                continue
        return None



# ============================================================================
# SCENE 5: Stage 2 - Prosody Values (QwenB)
# ============================================================================
class SceneStage2(Scene):
    """
    Scene 5: Stage 2 - Prosody values (QwenB)
    """
    ARCH_IMG_CANDIDATES = [
        "assets/qwenb_arch.svg",
        "assets/qwenb_arch.png",
        "assets/stage2_architecture.svg",
        "assets/stage2_architecture.png",
        "assets/model_arch_stage2.jpg",
    ]

    def construct(self):
        # --- Titre persistant ---
        title = Text("Stage 2: Prosody Prediction (QwenB)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=DUR_IN)
        self.wait(PAUSE)

        # ===================== Slide 1 — Image d'architecture + résumé =====================
        arch = self._load_arch_image()
        caption = Text("Architecture (Stage 2 / QwenB)", font_size=18, color=TEXT_COLOR, slant=ITALIC)

        if arch is not None:
            max_w = config.frame_width * 0.52
            max_h = config.frame_height * 0.60
            arch.scale_to_fit_width(max_w)
            if arch.height > max_h:
                arch.scale(max_h / arch.height)
            left_col = VGroup(arch, caption).arrange(DOWN, buff=0.2, aligned_edge=CENTER)
        else:
            ph = Rectangle(width=6.2, height=3.8, color=GREY_B)
            ph_text = Text("Architecture image not found", font_size=22, color=GREY_B)
            left_col = VGroup(ph, ph_text).arrange(DOWN, buff=0.2)

        model_info = VGroup(
            Text("Model: Qwen 2.5-7B (2nd instance)", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Fine-tuning: QLoRA adapter", font_size=24, color=TEXT_COLOR),
            Text("Input: SSML skeleton from QwenA", font_size=24, color=TEXT_COLOR),
            Text("Output: Numeric prosodic attributes", font_size=24, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        layout = VGroup(left_col, model_info).arrange(RIGHT, buff=0.8, aligned_edge=TOP).next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(left_col, shift=LEFT), FadeIn(model_info, shift=RIGHT), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # ===================== Slide 2 — Détails des features =====================
        slide_break(self, keep=title, intertitle="Prosodic Features")
        features_title = Text("Prosodic Features:", font_size=28, color=ACCENT_YELLOW, weight=BOLD)
        features = VGroup(
            Text("• Pitch: f₀ → semitone → % (±2% typical)", font_size=22, color=TEXT_COLOR),
            Text("• Volume: LUFS → gain % (~−10% typical)", font_size=22, color=TEXT_COLOR),
            Text("• Rate: words/sec → % (~−1% typical)", font_size=22, color=TEXT_COLOR),
            Text("• Break: silence gap (250–500 ms)", font_size=22, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        feat_group = VGroup(features_title, features).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=0.8)

        self.play(Write(features_title), run_time=DUR_ELT)
        self.play(FadeIn(features, shift=RIGHT), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # ===================== Slide 3 — Référence =====================
        slide_break(self, keep=title)
        citation = Text("Données : ICNLSP 2025, p. 4–5", font_size=18, color=TEXT_COLOR, slant=ITALIC).to_corner(DR)
        self.play(FadeIn(citation), run_time=DUR_ELT)
        self.wait(PAUSE + 0.2)

        # Nettoyage final
        self.play(FadeOut(VGroup(title, citation)), run_time=DUR_OUT)

    # ---------- Helpers ----------
    def _load_arch_image(self):
        """Charge l'image/SVG d'architecture si disponible (sans écraser la scène en cas d'échec)."""
        for p in self.ARCH_IMG_CANDIDATES:
            try:
                if p.lower().endswith(".svg"):
                    return SVGMobject(p, stroke_width=1)
                return ImageMobject(p)
            except Exception:
                continue
        return None


# ============================================================================
# SCENE 6: Objective Evaluation (refonte)
# ============================================================================
class SceneEvalObj(Scene):
    """
    Scene 6: Objective evaluation
    - Slide 1: F1 (barres horizontales)
    - Slide 2: MAE (table + mini barres)
    - Slide 3: Key finding + citation
    """

    def construct(self):
        # --- Titre persistant ---
        title = Text("Objective Evaluation", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=DUR_IN)
        self.wait(PAUSE)

        # ===================== Slide 1 — F1 Accuracy =====================
        f1_title = Text("Break Prediction Accuracy (F₁)", font_size=32, color=ACCENT_YELLOW, weight=BOLD)
        f1_title.next_to(title, DOWN, buff=0.6)

        # Axe horizontal 0.80 → 1.00 (lisible pour des scores élevés)
        from manim import NumberLine
        axis = NumberLine(
            x_range=[0.80, 1.00, 0.05],
            length=9.0,
            include_numbers=True,
            numbers_to_include=[0.80, 0.85, 0.90, 0.95, 1.00],
            decimal_number_config={"num_decimal_places": 2, "font_size": 20, "color": TEXT_COLOR},
            color=WHITE,
        )
        axis.next_to(f1_title, DOWN, buff=0.6)

        # Fonction utilitaire: barre horizontale ancrée au début d'axe
        def hbar(value, color, height=0.35):
            start = axis.n2p(axis.x_range[0])  # point (x) pour 0.80
            end   = axis.n2p(value)
            width = end[0] - start[0]
            bar = Rectangle(width=width, height=height, fill_opacity=0.9, fill_color=color, stroke_width=0)
            bar.set_anchor(start, aligned_edge=LEFT)
            bar.move_to(start + RIGHT * (width / 2.0))
            return bar

        # Données
        f1_ours  = 0.9924  # QwenA
        f1_bert  = 0.9206  # baseline

        bar_ours = hbar(f1_ours, ACCENT_BLUE)
        bar_bert = hbar(f1_bert, GREY_B)

        # Étiquettes à gauche des barres
        lbl_ours = Text("QwenA (Ours)", font_size=26, color=TEXT_COLOR)
        lbl_bert = Text("BERT Baseline", font_size=26, color=TEXT_COLOR)
        lbl_ours.next_to(axis, LEFT, buff=0.8).align_to(axis, UP)
        lbl_bert.next_to(axis, LEFT, buff=0.8).align_to(axis, DOWN)

        # Positionner les barres respectivement (haut/bas de l’axe)
        bar_ours.next_to(axis, UP, buff=0.25).align_to(axis, LEFT)
        bar_bert.next_to(axis, DOWN, buff=0.25).align_to(axis, LEFT)

        # Valeurs à droite des barres
        val_ours = Text("99.24%", font_size=24, color=ACCENT_YELLOW, weight=BOLD).next_to(bar_ours, RIGHT, buff=0.25)
        val_bert = Text("92.06%", font_size=24, color=TEXT_COLOR).next_to(bar_bert, RIGHT, buff=0.25)

        f1_group = VGroup(
            f1_title, axis, bar_ours, bar_bert, lbl_ours, lbl_bert, val_ours, val_bert
        )

        self.play(Write(f1_title), run_time=DUR_ELT)
        self.play(Create(axis), run_time=DUR_ELT)
        self.play(FadeIn(VGroup(lbl_ours, lbl_bert), shift=LEFT), run_time=DUR_ELT)
        self.play(FadeIn(bar_ours, shift=RIGHT), FadeIn(val_ours, shift=RIGHT), run_time=DUR_IN)
        self.play(FadeIn(bar_bert, shift=RIGHT), FadeIn(val_bert, shift=RIGHT), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # Transition nette vers Slide 2 (on garde le titre)
        slide_break(self, keep=title, intertitle="Mean Absolute Error (MAE)")

        # ===================== Slide 2 — MAE (table visuelle) =====================
        mae_title = Text("Mean Absolute Error (MAE) — Lower is better", font_size=28, color=ACCENT_YELLOW, weight=BOLD)
        mae_title.next_to(title, DOWN, buff=0.6)

        # Construit une ligne (libellé + mini-axe + 2 barres + valeurs)
        def mae_row(label, ours_val, base_val, max_scale=6.5):
            row_label = Text(label, font_size=24, color=TEXT_COLOR).scale(1.0)

            mini_axis = NumberLine(
                x_range=[0.0, max_scale, max_scale/5],
                length=6.5,
                include_numbers=True,
                numbers_to_include=[0, round(max_scale/2,1), max_scale],
                decimal_number_config={"num_decimal_places": 1, "font_size": 18, "color": TEXT_COLOR},
                color=WHITE,
            )

            # mini-barres (réutilisation simple)
            def mini_bar(v, color):
                start = mini_axis.n2p(mini_axis.x_range[0])
                end   = mini_axis.n2p(min(v, max_scale))
                width = end[0] - start[0]
                bar = Rectangle(width=width, height=0.28, fill_opacity=0.9, fill_color=color, stroke_width=0)
                bar.set_anchor(start, aligned_edge=LEFT)
                bar.move_to(start + RIGHT * (width / 2.0))
                return bar

            bar_o = mini_bar(ours_val, ACCENT_BLUE)
            bar_b = mini_bar(base_val, GREY_B)

            # positionnement: bar_o au-dessus, bar_b au-dessous
            bar_o.next_to(mini_axis, UP, buff=0.15).align_to(mini_axis, LEFT)
            bar_b.next_to(mini_axis, DOWN, buff=0.15).align_to(mini_axis, LEFT)

            val_o = Text(f"{ours_val:.2f}%", font_size=22, color=ACCENT_YELLOW, weight=BOLD).next_to(bar_o, RIGHT, buff=0.25)
            val_b = Text(f"{base_val:.2f}%", font_size=22, color=TEXT_COLOR).next_to(bar_b, RIGHT, buff=0.25)

            row = VGroup(row_label, VGroup(mini_axis, bar_o, bar_b, val_o, val_b).arrange(DOWN, buff=0.08, aligned_edge=LEFT)).arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
            return row

        # Données (%, depuis ton texte)
        row_pitch  = mae_row("Pitch",  0.97, 1.68, max_scale=6.5)
        row_volume = mae_row("Volume", 1.09, 6.04, max_scale=6.5)
        row_rate   = mae_row("Rate",   1.10, 0.84, max_scale=6.5)

        table = VGroup(row_pitch, row_volume, row_rate).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        table.next_to(mae_title, DOWN, buff=0.5).align_to(mae_title, LEFT)

        self.play(Write(mae_title), run_time=DUR_ELT)
        self.play(FadeIn(row_pitch, shift=UP), run_time=DUR_IN)
        self.play(FadeIn(row_volume, shift=UP), run_time=DUR_IN)
        self.play(FadeIn(row_rate, shift=UP), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # ===================== Slide 3 — Key finding + citation =====================
        slide_break(self, keep=title)
        key_finding = Text(
            "25–40% MAE reduction vs. baselines",
            font_size=30, color=ACCENT_BLUE, weight=BOLD
        ).next_to(title, DOWN, buff=0.8)

        citation = Text(
            "Données : ICNLSP 2025, p. 7",
            font_size=18, color=TEXT_COLOR, slant=ITALIC
        ).to_corner(DR)

        self.play(FadeIn(key_finding, shift=UP), run_time=DUR_IN)
        self.play(FadeIn(citation), run_time=DUR_ELT)
        self.wait(PAUSE + 0.2)

        # Nettoyage final
        self.play(FadeOut(VGroup(title, key_finding, citation)), run_time=DUR_OUT)


# ============================================================================
# SCENE 7: Subjective Evaluation (refonte en 3 slides)
# ============================================================================
class SceneEvalSubj(Scene):
    """
    Scene 7: Subjective evaluation
    - Slide 1: Study design (protocole)
    - Slide 2: MOS (barres 0–5)
    - Slide 3: Préférence + citation
    """

    def construct(self):
        # --- Titre persistant ---
        title = Text("Subjective Evaluation (AB Test)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=DUR_IN)
        self.wait(PAUSE)

        # ===================== Slide 1 — Study design =====================
        study_title = Text("Study Design", font_size=32, color=ACCENT_YELLOW, weight=BOLD)
        study_title.next_to(title, DOWN, buff=0.6)

        study_items = VGroup(
            self._bullet("18 participants"),
            self._bullet("30 audio pairs (≈ 1 min each)"),
            self._bullet("Baseline vs. SSML-enhanced"),
            self._bullet("AB forced-choice + MOS"),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(study_title, DOWN, buff=0.45)

        self.play(Write(study_title), run_time=DUR_ELT)
        self.play(FadeIn(study_items, shift=UP), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # Transition nette (on garde le titre)
        slide_break(self, keep=title, intertitle="Mean Opinion Score (MOS)")

        # ===================== Slide 2 — MOS (0–5) =====================
        mos_title = Text("Mean Opinion Score (0–5, higher is better)", font_size=28, color=ACCENT_YELLOW, weight=BOLD)
        mos_title.next_to(title, DOWN, buff=0.6)

        # Axe 0–5
        axis = NumberLine(
            x_range=[0, 5, 1],
            length=9.0,
            include_numbers=True,
            decimal_number_config={"num_decimal_places": 0, "font_size": 20, "color": TEXT_COLOR},
            color=WHITE,
        )
        axis.next_to(mos_title, DOWN, buff=0.6)

        # Barres MOS (Baseline 3.20 ; Enhanced 3.87)
        baseline = 3.20
        enhanced = 3.87

        bar_base = self._hbar(axis, baseline, GREY_B, height=0.38)
        bar_enh  = self._hbar(axis, enhanced, ACCENT_BLUE, height=0.38)

        lbl_base = Text("Baseline", font_size=26, color=TEXT_COLOR).next_to(axis, LEFT, buff=0.8).align_to(axis, UP)
        lbl_enh  = Text("SSML-enhanced", font_size=26, color=TEXT_COLOR).next_to(axis, LEFT, buff=0.8).align_to(axis, DOWN)

        bar_base.next_to(axis, UP, buff=0.22).align_to(axis, LEFT)
        bar_enh.next_to(axis, DOWN, buff=0.22).align_to(axis, LEFT)

        val_base = Text(f"{baseline:.2f}", font_size=24, color=TEXT_COLOR).next_to(bar_base, RIGHT, buff=0.25)
        val_enh  = Text(f"{enhanced:.2f}  (+0.67, +20%)", font_size=24, color=ACCENT_YELLOW, weight=BOLD).next_to(bar_enh, RIGHT, buff=0.25)

        pvalue = Text("p < 0.005 (statistically significant)", font_size=22, color=ACCENT_YELLOW, slant=ITALIC).next_to(axis, DOWN, buff=1.1)

        self.play(Write(mos_title), run_time=DUR_ELT)
        self.play(Create(axis), run_time=DUR_ELT)
        self.play(FadeIn(VGroup(lbl_base, lbl_enh), shift=LEFT), run_time=DUR_ELT)
        self.play(FadeIn(bar_base, shift=RIGHT), FadeIn(val_base, shift=RIGHT), run_time=DUR_IN)
        self.play(FadeIn(bar_enh,  shift=RIGHT), FadeIn(val_enh,  shift=RIGHT), run_time=DUR_IN)
        self.play(FadeIn(pvalue), run_time=DUR_ELT)
        self.wait(PAUSE + 0.2)

        # Transition nette (on garde le titre)
        slide_break(self, keep=title, intertitle="Preference")

        # ===================== Slide 3 — Préférence + citation =====================
        pref = Text(
            "15 of 18 participants preferred the SSML-enhanced version",
            font_size=28, color=ACCENT_BLUE, weight=BOLD
        ).next_to(title, DOWN, buff=0.8)

        citation = Text(
            "Données : ICNLSP 2025, p. 6",
            font_size=18, color=TEXT_COLOR, slant=ITALIC
        ).to_corner(DR)

        self.play(FadeIn(pref, shift=UP), run_time=DUR_IN)
        self.play(FadeIn(citation), run_time=DUR_ELT)
        self.wait(PAUSE + 0.2)

        # Nettoyage final
        self.play(FadeOut(VGroup(title, pref, citation)), run_time=DUR_OUT)

    # ---------- Helpers ----------
    def _bullet(self, text: str):
        """Un item de liste lisible sur fond sombre."""
        dot = Dot(radius=0.06, color=ACCENT_YELLOW)
        lbl = Text(text, font_size=24, color=TEXT_COLOR)
        g = VGroup(dot, lbl).arrange(RIGHT, buff=0.35, aligned_edge=ORIGIN)
        return g

    def _hbar(self, number_line: NumberLine, value: float, color, height=0.35):
        """Crée une barre horizontale alignée sur un NumberLine, de 0 jusqu'à 'value'."""
        start = number_line.n2p(number_line.x_range[0])
        end   = number_line.n2p(min(value, number_line.x_range[1]))
        width = end[0] - start[0]
        bar = Rectangle(width=width, height=height, fill_opacity=0.92, fill_color=color, stroke_width=0)
        bar.set_anchor(start, aligned_edge=LEFT)
        bar.move_to(start + RIGHT * (width / 2.0))
        return bar

# ============================================================================
# SCENE 8: Conclusions (refonte en 3 slides)
# ============================================================================
class SceneOutro(Scene):
    """
    Scene 8: Conclusions
    - Slide 1: Key achievements
    - Slide 2: Future work + lien
    - Slide 3: Merci + citation
    """
    def construct(self):
        # --- Titre persistant ---
        title = Text("Conclusions & Future Directions", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=DUR_IN)
        self.wait(PAUSE)

        # ===================== Slide 1 — Achievements =====================
        ach_title = Text("Key Achievements", font_size=32, color=ACCENT_YELLOW, weight=BOLD)
        ach_title.next_to(title, DOWN, buff=0.6)

        achievements = VGroup(
            self._tick("99.2% F₁ break placement"),
            self._tick("25–40% MAE reduction"),
            self._tick("MOS 3.20 → 3.87 (≈ +20%)"),
            self._tick("First comprehensive French SSML pipeline"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ach_title, DOWN, buff=0.45)

        self.play(Write(ach_title), run_time=DUR_ELT)
        self.play(FadeIn(achievements, shift=UP), run_time=DUR_IN)
        self.wait(PAUSE + 0.2)

        # Transition nette (on garde le titre)
        slide_break(self, keep=title, intertitle="Future Work")

        # ===================== Slide 2 — Future work =====================
        fw_title = Text("Future Work", font_size=32, color=ACCENT_YELLOW, weight=BOLD)
        fw_title.next_to(title, DOWN, buff=0.6)

        future = VGroup(
            self._arrow("Unified end-to-end model"),
            self._arrow("Multimodal audio embeddings"),
            self._arrow("Extension to other languages"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(fw_title, DOWN, buff=0.45)

        # Lien GitHub dans un badge afin d’éviter le chevauchement en bas d’écran
        badge = RoundedRectangle(corner_radius=0.15, color=ACCENT_BLUE, stroke_width=2)
        gh_text = Text("github.com/hi-paris/Prosody-Control-French-TTS", font_size=20, color=ACCENT_BLUE, slant=ITALIC)
        badge.surround(gh_text, buffer_factor=1.25)
        github = VGroup(badge, gh_text).to_edge(DOWN, buff=0.8)

        self.play(Write(fw_title), run_time=DUR_ELT)
        self.play(FadeIn(future, shift=UP), run_time=DUR_IN)
        self.play(FadeIn(github), run_time=DUR_ELT)
        self.wait(PAUSE + 0.2)

        # Transition nette (on garde le titre)
        slide_break(self, keep=title)

        # ===================== Slide 3 — Merci + citation =====================
        thanks = Text("Merci / Thank You", font_size=48, color=ACCENT_YELLOW, weight=BOLD).next_to(title, DOWN, buff=0.9)
        citation = Text("Données : ICNLSP 2025, p. 8", font_size=18, color=TEXT_COLOR, slant=ITALIC).to_corner(DR)

        self.play(FadeIn(thanks, scale=1.05), run_time=DUR_IN)
        self.play(FadeIn(citation), run_time=DUR_ELT)
        self.wait(PAUSE + 0.6)

        # Nettoyage final
        self.play(FadeOut(VGroup(title, thanks, citation)), run_time=DUR_OUT)

    # ---------- Helpers ----------
    def _tick(self, text: str):
        """Ligne avec ✓ lisible sur fond sombre."""
        mark = Text("✓", font_size=28, color=ACCENT_YELLOW, weight=BOLD)
        lbl  = Text(text, font_size=26, color=TEXT_COLOR)
        return VGroup(mark, lbl).arrange(RIGHT, buff=0.35)

    def _arrow(self, text: str):
        """Ligne avec flèche fine pour 'Future Work'."""
        mark = Text("→", font_size=28, color=ACCENT_YELLOW, weight=BOLD)
        lbl  = Text(text, font_size=24, color=TEXT_COLOR)
        return VGroup(mark, lbl).arrange(RIGHT, buff=0.35)

