# 🎬 سيرفر تحميل الفيديوهات والصوتيات

سيرفر Python متقدم لتحميل الفيديوهات والصوتيات من الإنترنت باستخدام FastAPI و yt-dlp.

## ✨ الميزات

- 🚀 **FastAPI**: سيرفر سريع ومتطور
- 🎵 **دعم الصوت والفيديو**: تحميل بجودات مختلفة
- 🌐 **CORS**: دعم جميع المصادر
- 🗑️ **إدارة الملفات**: حذف تلقائي للملفات المؤقتة
- 📖 **توثيق تلقائي**: Swagger UI و ReDoc
- 🔄 **إعادة التحميل التلقائي**: للتطوير
- 🛡️ **معالجة الأخطاء**: شاملة ومفصلة

## 🛠️ التثبيت والإعداد

### المتطلبات الأساسية

- Python 3.8 أو أحدث
- pip (مدير الحزم)
- FFmpeg (مُوصى به)

### التثبيت السريع

```bash
# 1. الانتقال إلى مجلد السيرفر
cd server

# 2. تثبيت التبعيات
pip install -r requirements.txt

# 3. تشغيل السيرفر
python start_server.py
```

### التثبيت اليدوي

```bash
# تثبيت المكتبات المطلوبة
pip install fastapi uvicorn yt-dlp python-multipart aiofiles

# تشغيل السيرفر مباشرة
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### تثبيت FFmpeg (مُوصى به)

**Windows:**
1. حمّل من: https://ffmpeg.org/download.html
2. أضف إلى PATH

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🚀 التشغيل

### الطريقة الأولى: السكريبت التلقائي
```bash
python start_server.py
```

### الطريقة الثانية: مباشرة
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### الطريقة الثالثة: Python مباشرة
```bash
python main.py
```

## 📡 استخدام API

### المعلومات الأساسية
- **الرابط**: http://localhost:8000
- **التوثيق**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints المتاحة

#### 1. الصفحة الرئيسية
```http
GET /
```

#### 2. فحص حالة السيرفر
```http
GET /health
```

#### 3. تحميل فيديو/صوت
```http
POST /download
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "type": "video"
}
```

#### 4. المواقع المدعومة
```http
GET /supported-sites
```

### أمثلة الاستخدام

#### تحميل فيديو
```bash
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "type": "video"
  }' \
  --output video.mp4
```

#### تحميل صوت
```bash
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "type": "audio"
  }' \
  --output audio.mp3
```

#### باستخدام Python
```python
import requests

# تحميل فيديو
response = requests.post(
    "http://localhost:8000/download",
    json={
        "url": "https://www.youtube.com/watch?v=VIDEO_ID",
        "type": "video"
    }
)

if response.status_code == 200:
    with open("video.mp4", "wb") as f:
        f.write(response.content)
    print("تم التحميل بنجاح!")
```

## 🔧 الإعدادات

يمكن تخصيص السيرفر عبر متغيرات البيئة في ملف `config.py`:

```python
# إعدادات السيرفر
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# إعدادات التحميل
MAX_FILE_SIZE = "500MB"
DEFAULT_AUDIO_QUALITY = "192"
DEFAULT_VIDEO_QUALITY = "720"
```

## 📱 ربط مع تطبيق الأندرويد

لربط السيرفر مع تطبيق الأندرويد:

1. **تشغيل السيرفر** على جهاز الكمبيوتر
2. **معرفة IP العنوان** للجهاز:
   ```bash
   ipconfig  # Windows
   ifconfig  # macOS/Linux
   ```
3. **تحديث رابط السيرفر** في التطبيق:
   ```kotlin
   // في ملف DownloadManager.kt
   var serverUrl = "http://192.168.1.100:8000/download"
   ```

## 🔍 استكشاف الأخطاء

### المشاكل الشائعة

#### خطأ: "ModuleNotFoundError"
```bash
# تأكد من تثبيت التبعيات
pip install -r requirements.txt
```

#### خطأ: "Port already in use"
```bash
# تغيير المنفذ
uvicorn main:app --port 8001
```

#### خطأ: "FFmpeg not found"
```bash
# تثبيت FFmpeg (مذكور أعلاه)
# أو تجاهل التحذير
```

#### خطأ في التحميل
- تأكد من صحة الرابط
- تحقق من الاتصال بالإنترنت
- بعض المواقع قد تحتاج إعدادات خاصة

## 📊 المواقع المدعومة

السيرفر يدعم أكثر من 1000 موقع عبر yt-dlp، منها:

- **فيديو**: YouTube, Vimeo, Dailymotion, Facebook, Instagram
- **صوت**: SoundCloud, Bandcamp, Spotify (الروابط العامة)
- **بث مباشر**: Twitch, YouTube Live
- **وأكثر**: TikTok, Twitter, Reddit...

## 🤝 المساهمة

نرحب بالمساهمات! يُرجى:

1. عمل Fork للمشروع
2. إنشاء branch جديد
3. إجراء التعديلات مع الاختبار
4. إرسال Pull Request

## 📄 الرخصة

هذا المشروع مرخص تحت رخصة MIT.

## 📧 الدعم

للاستفسارات والمساعدة:
- فتح issue في المستودع
- مراجعة التوثيق في `/docs`
- فحص الـ logs للأخطاء

---

🎉 استمتع بتحميل الفيديوهات والصوتيات!
