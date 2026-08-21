#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y poppler-utils qpdf tesseract-ocr tesseract-ocr-spa ocrmypdf

for command in pdftotext pdftoppm pdfinfo qpdf tesseract ocrmypdf; do
  command -v "$command" >/dev/null
  printf '%s: %s\n' "$command" "$(command -v "$command")"
done

tesseract --list-langs | grep -Fx spa >/dev/null
printf 'Entorno PDF/OCR listo.\n'
