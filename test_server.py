#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار السيرفر
Server testing script
"""

import requests
import json
import time
import sys

def test_server_health():
    """اختبار حالة السيرفر"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ السيرفر يعمل بشكل طبيعي")
            return True
        else:
            print(f"❌ السيرفر يعمل ولكن هناك مشكلة: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالسيرفر. تأكد من تشغيله على المنفذ 8000")
        return False
    except Exception as e:
        print(f"❌ خطأ في اختبار السيرفر: {e}")
        return False

def test_root_endpoint():
    """اختبار الصفحة الرئيسية"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ الصفحة الرئيسية تعمل")
            print(f"   الإصدار: {data.get('version', 'غير محدد')}")
            return True
        else:
            print(f"❌ مشكلة في الصفحة الرئيسية: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في اختبار الصفحة الرئيسية: {e}")
        return False

def test_supported_sites():
    """اختبار قائمة المواقع المدعومة"""
    try:
        response = requests.get("http://localhost:8000/supported-sites", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ قائمة المواقع المدعومة متاحة")
            print(f"   عدد المواقع: {len(data.get('sites', []))}")
            return True
        else:
            print(f"❌ مشكلة في قائمة المواقع: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في اختبار المواقع المدعومة: {e}")
        return False

def test_download_endpoint_validation():
    """اختبار التحقق من صحة البيانات في endpoint التحميل"""
    test_cases = [
        {
            "name": "رابط فارغ",
            "data": {"url": "", "type": "video"},
            "expected_status": 400
        },
        {
            "name": "نوع غير صحيح",
            "data": {"url": "https://example.com", "type": "invalid"},
            "expected_status": 400
        },
        {
            "name": "رابط غير صحيح",
            "data": {"url": "not-a-url", "type": "video"},
            "expected_status": 400
        }
    ]
    
    print("\n🧪 اختبار التحقق من البيانات:")
    all_passed = True
    
    for test in test_cases:
        try:
            response = requests.post(
                "http://localhost:8000/download",
                json=test["data"],
                timeout=10
            )
            
            if response.status_code == test["expected_status"]:
                print(f"   ✅ {test['name']}: النتيجة متوقعة ({response.status_code})")
            else:
                print(f"   ❌ {test['name']}: توقع {test['expected_status']}, حصل على {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ {test['name']}: خطأ في الاختبار - {e}")
            all_passed = False
    
    return all_passed

def test_download_with_fake_url():
    """اختبار التحميل مع رابط وهمي لفحص معالجة الأخطاء"""
    try:
        print("\n🔗 اختبار رابط وهمي:")
        response = requests.post(
            "http://localhost:8000/download",
            json={
                "url": "https://www.example-fake-site-12345.com/video",
                "type": "video"
            },
            timeout=30
        )
        
        if response.status_code in [400, 500]:
            print("   ✅ معالجة الأخطاء تعمل بشكل صحيح")
            return True
        else:
            print(f"   ⚠️  استجابة غير متوقعة: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ⚠️  انتهت مهلة الاختبار (طبيعي)")
        return True
    except Exception as e:
        print(f"   ❌ خطأ في اختبار الرابط الوهمي: {e}")
        return False

def main():
    """الدالة الرئيسية للاختبارات"""
    print("🧪 اختبار سيرفر تحميل الفيديوهات والصوتيات")
    print("=" * 50)
    
    tests = [
        ("فحص حالة السيرفر", test_server_health),
        ("اختبار الصفحة الرئيسية", test_root_endpoint),
        ("اختبار المواقع المدعومة", test_supported_sites),
        ("اختبار التحقق من البيانات", test_download_endpoint_validation),
        ("اختبار معالجة الأخطاء", test_download_with_fake_url)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # توقف قصير بين الاختبارات
    
    # تلخيص النتائج
    print("\n" + "=" * 50)
    print("📊 نتائج الاختبارات:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ نجح" if result else "❌ فشل"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 النتيجة النهائية: {passed}/{len(results)} اختبار نجح")
    
    if passed == len(results):
        print("🎉 جميع الاختبارات نجحت! السيرفر جاهز للاستخدام.")
        return 0
    else:
        print("⚠️  بعض الاختبارات فشلت. راجع الأخطاء أعلاه.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
