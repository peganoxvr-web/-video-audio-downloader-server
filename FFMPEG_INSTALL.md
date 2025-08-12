# 🎬 دليل تثبيت FFmpeg

FFmpeg مطلوب لتحويل ملفات الصوت إلى MP3 وضمان أفضل جودة.

## 🪟 **Windows:**

### الطريقة الأولى: تحميل مباشر
1. اذهب إلى: https://ffmpeg.org/download.html
2. اختر "Windows builds by BtbN"
3. حمّل "ffmpeg-master-latest-win64-gpl.zip"
4. فك الضغط إلى مجلد مثل `C:\ffmpeg`
5. أضف `C:\ffmpeg\bin` إلى PATH:
   - فتح إعدادات النظام > متقدم > متغيرات البيئة
   - أضف `C:\ffmpeg\bin` إلى PATH
   - إعادة تشغيل Terminal

### الطريقة الثانية: Chocolatey
```bash
choco install ffmpeg
```

### الطريقة الثالثة: WinGet
```bash
winget install ffmpeg
```

## 🍎 **macOS:**

### باستخدام Homebrew
```bash
brew install ffmpeg
```

### باستخدام MacPorts
```bash
sudo port install ffmpeg
```

## 🐧 **Linux:**

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

### CentOS/RHEL/Fedora
```bash
# Fedora
sudo dnf install ffmpeg

# CentOS/RHEL (مع EPEL)
sudo yum install epel-release
sudo yum install ffmpeg
```

### Arch Linux
```bash
sudo pacman -S ffmpeg
```

## ✅ **اختبار التثبيت:**

```bash
ffmpeg -version
```

## 🔄 **إعادة تشغيل السيرفر:**

بعد التثبيت، أعد تشغيل السيرفر:
```bash
cd server
python main.py
```

## ⚡ **بديل سريع:**

إذا لم تستطع تثبيت FFmpeg، السيرفر سيعمل مع الإعدادات الجديدة بدونه، لكن:
- ملفات الصوت قد تكون بصيغة M4A بدلاً من MP3
- جودة التحويل قد تكون أقل

السيرفر تم تحديثه للعمل بدون FFmpeg، لكن التثبيت مُوصى به لأفضل أداء.
