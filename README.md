# HSE Industrial Software Development Elective HW 1

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

A simple Flask archiving application.

## Usage
Installation:  
```
git clone https://github.com/QwertygidQ/isd_homework_1.git
cd isd_homework_1
pip3 install -r requirements.txt
```

Running:
```
cd ..  (if inside isd_homework_1/)
python3 -m isd_homework_1
```

Usage with curl:
```
curl -F 'file=@/path/to/your/file' http://127.0.0.1:8080/convert/*ARCHIVE TYPE* (--output *FILENAME*)
```

## Testing
```
python3 -m isd_homework_1  (run the server for integration testing)
pytest isd_homework_1
```

## Available formats
* tar
* tar.gz
* tar.bz2
* tar.xz
* zip
