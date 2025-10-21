from manim import *
import numpy as np

# CONFIGURATION SANS LATEX - Force Pango backend
config.text_backend = "pango"

# Theme colors
BG_COLOR = "#0b0f17"
ACCENT_BLUE = "#7cc5ff"
ACCENT_YELLOW = "#ffd166"
TEXT_COLOR = WHITE

config.background_color = BG_COLOR

# Image URLs from searches
WAVEFORM_IMAGE_URL = "https://dimg.wavevisual.com/v3/von-sample-2.png?width=3840"
SPECTROGRAM_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c5/Spectrogram-19thC.png"
PIPELINE_IMAGE_URL = "https://docs.nvidia.com/deeplearning/riva/user-guide/docs/_images/riva-tts-pipeline.png"

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
            Text("✓ 99.2% F1 for break placement", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(conference, DOWN, buff=0.8)
        
        # Animations with pauses for pedagogy
        self.play(Write(title), run_time=2)
        self.wait(2)  # Pause to read title
        self.play(FadeIn(authors), run_time=1)
        self.wait(1)
        self.play(FadeIn(affiliations), run_time=1)
        self.wait(1)
        self.play(Write(conference), run_time=1.5)
        self.wait(2)
        self.play(LaggedStart(*[FadeIn(h, shift=UP) for h in highlights], lag_ratio=0.5), run_time=4)
        self.wait(2)
        self.play(FadeIn(citation), run_time=1)
        self.wait(12)  # Adjusted wait to fit 30s total


# ============================================================================
# SCENE 1: Audio Basics - Waveform, Spectrogram, Pitch/F0 (90s)
# ============================================================================
class SceneBasics(Scene):
    """
    Scene 1: Waveform, spectrogram, pitch/F0 animations with images
    Duration: 90 seconds
    Sources: PPT slides 9, 12, 13, 16, 22
    """
    def construct(self):
        # Title
        title = Text("Audio Signal Basics", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(2)  # Pause for introduction
        
        # Pedagogical intro text
        intro_text = Text("Let's explore the fundamentals step by step", font_size=28, color=ACCENT_YELLOW)
        intro_text.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(intro_text), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(intro_text), run_time=1)
        
        # ===== WAVEFORM SECTION (30s) =====
        waveform_title = Text("Waveform: Amplitude vs. Time", font_size=32, color=ACCENT_YELLOW)
        waveform_title.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(waveform_title), run_time=1.5)
        self.wait(1)
        
        # Use real image instead of plot
        waveform_image = ImageMobject(WAVEFORM_IMAGE_URL).scale(0.6).shift(DOWN * 0.5)
        
        waveform_desc = Text(
            "Loudness: higher RMS amplitude → higher perceived loudness\n"
            "This visual represents how sound pressure changes over time.",
            font_size=22,
            color=TEXT_COLOR,
            line_spacing=1
        ).next_to(waveform_image, DOWN, buff=0.5)
        
        waveform_citation = Text(
            "D'après le cours (slide 9) et exemple d'onde sonore",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        self.play(FadeIn(waveform_image), run_time=3)
        self.wait(2)
        self.play(FadeIn(waveform_desc), run_time=2)
        self.wait(2)
        self.play(FadeIn(waveform_citation), run_time=1)
        self.wait(14)  # Adjusted for 30s section
        
        # Fade out waveform elements
        self.play(
            FadeOut(waveform_title),
            FadeOut(waveform_image),
            FadeOut(waveform_desc),
            FadeOut(waveform_citation),
            run_time=2
        )
        self.wait(1)
        
        # ===== SPECTROGRAM SECTION (30s) =====
        spectrogram_title = Text("Spectrogram: Frequency Energy over Time", font_size=32, color=ACCENT_YELLOW)
        spectrogram_title.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(spectrogram_title), run_time=1.5)
        self.wait(1)
        
        # Use real image
        spectro_image = ImageMobject(SPECTROGRAM_IMAGE_URL).scale(0.8).shift(DOWN * 0.5)
        
        spectro_desc = Text(
            "Window: 20-30 ms | Hop: ~10 ms | Hann window + FFT\n"
            "Colors indicate energy intensity at different frequencies.",
            font_size=22,
            color=TEXT_COLOR,
            line_spacing=1
        ).next_to(spectro_image, DOWN, buff=0.5)
        
        spectro_citation = Text(
            "D'après le cours (slide 12) et exemple de spectrogramme",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        self.play(FadeIn(spectro_image), run_time=3)
        self.wait(2)
        self.play(FadeIn(spectro_desc), run_time=2)
        self.wait(2)
        self.play(FadeIn(spectro_citation), run_time=1)
        self.wait(14)  # Adjusted for 30s
        
        # Fade out
        self.play(
            FadeOut(spectrogram_title),
            FadeOut(spectro_image),
            FadeOut(spectro_desc),
            FadeOut(spectro_citation),
            run_time=2
        )
        self.wait(1)
        
        # ===== PITCH/F0 SECTION (29s) =====
        pitch_title = Text("Pitch & Fundamental Frequency (F0)", font_size=32, color=ACCENT_YELLOW)
        pitch_title.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(pitch_title), run_time=1.5)
        self.wait(1)
        
        pitch_desc = VGroup(
            Text("Pitch is strongly related to F0", font_size=26, color=TEXT_COLOR),
            Text("(physical measure of vocal fold vibration)", font_size=22, color=GRAY, slant=ITALIC)
        ).arrange(DOWN, buff=0.2).shift(UP * 0.5)
        
        # F0 formula display - TEXT ONLY
        f0_formula = VGroup(
            Text("s_i = 12 × log2(f0(i) / f0_ref)", font_size=32, color=ACCENT_BLUE),
            Text("(semitone offset)", font_size=20, color=GRAY, slant=ITALIC),
            Text("p_i = (2^(s_i/12) - 1) × 100", font_size=32, color=ACCENT_BLUE),
            Text("(percentage pitch change)", font_size=20, color=GRAY, slant=ITALIC)
        ).arrange(DOWN, buff=0.3).shift(DOWN * 0.5)
        
        tools_text = Text(
            "Tools: librosa (spectrogram), pyworld (F0), Praat (verification)",
            font_size=22,
            color=ACCENT_YELLOW
        ).to_edge(DOWN, buff=1)
        
        pitch_citation = Text(
            "D'après le cours (slides 13, 16) + ICNLSP 2025, p. 4",
            font_size=16,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        
        self.play(FadeIn(pitch_desc, shift=UP), run_time=2)
        self.wait(1)
        self.play(LaggedStart(*[Write(f) for f in f0_formula], lag_ratio=0.5), run_time=4)
        self.wait(2)
        self.play(FadeIn(tools_text), run_time=1)
        self.wait(1)
        self.play(FadeIn(pitch_citation), run_time=1)
        self.wait(13)  # Adjusted for 29s
        
        # Clear all
        self.play(
            FadeOut(title),
            FadeOut(pitch_title),
            FadeOut(pitch_desc),
            FadeOut(f0_formula),
            FadeOut(tools_text),
            FadeOut(pitch_citation),
            run_time=2
        )
        self.wait(1)
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
        self.wait(2)
        
        # Problem statement with lagged animation
        problem_box = VGroup(
            Text("Current State:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("✗ Commercial TTS prioritizes clarity", font_size=26, color=TEXT_COLOR),
            Text("✗ Prosodic variation is limited", font_size=26, color=TEXT_COLOR),
            Text("✗ Results in monotone speech output", font_size=26, color=TEXT_COLOR),
            Text("✗ Particularly affects French prosody", font_size=26, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 0.5)
        
        self.play(LaggedStart(*[FadeIn(p, shift=UP) for p in problem_box], lag_ratio=0.3), run_time=5)
        self.wait(4)
        
        # SSML limitations
        ssml_box = VGroup(
            Text("SSML Challenges:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("✗ Manual markup doesn't scale", font_size=26, color=TEXT_COLOR),
            Text("✗ LLMs produce incomplete tags", font_size=26, color=TEXT_COLOR),
            Text("✗ Invalid syntax generation", font_size=26, color=TEXT_COLOR),
            Text("✗ Imprecise prosodic control", font_size=26, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 1)
        
        self.play(LaggedStart(*[FadeIn(s, shift=UP) for s in ssml_box], lag_ratio=0.3), run_time=5)
        self.wait(4)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 1-2",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Clear with fade out
        self.play(
            FadeOut(title),
            FadeOut(problem_box),
            FadeOut(ssml_box),
            FadeOut(citation),
            run_time=2
        )
        self.wait(48)


# ============================================================================
# SCENE 3: Pipeline Overview (90s)
# ============================================================================
class ScenePipeline(Scene):
    """
    Scene 3: Text → pauses → SSML → TTS pipeline with image
    Duration: 90 seconds
    Sources: PDF page 3, PPT slide 26
    """
    def construct(self):
        # Title
        title = Text("The Proposed Pipeline", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(2)
        
        # Corpus info with lagged
        corpus_info = VGroup(
            Text("Corpus: 14h French Podcast Audio", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Source: ETX Majelan", font_size=24, color=TEXT_COLOR),
            Text("14 speakers (42% female) | 122,303 words", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.5)
        
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN) for c in corpus_info], lag_ratio=0.3), run_time=3)
        self.wait(3)
        
        # Use pipeline image
        pipeline_image = ImageMobject(PIPELINE_IMAGE_URL).scale(0.5).shift(DOWN * 0.5)
        
        self.play(FadeIn(pipeline_image), run_time=3)
        self.wait(2)
        
        # Pipeline steps as overlays or separate
        step1 = self._create_step_box("1. Audio Preprocessing", "Demucs source separation\nWhisperTS alignment (WER 5.95%)", ACCENT_BLUE).scale(0.6).to_edge(LEFT)
        step2 = self._create_step_box("2. Baseline Generation", "MS Azure TTS (Henri voice)\nReference for delta calculation", ACCENT_YELLOW).scale(0.6).next_to(step1, RIGHT, buff=0.2)
        # Simplify steps for pedagogy, show one by one
        self.play(LaggedStart(FadeIn(step1), FadeIn(step2), lag_ratio=1), run_time=3)
        self.wait(2)
        
        step3 = self._create_step_box("3. Syntagm Segmentation", "Prosodic units\nPause detection", ACCENT_BLUE).scale(0.6).next_to(step2, RIGHT, buff=0.2)
        step4 = self._create_step_box("4. Feature Extraction", "Pitch, Volume, Rate, Breaks\nNormalized deltas", ACCENT_YELLOW).scale(0.6).next_to(step3, RIGHT, buff=0.2)
        self.play(LaggedStart(FadeIn(step3), FadeIn(step4), lag_ratio=1), run_time=3)
        self.wait(2)
        
        step5 = self._create_step_box("5. SSML Generation", "QwenA: Break insertion\nQwenB: Prosody values", ACCENT_BLUE).scale(0.6).next_to(step4, RIGHT, buff=0.2)
        self.play(FadeIn(step5), run_time=2)
        self.wait(2)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 3 (Section 3) + slide 26 + diagramme exemple",
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
            FadeOut(pipeline_image),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(step4),
            FadeOut(step5),
            FadeOut(citation),
            run_time=2
        )
        self.wait(54)  # Adjusted to fit 90s
    
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
    Scene 4: Stage 1 - Break insertion
    Duration: 60 seconds
    """
    def construct(self):
        # Title
        title = Text("Stage 1: Break Prediction (QwenA)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(2)
        
        # Model info with lagged
        model_info = VGroup(
            Text("Model: Qwen 2.5-7B", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Fine-tuning: QLoRA (4-bit, rank 8, α=16)", font_size=24, color=TEXT_COLOR),
            Text("Input: Up to 200-word French paragraphs", font_size=24, color=TEXT_COLOR),
            Text("Output: <break> tag placement", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5)
        
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN) for m in model_info], lag_ratio=0.2), run_time=4)
        self.wait(3)
        
        # Performance metrics
        perf_box = VGroup(
            Text("Performance:", font_size=32, color=ACCENT_BLUE, weight=BOLD),
            Text("F₁ Score: 99.24%", font_size=30, color=ACCENT_YELLOW, weight=BOLD),
            Text("Perplexity: 1.001", font_size=30, color=ACCENT_YELLOW, weight=BOLD),
            Text("vs. BERT baseline: 92.06% F₁", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=1.5)
        
        self.play(LaggedStart(*[FadeIn(p, shift=UP) for p in perf_box], lag_ratio=0.2), run_time=4)
        self.wait(3)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 7 (Table 4)",
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
            FadeOut(perf_box),
            FadeOut(citation),
            run_time=2
        )
        self.wait(35)


# ============================================================================
# SCENE 5: Stage 2 - Prosody Values (60s)
# ============================================================================
class SceneStage2(Scene):
    """
    Scene 5: Stage 2 - Prosody values
    Duration: 60 seconds
    """
    def construct(self):
        # Title
        title = Text("Stage 2: Prosody Prediction (QwenB)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(2)
        
        # Model info
        model_info = VGroup(
            Text("Model: Qwen 2.5-7B (2nd instance)", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("Fine-tuning: QLoRA adapter", font_size=24, color=TEXT_COLOR),
            Text("Input: SSML skeleton from QwenA", font_size=24, color=TEXT_COLOR),
            Text("Output: Numeric prosodic attributes", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5)
        
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN) for m in model_info], lag_ratio=0.2), run_time=4)
        self.wait(3)
        
        # Prosodic features
        features_title = Text("Prosodic Features:", font_size=28, color=ACCENT_YELLOW, weight=BOLD)
        features_title.shift(UP * 0.2)
        
        features = VGroup(
            Text("• Pitch: f₀ → semitone → % (±2% typical)", font_size=22, color=TEXT_COLOR),
            Text("• Volume: LUFS → gain % (~-10% typical)", font_size=22, color=TEXT_COLOR),
            Text("• Rate: words/sec → % (~-1% typical)", font_size=22, color=TEXT_COLOR),
            Text("• Break: silence gap (250-500 ms)", font_size=22, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(features_title, DOWN, buff=0.4)
        
        self.play(Write(features_title), run_time=1.5)
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT) for f in features], lag_ratio=0.3), run_time=4)
        self.wait(3)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 4-5",
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
            FadeOut(citation),
            run_time=2
        )
        self.wait(34)


# ============================================================================
# SCENE 6: Objective Evaluation (75s)
# ============================================================================
class SceneEvalObj(Scene):
    """
    Scene 6: Objective evaluation
    Duration: 75 seconds
    """
    def construct(self):
        # Title
        title = Text("Objective Evaluation", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(2)
        
        # F1 scores
        f1_title = Text("Break Prediction Accuracy", font_size=32, color=ACCENT_YELLOW)
        f1_title.next_to(title, DOWN, buff=0.5)
        
        f1_results = VGroup(
            Text("QwenA (Ours): 99.24% F₁", font_size=28, color=ACCENT_BLUE, weight=BOLD),
            Text("BERT Baseline: 92.06% F₁", font_size=28, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 0.5)
        
        self.play(Write(f1_title), run_time=1.5)
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(f, shift=DOWN) for f in f1_results], lag_ratio=0.3), run_time=3)
        self.wait(4)
        
        # Fade out f1
        self.play(
            FadeOut(f1_title),
            FadeOut(f1_results),
            run_time=1
        )
        self.wait(1)
        
        # MAE comparison
        mae_title = Text("Mean Absolute Error (MAE)", font_size=32, color=ACCENT_YELLOW)
        mae_title.shift(DOWN * 0.5)
        
        mae_results = VGroup(
            Text("Pitch: 0.97% (QwenB) vs 1.68% (BiLSTM)", font_size=24, color=TEXT_COLOR),
            Text("Volume: 1.09% (QwenB) vs 6.04% (BiLSTM)", font_size=24, color=TEXT_COLOR),
            Text("Rate: 1.10% (QwenB) vs 0.84% (BiLSTM)", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(mae_title, DOWN, buff=0.4)
        
        self.play(Write(mae_title), run_time=1.5)
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(m, shift=UP) for m in mae_results], lag_ratio=0.3), run_time=4)
        self.wait(4)
        
        # Key finding
        key_finding = Text(
            "25-40% MAE reduction vs. baselines",
            font_size=28,
            color=ACCENT_BLUE,
            weight=BOLD
        ).to_edge(DOWN, buff=1.5)
        
        self.play(FadeIn(key_finding), run_time=2)
        self.wait(3)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 7",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(mae_title),
            FadeOut(mae_results),
            FadeOut(key_finding),
            FadeOut(citation),
            run_time=2
        )
        self.wait(35)


# ============================================================================
# SCENE 7: Subjective Evaluation (60s)
# ============================================================================
class SceneEvalSubj(Scene):
    """
    Scene 7: Subjective evaluation
    Duration: 60 seconds
    """
    def construct(self):
        # Title
        title = Text("Subjective Evaluation (AB Test)", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(2)
        
        # Study design
        study_design = VGroup(
            Text("Study Design:", font_size=28, color=ACCENT_YELLOW, weight=BOLD),
            Text("• 18 participants", font_size=24, color=TEXT_COLOR),
            Text("• 30 audio pairs (1 min each)", font_size=24, color=TEXT_COLOR),
            Text("• Baseline vs. SSML-enhanced", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5)
        
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN) for s in study_design], lag_ratio=0.2), run_time=4)
        self.wait(3)
        
        # Fade out study design
        self.play(FadeOut(study_design), run_time=1)
        self.wait(1)
        
        # MOS scores
        mos_title = Text("Mean Opinion Score (MOS)", font_size=32, color=ACCENT_YELLOW)
        mos_title.shift(UP * 0.3)
        
        mos_results = VGroup(
            Text("Baseline: 3.20", font_size=28, color=GRAY),
            Text("Enhanced: 3.87 (+0.67, +20%)", font_size=28, color=ACCENT_BLUE, weight=BOLD),
            Text("p < 0.005 (statistically significant)", font_size=24, color=ACCENT_YELLOW, slant=ITALIC)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(mos_title, DOWN, buff=0.4)
        
        self.play(Write(mos_title), run_time=1.5)
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(m, shift=UP) for m in mos_results], lag_ratio=0.3), run_time=4)
        self.wait(3)
        
        # Preference
        preference = Text(
            "15 of 18 participants preferred enhanced version",
            font_size=26,
            color=ACCENT_BLUE,
            weight=BOLD
        ).to_edge(DOWN, buff=1.5)
        
        self.play(FadeIn(preference), run_time=2)
        self.wait(3)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 6",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(2)
        
        # Clear
        self.play(
            FadeOut(title),
            FadeOut(mos_title),
            FadeOut(mos_results),
            FadeOut(preference),
            FadeOut(citation),
            run_time=2
        )
        self.wait(23)


# ============================================================================
# SCENE 8: Conclusions (30s)
# ============================================================================
class SceneOutro(Scene):
    """
    Scene 8: Conclusions
    Duration: 30 seconds
    """
    def construct(self):
        # Title
        title = Text("Conclusions & Future Directions", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Key achievements
        achievements = VGroup(
            Text("Key Achievements:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("✓ 99.2% F₁ break placement", font_size=26, color=TEXT_COLOR),
            Text("✓ 25-40% MAE reduction", font_size=26, color=TEXT_COLOR),
            Text("✓ MOS 3.20 → 3.87 (20% improvement)", font_size=26, color=TEXT_COLOR),
            Text("✓ First comprehensive French SSML pipeline", font_size=26, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP * 0.8)
        
        self.play(LaggedStart(*[FadeIn(a, shift=DOWN) for a in achievements], lag_ratio=0.2), run_time=4)
        self.wait(2)
        
        # Future work
        future = VGroup(
            Text("Future Work:", font_size=32, color=ACCENT_YELLOW, weight=BOLD),
            Text("→ Unified end-to-end model", font_size=24, color=TEXT_COLOR),
            Text("→ Multimodal audio embeddings", font_size=24, color=TEXT_COLOR),
            Text("→ Extension to other languages", font_size=24, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(DOWN * 1.2)
        
        self.play(LaggedStart(*[FadeIn(f, shift=UP) for f in future], lag_ratio=0.2), run_time=3)
        self.wait(2)
        
        # GitHub
        github = Text(
            "github.com/hi-paris/Prosody-Control-French-TTS",
            font_size=20,
            color=ACCENT_BLUE,
            slant=ITALIC
        ).to_edge(DOWN, buff=1.5)
        
        self.play(FadeIn(github), run_time=1.5)
        self.wait(1)
        
        # Citation
        citation = Text(
            "Données : ICNLSP 2025, p. 8",
            font_size=18,
            color=GRAY,
            slant=ITALIC
        ).to_corner(DR)
        self.play(FadeIn(citation), run_time=1)
        self.wait(1)
        
        # Thank you
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
        self.wait(7)


# ============================================================================
# MAIN SCENE: Full 10-minute video
# ============================================================================
class VideoComplet(Scene):
    """
    Main scene that orchestrates all 8 scenes
    Total duration: ~600s (10 minutes)
    """
    def construct(self):
        # Scene 0: Introduction (30s)
        intro = SceneIntro()
        intro.renderer = self.renderer
        intro.construct()
        self._transition("Audio Signal Basics")
        
        # Scene 1: Audio Basics (90s)
        basics = SceneBasics()
        basics.renderer = self.renderer
        basics.construct()
        self._transition("The TTS Problem")
        
        # Scene 2: TTS Problem (75s)
        problem = SceneProblem()
        problem.renderer = self.renderer
        problem.construct()
        self._transition("The Proposed Pipeline")
        
        # Scene 3: Pipeline (90s)
        pipeline = ScenePipeline()
        pipeline.renderer = self.renderer
        pipeline.construct()
        self._transition("Stage 1: Break Prediction")
        
        # Scene 4: Stage 1 (60s)
        stage1 = SceneStage1()
        stage1.renderer = self.renderer
        stage1.construct()
        self._transition("Stage 2: Prosody Prediction")
        
        # Scene 5: Stage 2 (60s)
        stage2 = SceneStage2()
        stage2.renderer = self.renderer
        stage2.construct()
        self._transition("Objective Evaluation")
        
        # Scene 6: Objective Evaluation (75s)
        evalobj = SceneEvalObj()
        evalobj.renderer = self.renderer
        evalobj.construct()
        self._transition("Subjective Evaluation")
        
        # Scene 7: Subjective Evaluation (60s)
        evalsubj = SceneEvalSubj()
        evalsubj.renderer = self.renderer
        evalsubj.construct()
        self._transition("Conclusions")
        
        # Scene 8: Conclusions (30s)
        outro = SceneOutro()
        outro.renderer = self.renderer
        outro.construct()
    
    def _transition(self, next_scene_name):
        """Create a smooth transition between scenes"""
        transition_text = Text(
            next_scene_name,
            font_size=52,
            color=ACCENT_YELLOW,
            weight=BOLD
        )
        
        self.play(FadeIn(transition_text, scale=1.2), run_time=1)
        self.wait(1)  # Longer pause for reading
        self.play(FadeOut(transition_text, scale=0.8), run_time=1)
        self.wait(1)
