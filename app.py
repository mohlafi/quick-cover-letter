import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
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
        <p class="text-slate-400 mt-2">احصل على رسالة تغطية احترافية في أقل من دقيقة</p>
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
                    توليد الرسالة الآن ✨
                </button>
            </form>

            <div id="resultContainer" class="mt-8 hidden">
                <h3 class="text-xl font-bold mb-2 text-indigo-400">الرسالة الجاهزة:</h3>
                <textarea id="resultText" rows="10" class="w-full p-4 rounded-lg bg-slate-900 border border-slate-700 text-slate-200 dir-ltr text-left font-mono" readonly></textarea>
                <button onclick="copyText()" class="mt-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-6 rounded-lg transition">
                    نسخ النص 📋
                </button>
            </div>
        </div>
    </main>

    <footer class="p-6 border-t border-slate-800 text-center text-slate-500 text-sm">
        © 2026 Instant Cover Letter Generator. All rights reserved.
    </footer>

    <script>
        document.getElementById('generatorForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('name').value,
                job_title: document.getElementById('job_title').value,
                company_name: document.getElementById('company_name').value,
                experience_years: document.getElementById('experience_years').value,
                skills: document.getElementById('skills').value
            };

            const res = await fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            document.getElementById('resultText').value = result.cover_letter;
            document.getElementById('resultContainer').classList.remove('hidden');
        });

        function copyText() {
            const copyText = document.getElementById("resultText");
            copyText.select();
            document.execCommand("copy");
            alert("تم نسخ النص بنجاح!");
        }
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
    experience_years = data.get('experience_years', '3')
    skills = data.get('skills', 'Problem Solving, Teamwork')

    cover_letter_text = f"""Dear Hiring Manager at {company_name},

I am writing to express my strong interest in the {job_title} position. With over {experience_years} years of dedicated hands-on experience and deep expertise in {skills}, I am confident in my ability to deliver immediate value to your organization.

Throughout my career, I have consistently focused on building scalable, reliable solutions and optimizing workflows. My background equips me with the technical and practical skills necessary to solve complex challenges and drive practical results for your team.

Thank you for your time and consideration. I welcome the opportunity to discuss how my experience aligns with your current needs.

Sincerely,
{name}"""

    return jsonify({"status": "success", "cover_letter": cover_letter_text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)