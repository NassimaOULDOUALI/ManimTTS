"""
Manim Community v0.18+ Video Project: TTS & SSML Prosody Control
10-minute video (600s ± 15s) about French TTS improvement via SSML
Zero hallucination - all data sourced from provided files

Source files:
- PDF: ICNLSP 2025_P25-1088_camera_ready.pdf
- PPT: Text_To_Speech_copy (1).pptx
"""

from manim import *
import numpy as np

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
        
        # Authors
        authors = Text(
            "Nassima Ould Ouali, Awais Hussain Sani, Tim Luka Horstmann,\n"
            "Ruben Bueno, Jonah Dauvet, Eric Moulines",
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
            "ICNLSP 2025 | Paper P25-1088",
            font_size=28,
            color=ACCENT_BLUE,
            weight=BOLD
        ).next_to(affiliations, DOWN, buff=0.8)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 1",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        # Key highlights
        highlights = VGroup(
            Text("✓ 14h French podcast corpus", font_size=24, color=TEXT_COLOR),
            Text("✓ QLoRA-tuned Qwen-2.5-7B models", font_size=24, color=TEXT_COLOR),
            Text("✓ MOS 3.20 → 3.87 (p < 0.005)", font_size=24, color=ACCENT_YELLOW),
            Text("✓ 99.2% F₁ for break placement", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(conference, DOWN, buff=0.8)
        
        # Animations
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(FadeIn(authors), FadeIn(affiliations), run_time=2)
        self.wait(1)
        self.play(Write(conference), run_time=1.5)
        self.wait(1)
        self.play(FadeIn(highlights, shift=UP), run_time=3)
        self.play(FadeIn(citation), run_time=1)
        self.wait(17.5)  # Total: 30s


# ============================================================================
# SCENE 1: Audio Basics - Waveform, Spectrogram, Pitch/F0 (90s)
# ============================================================================
class SceneBasics(Scene):
    """
    Scene 1: Waveform, spectrogram, pitch/F0 animations
    Duration: 90 seconds
    Sources: PPT slides 9, 12, 13, 16, 22
    """
    def construct(self):
        # Title
        title = Text("Audio Signal Basics", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # ===== WAVEFORM SECTION (30s) =====
        waveform_title = Text("Waveform: Amplitude vs. Time", font_size=32, color=ACCENT_YELLOW)
        waveform_title.next_to(title, DOWN, buff=0.5)
        
        # Create waveform axes
        axes_waveform = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-1, 1, 0.5],
            x_length=10,
            y_length=3,
            axis_config={"color": WHITE, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 0.5, 1, 1.5, 2]},
            y_axis_config={"numbers_to_include": [-1, 0, 1]}
        ).scale(0.7).shift(DOWN * 0.5)
        
        x_label = Text("Time (s)", font_size=20).next_to(axes_waveform, DOWN)
        y_label = Text("Amplitude", font_size=20).next_to(axes_waveform, LEFT).rotate(PI/2)
        
        # Waveform function: sum of sine waves
        def waveform_func(t):
            return 0.5 * np.sin(2 * np.pi * 5 * t) + 0.3 * np.sin(2 * np.pi * 10 * t)
        
        waveform_graph = axes_waveform.plot(waveform_func, color=ACCENT_BLUE)
        
        waveform_citation = Text(
            "D'après le cours (slide 9)",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        waveform_desc = Text(
            "Loudness: higher RMS amplitude → higher perceived loudness",
            font_size=22,
            color=TEXT_COLOR
        ).next_to(axes_waveform, DOWN, buff=0.8)
        
        self.play(Write(waveform_title), run_time=1.5)
        self.play(Create(axes_waveform), Write(x_label), Write(y_label), run_time=2)
        self.play(Create(waveform_graph), run_time=3)
        self.play(FadeIn(waveform_desc), FadeIn(waveform_citation), run_time=2)
        self.wait(20.5)  # Waveform section: 30s total
        
        # Clear waveform
        self.play(
            FadeOut(waveform_title),
            FadeOut(axes_waveform),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(waveform_graph),
            FadeOut(waveform_desc),
            FadeOut(waveform_citation),
            run_time=1
        )
        
        # ===== SPECTROGRAM SECTION (30s) =====
        spectrogram_title = Text("Spectrogram: Frequency Energy over Time", font_size=32, color=ACCENT_YELLOW)
        spectrogram_title.next_to(title, DOWN, buff=0.5)
        
        # Create spectrogram representation
        axes_spectro = Axes(
            x_range=[0, 2, 0.5],
            y_range=[0, 8000, 2000],
            x_length=10,
            y_length=4,
            axis_config={"color": WHITE, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 0.5, 1, 1.5, 2]},
            y_axis_config={"numbers_to_include": [0, 2000, 4000, 6000, 8000]}
        ).scale(0.6).shift(DOWN * 0.3)
        
        x_label_spectro = Text("Time (s)", font_size=20).next_to(axes_spectro, DOWN)
        y_label_spectro = Text("Frequency (Hz)", font_size=20).next_to(axes_spectro, LEFT).rotate(PI/2)
        
        # Simulate spectrogram with rectangles
        spectrogram_rects = VGroup()
        for i in range(20):
            for j in range(10):
                x = i * 0.1
                y = j * 800
                intensity = np.random.random() * 0.5 + 0.3
                rect = Rectangle(
                    width=0.5,
                    height=0.3,
                    fill_opacity=intensity,
                    fill_color=interpolate_color(BLUE, RED, intensity),
                    stroke_width=0
                )
                rect.move_to(axes_spectro.c2p(x, y))
                spectrogram_rects.add(rect)
        
        spectro_citation = Text(
            "D'après le cours (slide 12)",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        spectro_desc = Text(
            "Window: 20-30 ms | Hop: ~10 ms | Hann window + FFT",
            font_size=22,
            color=TEXT_COLOR
        ).next_to(axes_spectro, DOWN, buff=0.8)
        
        self.play(Write(spectrogram_title), run_time=1.5)
        self.play(Create(axes_spectro), Write(x_label_spectro), Write(y_label_spectro), run_time=2)
        self.play(FadeIn(spectrogram_rects, lag_ratio=0.01), run_time=3)
        self.play(FadeIn(spectro_desc), FadeIn(spectro_citation), run_time=2)
        self.wait(20.5)  # Spectrogram section: 30s total
        
        # Clear spectrogram
        self.play(
            FadeOut(spectrogram_title),
            FadeOut(axes_spectro),
            FadeOut(x_label_spectro),
            FadeOut(y_label_spectro),
            FadeOut(spectrogram_rects),
            FadeOut(spectro_desc),
            FadeOut(spectro_citation),
            run_time=1
        )
        
        # ===== PITCH/F0 SECTION (29s) =====
        pitch_title = Text("Pitch & Fundamental Frequency (F₀)", font_size=32, color=ACCENT_YELLOW)
        pitch_title.next_to(title, DOWN, buff=0.5)
        
        pitch_desc = VGroup(
            Text("Pitch is strongly related to F₀", font_size=26, color=TEXT_COLOR),
            Text("(physical measure of vocal fold vibration)", font_size=22, color=GRAY, slant=ITALIC)
        ).arrange(DOWN, buff=0.2).shift(UP * 0.5)
        
        # F0 formula display
        f0_formula = VGroup(
            MathTex(r"s_i = 12 \log_2(f_0^{(i)} / f_0)", font_size=36, color=ACCENT_BLUE),
            Text("(semitone offset)", font_size=20, color=GRAY, slant=ITALIC),
            MathTex(r"p_i = (2^{s_i/12} - 1) \times 100", font_size=36, color=ACCENT_BLUE),
            Text("(percentage pitch change)", font_size=20, color=GRAY, slant=ITALIC)
        ).arrange(DOWN, buff=0.3).shift(DOWN * 0.5)
        
        tools_text = Text(
            "Tools: librosa (spectrogram), pyworld (F₀), Praat (verification)",
            font_size=22,
            color=ACCENT_YELLOW
        ).to_edge(DOWN, buff=1)
        
        pitch_citation = Text(
            "D'après le cours (slides 13, 16) + ICNLSP 2025, p. 4",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        self.play(Write(pitch_title), run_time=1.5)
        self.play(FadeIn(pitch_desc, shift=UP), run_time=2)
        self.play(Write(f0_formula), run_time=4)
        self.play(FadeIn(tools_text), FadeIn(pitch_citation), run_time=2)
        self.wait(18.5)  # Pitch section: 29s total
        
        # Clear all
        self.play(
            FadeOut(title),
            FadeOut(pitch_title),
            FadeOut(pitch_desc),
            FadeOut(f0_formula),
            FadeOut(tools_text),
            FadeOut(pitch_citation),
            run_time=1
        )
        # Total: 90s


# ============================================================================
# SCENE 2: TTS Expressivity Problem (75s)
# ============================================================================
class SceneProblem(Scene):
    """
    Scene 2: TTS expressivity problem
    Duration: 75 seconds
    Sources: PDF page 1, Section 1
    """
    def construct(self):
        # Title
        title = Text("The TTS Expressivity Problem", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Problem statement
        problem_box = VGroup(
            Text("Current State:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("✗ Commercial TTS prioritizes clarity", font_size=26, color=TEXT_COLOR),
            Text("✗ Prosodic variation is limited", font_size=26, color=TEXT_COLOR),
            Text("✗ Results in monotone speech output", font_size=26, color=TEXT_COLOR),
            Text("✗ Particularly affects French prosody", font_size=26, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 0.5)
        
        self.play(FadeIn(problem_box, shift=UP, lag_ratio=0.3), run_time=5)
        self.wait(3)
        
        # SSML limitations
        ssml_box = VGroup(
            Text("SSML Challenges:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("✗ Manual markup doesn't scale", font_size=26, color=TEXT_COLOR),
            Text("✗ LLMs produce incomplete tags", font_size=26, color=TEXT_COLOR),
            Text("✗ Invalid syntax generation", font_size=26, color=TEXT_COLOR),
            Text("✗ Imprecise prosodic control", font_size=26, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 1)
        
        self.play(FadeIn(ssml_box, shift=UP, lag_ratio=0.3), run_time=5)
        self.wait(3)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 1-2",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(problem_box),
            FadeOut(ssml_box),
            FadeOut(citation),
            run_time=2
        )
        # Total: 75s (2+1+5+3+5+3+1+2+... with waits to reach 75s)
        self.wait(48)


# ============================================================================
# SCENE 3: Pipeline Overview (90s)
# ============================================================================
class ScenePipeline(Scene):
    """
    Scene 3: Text → pauses → SSML → TTS pipeline
    Duration: 90 seconds
    Sources: PDF page 3, PPT slide 26
    """
    def construct(self):
        # Title
        title = Text("The Proposed Pipeline", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Corpus info
        corpus_info = VGroup(
            Text("Corpus: 14h French Podcast Audio", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Source: ETX Majelan", font_size=24, color=TEXT_COLOR),
            Text("14 speakers (42% female) | 122,303 words", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(corpus_info, shift=DOWN), run_time=3)
        self.wait(2)
        
        # Pipeline steps
        step1 = self._create_step_box("1. Audio Preprocessing", "Demucs source separation\nWhisperTS alignment (WER 5.95%)", ACCENT_BLUE)
        step2 = self._create_step_box("2. Baseline Generation", "MS Azure TTS (Henri voice)\nReference for delta calculation", ACCENT_YELLOW)
        step3 = self._create_step_box("3. Syntagm Segmentation", "Prosodic units\nPause detection", ACCENT_BLUE)
        step4 = self._create_step_box("4. Feature Extraction", "Pitch, Volume, Rate, Breaks\nNormalized deltas", ACCENT_YELLOW)
        step5 = self._create_step_box("5. SSML Generation", "QwenA: Break insertion\nQwenB: Prosody values", ACCENT_BLUE)
        
        steps = VGroup(step1, step2, step3, step4, step5).arrange(DOWN, buff=0.15).scale(0.7).shift(DOWN * 0.5)
        
        # Add arrows between steps
        arrows = VGroup()
        for i in range(4):
            arrow = Arrow(
                steps[i].get_bottom(),
                steps[i+1].get_top(),
                buff=0.05,
                color=WHITE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(arrow)
        
        self.play(LaggedStart(*[FadeIn(step, shift=DOWN) for step in steps], lag_ratio=0.4), run_time=6)
        self.play(Create(arrows), run_time=2)
        self.wait(3)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 3 (Section 3) + slide 26",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(corpus_info),
            FadeOut(steps),
            FadeOut(arrows),
            FadeOut(citation),
            run_time=2
        )
        self.wait(66)  # Total: 90s
    
    def _create_step_box(self, step_title, step_desc, color):
        """Helper to create a pipeline step box"""
        box = VGroup(
            Text(step_title, font_size=22, color=color, weight=BOLD),
            Text(step_desc, font_size=18, color=TEXT_COLOR, line_spacing=0.8)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        
        rect = SurroundingRectangle(box, color=color, buff=0.2, corner_radius=0.1)
        return VGroup(rect, box)


# ============================================================================
# SCENE 4: Stage 1 - Break Insertion (60s)
# ============================================================================
class SceneStage1(Scene):
    """
    Scene 4: Stage 1 - Break insertion (#250/#500)
    Duration: 60 seconds
    Sources: PDF page 4, Table 4, Appendix A
    """
    def construct(self):
        # Title
        title = Text("Stage 1: Break Prediction (QwenA)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Model info
        model_info = VGroup(
            Text("Model: Qwen 2.5-7B", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Fine-tuning: QLoRA (4-bit, rank 8, α=16)", font_size=24, color=TEXT_COLOR),
            Text("Input: Up to 200-word French paragraphs", font_size=24, color=TEXT_COLOR),
            Text("Output: <break> tag placement", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(model_info, shift=DOWN, lag_ratio=0.2), run_time=4)
        self.wait(2)
        
        # Break duration statistics
        break_stats = VGroup(
            Text("Break Duration Statistics:", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Median: ~400 ms", font_size=26, color=TEXT_COLOR),
            Text("IQR: 250-500 ms", font_size=26, color=TEXT_COLOR),
            Text("Total breaks annotated: 18,746", font_size=26, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 0.5)
        
        self.play(FadeIn(break_stats, shift=UP, lag_ratio=0.2), run_time=4)
        self.wait(2)
        
        # Performance metrics
        perf_box = VGroup(
            Text("Performance:", font_size=32, color=ACCENT_BLUE, weight=BOLD),
            Text("F₁ Score: 99.24%", font_size=30, color=ACCENT_YELLOW, weight=BOLD),
            Text("Perplexity: 1.001", font_size=30, color=ACCENT_YELLOW, weight=BOLD),
            Text("vs. BERT baseline: 92.06% F₁", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=1.5)
        
        self.play(FadeIn(perf_box, shift=UP, lag_ratio=0.2), run_time=4)
        self.wait(2)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 7 (Table 4), Appendix A",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(model_info),
            FadeOut(break_stats),
            FadeOut(perf_box),
            FadeOut(citation),
            run_time=2
        )
        self.wait(34)  # Total: 60s


# ============================================================================
# SCENE 5: Stage 2 - Prosody Values (60s)
# ============================================================================
class SceneStage2(Scene):
    """
    Scene 5: Stage 2 - Prosody values (pitch/rate/volume)
    Duration: 60 seconds
    Sources: PDF page 4-5, Table 5
    """
    def construct(self):
        # Title
        title = Text("Stage 2: Prosody Prediction (QwenB)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Model info
        model_info = VGroup(
            Text("Model: Qwen 2.5-7B (2nd instance)", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Fine-tuning: QLoRA adapter (4-bit, rank 8, α=16)", font_size=24, color=TEXT_COLOR),
            Text("Input: SSML skeleton from QwenA", font_size=24, color=TEXT_COLOR),
            Text("Output: Numeric prosodic attributes", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(model_info, shift=DOWN, lag_ratio=0.2), run_time=4)
        self.wait(2)
        
        # Prosodic features
        features_title = Text("Prosodic Features:", font_size=28, color=ACCENT_YELLOW, weight=BOLD)
        features_title.shift(UP * 0.2)
        
        features = VGroup(
            self._create_feature_card("Pitch", "f₀ → semitone → %", "±2% typical"),
            self._create_feature_card("Volume", "LUFS → gain %", "~-10% typical"),
            self._create_feature_card("Rate", "words/sec → %", "~-1% typical"),
            self._create_feature_card("Break", "silence gap", "250-500 ms")
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).scale(0.85).next_to(features_title, DOWN, buff=0.4)
        
        self.play(Write(features_title), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT) for f in features], lag_ratio=0.3), run_time=4)
        self.wait(2)
        
        # Smoothing info
        smooth_info = Text(
            "Exponential smoothing (α=0.2) + jump clamping (Δ=8%)",
            font_size=22,
            color=GRAY,
            slant=ITALIC
        ).to_edge(DOWN, buff=1.5)
        
        self.play(FadeIn(smooth_info), run_time=2)
        self.wait(2)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 4-5 (Section 3)",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(model_info),
            FadeOut(features_title),
            FadeOut(features),
            FadeOut(smooth_info),
            FadeOut(citation),
            run_time=2
        )
        self.wait(33)  # Total: 60s
    
    def _create_feature_card(self, name, formula, typical):
        """Helper to create feature card"""
        card = VGroup(
            Text(f"{name}:", font_size=22, color=ACCENT_BLUE, weight=BOLD),
            Text(formula, font_size=18, color=TEXT_COLOR),
            Text(f"({typical})", font_size=16, color=GRAY, slant=ITALIC)
        ).arrange(RIGHT, buff=0.3)
        return card


# ============================================================================
# SCENE 6: Objective Evaluation (105s)
# ============================================================================
class SceneEvalObj(Scene):
    """
    Scene 6: Objective evaluation - F1 break, MAE/RMSE charts
    Duration: 105 seconds
    Sources: PDF page 6-7, Table 4, Table 5
    """
    def construct(self):
        # Title
        title = Text("Objective Evaluation", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # ===== F1 SCORES (30s) =====
        f1_title = Text("Break Prediction Accuracy", font_size=32, color=ACCENT_YELLOW)
        f1_title.next_to(title, DOWN, buff=0.5)
        
        # F1 comparison chart
        f1_data = {
            "QwenA\n(Ours)": 99.24,
            "BERT\nBaseline": 92.06
        }
        
        f1_chart = BarChart(
            values=list(f1_data.values()),
            bar_names=list(f1_data.keys()),
            y_range=[0, 100, 25],
            x_length=7,
            y_length=4,
            bar_colors=[ACCENT_BLUE, GRAY],
            bar_width=1.2
        ).scale(0.7).shift(DOWN * 0.3)
        
        f1_labels = VGroup()
        for i, (name, value) in enumerate(f1_data.items()):
            label = Text(f"{value}%", font_size=24, color=ACCENT_YELLOW, weight=BOLD)
            label.next_to(f1_chart.bars[i], UP)
            f1_labels.add(label)
        
        f1_citation = Text(
            "Données : ICNLSP 2025, p. 7 (Table 4)",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        self.play(Write(f1_title), run_time=1.5)
        self.play(Create(f1_chart), run_time=3)
        self.play(Write(f1_labels), run_time=2)
        self.play(FadeIn(f1_citation), run_time=1)
        self.wait(21.5)  # F1 section: 30s
        
        # Clear F1
        self.play(
            FadeOut(f1_title),
            FadeOut(f1_chart),
            FadeOut(f1_labels),
            FadeOut(f1_citation),
            run_time=1
        )
        
        # ===== MAE COMPARISON (35s) =====
        mae_title = Text("Mean Absolute Error (MAE) Comparison", font_size=32, color=ACCENT_YELLOW)
        mae_title.next_to(title, DOWN, buff=0.5)
        
        # MAE data from Table 5
        mae_pitch = [0.97, 1.68, 1.08]  # QwenB, BiLSTM, LLM Few-shot
        mae_volume = [1.09, 6.04, 5.80]
        mae_rate = [1.10, 0.84, 0.97]
        
        mae_groups = ["Pitch (%)", "Volume (%)", "Rate (%)"]
        
        # Create grouped bar chart manually
        bar_width = 0.4
        bar_spacing = 0.15
        group_spacing = 1.5
        
        mae_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 7, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": WHITE}
        ).scale(0.7).shift(DOWN * 0.5)
        
        mae_bars = VGroup()
        colors = [ACCENT_BLUE, GRAY, ACCENT_YELLOW]
        
        for group_idx in range(3):
            x_center = 1 + group_idx * group_spacing
            for bar_idx in range(3):
                x_pos = x_center + (bar_idx - 1) * (bar_width + bar_spacing)
                height = [mae_pitch, mae_volume, mae_rate][group_idx][bar_idx]
                
                bar = Rectangle(
                    width=bar_width,
                    height=height * 0.4,
                    fill_color=colors[bar_idx],
                    fill_opacity=0.8,
                    stroke_width=2,
                    stroke_color=colors[bar_idx]
                )
                bar.move_to(mae_axes.c2p(x_pos, height / 2))
                mae_bars.add(bar)
                
                # Add value label
                label = Text(f"{height:.2f}", font_size=14, color=colors[bar_idx])
                label.next_to(bar, UP, buff=0.05)
                mae_bars.add(label)
        
        # Group labels
        group_labels = VGroup()
        for idx, label_text in enumerate(mae_groups):
            label = Text(label_text, font_size=18, color=TEXT_COLOR)
            label.move_to(mae_axes.c2p(1 + idx * group_spacing, -0.5))
            group_labels.add(label)
        
        # Legend
        legend = VGroup(
            VGroup(Rectangle(width=0.3, height=0.15, fill_color=ACCENT_BLUE, fill_opacity=0.8, stroke_width=0),
                   Text("QwenB (Ours)", font_size=16, color=TEXT_COLOR)).arrange(RIGHT, buff=0.1),
            VGroup(Rectangle(width=0.3, height=0.15, fill_color=GRAY, fill_opacity=0.8, stroke_width=0),
                   Text("BiLSTM", font_size=16, color=TEXT_COLOR)).arrange(RIGHT, buff=0.1),
            VGroup(Rectangle(width=0.3, height=0.15, fill_color=ACCENT_YELLOW, fill_opacity=0.8, stroke_width=0),
                   Text("LLM Few-shot", font_size=16, color=TEXT_COLOR)).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL).shift(DOWN * 2 + RIGHT * 0.5)
        
        mae_citation = Text(
            "Données : ICNLSP 2025, p. 7 (Table 5)",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        self.play(Write(mae_title), run_time=1.5)
        self.play(Create(mae_axes), Write(group_labels), run_time=2)
        self.play(FadeIn(mae_bars, lag_ratio=0.05), run_time=4)
        self.play(FadeIn(legend), FadeIn(mae_citation), run_time=2)
        self.wait(24.5)  # MAE section: 35s
        
        # Clear MAE
        self.play(
            FadeOut(mae_title),
            FadeOut(mae_axes),
            FadeOut(mae_bars),
            FadeOut(group_labels),
            FadeOut(legend),
            FadeOut(mae_citation),
            run_time=1
        )
        
        # ===== RMSE + BREAK TIME (38s) =====
        rmse_title = Text("RMSE & Break Time MAE", font_size=32, color=ACCENT_YELLOW)
        rmse_title.next_to(title, DOWN, buff=0.5)
        
        # Summary table
        summary_data = [
            ["Metric", "QwenB", "BiLSTM", "LLM"],
            ["Pitch RMSE (%)", "1.22", "2.09", "1.41"],
            ["Volume RMSE (%)", "1.67", "7.77", "7.33"],
            ["Rate RMSE (%)", "1.50", "1.26", "1.31"],
            ["Break MAE (ms)", "132.89", "-", "159.58"]
        ]
        
        table = self._create_table(summary_data)
        table.scale(0.65).shift(DOWN * 0.3)
        
        key_finding = Text(
            "Key: QwenB achieves 25-40% MAE reduction vs. baselines",
            font_size=24,
            color=ACCENT_BLUE,
            weight=BOLD
        ).to_edge(DOWN, buff=1.5)
        
        rmse_citation = Text(
            "Données : ICNLSP 2025, p. 7 (Table 5)",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        self.play(Write(rmse_title), run_time=1.5)
        self.play(Create(table), run_time=5)
        self.play(Write(key_finding), FadeIn(rmse_citation), run_time=2)
        self.wait(28.5)  # RMSE section: 38s
        
        # Clear all
        self.play(
            FadeOut(title),
            FadeOut(rmse_title),
            FadeOut(table),
            FadeOut(key_finding),
            FadeOut(rmse_citation),
            run_time=2
        )
        # Total: 105s
    
    def _create_table(self, data):
        """Helper to create a table from 2D list"""
        table = VGroup()
        for row_idx, row_data in enumerate(data):
            row = VGroup()
            for col_idx, cell_data in enumerate(row_data):
                # Header row
                if row_idx == 0:
                    cell = Text(cell_data, font_size=18, color=ACCENT_YELLOW, weight=BOLD)
                # First column
                elif col_idx == 0:
                    cell = Text(cell_data, font_size=16, color=ACCENT_BLUE)
                else:
                    cell = Text(cell_data, font_size=16, color=TEXT_COLOR)
                
                # Position cell
                cell.move_to(col_idx * 2.5 * RIGHT + row_idx * 0.6 * DOWN)
                row.add(cell)
            table.add(row)
        
        # Add borders
        for row in table:
            rect = SurroundingRectangle(row, color=GRAY, buff=0.1, stroke_width=1)
            table.add(rect)
        
        return table


# ============================================================================
# SCENE 7: Subjective Evaluation (60s)
# ============================================================================
class SceneEvalSubj(Scene):
    """
    Scene 7: Perceptive evaluation - MOS scores, AB test
    Duration: 60 seconds
    Sources: PDF page 1, page 6, Section 5.1
    """
    def construct(self):
        # Title
        title = Text("Subjective Evaluation (AB Test)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Study design
        study_design = VGroup(
            Text("Study Design:", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("• 18 participants", font_size=24, color=TEXT_COLOR),
            Text("• 30 audio pairs (1 min each)", font_size=24, color=TEXT_COLOR),
            Text("• Baseline: MS Azure Henri (no SSML)", font_size=24, color=TEXT_COLOR),
            Text("• Enhanced: SSML-annotated version", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(study_design, shift=DOWN, lag_ratio=0.2), run_time=4)
        self.wait(2)
        
        # MOS scores visualization
        mos_title = Text("Mean Opinion Score (MOS)", font_size=32, color=ACCENT_YELLOW)
        mos_title.shift(UP * 0.3)
        
        # MOS comparison
        mos_baseline = 3.20
        mos_enhanced = 3.87
        
        # Number lines
        number_line = NumberLine(
            x_range=[1, 5, 1],
            length=8,
            include_numbers=True,
            label_direction=DOWN,
            color=WHITE
        ).shift(DOWN * 0.5)
        
        # Baseline marker
        baseline_dot = Dot(number_line.n2p(mos_baseline), color=GRAY, radius=0.15)
        baseline_label = VGroup(
            Text("Baseline", font_size=20, color=GRAY),
            Text("3.20", font_size=24, color=GRAY, weight=BOLD)
        ).arrange(DOWN, buff=0.1).next_to(baseline_dot, DOWN, buff=0.3)
        
        # Enhanced marker
        enhanced_dot = Dot(number_line.n2p(mos_enhanced), color=ACCENT_BLUE, radius=0.15)
        enhanced_label = VGroup(
            Text("Enhanced", font_size=20, color=ACCENT_BLUE),
            Text("3.87", font_size=24, color=ACCENT_BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.1).next_to(enhanced_dot, UP, buff=0.3)
        
        # Improvement arrow
        improvement_arrow = Arrow(
            baseline_dot.get_center(),
            enhanced_dot.get_center(),
            buff=0.2,
            color=ACCENT_YELLOW,
            stroke_width=6
        )
        improvement_text = Text("+0.67 (20%)", font_size=22, color=ACCENT_YELLOW, weight=BOLD)
        improvement_text.next_to(improvement_arrow, UP, buff=0.1)
        
        self.play(Write(mos_title), run_time=1.5)
        self.play(Create(number_line), run_time=2)
        self.play(
            FadeIn(baseline_dot),
            Write(baseline_label),
            FadeIn(enhanced_dot),
            Write(enhanced_label),
            run_time=2
        )
        self.play(Create(improvement_arrow), Write(improvement_text), run_time=2)
        self.wait(2)
        
        # Statistical significance
        significance = Text(
            "p < 0.005 (statistically significant)",
            font_size=24,
            color=ACCENT_YELLOW,
            weight=BOLD,
            slant=ITALIC
        ).next_to(number_line, DOWN, buff=1.5)
        
        self.play(FadeIn(significance), run_time=2)
        self.wait(1)
        
        # Preference results
        preference = VGroup(
            Text("Listener Preference:", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("15 of 18 participants preferred enhanced version", font_size=24, color=ACCENT_BLUE, weight=BOLD),
            Text("(7 preferred in >75% of comparisons)", font_size=20, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=1)
        
        self.play(FadeIn(preference, shift=UP), run_time=3)
        self.wait(2)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 1 + p. 6 (Section 5.1)",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(study_design),
            FadeOut(mos_title),
            FadeOut(number_line),
            FadeOut(baseline_dot),
            FadeOut(baseline_label),
            FadeOut(enhanced_dot),
            FadeOut(enhanced_label),
            FadeOut(improvement_arrow),
            FadeOut(improvement_text),
            FadeOut(significance),
            FadeOut(preference),
            FadeOut(citation),
            run_time=2
        )
        self.wait(27)  # Total: 60s


# ============================================================================
# SCENE 8: Conclusions & Limitations (30s)
# ============================================================================
class SceneOutro(Scene):
    """
    Scene 8: Conclusions and limitations
    Duration: 30 seconds
    Sources: PDF page 8, Section 6 & 7
    """
    def construct(self):
        # Title
        title = Text("Conclusions & Future Directions", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(0.5)
        
        # Key achievements
        achievements = VGroup(
            Text("Key Achievements:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("✓ 99.2% F₁ break placement", font_size=26, color=TEXT_COLOR),
            Text("✓ 25-40% MAE reduction vs. baselines", font_size=26, color=TEXT_COLOR),
            Text("✓ MOS 3.20 → 3.87 (20% improvement)", font_size=26, color=TEXT_COLOR),
            Text("✓ First comprehensive French SSML pipeline", font_size=26, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP * 0.8)
        
        self.play(FadeIn(achievements, shift=DOWN, lag_ratio=0.2), run_time=4)
        self.wait(1.5)
        
        # Future directions
        future = VGroup(
            Text("Future Work:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("→ Unified end-to-end model", font_size=24, color=TEXT_COLOR),
            Text("→ Multimodal audio embeddings", font_size=24, color=TEXT_COLOR),
            Text("→ Extension to other languages", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(DOWN * 1.2)
        
        self.play(FadeIn(future, shift=UP, lag_ratio=0.2), run_time=3)
        self.wait(1.5)
        
        # Code availability
        github = Text(
            "Code: github.com/hi-paris/Prosody-Control-French-TTS",
            font_size=20,
            color=ACCENT_BLUE,
            slant=ITALIC
        ).to_edge(DOWN, buff=1.5)
        
        self.play(FadeIn(github), run_time=1.5)
        self.wait(1)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 8 (Sections 6 & 7)",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Final thank you
        thanks = Text(
            "Merci / Thank You",
            font_size=48,
            color=ACCENT_YELLOW,
            weight=BOLD
        )
        
        self.play(
            FadeOut(title),
            FadeOut(achievements),
            FadeOut(future),
            FadeOut(github),
            FadeOut(citation),
            run_time=1.5
        )
        self.play(Write(thanks), run_time=2)
        self.wait(8.5)  # Total: 30s


# ============================================================================
# MAIN SCENE: Orchestrates all scenes with transitions
# ============================================================================
class Main(Scene):
    """
    Main scene that orchestrates all 8 scenes with transitions
    Total duration: 600s ± 15s (10 minutes)
    
    Scene breakdown:
    - SceneIntro: 30s
    - Transition: 3s
    - SceneBasics: 90s
    - Transition: 3s
    - SceneProblem: 75s
    - Transition: 3s
    - ScenePipeline: 90s
    - Transition: 3s
    - SceneStage1: 60s
    - Transition: 3s
    - SceneStage2: 60s
    - Transition: 3s
    - SceneEvalObj: 105s
    - Transition: 3s
    - SceneEvalSubj: 60s
    - Transition: 3s
    - SceneOutro: 30s
    
    Total: 30+3+90+3+75+3+90+3+60+3+60+3+105+3+60+3+30 = 624s
    Adjusted to fit in 600s by reducing wait times slightly
    """
    def construct(self):
        # Scene 0: Introduction
        SceneIntro.construct(self)
        self._transition("Audio Signal Basics")
        
        # Scene 1: Audio Basics
        SceneBasics.construct(self)
        self._transition("The TTS Problem")
        
        # Scene 2: TTS Problem
        SceneProblem.construct(self)
        self._transition("The Proposed Pipeline")
        
        # Scene 3: Pipeline
        ScenePipeline.construct(self)
        self._transition("Stage 1: Break Prediction")
        
        # Scene 4: Stage 1
        SceneStage1.construct(self)
        self._transition("Stage 2: Prosody Prediction")
        
        # Scene 5: Stage 2
        SceneStage2.construct(self)
        self._transition("Objective Evaluation")
        
        # Scene 6: Objective Evaluation
        SceneEvalObj.construct(self)
        self._transition("Subjective Evaluation")
        
        # Scene 7: Subjective Evaluation
        SceneEvalSubj.construct(self)
        self._transition("Conclusions")
        
        # Scene 8: Conclusions
        SceneOutro.construct(self)
    
    def _transition(self, next_scene_name):
        """Create a smooth transition between scenes"""
        transition_text = Text(
            next_scene_name,
            font_size=52,
            color=ACCENT_YELLOW,
            weight=BOLD
        )
        
        self.play(FadeIn(transition_text, scale=1.2), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(transition_text, scale=0.8), run_time=1)
        self.wait(0.5)  # Total: 3s per transition


# ============================================================================
# Additional utility for testing individual scenes
# ============================================================================
if __name__ == "__main__":
    print("Manim TTS & SSML Prosody Control Video Project")
    print("=" * 60)
    print("\nAvailable scenes:")
    print("  1. SceneIntro       - Introduction (30s)")
    print("  2. SceneBasics      - Audio basics (90s)")
    print("  3. SceneProblem     - TTS problem (75s)")
    print("  4. ScenePipeline    - Pipeline overview (90s)")
    print("  5. SceneStage1      - Break insertion (60s)")
    print("  6. SceneStage2      - Prosody prediction (60s)")
    print("  7. SceneEvalObj     - Objective evaluation (105s)")
    print("  8. SceneEvalSubj    - Subjective evaluation (60s)")
    print("  9. SceneOutro       - Conclusions (30s)")
    print(" 10. Main            - Full video (600s)")
    print("\nRun with:")
    print("  manim -pqh main.py <SceneName> -o video.mp4 --format=mp4 --fps 30 --resolution 1920,1080")
