#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف إعدادات السيرفر
Server Configuration
"""

import os
from typing import List

# إعدادات السيرفر الأساسية
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"

# إعدادات CORS
ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# إعدادات التحميل
MAX_FILE_SIZE = os.getenv("MAX_FILE_SIZE", "500MB")
TEMP_DIR = os.getenv("TEMP_DIR", "./temp_downloads")
CLEANUP_INTERVAL = int(os.getenv("CLEANUP_INTERVAL", 3600))  # ثانية

# إعدادات yt-dlp
DEFAULT_AUDIO_QUALITY = os.getenv("DEFAULT_AUDIO_QUALITY", "192")
DEFAULT_VIDEO_QUALITY = os.getenv("DEFAULT_VIDEO_QUALITY", "720")

# إعدادات التسجيل
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "server.log")

# إعدادات الأمان (اختياري)
API_KEY = os.getenv("API_KEY", None)  # اتركه None للوصول المفتوح

# المواقع المدعومة (عينة)
SUPPORTED_SITES = [
    "youtube.com", "youtu.be", "vimeo.com", "dailymotion.com",
    "facebook.com", "instagram.com", "twitter.com", "tiktok.com",
    "twitch.tv", "soundcloud.com", "bandcamp.com"
]
