from manim import *
import numpy as np
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"

def load_img(stem: str, exts=(".png", ".jpg", ".jpeg", ".gif", ".ico")) -> ImageMobject:
    for ext in exts:
        p = ASSETS_DIR / f"{stem}{ext}"
        if p.exists():
            return ImageMobject(str(p))
    raise FileNotFoundError(f"Image introuvable pour '{stem}' dans assets/ ({exts})")

config.text_backend = "pango"

BG_COLOR      = "#0B1026"  
ACCENT_BLUE   = "#1363DF"  
ACCENT_YELLOW = "#E5007D" 
TEXT_COLOR    = "#F4F6FA"  

ACCENT_PURPLE = "#5A1E86"
ACCENT_CYAN   = "#14B8FF"
HI_GREY       = "#9AA3B2"  

config.background_color = BG_COLOR



# ============================================================================
# SCENE 0: Introduction (30s)
# ============================================================================
class SceneIntro(Scene):
    def construct(self):
        # 1) Titre robuste (police + outline + fond + z-index + clamp)
        title = Text(
            "Improving French Synthetic Speech Quality\nvia SSML Prosody Control",
            font_size=44,
            color=ACCENT_BLUE,
            font="DejaVu Sans",   # ou "Noto Sans" si dispo sur ta machine
            weight=BOLD
        )
        # largeur sûre + positionnement
        title.scale_to_fit_width(min(config.frame_width * 0.9, title.width))
        title.to_edge(UP, buff=0.55)
        # garde-fou anti-clipping vertical (quel que soit le ratio)
        title.set_y(min(title.get_y(), config.frame_height/2 - 0.7))
        # lisibilité (contour + fond léger)
        title.set_stroke(BLACK, width=2.2, opacity=0.75)
        title.add_background_rectangle(color=BLACK, opacity=0.18, buff=0.12)
        title.set_z_index(10)

        authors = Text(
            "Nassima Ould Ouali, Awais Hussain Sani, Ruben Bueno,\n"
            "Jonah Dauvet, Tim Luka Horstmann, Eric Moulines",
            font_size=26, color=TEXT_COLOR, font="DejaVu Sans"
        ).next_to(title, DOWN, buff=0.55).set_z_index(9)

        affiliations = Text(
            "École Polytechnique, Hi! PARIS Research Center, McGill University",
            font_size=22, color=HI_GREY, slant=ITALIC, font="DejaVu Sans"
        ).next_to(authors, DOWN, buff=0.4).set_z_index(9)

        conference = Text(
            "ICNLSP 2025", font_size=28, color=ACCENT_BLUE, weight=BOLD, font="DejaVu Sans"
        ).next_to(affiliations, DOWN, buff=0.6).set_z_index(9)

        self.play(Write(title), run_time=1.2); self.wait(0.4)
        self.play(FadeIn(authors, shift=UP), run_time=0.6)
        self.play(FadeIn(affiliations, shift=UP), run_time=0.6)
        self.play(Write(conference), run_time=0.6)
        self.wait(1.2)

        self.play(Flash(title, flash_radius=0.28), run_time=0.6); self.wait(0.25)
        self.play(FadeOut(conference), FadeOut(affiliations), FadeOut(authors), run_time=0.6)
        self.play(FadeOut(title), run_time=0.5) 


