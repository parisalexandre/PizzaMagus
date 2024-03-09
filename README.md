# Packages

```
conda create -n pizza python=3.9.7
conda activate pizza
conda install anaconda::flask
conda install werkzeug=2.2.3
conda install numpy
conda install conda-forge::pyspellchecker
conda install conda-forge::pytesseract
```

Linux:
```
sudo apt-get install tesseract-ocr-all
```

MacOS:
```
brew install tesseract-lang
```

Windows:
1. Choose the additional language and script models from e.g. one of the places linked from [here](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files)

2. Download the `traineddata` file to the `tessdata` folder of tesseract on your PC, e.g. `C:\Program Files\Tesseract-OCR\tessdata`. It is also possible to create new subfolders within that folder to distinguish for example the best and fast models.

3. Check that the new languages are recognized by:
```
tesseract --list-langs
```
