
# TTS & SSML Prosody Control - 10-Minute Manim Video

This project creates a comprehensive 10-minute video presentation about "Improving French Synthetic Speech Quality via SSML Prosody Control" using Manim Community v0.18+.

## 📁 Project Structure

```
tts_ssml_manim_video/
├── main.py                 # Main Manim script with all scenes
├── assets/                 # Visual assets extracted from PPT
│   ├── slide_20_img_8.png
│   ├── slide_23_img_7.png
│   └── slide_23_img_8.png
├── extracted_data/         # Data extraction from source files
│   └── data_extraction.json
├── citations.jsonl         # Complete source tracking
├── README.md              # This file
└── qc_report.md           # Anti-hallucination checklist

```

## 📊 Source Files

- **PDF**: `ICNLSP 2025_P25-1088_camera_ready.pdf` - Research paper
- **PPT**: `Text_To_Speech_copy (1).pptx` - Course slides

## 🎬 Video Structure

Total Duration: **600 seconds ± 15s (10 minutes)**

### Scene Breakdown

| Scene | Duration | Description | Source |
|-------|----------|-------------|--------|
| SceneIntro | 30s | Title, authors, paper reference | PDF p.1 |
| SceneBasics | 90s | Waveform, spectrogram, pitch/F0 | PPT slides 9,12,13,16,22 |
| SceneProblem | 75s | TTS expressivity problem | PDF p.1-2 |
| ScenePipeline | 90s | Text→SSML→TTS pipeline | PDF p.3 + PPT slide 26 |
| SceneStage1 | 60s | Break insertion (QwenA) | PDF p.4,7 Table 4 |
| SceneStage2 | 60s | Prosody prediction (QwenB) | PDF p.4-5 |
| SceneEvalObj | 105s | F1, MAE/RMSE metrics | PDF p.6-7 Tables 4-5 |
| SceneEvalSubj | 60s | MOS scores, AB test | PDF p.1,6 |
| SceneOutro | 30s | Conclusions & future work | PDF p.8 |
| **Total** | **600s** | *Including transitions* | |

## 🚀 Execution

### Requirements

```bash
# Install Manim Community v0.18+
pip install manim

# Verify installation
manim --version
```

### Generate the Full Video

```bash
manim -pqh main.py Main -o video.mp4 --format=mp4 --fps 30 --resolution 1920,1080
```

### Generate Individual Scenes

```bash
# Scene 0: Introduction
manim -pqh main.py SceneIntro -o intro.mp4 --format=mp4 --fps 30 --resolution 1920,1080

# Scene 1: Audio Basics
manim -pqh main.py SceneBasics -o basics.mp4 --format=mp4 --fps 30 --resolution 1920,1080

# Scene 2: TTS Problem
manim -pqh main.py SceneProblem -o problem.mp4 --format=mp4 --fps 30 --resolution 1920,1080

# Scene 3: Pipeline
manim -pqh main.py ScenePipeline -o pipeline.mp4 --format=mp4 --fps 30 --resolution 1920,1080

# Scene 4: Stage 1
manim -pqh main.py SceneStage1 -o stage1.mp4 --format=mp4 --fps 30 --resolution 1920,1080

# Scene 5: Stage 2
manim -pqh main.py SceneStage2 -o stage2.mp4 --format=mp4 --fps 30 --resolution 1920,1080

# Scene 6: Objective Evaluation
manim -pqh main.py SceneEvalObj -o eval_obj.mp4 --format=mp4 --fps 30 --resolution 1920,1080

# Scene 7: Subjective Evaluation
manim -pqh main.py SceneEvalSubj -o eval_subj.mp4 --format=mp4 --fps 30 --resolution 1920,1080

# Scene 8: Conclusions
manim -pqh main.py SceneOutro -o outro.mp4 --format=mp4 --fps 30 --resolution 1920,1080
```

### Command Options

- `-pqh`: Preview, Quality High
- `-o video.mp4`: Output filename
- `--format=mp4`: Video format (H.264)
- `--fps 30`: Frame rate
- `--resolution 1920,1080`: Full HD resolution

## 🎨 Visual Design

### Theme Colors

- **Background**: `#0b0f17` (dark blue-black)
- **Accent Blue**: `#7cc5ff` (titles, highlights)
- **Accent Yellow**: `#ffd166` (emphasis, numbers)
- **Text**: White

### Typography

- Clean sans-serif Text() objects
- Font sizes: 16-52pt depending on hierarchy
- Bold weights for emphasis
- Italic for citations

## 📈 Key Data Points

All data is sourced from the provided files with zero hallucination:

### From PDF (ICNLSP 2025)

- **Corpus**: 14h French, 14 speakers (42% female), 122,303 words
- **F₁ Score**: 99.24% (QwenA break prediction)
- **MAE**: Pitch 0.97%, Volume 1.09%, Rate 1.10%
- **Break MAE**: 132.89 ms
- **MOS**: 3.20 → 3.87 (p < 0.005)
- **Preference**: 15 of 18 participants

### From PPT (Course Slides)

- Waveform: Time (s) vs. Amplitude (normalized)
- Spectrogram: 20-30ms windows, ~10ms hop, Hann window
- Pitch: Related to F₀ (fundamental frequency)

## 📝 Citation Summary

### Scene-wise Source Distribution

- **SceneIntro**: PDF page 1
- **SceneBasics**: PPT slides 9, 12, 13, 16, 22
- **SceneProblem**: PDF pages 1-2
- **ScenePipeline**: PDF page 3 + PPT slide 26
- **SceneStage1**: PDF page 4, 7 (Table 4), Appendix A
- **SceneStage2**: PDF pages 4-5
- **SceneEvalObj**: PDF pages 6-7 (Tables 4-5)
- **SceneEvalSubj**: PDF pages 1, 6 (Section 5.1)
- **SceneOutro**: PDF page 8 (Sections 6-7)

## 📚 References

- **Paper**: [Improving French Synthetic Speech Quality via SSML Prosody Control](https://aclanthology.org/2025.icnlsp-1.30/) (Ouali et al., ICNLSP 2025)
- **Code Repository**: https://github.com/hi-paris/Prosody-Control-French-TTS

## 👥 Authors

- Nassima Ould Ouali 

## 📄 License

This project is licensed under the MIT License. 

---

**Manim Version**: Community v0.18+
**Duration**: 600s ± 15s
**Resolution**: 1920x1080 @ 30fps
**Format**: H.264 MP4
