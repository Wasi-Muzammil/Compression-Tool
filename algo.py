import heapq 
from collections import defaultdict
import os
from PIL import Image, ImageSequence
import numpy as np
import zipfile
import wave
from io import BytesIO
import tempfile

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCompressor:
    def __init__(self):
        self.codes = {}

    def _frequency_dict(self, text):
        return defaultdict(int, {ch: text.count(ch) for ch in set(text)})

    def _build_tree(self, freq):
        heap = [Node(ch, f) for ch, f in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            n1, n2 = heapq.heappop(heap), heapq.heappop(heap)
            merged = Node(None, n1.freq + n2.freq, n1, n2)
            heapq.heappush(heap, merged)
        return heap[0]

    def _generate_codes(self, node, current=""):
        if node.char is not None:
            self.codes[node.char] = current
        else:
            self._generate_codes(node.left, current + "0")
            self._generate_codes(node.right, current + "1")

    def _encode_text(self, text):
        return ''.join(self.codes[ch] for ch in text)

    def _pad_bits(self, bits):
        padding = 8 - len(bits) % 8
        return f"{padding:08b}" + bits + '0' * padding

    def _to_bytearray(self, bits):
        return bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

    def compress(self, text):
        freq = self._frequency_dict(text)
        root = self._build_tree(freq)
        self._generate_codes(root)
        encoded = self._encode_text(text)
        padded = self._pad_bits(encoded)
        return bytes(self._to_bytearray(padded))


def compress_text(data: bytes) -> bytes:
    return HuffmanCompressor().compress(data.decode('latin1'))

def compress_docx_file(data: bytes) -> bytes:
    with zipfile.ZipFile(BytesIO(data), 'r') as z:
        xml_text = z.read("word/document.xml").decode("utf-8")
    return HuffmanCompressor().compress(xml_text)

def compress_csv_file(data: bytes) -> bytes:
    return compress_text(data)

def compress_pdf_file(data: bytes) -> bytes:
    return HuffmanCompressor().compress(data.decode('latin1', errors="ignore"))

class RLEImageCompressor:
    @staticmethod
    def compress_image(image: Image.Image) -> bytes:
        arr = np.array(image.convert("L")).flatten()
        compressed = []
        count = 1
        for i in range(1, len(arr)):
            if arr[i] == arr[i - 1] and count < 255:
                count += 1
            else:
                compressed.extend([arr[i - 1], count])
                count = 1
        compressed.extend([arr[-1], count])
        return bytes(compressed)

def compress_image_file(data: bytes) -> bytes:
    return RLEImageCompressor.compress_image(Image.open(BytesIO(data)).convert("RGB"))

def compress_audio_rle_file(data: bytes) -> bytes:
    with wave.open(BytesIO(data), 'rb') as wf:
        audio_array = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    compressed = []
    count = 1
    for i in range(1, len(audio_array)):
        if audio_array[i] == audio_array[i-1] and count < 255:
            count += 1
        else:
            compressed.extend([audio_array[i-1], count])
            count = 1
    compressed.extend([audio_array[-1], count])
    return b''.join(int(x).to_bytes(2 if i % 2 == 0 else 1, 'little', signed=i % 2 == 0) for i, x in enumerate(compressed))

def rle_encode_array(arr):
    compressed = []
    count = 1
    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1] and count < 255:
            count += 1
        else:
            compressed.extend([arr[i - 1], count])
            count = 1
    compressed.extend([arr[-1], count])
    return compressed

def compress_video_rle_file(data: bytes):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp.write(data)
    temp.close()
    video = Image.open(temp.name)
    output = bytearray()
    color_preview_frames = []
    gray_preview_frames = []
    for i, frame in enumerate(ImageSequence.Iterator(video)):
        if i < 10:
            color_preview_frames.append(frame.copy().convert("RGB"))
        gray_frame = frame.convert("L")
        if i < 10:
            gray_preview_frames.append(gray_frame.copy())
        arr = np.array(gray_frame).flatten()
        compressed = rle_encode_array(arr)
        output.extend(len(compressed).to_bytes(4, "big"))
        output.extend(bytes(compressed))
    return bytes(output), color_preview_frames, gray_preview_frames



