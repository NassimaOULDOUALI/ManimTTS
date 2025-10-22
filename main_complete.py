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



def overlay_pitch_curve(width=6.5, height=2.4, color="#14B8FF"):
    """
    Courbe F0 stylisée (montées/descentes). Pas d’axes.
    """
    xs = np.linspace(-width/2, width/2, 320)
    # profil F0 synthétique lissé (en demi-tons arbitraires)
    base = 0.0
    contour = (0.6*np.sin(1.2*xs) + 0.3*np.sin(2.7*xs+0.6)
               + 0.15*np.sin(4.6*xs+1.4)) * 0.8 + base
    ys = np.clip(contour, -height/2+0.1, height/2-0.1)
    path = VMobject(stroke_width=3).set_color(color).set_opacity(0.85)
    path.set_points_smoothly([np.array([x, y, 0]) for x, y in zip(xs, ys)])
    # ligne de référence (pitch baseline) très légère
    ref = Line(LEFT*width/2, RIGHT*width/2, stroke_width=2).set_color(color).set_opacity(0.20)
    grp = VGroup(ref, path)
    return grp

def overlay_volume_envelope(width=6.5, height=2.4, color="#E5007D"):
    """
    Enveloppe d’amplitude (aire remplie) + ligne de crête. Loudness ~ énergie.
    """
    xs = np.linspace(-width/2, width/2, 240)
    env = 0.6 + 0.35*np.sin(0.9*xs+0.7) * np.sin(0.35*xs-0.3)
    env = np.clip(env, 0.05, 1.0)
    ys = (env - 0.5) * (height*0.9)  # centre vertical
    # aire (polygone)
    pts = [np.array([xs[i], ys[i], 0]) for i in range(len(xs))]
    poly = Polygon(
        *([*pts, np.array([xs[-1], 0, 0]), np.array([xs[0], 0, 0])]),
        stroke_width=0
    ).set_fill(color=color, opacity=0.18)
    crest = VMobject(stroke_width=3).set_color(color).set_opacity(0.85)
    crest.set_points_smoothly(pts)
    mid = Line(LEFT*width/2, RIGHT*width/2, stroke_width=2).set_color(color).set_opacity(0.15)
    return VGroup(poly, crest, mid)

def overlay_rate_markers(width=6.5, height=2.4, color="#5A1E86", syll_per_sec=4.0):
    """
    Marqueurs de syllabes (ticks) régulièrement espacés = tempo.
    Augmente/diminue syll_per_sec pour accélérer/ralentir visuellement.
    """
    dur = 6.0  # secondes arbitraires pour mapping horizontal
    n = int(dur * syll_per_sec)
    left, right = -width/2, width/2
    xs = np.linspace(left+0.3, right-0.3, n)
    baseline = Line(LEFT*width/2, RIGHT*width/2, stroke_width=2).set_color(color).set_opacity(0.25)
    ticks = VGroup()
    for x in xs:
        t = Line(np.array([x, -0.55*height/2, 0]), np.array([x, 0.55*height/2, 0]), stroke_width=2)
        t.set_color(color).set_opacity(0.55)
        ticks.add(t)
    # un ruban subtil pour le “flow”
    ribbon = Line(LEFT*width/2, RIGHT*width/2, stroke_width=6).set_color(color).set_opacity(0.08)
    return VGroup(ribbon, baseline, ticks)