# ============================================================================
# SCENE 1: Audio Basics - Waveform, Spectrogram, Pitch/F0 (90s)
# ============================================================================
class SceneBasics(Scene):
    """
    Scene 1: Waveform, spectrogram, pitch/F0 avec VRAIES images (assets/)
    Duration: ~90s
    """
    def construct(self):
        title = Text("Audio Signal Basics", font_size=48, color=ACCENT_BLUE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.6)
        self.wait(0.75)

        # ===== WAVEFORM (≈30s) =====
        waveform_title = Text("Waveform: Amplitude vs. Time", font_size=32, color=ACCENT_YELLOW).next_to(title, DOWN, buff=0.65)
        self.play(Write(waveform_title), run_time=1.0)

        wf = load_img("waveform").scale(1.0)
        if wf.width > config.frame_width * 1.05:
            wf.width = config.frame_width * 1.05
        wf.shift(DOWN * 0.3)

        wf_desc = Text(
            "Loudness ~ RMS amplitude (Average Energy)\nTemporal variation of the audio signal.",
            font_size=22, color=TEXT_COLOR, line_spacing=1
        ).next_to(wf, DOWN, buff=0.4)

        wf_cite = Text("Databootcamp TTS Course", font_size=16, color=GRAY, slant=ITALIC).to_corner(DR)

        self.play(FadeIn(wf, shift=UP), run_time=1)
        self.play(FadeIn(wf_desc), FadeIn(wf_cite), run_time=0.7)
        self.wait(10)

        self.play(FadeOut(waveform_title), FadeOut(wf), FadeOut(wf_desc), FadeOut(wf_cite), run_time=0.8)
        self.wait(0.35)

        # ===== SPECTROGRAM (≈30s) =====
        spect_title = Text("Spectrogram: Frequency Energy over Time", font_size=32, color=ACCENT_YELLOW).next_to(title, DOWN, buff=0.5)
        self.play(Write(spect_title), run_time=1.0)

        sp = load_img("spectrogramme").scale(1.0)
        if sp.width > config.frame_width * 1.05:
            sp.width = config.frame_width * 1.05
        sp.shift(DOWN * 0.2)

        sp_desc = Text("Window 20–30 ms • Hop ≈10 ms • Hann + FFT", font_size=22, color=TEXT_COLOR).next_to(sp, DOWN, buff=0.35)
        sp_cite = Text("Databootcamp TTS Course", font_size=16, color=GRAY, slant=ITALIC).to_corner(DR)

        self.play(FadeIn(sp, shift=UP), run_time=1.0)
        self.play(FadeIn(sp_desc), FadeIn(sp_cite), run_time=0.6)
        self.wait(12)

        self.play(FadeOut(spect_title), FadeOut(sp), FadeOut(sp_desc), FadeOut(sp_cite), run_time=0.8)
        self.wait(0.2)

        # ===== PITCH/F0 (≈29s) =====
        pitch_title = Text("Pitch & Fundamental Frequency (F0)", font_size=32, color=ACCENT_YELLOW).next_to(title, DOWN, buff=0.5)
        self.play(Write(pitch_title), run_time=1.0)

        # ⚠️ Linux est sensible à la casse : fichier 'F0.png'
        f0img = load_img("f0").scale(1.0)
        if f0img.width > config.frame_width * 1.05:
            f0img.width = config.frame_width * 1.05
        f0img.shift(DOWN * 0.2)

        pitch_desc = VGroup(
            Text("Perceived pitch ↔ F0 (fundamental frequency)", font_size=26, color=TEXT_COLOR),
            Text("Typical extraction: pyworld, Praat, post-processing outliers", font_size=22, color=GRAY, slant=ITALIC)
        ).arrange(DOWN, buff=0.2).next_to(f0img, DOWN, buff=0.45)

        pitch_cite = Text("Databootcamp TTS Course", font_size=16, color=GRAY, slant=ITALIC).to_corner(DR)

        self.play(FadeIn(f0img, shift=UP), run_time=1.0)
        self.play(FadeIn(pitch_desc), FadeIn(pitch_cite), run_time=0.6)
        self.wait(12)

        self.play(FadeOut(title), FadeOut(pitch_title), FadeOut(f0img), FadeOut(pitch_desc), FadeOut(pitch_cite), run_time=0.9)
        self.wait(0.1)


# ============================================================================
# SCENE 2A: TTS Expressivity Problem (~35s)
# ============================================================================
class SceneProblemTTS(Scene):
    def construct(self):
        title = Text("The TTS Expressivity Problem", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.4); self.wait(0.4)

        # Bloc central avec fond pour éviter l'effet d'écrasement
        heading = Text("Current State", font_size=34, color=ACCENT_YELLOW, weight=BOLD)

        bullets = VGroup(
            Text("✗ Commercial TTS prioritizes clarity", font_size=26, color=TEXT_COLOR),
            Text("✗ Prosodic variation is limited",      font_size=26, color=TEXT_COLOR),
            Text("✗ Results in monotone speech output",  font_size=26, color=TEXT_COLOR),
            Text("✗ Particularly affects French prosody",font_size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        content = VGroup(heading, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.45)

        panel = RoundedRectangle(corner_radius=0.25, width=10.8, height=4.6, stroke_width=2, stroke_color=ACCENT_BLUE)
        panel.set_fill(BG_COLOR, opacity=0.0)
        # on met un léger padding visuel en centrant le groupe dans le panel
        content.move_to(panel.get_center())

        card = Group(panel, content).next_to(title, DOWN, buff=0.6)

        # Animations
        self.play(Create(panel), run_time=0.8)
        self.play(FadeIn(heading, shift=UP), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=UP) for b in bullets], lag_ratio=0.22), run_time=2.4)
        self.wait(2.0)

        # petit focus sur deux points clés (remplit le temps sans “blanc”)
        self.play(Indicate(bullets[1], scale_factor=1.05), run_time=0.7); self.wait(0.3)
        self.play(Indicate(bullets[2], scale_factor=1.05), run_time=0.7); self.wait(0.6)

        citation = Text("Données : ICNLSP 2025, p. 1–2", font_size=18, color=HI_GREY if 'HI_GREY' in globals() else GRAY, slant=ITALIC).to_corner(DR)
        self.play(FadeIn(citation), run_time=0.5); self.wait(1.0)

        # sortie propre
        self.play(FadeOut(citation, run_time=0.4))
        self.play(FadeOut(card, shift=DOWN, run_time=0.8), FadeOut(title, run_time=0.8))
        self.wait(0.6)

