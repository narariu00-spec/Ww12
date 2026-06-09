#!/usr/bin/env python3
"""
Fingerprint Animation Theme Creator
Tạo file fingerprint animation cho OnePlus, Realme, Oppo
"""

import os
import json
import zipfile
from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET

class FingerprintAnimationCreator:
    def __init__(self, theme_name="Wuthering_Waves_Cynthia"):
        self.theme_name = theme_name
        self.base_dir = Path(theme_name)
        self.animation_dir = self.base_dir / "animation"
        
    def create_directory_structure(self):
        """Tạo cấu trúc thư mục"""
        print(f"✓ Tạo thư mục cho theme: {self.theme_name}")
        
        # Tạo thư mục chính
        self.base_dir.mkdir(exist_ok=True)
        
        # Tạo thư mục animation
        (self.animation_dir / "unlock").mkdir(parents=True, exist_ok=True)
        (self.animation_dir / "lock").mkdir(parents=True, exist_ok=True)
        (self.animation_dir / "error").mkdir(parents=True, exist_ok=True)
        
        print(f"  ├── {self.base_dir}/")
        print(f"  ├── animation/unlock/")
        print(f"  ├── animation/lock/")
        print(f"  └── animation/error/")
        
    def create_sample_image(self, size=(1080, 2340), color=(0, 212, 255, 255), text=""):
        """Tạo hình ảnh sample"""
        from PIL import ImageDraw, ImageFont
        
        img = Image.new('RGBA', size, (10, 14, 39, 255))  # Dark background
        draw = ImageDraw.Draw(img)
        
        # Vẽ hình tròn (fingerprint indicator)
        center_x, center_y = size[0] // 2, size[1] - 300
        radius = 100
        
        # Draw circle
        bbox = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
        draw.ellipse(bbox, outline=color, width=3)
        
        # Vẽ text nếu có
        if text:
            try:
                # Cố gắng sử dụng font mặc định
                draw.text((center_x - 50, center_y - 30), text, fill=color)
            except:
                pass
        
        return img
    
    def generate_unlock_frames(self, count=30):
        """Tạo frames cho unlock animation"""
        print(f"\n✓ Tạo {count} frames cho unlock animation...")
        
        unlock_dir = self.animation_dir / "unlock"
        
        for i in range(1, count + 1):
            # Tính toán alpha gradient
            alpha = int((i / count) * 255)
            
            # Tạo hình ảnh với transparency tăng dần
            img = Image.new('RGBA', (1080, 2340), (10, 14, 39, 255))
            pixels = img.load()
            
            # Điều chỉnh alpha
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b, a = pixels[x, y]
                    pixels[x, y] = (r, g, b, alpha)
            
            # Vẽ animation frame
            draw = ImageDraw.Draw(img)
            center_x, center_y = 540, 2040
            
            # Vẽ ripple effect
            for j in range(1, 4):
                radius = 50 + (i * 5) // count * j
                color_val = (0, 212, 255, max(0, 200 - (i * 20)))
                try:
                    draw.ellipse(
                        [center_x - radius, center_y - radius, 
                         center_x + radius, center_y + radius],
                        outline=color_val,
                        width=2
                    )
                except:
                    pass
            
            # Vẽ fingerprint
            draw.ellipse(
                [center_x - 80, center_y - 80, center_x + 80, center_y + 80],
                outline=(0, 212, 255, alpha // 2),
                width=3
            )
            
            # Lưu file
            filename = unlock_dir / f"unlock_{i}.png"
            img.save(filename, 'PNG')
            
            if i % 10 == 0:
                print(f"  ✓ Frame {i}/{count} tạo xong")
    
    def generate_lock_frames(self, count=20):
        """Tạo frames cho lock animation"""
        print(f"\n✓ Tạo {count} frames cho lock animation...")
        
        lock_dir = self.animation_dir / "lock"
        
        for i in range(1, count + 1):
            # Tính toán alpha giảm dần
            alpha = int((1 - i / count) * 255)
            
            img = Image.new('RGBA', (1080, 2340), (10, 14, 39, 255))
            draw = ImageDraw.Draw(img)
            
            center_x, center_y = 540, 2040
            
            # Vẽ lock animation (ngược lại với unlock)
            radius = 100 - (i * 3)
            if radius > 0:
                draw.ellipse(
                    [center_x - radius, center_y - radius, 
                     center_x + radius, center_y + radius],
                    outline=(255, 107, 157, alpha),
                    width=3
                )
            
            # Lưu file
            filename = lock_dir / f"lock_{i}.png"
            img.save(filename, 'PNG')
            
            if i % 5 == 0:
                print(f"  ✓ Frame {i}/{count} tạo xong")
    
    def generate_error_frames(self, count=8):
        """Tạo frames cho error animation"""
        print(f"\n✓ Tạo {count} frames cho error animation...")
        
        error_dir = self.animation_dir / "error"
        
        for i in range(1, count + 1):
            img = Image.new('RGBA', (1080, 2340), (10, 14, 39, 255))
            draw = ImageDraw.Draw(img)
            
            center_x, center_y = 540, 2040
            
            # Tạo shake effect
            shake_offset = (i % 2) * 20 - 10
            
            # Vẽ error indicator (X)
            offset = 80
            draw.line(
                [(center_x - offset + shake_offset, center_y - offset),
                 (center_x + offset + shake_offset, center_y + offset)],
                fill=(255, 0, 0, 200),
                width=4
            )
            draw.line(
                [(center_x - offset + shake_offset, center_y + offset),
                 (center_x + offset + shake_offset, center_y - offset)],
                fill=(255, 0, 0, 200),
                width=4
            )
            
            # Lưu file
            filename = error_dir / f"error_{i}.png"
            img.save(filename, 'PNG')
            
            print(f"  ✓ Frame {i}/{count} tạo xong")
    
    def create_manifest(self):
        """Tạo manifest.xml"""
        print(f"\n✓ Tạo manifest.xml...")
        
        manifest_content = """<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <metadata>
        <name>Wuthering Waves - Cynthia</name>
        <description>Fingerprint animation theme featuring Cynthia from Wuthering Waves</description>
        <author>Theme Creator</author>
        <version>1.0.0</version>
        <api_level>1</api_level>
    </metadata>
    
    <preview>
        <icon>icon.png</icon>
        <preview_image>preview.png</preview_image>
    </preview>
    
    <animation>
        <name>Cynthia Theme</name>
        <unlock_animation>
            <frames>30</frames>
            <frame_duration>33</frame_duration>
            <frame_path>animation/unlock</frame_path>
        </unlock_animation>
        <lock_animation>
            <frames>20</frames>
            <frame_duration>50</frame_duration>
            <frame_path>animation/lock</frame_path>
        </lock_animation>
        <error_animation>
            <frames>8</frames>
            <frame_duration>62</frame_duration>
            <frame_path>animation/error</frame_path>
        </error_animation>
    </animation>
    
    <compatibility>
        <devices>
            <device>OnePlus</device>
            <device>Realme</device>
            <device>Oppo</device>
        </devices>
        <min_android_version>9</min_android_version>
    </compatibility>
</manifest>"""
        
        with open(self.base_dir / "manifest.xml", 'w', encoding='utf-8') as f:
            f.write(manifest_content)
    
    def create_icon_and_preview(self):
        """Tạo icon và preview"""
        print(f"\n✓ Tạo icon.png và preview.png...")
        
        # Tạo icon (512x512)
        icon = Image.new('RGBA', (512, 512), (10, 14, 39, 255))
        draw = ImageDraw.Draw(icon)
        draw.ellipse([100, 100, 412, 412], outline=(0, 212, 255, 255), width=4)
        icon.save(self.base_dir / "icon.png", 'PNG')
        print("  ✓ icon.png tạo xong")
        
        # Tạo preview (1080x1920)
        preview = Image.new('RGBA', (1080, 1920), (10, 14, 39, 255))
        draw = ImageDraw.Draw(preview)
        draw.ellipse([390, 860, 690, 1160], outline=(0, 212, 255, 255), width=6)
        preview.save(self.base_dir / "preview.png", 'PNG')
        print("  ✓ preview.png tạo xong")
    
    def create_fpanim_file(self):
        """Tạo file .fpanim (ZIP)"""
        print(f"\n✓ Tạo file .fpanim...")
        
        fpanim_path = f"{self.theme_name}.fpanim"
        
        with zipfile.ZipFile(fpanim_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Thêm tất cả file
            for root, dirs, files in os.walk(self.base_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.base_dir.parent)
                    zipf.write(file_path, arcname)
        
        print(f"  ✓ File {fpanim_path} tạo thành công!")
        print(f"  ✓ Size: {os.path.getsize(fpanim_path) / (1024*1024):.2f} MB")
    
    def build(self):
        """Build toàn bộ theme"""
        print("=" * 60)
        print("Fingerprint Animation Theme Creator")
        print("=" * 60)
        
        try:
            self.create_directory_structure()
            self.create_icon_and_preview()
            self.generate_unlock_frames(30)
            self.generate_lock_frames(20)
            self.generate_error_frames(8)
            self.create_manifest()
            self.create_fpanim_file()
            
            print("\n" + "=" * 60)
            print("✓ Theme tạo thành công!")
            print("=" * 60)
            print(f"\nFile ready: {self.theme_name}.fpanim")
            print("Bạn có thể transfer file này tới thiết bị của mình.")
            
        except Exception as e:
            print(f"\n✗ Lỗi: {e}")

if __name__ == "__main__":
    creator = FingerprintAnimationCreator()
    creator.build()
