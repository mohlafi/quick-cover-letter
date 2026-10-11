import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# رابط منتج Gumroad الخاص بك
GUMROAD_LINK = "https://mohlafi.gumroad.com/l/dxdbct"

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مولد رسائل التغطية الاحترافية | Quick Cover Letter</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white min-h-screen flex flex-col justify-between font-sans">
    <header class="p-6 border-b border-slate-800 text-center">
        <h1 class="text-3xl font-bold text-indigo-400">⚡ Instant Cover Letter Generator</h1>
        <p class="text-slate-400 mt-2">احصل على رسالة تغطية احترافية ومخصصة بـ $3 فقط</p>
    </header>

    <main class="max-w-3xl mx-auto p-6 w-full">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-xl border border-slate-700">
            <form id="generatorForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-1">الاسم الكامل (Full Name)</label>
                    <input type="text" id="name" required class="w-full p-3 rounded-lg bg-slate-900 border border-slate-700 focus:outline-none focus:border-indigo-500" placeholder="مثال: محمد لافي">
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium mb-1">المسمى الوظيفي (Job Title)</label>
                        <input type="text" id="job_title" required class="w-full p-3 rounded-lg bg-slate-900 border border-slate-700 focus:outline-none focus:border-indigo-500" placeholder="مثال: Mobile Software Developer">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">اسم الشركة (Company Name)</label>
                        <input type="text" id="company_name" required class="w-full p-3 rounded-lg bg-slate-900 border border-slate-700 focus:outline-none focus:border-indigo-500" placeholder="مثال: Tech Solutions">
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium mb-1">سنوات الخبرة (Years of Experience)</label>
                        <input type="number" id="experience_years" required class="w-full p-3 rounded-lg bg-slate-900 border border-slate-700 focus:outline-none focus:border-indigo-500" placeholder="مثال: 4">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">المهارات الرئيسية (Main Skills)</label>
                        <input type="text" id="skills" required class="w-full p-3 rounded-lg bg-slate-900 border border-slate-700 focus:outline-none focus:border-indigo-500" placeholder="مثال: Flutter, Android, Java, Automation">
                    </div>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3 rounded-lg transition duration-200">
                    توليد المعاينة مجاناً ✨
                </button>
            </form>

            <div id="resultContainer" class="mt-8 hidden">
                <h3 class="text-xl font-bold mb-2 text-indigo-400">معاينة الرسالة:</h3>
                <textarea id="resultText" rows="5" class="w-full p-4 rounded-lg bg-slate-900 border border-slate-700 text-slate-400 dir-ltr text-left font-mono" readonly></textarea>
                
                <div class="mt-6 bg-indigo-950/60 border border-indigo-500/30 p-6 rounded-xl text-center">
                    <p class="text-lg font-semibold text-indigo-200 mb-2">🔒 للحصول على الرسالة الكاملة القابلة للنسخ والتعديل</p>
                    <p class="text-slate-400 text-sm mb-4">احصل على وصول كامل فوري بـ $3 فقط</p>
                    <a href="{GUMROAD_LINK}" target="_blank" class="inline-block bg-emerald-500 hover:bg-emerald-400 text-slate-900 font-extrabold text-lg py-3 px-8 rounded-xl shadow-lg transition transform hover:scale-105">
                        فتح واستلام الرسالة الكاملة بـ $3 🚀
                    </a>
                </div>
            </div>
        </div>
    </main>

    <footer class="p-6 border-t border-slate-800 text-center text-slate-500 text-sm">
        © 2026 Instant Cover Letter Generator. All rights reserved.
    </footer>

    <script>
        document.getElementById('generatorForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            const data = {{
                name: document.getElementById('name').value,
                job_title: document.getElementById('job_title').value,
                company_name: document.getElementById('company_name').value,
                experience_years: document.getElementById('experience_years').value,
                skills: document.getElementById('skills').value
            }};

            const res = await fetch('/generate', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify(data)
            }});
            const result = await res.json();
            document.getElementById('resultText').value = result.preview;
            document.getElementById('resultContainer').classList.remove('hidden');
        }});
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_cover_letter():
    data = request.json or {}
    name = data.get('name', 'Applicant')
    job_title = data.get('job_title', 'Professional')
    company_name = data.get('company_name', 'Hiring Manager')

    preview_text = f"Dear Hiring Manager at {company_name},\n\nI am writing to express my strong interest in the {job_title} position. With my background in technology and dedicated hands-on experience, I am confident in my ability to deliver immediate value...\n\n[🔒 المتبقي من النص محجوب - اضغط الزر بالأسفل لفتح النص بالكامل]"

    return jsonify({"status": "success", "preview": preview_text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
