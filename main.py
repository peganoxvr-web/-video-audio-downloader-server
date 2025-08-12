#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سيرفر تحميل الفيديوهات والصوتيات
Server for downloading videos and audio files
"""

import os
import tempfile
import shutil
import asyncio
import logging
from pathlib import Path
from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
import yt_dlp

# إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Video/Audio Download API",
    description="API لتحميل الفيديوهات والصوتيات من الإنترنت",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إعداد CORS لجميع المصادر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح لجميع المصادر
    allow_credentials=True,
    allow_methods=["*"],  # السماح بجميع الطرق
    allow_headers=["*"],  # السماح بجميع الHeaders
)

# نماذج البيانات
class DownloadRequest(BaseModel):
    url: str
    type: str  # "video" أو "audio"
    format: Optional[str] = None  # اختياري

class DownloadResponse(BaseModel):
    message: str
    filename: str
    size: int

# مجلد مؤقت للتحميلات
TEMP_DIR = Path(tempfile.gettempdir()) / "video_downloads"
TEMP_DIR.mkdir(exist_ok=True)

def cleanup_file(file_path: str):
    """حذف الملف بعد إرساله"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"تم حذف الملف: {file_path}")
    except Exception as e:
        logger.error(f"خطأ في حذف الملف {file_path}: {e}")

def get_ydl_opts(download_type: str, output_path: str) -> dict:
    """إعداد خيارات yt-dlp حسب نوع التحميل"""
    base_opts = {
        'outtmpl': output_path,
        'noplaylist': True,
        'writeinfojson': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
    }
    
    if download_type == "audio":
        # تحديد أفضل جودة صوت متاحة بدون تحويل
        base_opts.update({
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio[ext=mp3]/bestaudio',
            'extractaudio': False,  # عدم استخراج الصوت لتجنب الحاجة لـ FFmpeg
        })
    else:  # video
        base_opts.update({
            'format': 'best[ext=mp4]/best[height<=720]/best',
        })
    
    return base_opts

def validate_url(url: str) -> bool:
    """التحقق من صحة الرابط"""
    try:
        # قائمة المواقع المدعومة الأساسية
        supported_domains = [
            'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
            'facebook.com', 'instagram.com', 'twitter.com', 'tiktok.com'
        ]
        
        # فحص أساسي للرابط
        if not url.startswith(('http://', 'https://')):
            return False
            
        # يمكن إضافة فحوصات أكثر تعقيداً هنا
        return True
    except Exception:
        return False

@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {
        "message": "مرحباً بك في API تحميل الفيديوهات والصوتيات",
        "version": "1.0.0",
        "endpoints": {
            "download": "/download",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """فحص حالة السيرفر"""
    return {
        "status": "healthy",
        "message": "السيرفر يعمل بشكل طبيعي"
    }

@app.post("/download")
async def download_media(
    request: DownloadRequest,
    background_tasks: BackgroundTasks
):
    """
    تحميل فيديو أو صوت من رابط
    """
    try:
        # التحقق من صحة البيانات
        if not request.url:
            raise HTTPException(status_code=400, detail="الرابط مطلوب")
        
        if request.type not in ["video", "audio"]:
            raise HTTPException(
                status_code=400, 
                detail="نوع التحميل يجب أن يكون 'video' أو 'audio'"
            )
        
        if not validate_url(request.url):
            raise HTTPException(status_code=400, detail="رابط غير صحيح")
        
        logger.info(f"بدء تحميل: {request.url} - النوع: {request.type}")
        
        # إنشاء اسم ملف فريد
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        # استخدام امتداد عام للاختيار التلقائي
        extension = "%(ext)s"  # دع yt-dlp يختار الامتداد المناسب
        filename = f"download_{unique_id}.{extension}"
        output_path = TEMP_DIR / filename
        
        # إعداد خيارات yt-dlp
        ydl_opts = get_ydl_opts(request.type, str(output_path))
        
        # تحميل الملف
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # استخراج معلومات الفيديو أولاً
                info = ydl.extract_info(request.url, download=False)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                
                logger.info(f"العنوان: {title}, المدة: {duration} ثانية")
                
                # بدء التحميل
                ydl.download([request.url])
                
            except yt_dlp.utils.DownloadError as e:
                logger.error(f"خطأ في التحميل: {e}")
                raise HTTPException(
                    status_code=400, 
                    detail=f"فشل في تحميل الملف: {str(e)}"
                )
        
        # البحث عن الملف المحمل (قد يكون له اسم مختلف)
        downloaded_files = list(TEMP_DIR.glob(f"download_{unique_id}.*"))
        
        if not downloaded_files:
            raise HTTPException(
                status_code=500, 
                detail="لم يتم العثور على الملف المحمل"
            )
        
        # اختيار أفضل ملف (أكبر حجم عادة يعني جودة أفضل)
        final_file = max(downloaded_files, key=lambda f: f.stat().st_size)
        
        # تحديد امتداد الملف الفعلي
        actual_extension = final_file.suffix
        
        # التحقق من وجود الملف
        if not final_file.exists():
            raise HTTPException(
                status_code=500, 
                detail="الملف المحمل غير موجود"
            )
        
        file_size = final_file.stat().st_size
        logger.info(f"تم التحميل بنجاح: {final_file}, الحجم: {file_size} بايت")
        
        # إضافة مهمة حذف الملف في الخلفية
        background_tasks.add_task(cleanup_file, str(final_file))
        
        # إرجاع الملف
        safe_filename = f"{title[:50] if title else 'download'}{actual_extension}"
        return FileResponse(
            path=str(final_file),
            filename=safe_filename,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename=\"{safe_filename}\"",
                "Content-Length": str(file_size)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ غير متوقع: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"خطأ في السيرفر: {str(e)}"
        )

@app.get("/supported-sites")
async def get_supported_sites():
    """قائمة المواقع المدعومة"""
    try:
        with yt_dlp.YoutubeDL() as ydl:
            extractors = ydl.list_extractors()
            # أخذ عينة من المواقع المدعومة
            sample_sites = [
                "YouTube", "Vimeo", "Facebook", "Instagram", 
                "Twitter", "TikTok", "Dailymotion", "Twitch"
            ]
            
        return {
            "message": "المواقع المدعومة (عينة)",
            "sites": sample_sites,
            "total_extractors": len(extractors),
            "note": "yt-dlp يدعم أكثر من 1000 موقع"
        }
    except Exception as e:
        return {
            "message": "خطأ في جلب قائمة المواقع",
            "error": str(e)
        }

# معالج الأخطاء العامة
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"خطأ غير متوقع: {exc}")
    return {
        "error": "حدث خطأ في السيرفر",
        "detail": str(exc)
    }

if __name__ == "__main__":
    print("""
    🚀 سيرفر تحميل الفيديوهات والصوتيات
    =====================================
    📡 المنفذ: 8000
    🌐 الرابط: http://localhost:8000
    📖 التوثيق: http://localhost:8000/docs
    
    للتوقف: اضغط Ctrl+C
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
