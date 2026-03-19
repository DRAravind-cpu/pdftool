# PDF Tools (Streamlit)

A local Streamlit web app that bundles common **PDF + Image** operations (merge/split/compress/convert/edit/security and image compress/resize/crop/convert/editor/upscale/background removal/watermark/memes/blur).

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- There are **no in-app quotas/limits**; processing is constrained only by your machine resources.
- Security-related tools are implemented safely (e.g., **Unlock PDF requires you to know the password**; the app does not brute-force or bypass encryption).

- Multi-file uploads (images/PDFs) are processed in **ascending filename order (A→Z)**.
- Image uploads support common formats including **HEIC/HEIF, PNG, JPG/JPEG, WebP, TIFF**, etc. (HEIC/HEIF via `pillow-heif`).
- Some features (e.g., Office conversions, OCR, PDF/A) may require optional system tools:
  - **LibreOffice** for Word/PowerPoint/Excel conversions
  - **Tesseract** for OCR
  - **Poppler** for PDF → image rendering
  - **Ghostscript** for PDF/A and some optimization workflows
  - **qpdf** for better optimize/repair (recommended)

- Some Image tools have optional enhancements:
  - **rembg** (Python package) for stronger background removal (otherwise the app uses a simple near-white remover)
  - **opencv-python** (Python package) for auto face detection in “Blur face” (otherwise use manual boxes)

The UI will show clear messages if an optional dependency is missing.

## Optional installs (macOS with Homebrew)

```bash
brew install poppler tesseract ghostscript qpdf
brew install --cask libreoffice
```