# ============================================================================
# SCENE 2B: SSML Challenges (~40s)
# ============================================================================
class SceneProblemSSML(Scene):
    def construct(self):
        title = Text("SSML Challenges", font_size=48, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.2); self.wait(0.4)

        heading = Text("Why SSML is hard in practice", font_size=34, color=ACCENT_YELLOW, weight=BOLD)

        bullets = VGroup(
            Text("✗ Manual markup doesn't scale",    font_size=26, color=TEXT_COLOR),
            Text("✗ LLMs produce incomplete tags",  font_size=26, color=TEXT_COLOR),
            Text("✗ Invalid syntax generation",     font_size=26, color=TEXT_COLOR),
            Text("✗ Imprecise prosodic control",    font_size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        content = VGroup(heading, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.45)

        panel = RoundedRectangle(corner_radius=0.25, width=10.8, height=4.6, stroke_width=2, stroke_color=ACCENT_BLUE)
        panel.set_fill(BG_COLOR, opacity=0.0)
        content.move_to(panel.get_center())

        card = Group(panel, content).next_to(title, DOWN, buff=0.6)

        self.play(Create(panel), run_time=0.8)
        self.play(FadeIn(heading, shift=UP), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=UP) for b in bullets], lag_ratio=0.22), run_time=2.6)
        self.wait(1.2)

        # mini “callout” pédagogique sur deux points
        self.play(Indicate(bullets[0], scale_factor=1.06), run_time=0.7); self.wait(0.3)
        self.play(Indicate(bullets[3], scale_factor=1.06), run_time=0.7); self.wait(0.6)

        citation = Text("Données : ICNLSP 2025, p. 1–2", font_size=18, color=HI_GREY if 'HI_GREY' in globals() else GRAY, slant=ITALIC).to_corner(DR)
        self.play(FadeIn(citation), run_time=0.5); self.wait(0.8)

        self.play(FadeOut(citation, run_time=0.4))
        self.play(FadeOut(card, shift=DOWN, run_time=0.8), FadeOut(title, run_time=0.8))
        self.wait(0.5)

