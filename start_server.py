#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت بدء تشغيل السيرفر
Server startup script
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """فحص إصدار Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 أو أحدث مطلوب")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def check_dependencies():
    """فحص وتثبيت التبعيات"""
    try:
        print("🔍 فحص التبعيات...")
        
        # فحص pip
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        
        # تثبيت التبعيات
        print("📦 تثبيت التبعيات...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ فشل في تثبيت التبعيات: {result.stderr}")
            return False
            
        print("✅ تم تثبيت جميع التبعيات")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص التبعيات: {e}")
        return False

def check_ffmpeg():
    """فحص وجود FFmpeg (اختياري ولكن مُوصى به)"""
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      capture_output=True, check=True)
        print("✅ FFmpeg متوفر")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  FFmpeg غير متوفر (مُوصى بتثبيته لأفضل أداء)")
        print("   لتثبيت FFmpeg:")
        print("   - Windows: https://ffmpeg.org/download.html")
        print("   - macOS: brew install ffmpeg")
        print("   - Ubuntu: sudo apt install ffmpeg")
        return False

def create_temp_dir():
    """إنشاء مجلد مؤقت للتحميلات"""
    temp_dir = Path("temp_downloads")
    temp_dir.mkdir(exist_ok=True)
    print(f"📁 مجلد التحميل المؤقت: {temp_dir.absolute()}")

def start_server():
    """بدء تشغيل السيرفر"""
    try:
        print("\n🚀 بدء تشغيل السيرفر...")
        print("=" * 50)
        print("📡 الرابط: http://localhost:8000")
        print("📖 التوثيق: http://localhost:8000/docs")
        print("🔄 إعادة التحميل التلقائي: مُفعل")
        print("⏹️  للتوقف: اضغط Ctrl+C")
        print("=" * 50)
        
        # تشغيل السيرفر
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف السيرفر")
    except Exception as e:
        print(f"❌ خطأ في تشغيل السيرفر: {e}")

def main():
    """الدالة الرئيسية"""
    print("🎬 سيرفر تحميل الفيديوهات والصوتيات")
    print("=" * 40)
    
    # فحص متطلبات النظام
    if not check_python_version():
        return
    
    # إنشاء مجلد مؤقت
    create_temp_dir()
    
    # فحص وتثبيت التبعيات
    if not check_dependencies():
        return
    
    # فحص FFmpeg
    check_ffmpeg()
    
    # بدء السيرفر
    start_server()

if __name__ == "__main__":
    main()