def overlay_breaks_bands(width=6.5, height=2.4, color="#1363DF", break_positions=( -2.3, 0.0, 2.1 ), band_width=0.55):
    """
    Bandes verticales translucides = pauses. positions en coordonnées écran (x).
    """
    bands = VGroup()
    for x in break_positions:
        rect = Rectangle(width=band_width, height=height, stroke_width=0)
        rect.set_fill(color=color, opacity=0.20)
        rect.move_to(np.array([x, 0, 0]))
        bands.add(rect)
    baseline = Line(LEFT*width/2, RIGHT*width/2, stroke_width=2).set_color(color).set_opacity(0.18)
    return VGroup(baseline, bands)


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
        title = Text(
            "Improving French Synthetic Speech Quality\nvia SSML Prosody Control",
            font_size=44,
            color=ACCENT_BLUE,
            font="DejaVu Sans",
            weight=BOLD
        )
        title.scale_to_fit_width(min(config.frame_width * 0.9, title.width))
        title.to_edge(UP, buff=0.55)
        title.set_y(min(title.get_y(), config.frame_height/2 - 0.7))
        title.set_stroke(BLACK, width=2.2, opacity=0.75)
        title.add_background_rectangle(color=BLACK, opacity=0.18, buff=0.12)
        title.set_z_index(10)

        # split authors en lignes pour révélation progressive
        authors_text = ["Nassima Ould Ouali, Awais Hussain Sani, Ruben Bueno,",
                        "Jonah Dauvet, Tim Luka Horstmann, Eric Moulines"]
        authors_lines = VGroup(*[
            Text(line, font_size=26, color=TEXT_COLOR, font="DejaVu Sans")
            for line in authors_text
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        authors_lines.next_to(title, DOWN, buff=0.55).set_z_index(9)

        affiliations = Text(
            "École Polytechnique, Hi! PARIS Research Center, McGill University",
            font_size=22, color=HI_GREY, slant=ITALIC, font="DejaVu Sans"
        ).next_to(authors_lines, DOWN, buff=0.4).set_z_index(9)

        conference = Text(
            "ICNLSP 2025", font_size=28, color=ACCENT_BLUE, weight=BOLD, font="DejaVu Sans"
        ).next_to(affiliations, DOWN, buff=0.6).set_z_index(9)

        # --- animations ---
        self.play(Write(title), run_time=1.8)
        self.wait(1.1)

        # reveal each author line with a small staggering
        self.play(LaggedStart(*[FadeIn(line, shift=UP) for line in authors_lines], lag_ratio=0.5, run_time=1.2))
        self.wait(1.1)

        # affiliation appear
        self.play(FadeIn(affiliations, shift=UP), run_time=1.2)
        self.wait(1.0)

        # conference with emphasis
        self.play(FadeIn(conference, shift=UP), run_time=1.9)
        self.wait(1.6)

        # emphasis and exit
        self.play(Flash(title, flash_radius=0.32), run_time=1.1)
        self.wait(0.5)
        self.play(LaggedStart(FadeOut(conference), FadeOut(affiliations), *[FadeOut(l) for l in authors_lines], lag_ratio=0.12, run_time=0.9))
        self.play(FadeOut(title), run_time=0.8)


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

        # EFFACER TOUT de la section waveform AVANT de passer à la suivante
        self.play(
            FadeOut(waveform_title), FadeOut(wf), FadeOut(wf_desc), FadeOut(wf_cite),
            run_time=0.8
        )
        self.wait(0.35)

        # ===== SPECTROGRAM (≈30s) =====
        spect_title = Text("Spectrogram: Frequency Energy over Time", font_size=32, color=ACCENT_YELLOW).next_to(title, DOWN, buff=0.5)
        self.play(Write(spect_title), run_time=0.7) 

        sp = load_img("spectrogramme").scale(0.6)
        if sp.width > config.frame_width * 1.05:
            sp.width = config.frame_width * 1.05
        sp.shift(DOWN * 0.2)

        sp_desc = Text(
            "Window 20–30 ms • Hop ≈10 ms • Hann + FFT\n"
            "→ Short window to capture temporal evolution\n"
            "→ Overlap (hop) to smooth transitions\n"
            "→ FFT: transforms signal into frequencies",
            font_size=20, color=TEXT_COLOR, line_spacing=1.1
        ).next_to(sp, DOWN, buff=0.35)
        sp_cite = Text("Databootcamp TTS Course", font_size=16, color=GRAY, slant=ITALIC).to_corner(DR)

        self.play(FadeIn(sp, shift=UP), run_time=0.6)
        
        # CORRECTION : sp_cite HORS de la boucle
        for line in sp_desc:
            self.play(FadeIn(line), run_time=0.12)
        self.play(FadeIn(sp_cite), run_time=0.5)  # ← DÉPLACÉ après la boucle
        
        self.wait(8)  # Temps pour lire le spectrogramme

        # EFFACER TOUT de la section spectrogramme
        self.play(
            FadeOut(spect_title), FadeOut(sp), FadeOut(sp_desc), FadeOut(sp_cite),
            run_time=0.8
        )
        self.wait(0.2)

        # ===== PITCH/F0 (≈29s) =====
        pitch_title = Text("Pitch & Fundamental Frequency (F0)", font_size=32, color=ACCENT_YELLOW).next_to(title, DOWN, buff=0.5)
        self.play(Write(pitch_title), run_time=1.0)

        # ⚠️ Linux est sensible à la casse : fichier 'F0.png'
        f0img = load_img("f0").scale(1.2)
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

        # FIN - effacer tout
        self.play(
            FadeOut(title), FadeOut(pitch_title), FadeOut(f0img), 
            FadeOut(pitch_desc), FadeOut(pitch_cite),
            run_time=0.9
        )
        self.wait(0.1)

# ============================================================================
# SCENE 1bis: Prosody Primer (definitions + SSML + references, 1 page)
# ============================================================================
from manim import *
import numpy as np

# -------------------------------------------------------------------
# Thème & config
# -------------------------------------------------------------------
config.text_backend = "pango"
config.disable_latex = True

BG_COLOR      = "#0B1026"
ACCENT_BLUE   = "#1363DF"
ACCENT_YELLOW = "#E5007D"
TEXT_COLOR    = "#F4F6FA"
ACCENT_PURPLE = "#5A1E86"
ACCENT_CYAN   = "#14B8FF"
HI_GREY       = "#9AA3B2"

config.background_color = BG_COLOR
np.random.seed(7)

# -------------------------------------------------------------------
# Petits utilitaires visuels (sans boîtes)
# -------------------------------------------------------------------
def subtle_background(width=config.frame_width, height=config.frame_height):
    """Grille de points + lignes fines, très faible opacité."""
    dots = VGroup()
    step = 0.6
    for x in np.arange(-width/2, width/2 + 1e-6, step):
        for y in np.arange(-height/2, height/2 + 1e-6, step):
            d = Dot(point=[x, y, 0], radius=0.008, color=HI_GREY)
            d.set_opacity(0.08)
            dots.add(d)
    # Quelques lignes diagonales très légères
    diag1 = Line(LEFT*7+DOWN*3.6, RIGHT*7+UP*3.6, stroke_width=1).set_color(HI_GREY).set_opacity(0.06)
    diag2 = Line(LEFT*7+UP*3.2, RIGHT*7+DOWN*3.2, stroke_width=1).set_color(HI_GREY).set_opacity(0.04)
    return VGroup(dots, diag1, diag2)

def under_title(txt: str, color=ACCENT_BLUE, font_size=46):
    """Titre avec soulignement courbe (sans rectangle)."""
    t = Text(txt, font="DejaVu Sans", weight=BOLD, font_size=font_size, color=color)
    underline = Line(t.get_bottom()+DOWN*0.06+LEFT*0.1, t.get_bottom()+DOWN*0.06+RIGHT*0.1, stroke_width=3)
    underline.set_color(color)
    return VGroup(t, underline).arrange(DOWN, buff=0.08)

def chip(label: str, color=ACCENT_BLUE, font_size=26):
    """
    Tag minimaliste : • pastille + tiret + label (sans box).
    Exemple d’usage : chip("Pitch (F0)", ACCENT_CYAN)
    """
    bullet = Dot(radius=0.06, color=color)
    dash = Line(ORIGIN, RIGHT*0.5, stroke_width=3, color=color)
    txt = Text(label, font="DejaVu Sans", font_size=font_size, color=TEXT_COLOR)
    g = VGroup(bullet, dash, txt).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
    return g

def ssml_line(ssml: str):
    """
    Extrait SSML sur une ligne de base (monospace), sans encadré.
    """
    base = Line(ORIGIN, RIGHT*6.2, stroke_width=2).set_color(HI_GREY).set_opacity(0.35)
    code = Text(ssml, font="DejaVu Sans Mono", font_size=22, color=HI_GREY, slant=ITALIC)
    code.next_to(base, UP, buff=0.12).align_to(base, LEFT)
    return VGroup(base, code)

def tiny_legend(items):
    """
    items: list[(label:str, color:str)]
    Rend une petite légende en ligne (pastilles + labels).
    """
    groups = []
    for label, color in items:
        dot = Dot(radius=0.05, color=color)
        tx  = Text(label, font="DejaVu Sans", font_size=18, color=HI_GREY)
        g   = VGroup(dot, tx).arrange(RIGHT, buff=0.12)
        groups.append(g)
    return VGroup(*groups).arrange(RIGHT, buff=0.5)

def flowing_path():
    """Chemin courbe doux pour un curseur animé (mouvement subtil de gauche à droite)."""
    p = VMobject(stroke_width=3).set_color(ACCENT_BLUE).set_opacity(0.25)
    pts = [
        LEFT*6 + DOWN*1.2,
        LEFT*2.5 + UP*0.2,
        RIGHT*1.5 + DOWN*0.1,
        RIGHT*6 + UP*0.8,
    ]
    p.set_points_smoothly([*pts])
    return p

def moving_cursor_along(path: VMobject, color=WHITE):
    """Petit curseur lumineux qui glisse sur le chemin."""
    dot = Dot(radius=0.08, color=color).set_glow_factor(0.6)
    return dot, MoveAlongPath(dot, path, rate_func=rate_functions.smooth)

# -------------------------------------------------------------------
# Données sémantiques
# -------------------------------------------------------------------
PARAMS = [
    dict(
        key="Pitch (F0)",
        color=ACCENT_CYAN,
        what="Perceived vocal pitch (fundamental frequency).",
        controls="Emphasis, interrogative contours, emotions, boundary tones.",
        ssml='<prosody pitch="+5%">important</prosody>',
        impact="Higher → excitement / Lower → seriousness / Variability → naturalness."
    ),
    dict(
        key="Volume (Loudness)",
        color=ACCENT_YELLOW,
        what="Perceived intensity/energy of speech.",
        controls="Prominence, emotional intensity, attention focus.",
        ssml='<prosody volume="+8dB">listen!</prosody>',
        impact="Loud → emphasis / Soft → intimacy / Dynamics → engagement."
    ),
    dict(
        key="Rate (Speech Tempo)",
        color=ACCENT_PURPLE,
        what="Speed of articulation and pacing.",
        controls="Urgency, clarity, emphasis, speaker personality.",
        ssml='<prosody rate="slow">carefully</prosody>',
        impact="Fast → excitement / Slow → importance / Variation → rhythm."
    ),
    dict(
        key="Breaks (Pauses)",
        color=ACCENT_BLUE,
        what="Strategic silences between phrases.",
        controls="Structure, breathing, emphasis, comprehension.",
        ssml='<break time="500ms"/>',
        impact="Short → rhythm / Long → emphasis / Placement → clarity."
    ),
]

# -------------------------------------------------------------------
# Scène principale (multi-“slides” dans la même scène, pas de boîtes)
# -------------------------------------------------------------------
class SceneProsodyPrimer(Scene):
    # Réglages de timing (ajuste ici pour ralentir/accélérer)
    SLIDE_FADE_IN = 1.00      # apparition d'un slide (avant: 0.5)
    EMPHASIS_IN   = 0.45      # apparition du soulignement du tag (avant: 0.25)
    EMPHASIS_HOLD = 0.45      # respiration après l'emphase (avant: 0.25)
    EMPHASIS_OUT  = 0.35      # disparition du soulignement (avant: 0.2)
    DWELL_BASE    = 1.30      # temps de lecture additionnel sur chaque slide (avant: 0.3)
    SLIDE_FADE_OUT= 0.70      # sortie d'un slide (avant: 0.35)

    # Option: dwell par slide (Pitch, Loudness, Rate, Breaks). Si None, on utilise DWELL_BASE.
    PER_SLIDE_DWELL = [1.6, 1.6, 1.6, 1.6]

    def construct(self):
        # --- Première page : habillage visible ---
        bg = subtle_background()
        self.add(bg)

        title = under_title("Prosody Control Parameters", color=ACCENT_BLUE, font_size=44)
        title.to_edge(UP, buff=0.6)
        subtitle = Text(
            "How pitch, loudness, rate, and pauses shape naturalness",
            font="DejaVu Sans", font_size=22, color=HI_GREY
        ).next_to(title, DOWN, buff=0.25)

        self.play(FadeIn(title, shift=DOWN*0.2), FadeIn(subtitle, shift=DOWN*0.2), run_time=0.8)
        self.wait(0.2)

        # Chemin fluide + curseur (mouvement ambiant)
        path = flowing_path()
        cursor, cursor_anim = moving_cursor_along(path, color=TEXT_COLOR)
        path.shift(DOWN*0.8)
        self.play(Create(path), run_time=0.8)
        self.add(cursor)
        self.play(cursor_anim, run_time=4.2)
        self.wait(0.1)

        # Légende
        legend = tiny_legend([
            ("Pitch", ACCENT_CYAN),
            ("Loudness", ACCENT_YELLOW),
            ("Rate", ACCENT_PURPLE),
            ("Breaks", ACCENT_BLUE),
        ])
        legend.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(legend, shift=UP*0.2), run_time=0.5)
        self.wait(0.4)

        # --- Effacer l'habillage pour les slides suivants (on garde titre + sous-titre) ---
        self.play(
            FadeOut(legend),
            FadeOut(path),
            FadeOut(cursor),
            FadeOut(bg),
            run_time=0.6
        )

        # --- Slides paramétriques : contenu pur (pas de SSML, pas d'habillage) ---
        slides = []
        for p in PARAMS:
            # Tag (pastille + tiret + label)
            tag = chip(p["key"], color=p["color"], font_size=30)

            # Bloc sémantique aéré (What / Controls / Impact)
            what = Text("What", font="DejaVu Sans", weight=BOLD, font_size=22, color=p["color"])
            what_txt = Text(p["what"], font="DejaVu Sans", font_size=22, color=TEXT_COLOR)
            row_what = VGroup(what, what_txt).arrange(RIGHT, buff=0.2, aligned_edge=UP)

            controls = Text("Controls", font="DejaVu Sans", weight=BOLD, font_size=22, color=p["color"])
            controls_txt = Text(p["controls"], font="DejaVu Sans", font_size=22, color=TEXT_COLOR)
            row_ctrl = VGroup(controls, controls_txt).arrange(RIGHT, buff=0.2, aligned_edge=UP)

            impact = Text("Impact", font="DejaVu Sans", weight=BOLD, font_size=22, color=p["color"])
            impact_txt = Text(p["impact"], font="DejaVu Sans", font_size=22, color=TEXT_COLOR)
            row_imp = VGroup(impact, impact_txt).arrange(RIGHT, buff=0.2, aligned_edge=UP)

            # Colonne gauche uniquement (pas de colonne droite)
            left_col = VGroup(tag, row_what, row_ctrl, row_imp).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
            left_col.to_edge(LEFT, buff=1.2).shift(DOWN*0.3)

            slide = VGroup(left_col)
            slide.set_opacity(0)
            slides.append(slide)

        # --- Affichage séquentiel des slides (contenu pur, ralenti) ---
        for i, slide in enumerate(slides):
            # apparition du slide
            self.add(slide)
            self.play(slide.animate.set_opacity(1), run_time=self.SLIDE_FADE_IN)

            # Accent léger : souligner le tag, respiration, disparition
            tag_label = slide[0][0]  # chip(...)
            accent = Line(
                tag_label.get_bottom()+DOWN*0.12+LEFT*0.1,
                tag_label.get_bottom()+DOWN*0.12+RIGHT*0.1,
                stroke_width=4
            ).set_color(PARAMS[i]["color"])
            self.play(GrowFromCenter(accent), run_time=self.EMPHASIS_IN)
            self.wait(self.EMPHASIS_HOLD)
            self.play(FadeOut(accent), run_time=self.EMPHASIS_OUT)

            # Temps de lecture (dwell) plus long
            dwell = (self.PER_SLIDE_DWELL[i]
                     if self.PER_SLIDE_DWELL and i < len(self.PER_SLIDE_DWELL)
                     else self.DWELL_BASE)
            self.wait(dwell)

            # transition vers le slide suivant
            if i < len(slides) - 1:
                self.play(slide.animate.set_opacity(0), run_time=self.SLIDE_FADE_OUT)
                self.remove(slide)

        # --- Conclusion compacte (pipeline) ---
        pipeline_title = Text(
            "Prosody Control Pipeline",
            font="DejaVu Sans", font_size=26, color=ACCENT_BLUE, weight=BOLD
        ).to_edge(DOWN, buff=1.0)

        steps = Text(
            "Analyze speech → Extract parameters → Apply via SSML → Synthesize natural output",
            font="DejaVu Sans", font_size=22, color=TEXT_COLOR
        ).next_to(pipeline_title, UP, buff=0.3).align_on_border(DOWN, buff=1.6)

        connector = Line(LEFT*5.2, RIGHT*5.2, stroke_width=2).set_color(HI_GREY).set_opacity(0.25)
        connector.next_to(steps, UP, buff=0.35)

        self.play(
            FadeIn(connector, shift=UP*0.2),
            FadeIn(steps, shift=UP*0.2),
            FadeIn(pipeline_title, shift=UP*0.2),
            run_time=0.9
        )
        self.wait(1.0)

        # Sortie propre
        self.play(
            FadeOut(steps),
            FadeOut(pipeline_title),
            FadeOut(connector),
            FadeOut(title),
            FadeOut(subtitle),
            run_time=0.9
        )

# ============================================================================
# SCENE 2A: TTS Expressivity Problem (~35s)
# ============================================================================
# --- Helper PATCHÉ : même police pour le titre souligné ---
FONT_SANS = "DejaVu Sans"

def under_title(txt: str, color=ACCENT_BLUE, font_size=46, font: str = FONT_SANS):
    t = Text(txt, font=font, weight=BOLD, font_size=font_size, color=color)
    underline = Line(
        t.get_bottom() + DOWN*0.06 + LEFT*0.1,
        t.get_bottom() + DOWN*0.06 + RIGHT*0.1,
        stroke_width=3
    ).set_color(color)
    return VGroup(t, underline).arrange(DOWN, buff=0.08)


class SceneProblemTTS(Scene):
    # Timings
    T_IN_TITLE   = 1.0
    T_IN_BLOCK   = 0.9
    T_LIST       = 2.0
    T_DWELL_1    = 1.2
    T_TRANSITION = 0.7
    T_IN_S2      = 0.8
    T_DWELL_2    = 1.2
    T_OUT        = 0.8

    FONT_SANS = FONT_SANS  # "DejaVu Sans"

    def T(self, s, **kw):
        """Wrapper Text : force la même police partout."""
        kw.setdefault("font", self.FONT_SANS)
        return Text(s, **kw)

    def construct(self):
        # --- Titre (persiste sur les 2 slides) : même police via helper patché
        title = under_title("The TTS Expressivity Problem",
                            color=ACCENT_BLUE, font_size=46, font=self.FONT_SANS)
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title, shift=DOWN*0.2), run_time=self.T_IN_TITLE)
        self.wait(0.15)

        # --- Baromètre (même police pour les labels)
        lbl_intel = self.T("Intelligibility", font_size=22, color=HI_GREY)
        lbl_expr  = self.T("Expressivity",  font_size=22, color=HI_GREY)
        bar_w = 4.8

        bar_i_bg = Line(ORIGIN, RIGHT*bar_w, stroke_width=8).set_color(HI_GREY).set_opacity(0.25)
        bar_i_fg = Line(ORIGIN, RIGHT*(bar_w*0.86), stroke_width=10).set_color(ACCENT_YELLOW)
        g_i = VGroup(lbl_intel, VGroup(bar_i_bg, bar_i_fg).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.16)

        bar_e_bg = Line(ORIGIN, RIGHT*bar_w, stroke_width=8).set_color(HI_GREY).set_opacity(0.25)
        bar_e_fg = Line(ORIGIN, RIGHT*(bar_w*0.28), stroke_width=10).set_color(ACCENT_PURPLE)
        g_e = VGroup(lbl_expr, VGroup(bar_e_bg, bar_e_fg).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.16)

        meter = VGroup(g_i, g_e).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.8).shift(DOWN*0.2)
        self.play(FadeIn(meter, shift=UP*0.1), run_time=self.T_IN_BLOCK)

        # ========== SLIDE 1 ==========
        heading = self.T("Current State", font_size=32, color=ACCENT_YELLOW, weight=BOLD)
        bullet_items = [
            "• Commercial TTS prioritizes clarity",
            "• Prosodic variation is limited",
            "• Leads to monotonous speech",
            "• French prosody particularly affected",
        ]
        bullets = VGroup(*[
            self.T(item, font_size=26, color=TEXT_COLOR)
            for item in bullet_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        col_state = VGroup(heading, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.42)

        heading2 = self.T("Consequences", font_size=32, color=ACCENT_CYAN, weight=BOLD)
        cons_items = [
            "↓ Engagement & naturalness",
            "↓ Perceived speaker intent",
            "↑ Listening fatigue",
        ]
        cons = VGroup(*[
            self.T(s, font_size=24, color=TEXT_COLOR) for s in cons_items
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
            run_time=self.T_IN_BLOCK
        )
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.08) for b in bullets], lag_ratio=0.22), run_time=self.T_LIST)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in cons],    lag_ratio=0.22), run_time=self.T_LIST*0.7)
        self.wait(self.T_DWELL_1)

        # ========== TRANSITION ==========
        self.play(FadeOut(slide1), run_time=self.T_TRANSITION)

        # ========== SLIDE 2 : Why French? ==========
        why = self.T("Why French?", font_size=30, color=ACCENT_BLUE, weight=BOLD)
        why_u = Line(
            why.get_bottom()+DOWN*0.06+LEFT*0.1,
            why.get_bottom()+DOWN*0.06+RIGHT*0.1,
            stroke_width=3
        ).set_color(ACCENT_BLUE)

        # Bloc multi-lignes : même police
        why_items = ["• Dense liaison & schwa deletion",
        "• Rich boundary tones",
        "• Subtle phrase-final lengthening",
        "• Low prosodic control → flatter contours",
        "• Misplaced pauses",]

        why_bullets = VGroup(*[self.T(s, font_size=26, color=TEXT_COLOR) for s in why_items]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)


        why_blk = VGroup(
            VGroup(why, why_u).arrange(DOWN, buff=0.06),
            why_bullets
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)

        why_blk.next_to(meter, RIGHT, buff=1.2).align_to(meter, UP)
        self.play(FadeIn(why_blk, shift=UP*0.12), run_time=self.T_IN_S2)
        self.wait(self.T_DWELL_2)



        citation = self.T("Ref: ICNLSP 2025 (pp. 1–2)", font_size=18, color=HI_GREY, slant=ITALIC).to_corner(DR)
        self.play(FadeIn(citation), run_time=0.5)
        self.wait(0.6)

        # Sortie propre
        self.play(
            FadeOut(citation),
            FadeOut(why_blk),
            FadeOut(meter),
            run_time=self.T_OUT
        )
        self.play(FadeOut(title), run_time=self.T_OUT*0.9)
        self.wait(0.3)