# ============================================================================
# SCENE 3A: Proposed Pipeline — Interactive Overview (~45s)
# ============================================================================
class ScenePipelineInteractive(Scene):
    def _create_step_box(self, step_title, step_desc, color):
        box = VGroup(
            Text(step_title, font_size=30, color=color, weight=BOLD),
            Text(step_desc, font_size=22, color=TEXT_COLOR, line_spacing=0.9),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rect = RoundedRectangle(corner_radius=0.18, stroke_color=color, stroke_width=3)
        rect.surround(box, buff=0.28)
        return VGroup(rect, box)

    def construct(self):
        title = Text("The Proposed Pipeline — Interactive Overview",
                     font_size=46, color=ACCENT_BLUE, weight=BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.2); self.wait(0.4)

        # 5 gros “cubes”
        step1 = self._create_step_box("1. Audio Preprocessing",
                "Demucs source separation\nWhisperTS alignment (WER 5.95%)", ACCENT_BLUE)
        step2 = self._create_step_box("2. Baseline Generation",
                "MS Azure TTS (Henri voice)\nReference for delta calculation", ACCENT_YELLOW)
        step3 = self._create_step_box("3. Syntagm Segmentation",
                "Prosodic units\nPause detection", ACCENT_BLUE)
        step4 = self._create_step_box("4. Feature Extraction",
                "Pitch, Volume, Rate, Breaks\nNormalized deltas", ACCENT_YELLOW)
        step5 = self._create_step_box("5. SSML Generation",
                "QwenA: Break insertion\nQwenB: Prosody values", ACCENT_BLUE)

        # Disposition: colonne centrée, grands blocs
        steps = VGroup(step1, step2, step3, step4, step5)\
                .arrange(DOWN, buff=0.35, aligned_edge=LEFT)\
                .scale(0.9)\
                .next_to(title, DOWN, buff=0.5)

        self.play(LaggedStart(*[FadeIn(s, shift=UP) for s in steps], lag_ratio=0.18), run_time=2.2)
        self.wait(0.4)

        # Flèches entre blocs (courtes pour lisibilité)
        arrows = VGroup()
        for i in range(4):
            a = Arrow(steps[i].get_bottom(), steps[i+1].get_top(),
                      buff=0.18, stroke_width=3, max_tip_length_to_length_ratio=0.12, color=TEXT_COLOR)
            arrows.add(a)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.12), run_time=1.0)

        # Mise en avant rapide de 3 points (remplit le temps sans “blanc”)
        for idx in (0, 2, 4):
            self.play(Indicate(steps[idx][0], scale_factor=1.04), run_time=0.6)
            self.wait(0.25)

        citation = Text("Données : ICNLSP 2025, p. 3 (Section 3) + slide 26",
                        font_size=18, color=HI_GREY if 'HI_GREY' in globals() else GRAY, slant=ITALIC)\
                        .to_corner(DR)
        self.play(FadeIn(citation), run_time=0.4); self.wait(1.0)

        self.play(FadeOut(arrows, run_time=0.6))
        self.play(FadeOut(steps, shift=DOWN, run_time=0.8),
                  FadeOut(citation, run_time=0.4),
                  FadeOut(title, run_time=0.6))
        self.wait(0.4)


# ============================================================================
# SCENE 3B: Proposed Pipeline — Figure (Image) (~45s)
# ============================================================================
class ScenePipelineFigure(Scene):
    def construct(self):
        title = Text("The Proposed Pipeline — Figure",
                     font_size=46, color=ACCENT_BLUE, weight=BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.0); self.wait(0.4)

        # Ton image locale (assets/pipeline.png)
        img = load_img("pipeline").scale(1.0)
        # sécurité largeur
        if img.width > config.frame_width * 1.04:
            img.width = config.frame_width * 1.04
        grp = Group(img).next_to(title, DOWN, buff=0.4)

        cap = Text("Overview of the full data & SSML pipeline",
                   font_size=20, color=HI_GREY if 'HI_GREY' in globals() else GRAY, slant=ITALIC)\
                   .next_to(grp, DOWN, buff=0.35)

        self.play(FadeIn(grp, shift=UP), run_time=1.0)
        self.play(FadeIn(cap), run_time=0.4)
        self.wait(2.0)

        # zoom léger + pan pour donner vie à la figure
        self.play(grp.animate.scale(1.06).shift(UP*0.06), run_time=0.8)
        self.wait(1.2)

        citation = Text("Figure: internal design (assets/pipeline.png)",
                        font_size=18, color=HI_GREY if 'HI_GREY' in globals() else GRAY, slant=ITALIC)\
                        .to_corner(DR)
        self.play(FadeIn(citation), run_time=0.4); self.wait(0.8)

        self.play(FadeOut(citation, run_time=0.4))
        self.play(FadeOut(cap, run_time=0.5),
                  FadeOut(grp, run_time=0.6),
                  FadeOut(title, run_time=0.6))
        self.wait(0.4)


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
    def construct(self):
        # 0) Intro
        intro = SceneIntro(); intro.renderer = self.renderer; intro.construct()
        self._transition("Audio Signal Basics")

        # 1) Basics
        basics = SceneBasics(); basics.renderer = self.renderer; basics.construct()
        self._transition("The TTS Problem")

        # 2A) TTS Problem
        problem_tts = SceneProblemTTS(); problem_tts.renderer = self.renderer; problem_tts.construct()
        self._transition("SSML Challenges")

        # 2B) SSML Challenges
        problem_ssml = SceneProblemSSML(); problem_ssml.renderer = self.renderer; problem_ssml.construct()
        self._transition("Pipeline — Interactive")

        # 3A) Pipeline — Interactive
        pipe_int = ScenePipelineInteractive(); pipe_int.renderer = self.renderer; pipe_int.construct()
        self._transition("Pipeline — Figure")

        # 3B) Pipeline — Figure (ton image)
        pipe_fig = ScenePipelineFigure(); pipe_fig.renderer = self.renderer; pipe_fig.construct()
        self._transition("Stage 1: Break Prediction")

        # 4) Stage 1
        stage1 = SceneStage1(); stage1.renderer = self.renderer; stage1.construct()
        self._transition("Stage 2: Prosody Prediction")

        # 5) Stage 2
        stage2 = SceneStage2(); stage2.renderer = self.renderer; stage2.construct()
        self._transition("SSML Example")

        # 5bis) SSML example (image du cours)
        ssml_img = SceneSSMLImage(); ssml_img.renderer = self.renderer; ssml_img.construct()
        self._transition("Key Formulas")

        # 5ter) Formules
        formulas = SceneMathFormulas(); formulas.renderer = self.renderer; formulas.construct()
        self._transition("Cascaded Architecture")

        # 5quater) Architecture en cascade (si tu la gardes)
        cascade_fig = SceneCascadeFigure(); cascade_fig.renderer = self.renderer; cascade_fig.construct()
        self._transition("Objective Evaluation")

        # 6) Objective eval
        evalobj = SceneEvalObj(); evalobj.renderer = self.renderer; evalobj.construct()
        self._transition("Subjective Evaluation")

        # 7) Subjective eval
        evalsubj = SceneEvalSubj(); evalsubj.renderer = self.renderer; evalsubj.construct()
        self._transition("Conclusions")

        # 8) Outro
        outro = SceneOutro(); outro.renderer = self.renderer; outro.construct()

    def _transition(self, next_scene_name: str):
        t = Text(next_scene_name, font_size=52, color=ACCENT_YELLOW, weight=BOLD)
        self.play(FadeIn(t, scale=1.2), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(t, scale=0.9), run_time=1.0)
        self.wait(0.6)


