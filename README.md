
# RLE Compression - Time & Space Complexity Analysis

This document provides a clear and structured **Time and Space Complexity** analysis of the **Run-Length Encoding (RLE)** algorithm for images, audio, and video data. The format matches the structure used in the Huffman complexity `.md` file.

---

## Time Complexity

Let **n** = total number of samples (pixels, audio samples, or frame pixels)  
Let **k** = number of unique values in the data (included only for format consistency)

---

### **Compression Steps**

1. **Convert data to appropriate format (image/audio/video)**: `O(n)`  
2. **Flatten sample array (if required)**: `O(n)`  
3. **Run-Length Encode samples (main loop)**: `O(n)`  
4. **Convert RLE output to byte stream**: `O(n)`

**Total Compression Time:**

```
O(n)
```

---


## Space Complexity

### **Compression Space Usage:**

- Input data array: `O(n)`  
- Flattened array (image/video only): `O(n)`  
- Compressed RLE output array: `O(n)`  
- Temporary counters/variables: `O(1)`

**Total Compression Space:**

```
O(n)
```

## Summary Table

| Step                              | Time Complexity | Space Complexity |
|----------------------------------|-----------------|------------------|
| Data Conversion                  | O(n)            | O(n)             |
| Flattening (if needed)           | O(n)            | O(n)             |
| RLE Encoding Loop                | O(n)            | O(1)             |
| Byte Packing                     | O(n)            | O(n)             |
| **Total Compression**            | **O(n)**        | **O(n)**         |
| RLE Decoding                     | O(n)            | O(n)             |

---


# RLE Image, Audio, and Video Compression - Time & Space Complexity Analysis

This document provides detailed **Time and Space Complexity** analysis for every function in the RLE compression implementation. The format matches the structure used in the Huffman complexity `.md` file.

---

# 1. `RLEImageCompressor.compress_image()`

Let **n = total number of pixels**.

## Time Complexity

### Compression Steps:
- Convert image to grayscale array: `O(n)`  
- Flatten pixel array: `O(n)`  
- Run-Length Encode pixels: `O(n)`  
- Convert compressed list to bytes: `O(n)`  

### **Total Compression Time:**
```
O(n)
```

## Space Complexity
- Grayscale array: `O(n)`  
- Flattened pixel list: `O(n)`  
- Compressed RLE output: `O(n)`  
- Temporary counters: `O(1)`  

### **Total Compression Space:**
```
O(n)
```

---

# 2. `compress_image_file()`

Let **n = total number of pixels**.

## Time Complexity
- Open image from bytes: `O(n)`  
- Convert to RGB: `O(n)`  
- Call `compress_image()`: `O(n)`  

### **Total Time:**
```
O(n)
```

## Space Complexity
- Loaded image (RGB): `O(n)`  
- Grayscale representation: `O(n)`  
- Compressed output: `O(n)`  

### **Total Space:**
```
O(n)
```

---

# 3. `compress_audio_rle_file()`

Let **n = total number of audio samples**.

## Time Complexity
- Read PCM audio frames: `O(n)`  
- Convert frames to NumPy array: `O(n)`  
- Run-Length Encode samples: `O(n)`  
- Pack samples + counts into bytes: `O(n)`  

### **Total Compression Time:**
```
O(n)
```

## Space Complexity
- Audio sample array: `O(n)`  
- RLE compressed list: `O(n)`  
- Final byte output: `O(n)`  
- Temporary counters: `O(1)`  

### **Total Compression Space:**
```
O(n)
```

---

# 4. `rle_encode_array(arr)`

Let **n = length of the array**.

## Time Complexity
- Single-pass RLE loop: `O(n)`  
- Return compressed list: `O(n)`  

### **Total Time:**
```
O(n)
```

## Space Complexity
- Input array: `O(n)`  
- Compressed list: `O(n)`  
- Temporary counters: `O(1)`  

### **Total Space:**
```
O(n)
```

---

# 5. `compress_video_rle_file()`

Let:
- **f = number of frames**  
- **p = pixels per frame**  
- **n = total pixels = f × p**

## Time Complexity
- Write input bytes to temporary file: `O(n)`  
- Load video container: `O(f)`  
- For each frame:  
  - Convert to grayscale: `O(p)`  
  - Extract preview frames: `O(p)`  
  - Flatten pixels: `O(p)`  
  - RLE encode using `rle_encode_array()`: `O(p)`  
  - Write output bytes: `O(p)`  

Total across all frames:
```
O(f × p) = O(n)
```

### **Total Compression Time:**
```
O(n)
```

## Space Complexity
- Temporary MP4/GIF file: `O(n)`  
- Grayscale frame buffer: `O(p)`  
- Compressed output: `O(n)`  
- Preview frames (constant 10): `O(1)`  
- Temporary counters: `O(1)`  

### **Total Compression Space:**
```
O(n)
```

---

# Summary Table

| Function | Total Time | Total Space | Notes |
|----------|------------|-------------|-------|
| `compress_image()` | **O(n)** | **O(n)** | n = number of pixels |
| `compress_image_file()` | **O(n)** | **O(n)** | Includes image loading |
| `compress_audio_rle_file()` | **O(n)** | **O(n)** | n = audio samples |
| `rle_encode_array()` | **O(n)** | **O(n)** | Core RLE routine |
| `compress_video_rle_file()` | **O(n)** | **O(n)** | n = total pixels across frames |

---