# ============================================================================
# SCENE 2B: SSML Challenges (~40s)
# ============================================================================
class SceneProblemSSML(Scene):
    # Timings (ajuste ici au besoin)
    T_IN_TITLE   = 1.0
    T_IN_BLOCK   = 0.9
    T_LIST       = 2.0
    T_DWELL_1    = 1.2
    T_TRANSITION = 0.7
    T_IN_S2      = 0.8
    T_DWELL_2    = 1.2
    T_OUT        = 0.8

    FONT_SANS = "DejaVu Sans"  # police robuste avec Pango

    def T(self, s, **kw):
        """Text wrapper: applique la même police partout."""
        kw.setdefault("font", self.FONT_SANS)
        return Text(s, **kw)

    def construct(self):
        # --- Titre (persiste sur 2 slides)
        title = under_title("SSML Challenges", color=ACCENT_BLUE, font_size=46, font=self.FONT_SANS)
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title, shift=DOWN*0.2), run_time=self.T_IN_TITLE)
        self.wait(0.15)

        # =========================
        # SLIDE 1 : Why SSML is hard in practice
        # =========================
        heading = self.T("Why SSML is hard in practice", font_size=32, color=ACCENT_YELLOW, weight=BOLD)
        bullet_items = [
            "• Manual markup does not scale",
            "• LLMs often omit or misplace closing tags",
            "• Invalid / non-standard attributes and values",
            "• Imprecise prosodic control across engines",
            "• Vendor dialects diverge from W3C baseline",
        ]
        bullets = VGroup(*[
            self.T(item, font_size=26, color=TEXT_COLOR) for item in bullet_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)

        slide1 = VGroup(heading, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        slide1.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=1.2)

        self.play(FadeIn(heading, shift=UP*0.12), run_time=self.T_IN_BLOCK)
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.08) for b in bullets], lag_ratio=0.22), run_time=self.T_LIST)
        self.wait(self.T_DWELL_1)

        self.play(Indicate(bullets[0], scale_factor=1.05), run_time=0.7); self.wait(0.3)
        self.play(Indicate(bullets[3], scale_factor=1.05), run_time=0.7); self.wait(0.42)

        # =========================
        # TRANSITION → SLIDE 2
        # =========================
        self.play(FadeOut(slide1), run_time=self.T_TRANSITION)

        # =========================
        # SLIDE 2 : Typical failure patterns (UNE SEULE COLONNE)
        # =========================
        heading2 = self.T("Typical failure patterns", font_size=32, color=ACCENT_CYAN, weight=BOLD)

        cat1 = VGroup(
            self.T("• Syntax: unclosed/misaligned tags, bad nesting", font_size=26, color=TEXT_COLOR),
            self.T("• Escaping issues in XML contexts",              font_size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        cat2 = VGroup(
            self.T("• Semantics: unsupported params or units",       font_size=26, color=TEXT_COLOR),
            self.T("• Engine-specific ranges silently clipped",      font_size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        cat3 = VGroup(
            self.T("• Control: conflicting nested <prosody>",        font_size=26, color=TEXT_COLOR),
            self.T("• Global vs local overrides not explicit",       font_size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        cat4 = VGroup(
            self.T("• Evaluation: MOS-only, no prosody metrics",     font_size=26, color=TEXT_COLOR),
            self.T("• No automatic validation step",                 font_size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        # UNE COLONNE : on empile les 4 catégories verticalement
        grid_single = VGroup(cat1, cat2, cat3, cat4).arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        slide2 = VGroup(heading2, grid_single).arrange(DOWN, aligned_edge=LEFT, buff=0.42)

        # Placement sous le titre, à gauche
        slide2.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=1.2)

        # --- Auto-scale pour garantir "jamais hors cadre" ---
        margin_w = 0.7   # marge latérale
        margin_h = 0.9   # marge sous le titre
        max_w = config.frame_width  - 2*margin_w
        max_h = config.frame_height - (title.height + margin_h) - 0.4

        scale_factor = min(max_w / slide2.width, max_h / slide2.height, 1.0)
        if scale_factor < 1.0:
            slide2.scale(scale_factor)

        # reposition après scale
        slide2.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=margin_w)

        # Arrivée slide 2
        self.play(FadeIn(heading2, shift=UP*0.12), run_time=self.T_IN_S2)
        self.play(
            LaggedStart(
                FadeIn(cat1, shift=UP*0.08),
                FadeIn(cat2, shift=UP*0.08),
                FadeIn(cat3, shift=UP*0.08),
                FadeIn(cat4, shift=UP*0.08),
                lag_ratio=0.18
            ),
            run_time=self.T_LIST
        )
        self.wait(self.T_DWELL_2)

        # Référence (coin bas droit)
        citation = self.T("Ref: ICNLSP 2025 (pp. 1–2)", font_size=18, color=HI_GREY, slant=ITALIC).to_corner(DR)
        self.play(FadeIn(citation), run_time=0.5)
        self.wait(0.8)

        # Sortie propre
        self.play(FadeOut(citation), FadeOut(slide2), run_time=self.T_OUT)
        self.play(FadeOut(title), run_time=self.T_OUT*0.9)
        self.wait(0.7)


# ============================================================================
# SCENE 3A: Proposed Pipeline — Interactive Overview (HORIZONTAL, step-by-step)
# ============================================================================
class ScenePipelineInteractive(Scene):
    def _create_step_box(self, step_title: str, step_desc: str, color):
        title = Text(step_title, font_size=30, color=color, weight=BOLD, font="DejaVu Sans")
        desc  = Text(step_desc,  font_size=22, color=TEXT_COLOR, line_spacing=0.9, font="DejaVu Sans")
        box_content = VGroup(title, desc).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rect = RoundedRectangle(corner_radius=0.18, stroke_color=color, stroke_width=3)
        rect.surround(box_content, buff=0.28)
        return VGroup(rect, box_content)

    def construct(self):
        # Titre
        title = Text("The Proposed Pipeline — Interactive Overview",
                     font_size=46, color=ACCENT_BLUE, weight=BOLD, font="DejaVu Sans")\
                .to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.0); self.wait(0.3)

        # Étapes (texte à la ligne pour contrôler la largeur)
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

        steps = VGroup(step1, step2, step3, step4, step5).arrange(RIGHT, buff=0.6, aligned_edge=UP)

        # Placement sous le titre + auto-fit pour tenir dans le cadre
        layout = VGroup(steps).next_to(title, DOWN, buff=0.5)
        max_w = config.frame_width * 0.92
        if layout.width > max_w:
            layout.scale_to_fit_width(max_w)
        self.add(layout)  # on gère l’apparition manuellement étape par étape

        # Animation interactive : apparition 1 par 1 + flèche vers l'étape suivante
        # On cache tout au départ
        for s in steps:
            s.set_opacity(0)
        self.wait(0.1)

        arrows = VGroup()  # pour pouvoir faire un FadeOut groupé ensuite

        # Déroulé pas-à-pas
        for i, s in enumerate(steps):
            # fade-in de l’étape i
            self.play(s.animate.set_opacity(1), run_time=0.6)
            self.play(Indicate(s[0], scale_factor=1.03), run_time=0.4)  # met en avant le cadre
            self.wait(0.1)

            # si une étape suivante existe, on trace la flèche après apparition du bloc courant
            if i < len(steps) - 1:
                a = Arrow(
                    start=steps[i].get_right(),
                    end=steps[i+1].get_left(),
                    buff=0.18,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.12,
                    color=TEXT_COLOR
                )
                arrows.add(a)
                self.play(Create(a), run_time=0.4)
                self.wait(0.05)

        # Petite mise en avant alternée (donne du rythme sans surcharger)
        for idx in (0, 2, 4):
            self.play(Indicate(steps[idx][0], scale_factor=1.04), run_time=0.45)
            self.wait(0.1)

        # Citation (optionnelle)
        citation = Text("Données : ICNLSP 2025, p. 3 (Section 3) + slide 26",
                        font_size=18, color=HI_GREY, slant=ITALIC, font="DejaVu Sans")\
                        .to_corner(DR)
        self.play(FadeIn(citation), run_time=0.4); self.wait(0.6)

        # Sortie propre
        self.play(FadeOut(arrows, run_time=0.5))
        self.play(FadeOut(steps, shift=DOWN, run_time=0.7),
                  FadeOut(citation, run_time=0.4),
                  FadeOut(title, run_time=0.6))
        self.wait(0.2)

# ============================================================================
# SCENE 3B: Proposed Pipeline — Figure (Image) (~45s)
# ============================================================================
from manim import *
from pathlib import Path

class ScenePipelineFigure(Scene):
    FONT_SANS = "DejaVu Sans"

    def T(self, s, **kw):
        kw.setdefault("font", self.FONT_SANS)
        return Text(s, **kw)

    def _load_image_or_placeholder(self, path: str, width_hint: float) -> Mobject:
        p = Path(path)
        if p.exists():
            img = ImageMobject(str(p))
            # normalise un peu la taille initiale
            if img.width > width_hint:
                img.width = width_hint
            return img
        # Fallback : placeholder discret (pas de “boîte” ; juste contours fins)
        warn = self.T("assets/pipeline.png not found", font_size=22, color=RED, slant=ITALIC)
        w, h = width_hint, width_hint * 0.56
        frame = Rectangle(width=w, height=h, stroke_color=HI_GREY, stroke_width=2).set_opacity(0)
        cross = VGroup(
            Line(frame.get_corner(UL), frame.get_corner(DR)),
            Line(frame.get_corner(UR), frame.get_corner(DL)),
        ).set_color(HI_GREY).set_opacity(0.35)
        ph = VGroup(frame, cross, warn).arrange(DOWN, buff=0.25)
        return ph

    def construct(self):
        # --- Titre (même police que partout)
        title = self.T("The Proposed Pipeline — Figure",
                       font_size=46, color=ACCENT_BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN*0.15), run_time=1.0)
        self.wait(0.25)

        # --- Chargement image (robuste)
        # Mets ton chemin réel ici si différent :
        img = self._load_image_or_placeholder("assets/pipeline.png", width_hint=config.frame_width * 0.92)

        # --- Caption (pré-créée pour estimer la place)
        cap = self.T("Overview of the full data & SSML pipeline",
                     font_size=20, color=HI_GREY, slant=ITALIC)

        # --- Layout & auto-scale pour ne JAMAIS sortir du cadre
        top_margin   = 0.60
        bottom_space = 0.80
        side_margin  = 0.60

        # largeur/hauteur utiles sous le titre
        max_w = config.frame_width  - 2*side_margin
        max_h = config.frame_height - (title.height + top_margin + bottom_space + cap.height)

        # on met d’abord l’image à une largeur “raisonnable”
        img_width_target = min(max_w, config.frame_width * 0.92)
        if hasattr(img, "width"):
            if img.width > img_width_target:
                img.width = img_width_target

        # si la hauteur dépasse, on scale proportionnellement
        # (on a besoin du groupe pour mesurer hauteur avec caption)
        grp = VGroup(img, cap).arrange(DOWN, buff=0.3, aligned_edge=CENTER)

        # scale pour rentrer en hauteur/largeur
        scale_factor = min(max_w / grp.width, max_h / grp.height, 1.0)
        if scale_factor < 1.0:
            grp.scale(scale_factor)

        # position finale sous le titre
        grp.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=side_margin)

        # --- Apparition
        self.play(FadeIn(img, shift=UP*0.12), run_time=0.9)
        self.play(FadeIn(cap, shift=UP*0.06), run_time=0.4)
        self.wait(0.6)

        # --- Ken Burns discret (scale + léger pan vertical)
        # (sans MovingCameraScene, on anime le groupe)
        self.play(grp.animate.scale(1.04).shift(UP*0.06), run_time=0.9)
        self.wait(1.0)

        # --- Citation en bas à droite
        citation = self.T("Figure: internal design (assets/pipeline.png)",
                          font_size=18, color=HI_GREY, slant=ITALIC).to_corner(DR)
        self.play(FadeIn(citation), run_time=0.4)
        self.wait(0.6)

        # --- Sortie propre
        self.play(
            FadeOut(citation, run_time=0.4),
            FadeOut(cap, run_time=0.5),
            FadeOut(img, run_time=0.6),
        )
        self.play(FadeOut(title), run_time=0.6)
        self.wait(0.3)


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
# SCENE 1bis: Prosody — Interactive Definitions (EN, short, step-by-step)
# ============================================================================
class SceneProsodyInteractive(Scene):
    def _card(self, title: str, lines: list[str], color):
        head = Text(title, font_size=30, color=color, weight=BOLD, font="DejaVu Sans")
        body = VGroup(*[
            Text(line, font_size=22, color=TEXT_COLOR, font="DejaVu Sans")
            for line in lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        content = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rect = RoundedRectangle(corner_radius=0.2, stroke_color=color, stroke_width=3)
        rect.surround(content, buff=0.28)
        return VGroup(rect, content)

    def construct(self):
        # Title
        title = Text("Prosody — the building blocks",
                     font_size=46, color=ACCENT_BLUE, weight=BOLD, font="DejaVu Sans")\
                .to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=0.9)

        # 4 concise definition cards (EN)
        card_pitch = self._card(
            "Pitch (F0)",
            ["Perceived height of the voice.", "Linked to vocal-fold vibration (frequency)."],
            ACCENT_CYAN
        )
        card_volume = self._card(
            "Volume (loudness)",
            ["Perceived intensity of the sound.", "How strong or soft it feels."],
            ACCENT_YELLOW
        )
        card_rate = self._card(
            "Rate (tempo)",
            ["Speed of speaking.", "How fast words are delivered."],
            ACCENT_PURPLE
        )
        card_breaks = self._card(
            "Breaks (pauses)",
            ["Short silences between phrases.", "They shape rhythm and meaning."],
            ACCENT_BLUE
        )

        cards = VGroup(card_pitch, card_volume, card_rate, card_breaks)\
            .arrange(RIGHT, buff=0.6, aligned_edge=UP)

        # Place row below title and auto-fit to one page
        cards.next_to(title, DOWN, buff=0.55)
        max_w = config.frame_width * 0.94
        if cards.width > max_w:
            cards.scale_to_fit_width(max_w)

        # Start hidden
        for c in cards:
            c.set_opacity(0)
        self.add(cards)

        arrows = VGroup()

        # Step-by-step reveal: card -> arrow -> next card
        for i, c in enumerate(cards):
            self.play(c.animate.set_opacity(1), run_time=0.55)
            self.play(Indicate(c[0], scale_factor=1.03), run_time=0.35)
            if i < len(cards) - 1:
                a = Arrow(
                    start=cards[i].get_right(),
                    end=cards[i+1].get_left(),
                    buff=0.18,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.12,
                    color=TEXT_COLOR
                )
                arrows.add(a)
                self.play(Create(a), run_time=0.4)

        # Clean exit
        self.wait(0.4)
        self.play(FadeOut(arrows, run_time=0.5),
                  FadeOut(cards, shift=DOWN, run_time=0.6),
                  FadeOut(title, run_time=0.6))


# ============================================================================
# MAIN SCENE: Full 10-minute video
# ============================================================================
class VideoComplet(Scene):
    def construct(self):
        # 0) Intro
        intro = SceneIntro(); intro.renderer = self.renderer; intro.construct()
        self._transition("Audio Signal Basics")

        basics = SceneBasics(); basics.renderer = self.renderer; basics.construct()
        self._transition("Prosody building blocks")

        pros = SceneProsodyInteractive(); pros.renderer = self.renderer; pros.construct()
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

# ============================================================================