class SceneSSMLImage(Scene):
    def construct(self):
        title = Text("SSML Example", font_size=44, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)
        img = load_img("exemple_ssml").scale(1.0)
        if img.width > config.frame_width * 1.05:
            img.width = config.frame_width * 1.05
        cap = Text("Balises <prosody> / <break> — extrait du cours", font_size=20, color=GRAY, slant=ITALIC)
        grp = Group(img, cap).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)   # ← Group
        self.play(FadeIn(img, shift=UP), FadeIn(cap), run_time=1.4)
        self.wait(3)
        self.play(*map(FadeOut, [title, grp]), run_time=0.8)

class ScenePipelineFigure(Scene):
    def construct(self):
        title = Text("SSML Annotation Pipeline", font_size=44, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))
        img = load_img("pipeline").scale(1.0)
        if img.width > config.frame_width * 1.05:
            img.width = config.frame_width * 1.05
        cap = Text("Figure — Overview of the pipeline", font_size=20, color=GRAY, slant=ITALIC)
        grp = Group(img, cap).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)   # ← Group au lieu de VGroup
        self.play(FadeIn(img, shift=UP), FadeIn(cap))
        self.wait(3)
        self.play(*map(FadeOut, [title, grp]))

class SceneCascadeFigure(Scene):
    def construct(self):
        title = Text("Cascaded Architecture (QwenA → QwenB)", font_size=44, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))
        img = load_img("cascade").scale(1.0)
        if img.width > config.frame_width * 1.05:
            img.width = config.frame_width * 1.05
        cap = Text("Figure — Cascaded LLM for SSML", font_size=20, color=GRAY, slant=ITALIC)
        grp = Group(img, cap).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)   # ← Group
        self.play(FadeIn(img, shift=UP), FadeIn(cap))
        self.wait(3)
        self.play(*map(FadeOut, [title, grp]))


def show_formula(scene: Scene, latex: str, title: str, note: str | None = None):
    y_title = Text(title, font_size=34, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.5)
    scene.play(Write(y_title), run_time=0.8)
    try:
        # Essaie LaTeX (si TeX est installé sur le serveur)
        formula = MathTex(latex).scale(1.2)
        scene.play(Write(formula), run_time=1.6)
    except Exception:
        # Fallback sans LaTeX → remplace les backslashes pour un affichage propre
        safe = latex.replace("\\", "")
        formula = Text(safe, font_size=28, color=WHITE).scale(0.9)
        scene.play(FadeIn(formula, shift=UP), run_time=1.2)
    elems = [y_title, formula]
    if note:
        caption = Text(note, font_size=22, color=GRAY, slant=ITALIC).next_to(formula, DOWN, buff=0.4)
        scene.play(FadeIn(caption), run_time=0.6)
        elems.append(caption)
    scene.wait(2)
    scene.play(*[FadeOut(e) for e in elems], run_time=0.8)


