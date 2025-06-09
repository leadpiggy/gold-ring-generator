# Headshot Ring Overlay

This repository provides a Python script (`gold-ring.py`) to automatically detect and crop a face-centric square headshot, apply a smooth, anti-aliased circular mask via supersampling, and overlay a gold ring—producing a crisp, 800×800 PNG ready for avatars or profile images.

## Features

* **Face Detection & Centering**: Uses OpenCV’s Haar cascade to locate the largest face and center the crop on it.
* **Fallback Crop**: If no face is detected, the image is center-cropped to the largest square possible.
* **Supersampled Anti-Aliased Mask**: Generates a high-quality circular mask via 4× supersampling and downsampling with LANCZOS.
* **Ring Overlay**: Overlays a provided 800×800 transparent gold ring PNG (`RING_IMAGE`) on top of the circular headshot.
* **Test Mode & CLI**: Includes a hardcoded `TEST_IMAGE` for quick tests and an optional CLI interface via `argparse_test()`.

## Requirements

* Python 3.7+
* [Pillow](https://pypi.org/project/Pillow/)
* [opencv-python](https://pypi.org/project/opencv-python/)

## Installation

1. Clone this repository:

   ```bash
   git clone https://your-repo-url.git
   cd your-repo
   ```
2. Install dependencies:

   ```bash
   pip install Pillow opencv-python
   ```

## Configuration

Edit the top of `gold-ring.py` and update the constants:

```python
# Path to your gold ring PNG (should be 800×800 with transparency)
RING_IMAGE = "/path/to/your/gold-ring.png"

# Path to a test headshot image (any size)
TEST_IMAGE = "/path/to/your/test/headshot.jpg"
```

## Usage

### Quick Test (default)

By default, running `gold-ring.py` will use the hardcoded `TEST_IMAGE`:

```bash
python gold-ring.py
```

### Command-Line Mode

To supply a custom headshot via CLI:

1. In `gold-ring.py`, comment out:

   ```python
   test_image_test()
   ```
2. Uncomment:

   ```python
   argparse_test()
   ```
3. Run with your image path:

   ```bash
   python gold-ring.py /path/to/your-headshot.jpg
   ```

The output file will be named `<your-headshot-stem>_with-ring.png` and saved in the working directory.

## Development

* Adjust the `oversample` factor in `circular_mask()` for finer edge smoothing.
* To integrate into a webhook or web service, import and call `compose_with_ring(headshot_path)` directly.
