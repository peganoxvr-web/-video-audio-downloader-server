# 🚀 دليل النشر على Railway

## خطوات النشر - سهل جداً!

### 1️⃣ إنشاء حساب Railway
1. اذهب إلى [railway.app](https://railway.app)
2. اضغط **"Start a New Project"**
3. سجل الدخول بـ GitHub

### 2️⃣ رفع الكود على GitHub
1. إنشئ Repository جديد على GitHub
2. ارفع مجلد `server` كامل
3. تأكد من وجود هذه الملفات:
   - `main.py`
   - `requirements.txt`
   - `Procfile`
   - `railway.json`

### 3️⃣ ربط المشروع بـ Railway
1. في Railway، اختر **"Deploy from GitHub repo"**
2. اختر Repository الخاص بك
3. اختر مجلد `server`
4. اضغط **"Deploy"**

### 4️⃣ الانتظار (3-5 دقائق)
- Railway سيقوم بـ:
  - تحميل المتطلبات تلقائياً
  - تشغيل السيرفر
  - إعطائك رابط HTTPS

### 5️⃣ الحصول على الرابط
- بعد النشر الناجح، ستحصل على رابط مثل:
- `https://your-app-name-production.up.railway.app`

### 6️⃣ تحديث تطبيق Android
```kotlin
// في DownloadManager.kt
var serverUrl = "https://your-app-name-production.up.railway.app/download"
```

## 🎯 **مميزات Railway:**

✅ **500 ساعة مجانية** شهرياً
✅ **نشر تلقائي** عند التحديث
✅ **HTTPS مجاني** فوري
✅ **مراقبة** و **Logs** مجانية
✅ **لا نوم للسيرفر** (24/7)

## 🔧 **ملاحظات مهمة:**

1. **الرابط ثابت**: لن يتغير بعد النشر
2. **التحديث التلقائي**: أي تغيير في GitHub = نشر جديد
3. **المراقبة**: يمكنك رؤية استخدام السيرفر
4. **العجز**: إذا انتهت الـ 500 ساعة، السيرفر يتوقف

## 📱 **تحديث التطبيق:**

بعد النشر، حدث في Android:

```kotlin
// في ملف DownloadManager.kt
var serverUrl = "https://your-railway-url.up.railway.app/download"
```

## 🆘 **حل المشاكل:**

**المشكلة**: Build فشل
**الحل**: تأكد من وجود `requirements.txt` و `Procfile`

**المشكلة**: السيرفر لا يرد
**الحل**: تحقق من Logs في Railway dashboard

**المشكلة**: CORS errors
**الحل**: السيرفر مُعد مسبقاً لـ CORS

## 🎉 **كل شيء جاهز!**

السيرفر سيكون متاح على مدار الساعة مجاناً!

---

### 💡 **نصائح إضافية:**

- احفظ رابط Railway dashboard للمراقبة
- استخدم Git للتحديثات (push = deploy تلقائي)
- راقب استهلاك الساعات من dashboard
- يمكنك إضافة domain مخصص لاحقاً

**🔗 Railway Dashboard**: [railway.app/dashboard](https://railway.app/dashboard)