class SceneMathFormulas(Scene):
    """
    Formules clés : semitones, pourcentage de pitch, MAE, F1
    """
    def construct(self):
        # 1) Semitone offset
        show_formula(
            self,
            r"s_i = 12 \cdot \log_2\!\left(\frac{f_0(i)}{f_{0,\mathrm{ref}}}\right)",
            "Pitch → Semitone",
            "Référence: f_{0,ref} (ex: médiane locuteur·rice)"
        )
        # 2) Pourcentage de pitch
        show_formula(
            self,
            r"p_i = \big(2^{\,s_i/12}-1\big)\times 100\%",
            "Semitone → % Pitch",
            "Interprétation pédagogique : variation relative du F0"
        )
        # 3) MAE
        show_formula(
            self,
            r"\mathrm{MAE}=\frac{1}{N}\sum_{i=1}^{N}\left|\,\hat{y}_i - y_i\,\right|",
            "Erreur absolue moyenne (MAE)",
            "Utilisée pour pitch/volume/rate (QwenB vs. baseline)"
        )
        # 4) F1 (break prediction)
        show_formula(
            self,
            r"F_1=2\cdot\frac{P\cdot R}{P+R}",
            "F1-score",
            "P: précision, R: rappel — QwenA ≈ 99.2% sur les pauses"
        )

"""
# ============================================================================
# MAIN SCENE: Full ~10-minute video (orchestrator)
# ============================================================================
class VideoComplet(Scene):

    def construct(self):
        # 0) Intro
        intro = SceneIntro(); intro.renderer = self.renderer; intro.construct()
        self._transition("Audio Signal Basics")

        # 1) Basics
        basics = SceneBasics(); basics.renderer = self.renderer; basics.construct()
        self._transition("The TTS Problem")

        # 2) Problem
        problem = SceneProblem(); problem.renderer = self.renderer; problem.construct()
        self._transition("The Proposed Pipeline")

        # 3) Pipeline (animated boxes)
        pipeline = ScenePipeline(); pipeline.renderer = self.renderer; pipeline.construct()
        self._transition("Pipeline Figure")

        # 3bis) Pipeline (publication figure PNG)
        spf = ScenePipelineFigure(); spf.renderer = self.renderer; spf.construct()
        self._transition("Stage 1: Break Prediction")

        # 4) Stage 1
        stage1 = SceneStage1(); stage1.renderer = self.renderer; stage1.construct()
        self._transition("Stage 2: Prosody Prediction")

        # 5) Stage 2
        stage2 = SceneStage2(); stage2.renderer = self.renderer; stage2.construct()
        self._transition("SSML Example")

        # 5bis) SSML example (image issue du cours)
        ssml_img = SceneSSMLImage(); ssml_img.renderer = self.renderer; ssml_img.construct()
        self._transition("Key Formulas")

        # 5ter) Formules mathématiques (pédagogie)
        formulas = SceneMathFormulas(); formulas.renderer = self.renderer; formulas.construct()
        self._transition("Cascaded Architecture")

        # 5quater) Architecture en cascade (figure PNG)
        cascade_fig = SceneCascadeFigure(); cascade_fig.renderer = self.renderer; cascade_fig.construct()
        self._transition("Objective Evaluation")

        # 6) Objective eval
        evalobj = SceneEvalObj(); evalobj.renderer = self.renderer; evalobj.construct()
        self._transition("Subjective Evaluation")

        # 7) Subjective eval
        evalsubj = SceneEvalSubj(); evalsubj.renderer = self.renderer; evalsubj.construct()
        self._transition("Conclusions")

        # 8) Outro
        outro = SceneOutro(); outro.renderer = self.renderer; outro.construct()

    def _transition(self, next_scene_name: str):
        t = Text(next_scene_name, font_size=52, color=ACCENT_YELLOW, weight=BOLD)
        self.play(FadeIn(t, scale=1.2), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(t, scale=0.9), run_time=1.0)
        self.wait(0.6)
"""