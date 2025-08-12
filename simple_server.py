#!/usr/bin/env python3
"""
🎵 سيرفر تحميل الفيديوهات والصوتيات البسيط
كل شي في ملف واحد - سهل ومرتب!

استخدام:
pip install fastapi uvicorn yt-dlp
python simple_server.py

الرابط: http://localhost:8000
"""

import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Optional

import yt_dlp
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn


# 🚀 إعداد التطبيق
app = FastAPI(
    title="🎵 Video Audio Downloader",
    description="سيرفر بسيط لتحميل الفيديوهات والصوتيات",
    version="1.0.0"
)

# 🌐 السماح بـ CORS لجميع المصادر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📁 مجلد مؤقت للتحميلات
TEMP_DIR = Path(tempfile.gettempdir()) / "video_downloader"
TEMP_DIR.mkdir(exist_ok=True)


# 📝 نموذج البيانات
class DownloadRequest(BaseModel):
    url: str
    type: str  # "video" or "audio"


# 🧹 وظيفة تنظيف الملف
def cleanup_file(file_path: Path):
    """حذف الملف بعد الإرسال"""
    try:
        if file_path.exists():
            file_path.unlink()
            print(f"✅ تم حذف الملف: {file_path}")
    except Exception as e:
        print(f"⚠️ خطأ في حذف الملف: {e}")


# 🔍 فحص صحة الرابط
def is_valid_url(url: str) -> bool:
    """فحص صحة الرابط"""
    return url.strip().startswith(("http://", "https://"))


# ⚙️ إعداد خيارات التحميل
def get_download_options(download_type: str, output_path: str) -> dict:
    """إعداد خيارات yt-dlp حسب نوع التحميل"""
    
    base_options = {
        'outtmpl': output_path,
        'noplaylist': True,
        'writeinfojson': False,
        'writesubtitles': False,
        'quiet': True,  # تقليل الرسائل
    }
    
    if download_type == "audio":
        # تحميل أفضل صوت متاح بدون تحويل
        base_options.update({
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio[ext=mp3]/bestaudio',
            'extractaudio': False,
        })
    else:  # video
        # تحميل أفضل فيديو متاح
        base_options.update({
            'format': 'best[ext=mp4]/best[height<=720]/best',
        })
    
    return base_options


# 🏠 الصفحة الرئيسية
@app.get("/")
async def home():
    """صفحة ترحيب بسيطة"""
    return {
        "message": "🎵 سيرفر تحميل الفيديوهات والصوتيات يعمل!",
        "endpoints": {
            "health": "/health - فحص حالة السيرفر",
            "download": "/download - تحميل فيديو أو صوت"
        },
        "usage": "أرسل POST request إلى /download مع url و type",
        "example": {
            "url": "https://www.youtube.com/watch?v=VIDEO_ID",
            "type": "video"  # أو "audio"
        }
    }


# 💚 فحص صحة السيرفر
@app.get("/health")
async def health_check():
    """فحص حالة السيرفر"""
    return {
        "status": "healthy",
        "message": "السيرفر يعمل بشكل طبيعي ✅",
        "temp_dir": str(TEMP_DIR),
        "temp_files": len(list(TEMP_DIR.glob("*")))
    }


# 📥 تحميل الملفات
@app.post("/download")
async def download_media(request: DownloadRequest, background_tasks: BackgroundTasks):
    """تحميل فيديو أو صوت من الرابط المُرسل"""
    
    try:
        # 🔍 فحص الرابط
        if not is_valid_url(request.url):
            raise HTTPException(
                status_code=400, 
                detail="رابط غير صحيح! يجب أن يبدأ بـ http:// أو https://"
            )
        
        # 🔍 فحص نوع التحميل
        if request.type not in ["video", "audio"]:
            raise HTTPException(
                status_code=400,
                detail="نوع التحميل يجب أن يكون 'video' أو 'audio'"
            )
        
        print(f"🎯 بدء تحميل {request.type} من: {request.url}")
        
        # 📁 إنشاء اسم ملف فريد
        unique_id = str(uuid.uuid4())[:8]
        filename_template = f"download_{unique_id}.%(ext)s"
        output_path = TEMP_DIR / filename_template
        
        # ⚙️ إعداد خيارات التحميل
        ydl_opts = get_download_options(request.type, str(output_path))
        
        # 📥 تحميل الملف
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 📊 جلب معلومات الفيديو أولاً
            info = ydl.extract_info(request.url, download=False)
            title = info.get('title', 'تحميل')
            duration = info.get('duration', 0)
            
            print(f"📺 العنوان: {title}")
            print(f"⏱️ المدة: {duration} ثانية")
            
            # 📥 تحميل الملف الفعلي
            ydl.download([request.url])
        
        # 🔍 البحث عن الملف المُحمّل
        downloaded_files = list(TEMP_DIR.glob(f"download_{unique_id}.*"))
        
        if not downloaded_files:
            raise HTTPException(
                status_code=500,
                detail="فشل في تحميل الملف - لم يتم العثور على الملف المُحمّل"
            )
        
        # 📄 اختيار أفضل ملف (أكبر حجم عادة = جودة أفضل)
        final_file = max(downloaded_files, key=lambda f: f.stat().st_size)
        file_size = final_file.stat().st_size
        actual_extension = final_file.suffix
        
        print(f"✅ تم التحميل بنجاح: {final_file.name}")
        print(f"📦 حجم الملف: {file_size / 1024 / 1024:.2f} MB")
        
        # 📤 إعداد اسم الملف للتحميل
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))[:50]
        download_filename = f"{safe_title}{actual_extension}"
        
        # 🧹 جدولة حذف الملف بعد الإرسال
        background_tasks.add_task(cleanup_file, final_file)
        
        # 📤 إرسال الملف
        return FileResponse(
            path=str(final_file),
            filename=download_filename,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename=\"{download_filename}\"",
                "Content-Length": str(file_size),
                "X-File-Title": title,
                "X-File-Type": request.type
            }
        )
        
    except HTTPException:
        # 🔄 إعادة رفع أخطاء HTTP كما هي
        raise
        
    except Exception as e:
        # 🚨 معالجة الأخطاء العامة
        error_msg = str(e)
        print(f"❌ خطأ في التحميل: {error_msg}")
        
        # 🧹 تنظيف الملفات المؤقتة في حالة الخطأ
        try:
            for temp_file in TEMP_DIR.glob(f"download_{unique_id}.*"):
                temp_file.unlink()
        except:
            pass
        
        raise HTTPException(
            status_code=500,
            detail=f"خطأ في تحميل الملف: {error_msg}"
        )


# 🚀 تشغيل السيرفر
if __name__ == "__main__":
    print("🎵 بدء تشغيل سيرفر تحميل الفيديوهات والصوتيات...")
    print("📡 الرابط: http://localhost:8000")
    print("🔗 API: http://localhost:8000/docs")
    print("💚 Health: http://localhost:8000/health")
    print("=" * 50)
    
    # 🧹 تنظيف الملفات المؤقتة القديمة عند البدء
    try:
        for old_file in TEMP_DIR.glob("download_*"):
            old_file.unlink()
        print("🧹 تم تنظيف الملفات المؤقتة القديمة")
    except:
        pass
    
    # 🚀 تشغيل السيرفر
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=False,  # إيقاف reload للإنتاج
        access_log=True
    )
