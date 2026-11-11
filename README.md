# Book-converter — free 3D movie production prototype

A free, reproducible first-stage pipeline for turning a book into structured scenes and a basic Blender 3D animatic. **This is a prototype, not a fully autonomous feature-film generator.**

## What works
- Upload a UTF-8 .txt manuscript through a lightweight browser interface
- Split text into deterministic, editable scene records and export JSON
- Generate a Blender Python script that creates a basic 3D scene, animated camera, lights, placeholder characters, and an MP4 render
- Download the scene plan and Blender script; use free Google Colab to render without taxing your computer
- No API keys, paid AI services, or local GPU required for the planning stage

## Run the website
In a terminal (or a Colab notebook):
```bash
git clone https://github.com/mhenbeetsehuk-dot/Book-converter.git
cd Book-converter
python -m pip install -r requirements.txt
python app.py
```
Open http://localhost:8000. On a slow computer, use the Colab notebook workflow instead of local rendering.

## Free cloud rendering
Open `notebooks/render_in_colab.ipynb` in Google Colab, run the cells, upload a generated Blender script and download the MP4. Colab free runtimes are temporary, resource-limited and not guaranteed.

## Limitations
The initial parser uses chapter/paragraph heuristics, not a trained narrative model. Generated actors and sets are placeholders, not characters from your book. No dialogue, lip sync, sound design, long-term continuity, or feature-film automation is implemented yet. These are later milestones.

## Safety
Treat uploaded manuscripts as private; the local server holds uploaded content only in process memory. Do not expose the development server publicly. Review Colab's privacy and usage terms before uploading unpublished manuscripts.
