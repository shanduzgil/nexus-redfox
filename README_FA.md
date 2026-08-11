<div align="center">

[🇬🇧 English](README.md) • [🇮🇷 فارسی](README_FA.md)

</div>



<p align="center">
  <img src="assets/logo.png" alt="NEXUS REDFOX" width="260">
</p><h1 align="center">NEXUS REDFOX</h1><p align="center">
  <strong>هوشمندی کدبیس، تحلیل امنیتی و محیط کاری امنیت توسعه‌دهندگان با رویکرد Local-First</strong>
</p><p align="center">
  <a href="https://github.com/shanduzgil/nexus-redfox">GitHub</a>
  ·
  <a href="https://github.com/shanduzgil/nexus-redfox/issues">Issues</a>
  ·
  <a href="SECURITY.md">سیاست امنیتی</a>
  ·
  <a href="LICENSE">مجوز</a>
</p><p align="center">
  <em>کدبیس خود را بشناسید. معماری آن را ترسیم کنید. ریسک‌های امنیتی را پیدا کنید. وابستگی‌ها را بررسی کنید. یکپارچگی پروژه را تأیید کنید. همه‌چیز را به‌صورت محلی کنترل کنید.</em>
</p>---

📖 معرفی

NEXUS REDFOX 0.2.0 یک محیط هوشمندی کدبیس و تحلیل امنیتی با رویکرد Local-First است که برای توسعه‌دهندگان، مهندسان امنیت، پژوهشگران، نگهدارندگان پروژه و تیم‌های DevSecOps ساخته شده است تا بتوانند پروژه‌های نرم‌افزاری را از طریق یک ابزار واحد بررسی و درک کنند.

NEXUS قابلیت‌هایی را که معمولاً میان ابزارهای مختلف پراکنده هستند، در یک محیط واحد ترکیب می‌کند:

- 🔐 اسکن امنیتی قطعی و قابل تکرار
- 🧠 هوشمندی کدبیس و تحلیل معماری
- 🕸️ ساخت گراف وابستگی‌ها و Importها
- 🔎 جست‌وجوی Symbol و Path
- 🎯 تحلیل تأثیر تغییرات و Reverse Traversal
- 📦 تولید Software Bill of Materials یا SBOM
- 🧾 ساخت Manifest با SHA-256 و بررسی یکپارچگی
- 📦 ساخت Capsuleهای قابل انتقال از نتایج تحلیل
- 📊 تولید گزارش‌های JSON، HTML و SARIF
- 🤖 تحلیل اختیاری با هوش مصنوعی محلی از طریق Ollama
- 🔌 سرور سازگار با MCP
- 🌐 داشبورد وب محلی و آفلاین
- 🛠️ بررسی وضعیت Repositoryهای Git
- 🩺 تشخیص وضعیت محیط و پروژه

این پروژه عمداً بر پایهٔ یک مدل Local-First طراحی شده است. موتور تحلیل قطعی آن به Cloud API نیاز ندارد، فایل‌های Source را به‌صورت محلی می‌خواند و داشبورد وب نیز به‌صورت پیش‌فرض روی "127.0.0.1" اجرا می‌شود.

«نکته مهم: NEXUS REDFOX یک ابزار تحلیل و امنیت دفاعی است. هدف آن بررسی پروژه‌های نرم‌افزاری، شناسایی الگوهای مرتبط با امنیت، درک معماری و تولید گزارش‌های ساختاریافته است. این پروژه یک Exploit Framework نیست.»

---

✨ قابلیت‌ها

🔐 اسکنر امنیتی

NEXUS با استفاده از Rule Pack داخلی خود، تحلیل امنیتی ایستای قطعی را روی Source Tree انجام می‌دهد.

اسکنر می‌تواند الگوهای امنیتی مختلفی مانند موارد زیر را شناسایی کند:

- Secret و Credentialهای Hard-Coded
- Cloud Access Keyها
- Private Keyها
- Authentication Tokenها
- الگوهای خطرناک اجرای Command
- Dynamic Evaluation ناامن
- الگوهای ناامن Deserialization
- استفاده از رمزنگاری ضعیف
- مشکلات TLS Verification
- ساخت ناامن Queryهای SQL
- تنظیمات ناامن Workflowها
- سایر ضعف‌های امنیتی تعریف‌شده در Ruleها

سطح شدت Ruleها شامل موارد زیر است:

Critical
High
Medium
Low
Info

اسکن معمولی:

nexus scan .

اسکن عمیق:

nexus scan . --deep

می‌توانید کاری کنید که در صورت وجود Finding با شدت High یا Critical، فرآیند با وضعیت خطا پایان یابد:

nexus scan . --fail-on-high

---

🧠 هوشمندی کدبیس

NEXUS فقط فایل‌ها را Scan نمی‌کند.

این ابزار یک درک ساختاریافته از Repository ایجاد می‌کند و اطلاعاتی مانند موارد زیر را استخراج می‌کند:

- فایل‌ها
- مسیرها
- Symbolها
- Classها
- Functionها
- Methodها
- Importها
- ارتباط میان اجزای مختلف پروژه

سپس می‌توان از این اطلاعات برای جست‌وجو، Export، Traversal و سایر قابلیت‌های NEXUS استفاده کرد.

---

🕸️ گراف معماری

موتور Graph کدبیس را به یک گراف مبتنی بر معماری تبدیل می‌کند.

نمونهٔ ساده:

Application
│
├── authentication
│   ├── login()
│   └── session()
│
├── database
│   ├── connect()
│   └── query()
│
└── API
    ├── routes
    └── handlers

NEXUS این اطلاعات را به‌صورت Node و Relationship ذخیره می‌کند.

برای ساخت Graph:

nexus graph .

برای ذخیره Graph در فایل:

nexus graph . --out nexus-graph.json

خروجی Graph را می‌توان در اسکریپت‌ها، ابزارهای تحلیلی، داشبورد یا Automationهای دیگر استفاده کرد.

---

🎯 تحلیل تأثیر تغییرات

قابلیت Impact Analysis به شما اجازه می‌دهد یک Symbol، Path یا Node را در Graph پیدا کنید و اجزای مرتبط و وابسته را بررسی کنید.

مثال:

nexus impact authentication .

این قابلیت می‌تواند به پرسش‌هایی مانند موارد زیر پاسخ دهد:

- چه بخش‌هایی از پروژه به یک Component وابسته هستند؟
- چه فایل‌هایی به یک Symbol متصل‌اند؟
- با تغییر یک بخش، چه قسمت‌هایی ممکن است تحت تأثیر قرار بگیرند؟
- یک قابلیت خاص در کدام قسمت‌های معماری استفاده شده است؟

نتیجه به‌صورت JSON ساختاریافته شامل Nodeهای پیدا‌شده و Nodeهای تحت تأثیر ارائه می‌شود.

---

🔎 جست‌وجوی کد

NEXUS یک Index محلی برای پروژه دارد که امکان جست‌وجو بر اساس Symbol یا Path را فراهم می‌کند.

مثال:

nexus search login .

خروجی می‌تواند شامل اطلاعاتی مانند موارد زیر باشد:

id
kind
name
path
line

بنابراین به‌جای جست‌وجوی دستی میان همهٔ فایل‌ها، می‌توانید در ساختار پروژه جست‌وجوی سریع انجام دهید.

---

⚡ Index افزایشی پروژه

NEXUS یک Index مبتنی بر SQLite را در مسیر زیر نگهداری می‌کند:

.nexus/index.db

این Index اطلاعات استخراج‌شده از فایل‌های پروژه را ذخیره می‌کند و با استفاده از Metadata و Hash فایل‌ها می‌تواند از پردازش غیرضروری دوباره جلوگیری کند.

Workflow معمول:

nexus init .
nexus index .

پس از ایجاد Index، اجرای مجدد Index می‌تواند روی فایل‌های تغییرکرده تمرکز کند، به‌جای اینکه کل پروژه هر بار به‌عنوان یک پروژه کاملاً جدید بررسی شود.

---

📦 تولید Software Bill of Materials یا SBOM

NEXUS می‌تواند فایل‌های وابستگی و Manifestهای رایج را بررسی کرده و اطلاعات SBOM تولید کند.

دو قالب اصلی پشتیبانی‌شده:

- SPDX
- CycloneDX

برای تولید SBOM:

nexus sbom .

برای ذخیره در فایل:

nexus sbom . --out sbom.json

این قابلیت برای موارد زیر کاربرد دارد:

- Inventory وابستگی‌ها
- مشاهدهٔ زنجیرهٔ تأمین نرم‌افزار
- مستندسازی Release
- بررسی امنیتی
- Workflowهای Compliance
- تحلیل Dependencyها

---

🧾 Snapshot و بررسی یکپارچگی پروژه

NEXUS می‌تواند یک Manifest از پروژه ایجاد کند که شامل اطلاعات Integrity فایل‌ها است.

ساخت Snapshot:

nexus snapshot .

مسیر پیش‌فرض Snapshot:

.nexus/snapshot.json

امکان تعیین مسیر دلخواه:

nexus snapshot . --out release-manifest.json

Manifest شامل اطلاعات Integrity هر فایل بر پایهٔ Hashهای SHA-256 است.

برای بررسی پروژه با یک Manifest قبلی:

nexus verify .nexus/snapshot.json .

این Command یک JSON ساختاریافته برمی‌گرداند که مشخص می‌کند پروژه با Manifest ثبت‌شده مطابقت دارد یا خیر.

Snapshot برای موارد زیر مفید است:

- بررسی یکپارچگی
- کنترل Release
- Workflowهای قابل تکرار
- تشخیص تغییرات ناخواسته در فایل‌ها

---

📦 Capsuleهای قابل انتقال

Capsule در NEXUS یک فایل ZIP قابل حمل است که شامل Artifactهای تحلیل‌شدهٔ پروژه می‌شود.

ساخت Capsule:

nexus capsule .

تعیین مسیر خروجی:

nexus capsule . --out nexus-analysis.nexus.zip

Capsule می‌تواند شامل موارد زیر باشد:

- نتایج Security Scan
- اطلاعات Architecture Graph
- اطلاعات SBOM
- Manifest
- Metadata مربوط به Release
- Checksumهای SHA-256

برای قرار دادن Source پروژه داخل Capsule:

nexus capsule . --include-source

برای استفاده از Scan عمیق:

nexus capsule . --deep

ترکیب این گزینه‌ها:

nexus capsule . --include-source --deep --out nexus-analysis.nexus.zip

---

✅ بررسی Capsule

Capsule شامل Checksumهایی است که می‌توان بعداً آن‌ها را بررسی کرد.

اجرا:

nexus capsule-verify nexus-analysis.nexus.zip

این Command محتوای Capsule را با اطلاعات Checksum موجود در آن مقایسه می‌کند.

این قابلیت زمانی مفید است که بخواهید نتایج تحلیل را میان سیستم‌های مختلف جابه‌جا کنید یا یک بستهٔ تحلیل قابل بررسی و قابل نگهداری ایجاد کنید.

---

📊 گزارش‌های امنیتی

NEXUS از چند قالب گزارش پشتیبانی می‌کند.

HTML

برای تولید گزارش قابل مشاهده در مرورگر:

nexus scan . --format html --out nexus-report.html

گزارش HTML برای موارد زیر مناسب است:

- بررسی دستی
- ارزیابی امنیتی
- اشتراک‌گذاری داخلی
- مشاهدهٔ سریع نتایج

JSON

برای خروجی ساختاریافته:

nexus scan . --format json --out nexus-report.json

JSON برای اسکریپت‌ها و Integrationهای سفارشی مناسب است.

SARIF

برای تولید خروجی SARIF:

nexus scan . --format sarif --out nexus.sarif.json

SARIF برای اتصال به ابزارهای Security و Code Scanning بسیار مناسب است.

مثال:

nexus scan . --deep --format sarif --out nexus.sarif.json

---

🌐 داشبورد وب محلی

NEXUS یک داشبورد وب سبک و محلی نیز دارد.

برای اجرای آن:

nexus serve .

آدرس پیش‌فرض:

http://127.0.0.1:8765

داشبورد یک رابط محلی برای کار با داده‌های تحلیل پروژه فراهم می‌کند.

این داشبورد بخش‌هایی مرتبط با موارد زیر دارد:

- Security Findings
- Architecture Data
- SBOM
- Search

و APIهای داخلی آن نیز برای قابلیت‌هایی مانند Scan، Graph، SBOM و Search استفاده می‌شوند.

به‌صورت پیش‌فرض Server روی Loopback اجرا می‌شود.

---

🌍 فعال‌سازی دسترسی از راه دور

دسترسی Remote به‌صورت پیش‌فرض فعال نیست.

اگر عمداً نیاز دارید Server روی Interfaceهای غیر Loopback نیز در دسترس باشد:

nexus serve . --host 0.0.0.0 --port 8765 --allow-remote

این گزینه را فقط زمانی فعال کنید که از Exposure شبکه آگاه باشید و کنترل دسترسی مناسب داشته باشید.

برای استفادهٔ عادی و محلی، همان حالت پیش‌فرض را نگه دارید:

nexus serve .

---

🤖 هوش مصنوعی محلی با Ollama

NEXUS می‌تواند به‌صورت اختیاری از یک Ollama محلی برای تحلیل طبیعی و پرسش از پروژه استفاده کند.

پیکربندی پیش‌فرض:

Endpoint: http://127.0.0.1:11434
Model:    qwen2.5-coder:7b

1. نصب Ollama

Ollama را برای سیستم‌عامل خود از توزیع رسمی آن نصب کنید.

پس از نصب، مطمئن شوید Ollama در دسترس است.

2. دریافت مدل پیش‌فرض

ollama pull qwen2.5-coder:7b

برای اجرای مستقیم مدل:

ollama run qwen2.5-coder:7b

3. پرسیدن سؤال از NEXUS

از ریشهٔ پروژه:

nexus ask "Explain the authentication flow" .

نمونهٔ سؤال:

nexus ask "Explain the architecture of this project" .

یا:

nexus ask "Where are the main security-sensitive components?" .

یا:

nexus ask "Which components appear to depend on the authentication subsystem?" .

NEXUS اطلاعات مرتبط با پروژه را جمع‌آوری کرده و Context مناسب را برای مدل محلی ارسال می‌کند.

Endpoint پیش‌فرض:

127.0.0.1:11434

است.

---

⚙️ استفاده از مدل یا Endpoint سفارشی

می‌توانید مدل را تغییر دهید:

nexus ask "Explain the project" . --model qwen2.5-coder:7b

Endpoint را نیز می‌توان تغییر داد:

nexus ask "Explain the project" . --url http://127.0.0.1:11434

زمان Timeout:

nexus ask "Explain the project" . --timeout 300

برای Endpointهای غیرمحلی، باید Remote Access را به‌صورت صریح فعال کنید:

nexus ask "Explain the project" . --url http://your-server:11434 --allow-remote

فقط زمانی از Remote Endpoint استفاده کنید که عمداً بخواهید اطلاعات پروژه به یک سیستم دیگر ارسال شود.

---

🔌 سرور MCP

NEXUS یک Server سازگار با MCP دارد تا ابزارهای سازگار با MCP بتوانند به قابلیت‌های تحلیل پروژه دسترسی داشته باشند.

اجرای MCP Server:

nexus mcp .

این Interface برای دسترسی Read-Oriented به اطلاعات پروژه طراحی شده و می‌تواند قابلیت‌هایی مانند موارد زیر را در اختیار MCP Client قرار دهد:

- Security Findings
- Architecture
- Code Relationships
- Symbolها
- Dependencyها
- Remediation Information

به این ترتیب می‌توان NEXUS را میان یک AI Assistant و Codebase قرار داد تا AI بتواند اطلاعات ساختاریافتهٔ پروژه را دریافت کند.

---

🧾 توضیح Ruleهای امنیتی

NEXUS یک Knowledge Base محلی برای Security و Remediation دارد.

برای توضیح یک Rule:

nexus explain NXS101

این Command اطلاعات مرتبط با Rule را نمایش می‌دهد و در صورت وجود، توضیحات و راهنمای Remediation آن را ارائه می‌کند.

این قابلیت زمانی بسیار مفید است که یک Finding از Scan دریافت کرده‌اید و می‌خواهید قبل از بررسی دقیق کد، مفهوم Rule را بهتر متوجه شوید.

---

🩺 Doctor

Command "doctor" برای بررسی وضعیت محیط و پروژه استفاده می‌شود.

اجرا:

nexus doctor .

این Command اطلاعاتی مانند موارد زیر را بررسی می‌کند:

- نسخهٔ Python
- آیا پروژه Git Repository است یا خیر
- آیا Ollama قابل دسترسی است یا خیر
- آمار Graph

این یکی از اولین ابزارهایی است که هنگام Troubleshooting می‌توانید اجرا کنید.

---

🌿 خلاصهٔ وضعیت Git

NEXUS می‌تواند وضعیت Git Repository را بررسی کند.

اجرا:

nexus git-summary .

این Command اطلاعاتی مانند وضعیت Repository، Branch، Commit و وضعیت Working Tree را برای Workflowهای تحلیل ارائه می‌کند.

---

🚀 نصب

NEXUS REDFOX به موارد زیر نیاز دارد:

- Python 3.11 یا جدیدتر
- Windows، macOS یا Linux
- Git در صورت Clone کردن Repository
- Ollama فقط در صورتی که قابلیت Local AI را بخواهید

هستهٔ پروژه با Python پیاده‌سازی شده و برای سه خانوادهٔ اصلی سیستم‌عامل دسکتاپ و Server طراحی شده است.

سیستم‌عامل‌های موبایل به‌عنوان Target رسمی این نسخه معرفی نشده‌اند.

---

🐍 روش اول — نصب از GitHub

Repository را Clone کنید:

git clone https://github.com/shanduzgil/nexus-redfox.git

وارد پوشه شوید:

cd nexus-redfox

یک Virtual Environment بسازید.

Linux / macOS

python3 -m venv .venv
source .venv/bin/activate

Windows PowerShell

py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1

Windows Command Prompt

py -3.11 -m venv .venv
.venv\Scripts\activate.bat

NEXUS را نصب کنید:

python -m pip install --upgrade pip
python -m pip install .

بررسی نصب:

nexus --version

---

⚡ روش دوم — نصب Wheel

در صورتی که Release شامل Wheel باشد، معمولاً می‌توانید فایل داخل:

dist/

را نصب کنید.

مثال:

python -m pip install dist/nexus_redfox-0.2.0-py3-none-any.whl

سپس:

nexus --version

---

🛠️ نصب برای توسعه

اگر می‌خواهید خود NEXUS را توسعه دهید:

git clone https://github.com/shanduzgil/nexus-redfox.git
cd nexus-redfox

پس از ساخت و فعال‌سازی Virtual Environment:

python -m pip install -e .

اکنون تغییرات Source به‌صورت مستقیم روی نسخهٔ نصب‌شده اعمال خواهند شد.

---

🪟 اسکریپت‌های کمکی Windows

Repository شامل Scriptهای کمکی زیر نیز است:

nexus.bat
nexus.ps1
nexus.sh

این فایل‌ها برای اجرای ساده‌تر پروژه در محیط‌های مختلف ارائه شده‌اند.

روش استاندارد نصب Python همچنان روش پیشنهادی برای نصب Cross-Platform است.

---

🐳 Docker

NEXUS شامل Dockerfile و فایل Compose نیز می‌باشد.

ساخت Image:

docker build -t nexus-redfox .

اجرای Container:

docker run --rm -p 8765:8765 nexus-redfox

داشبورد روی Port زیر در دسترس قرار می‌گیرد:

8765

فایل Compose نیز از گزینه‌های Hardening مانند موارد زیر استفاده می‌کند:

- Filesystem فقط خواندنی
- "/tmp" موقت و قابل نوشتن
- "no-new-privileges"

اجرای Compose:

docker compose up --build

سپس:

http://127.0.0.1:8765

را باز کنید.

---

🧭 راه‌اندازی اولیه

پس از نصب، یک پروژه را Initialize کنید:

cd /path/to/your-project
nexus init .

این کار فایل زیر را ایجاد می‌کند:

.nexus/
└── config.json

در این تنظیمات مواردی مانند زیر قرار می‌گیرند:

- حداکثر اندازه فایل
- رفتار نسبت به فایل‌های Hidden
- مسیرهای Ignore
- تنظیمات Worker
- Ollama Endpoint
- مدل AI
- Timeout
- Policy مربوط به Remote Agent
- Scan Mode

---

🔥 Workflow پیشنهادی برای شروع

برای یک پروژهٔ جدید، می‌توانید با این Workflow شروع کنید:

nexus init .

سپس Index را بسازید:

nexus index .

اسکن امنیتی:

nexus scan . --format html --out nexus-report.html

ساخت Architecture Graph:

nexus graph . --out nexus-graph.json

ساخت SBOM:

nexus sbom . --out sbom.json

ساخت Snapshot:

nexus snapshot .

و در آینده بررسی Snapshot:

nexus verify .nexus/snapshot.json .

در نهایت ساخت Capsule:

nexus capsule . --out nexus-analysis.nexus.zip

---

🧪 تحلیل امنیتی عمیق

برای بررسی عمیق‌تر Ruleها:

nexus scan . --deep --format html --out nexus-deep-report.html

برای SARIF:

nexus scan . --deep --format sarif --out nexus-deep.sarif.json

برای CI که باید در صورت وجود Finding با شدت High یا Critical شکست بخورد:

nexus scan . --deep --fail-on-high

---

🗂️ فایل‌هایی که NEXUS ایجاد می‌کند

یک پروژهٔ تحلیل‌شده ممکن است ساختاری شبیه زیر داشته باشد:

your-project/
│
├── .nexus/
│   ├── config.json
│   ├── index.db
│   └── snapshot.json
│
├── nexus-report.html
├── nexus-graph.json
├── sbom.json
└── nexus-analysis.nexus.zip

این فایل‌ها بسته به Commandهایی که اجرا می‌کنید ایجاد می‌شوند.

پوشهٔ ".nexus/" فضای کاری محلی NEXUS برای Configuration، Index و Snapshot است.

---

🔒 مدل امنیتی Local-First

یکی از اهداف اصلی NEXUS این است که تحلیل قطعی تا حد ممکن به‌صورت محلی انجام شود.

Workflow اصلی به Cloud API برای موارد زیر نیاز ندارد:

- Scan
- Graph
- Index
- Search
- Impact Analysis
- SBOM
- Manifest
- Capsule

NEXUS فایل‌های پروژه را به‌صورت محلی می‌خواند.

داشبورد به‌صورت پیش‌فرض روی:

127.0.0.1

و Endpoint پیش‌فرض AI روی:

127.0.0.1:11434

قرار دارد.

دسترسی Remote برای Dashboard و AI نیاز به فعال‌سازی صریح دارد.

---

🚫 کد Repository در Workflow اصلی اجرا نمی‌شود

NEXUS برای بررسی Source Tree طراحی شده است، نه اجرای Repository مورد تحلیل.

در عملیات اصلی مانند:

scan
graph
sbom
capsule

تمرکز بر خواندن و تحلیل محتویات Repository است.

بنابراین برای تحلیل اولیهٔ یک Source Tree نیازی نیست خود پروژه را اجرا کنید.

---

🧩 اکوسیستم تحلیل‌شده

NEXUS منطق تحلیل برای طیف گسترده‌ای از زبان‌ها و فرمت‌ها دارد، از جمله:

Python
JavaScript
TypeScript
Java
Kotlin
Go
Rust
Ruby
PHP
C
C++
C#
Swift
Scala
Shell
SQL
HTML
CSS
JSON
YAML
TOML
XML
Gradle
Properties

همچنین فایل‌های رایج پروژه و Manifestهای Build و Dependency را شناسایی می‌کند.

پشتیبانی واقعی به منطق تحلیل موجود در نسخهٔ فعلی بستگی دارد.

---

🏗️ معماری پروژه

در سطح بالا، NEXUS از چند لایهٔ منطقی تشکیل شده است:

                    ┌───────────────────────┐
                    │       NEXUS CLI       │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
        ▼                       ▼                        ▼
   Security Scanner        Code Graph               Indexer
        │                       │                        │
        ▼                       ▼                        ▼
     Findings              Architecture               SQLite
        │                   Relationships              Index
        │
        ├──────────────┐
        ▼              ▼
      Reports         CWE / Remediation
        │
        ├── JSON
        ├── HTML
        └── SARIF

        ┌─────────────────────────────────────────┐
        │               موتورهای دیگر             │
        ├─────────────────────────────────────────┤
        │ SBOM │ Manifest │ Capsule │ Git │ MCP  │
        └─────────────────────────────────────────┘
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
             Web Dashboard       Local AI
                                  Ollama

پیاده‌سازی اصلی پروژه با Python انجام شده و داشبورد نیز از Assetهای وب استفاده می‌کند.

---

🔬 Pipeline تحلیل

Workflow ساده‌شدهٔ NEXUS:

Repository
    │
    ▼
File Discovery
    │
    ├──────────────► Security Scanner ─────► Findings
    │
    ├──────────────► Symbol Extraction ────► Index
    │
    ├──────────────► Import Analysis ──────► Graph
    │
    ├──────────────► Dependency Parsing ───► SBOM
    │
    └──────────────► File Hashing ─────────► Manifest
                                              │
                                              ▼
                                           Capsule

نتایج تولیدشده می‌توانند از طریق موارد زیر مصرف شوند:

CLI
Web Dashboard
JSON
HTML
SARIF
MCP
Local AI

---

📁 ساختار Repository

ساختار ساده‌شده:

nexus-redfox/
│
├── nexus/
│   ├── agent.py
│   ├── capsule.py
│   ├── cli.py
│   ├── config.py
│   ├── gitops.py
│   ├── graph.py
│   ├── indexer.py
│   ├── manifest.py
│   ├── mcp.py
│   ├── models.py
│   ├── playbook.py
│   ├── reports.py
│   ├── rules.py
│   ├── sbom.py
│   ├── scanner.py
│   ├── web.py
│   └── workflows.py
│
├── web/
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
├── tests/
├── docs/
├── dist/
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── SECURITY.md
├── THREAT_MODEL.md
└── LICENSE

---

🧰 مرجع Commandها

Initialize

nexus init .

Index

nexus index .

Search

nexus search <query> .

مثال:

nexus search login .

Scan

nexus scan .

Deep Scan

nexus scan . --deep

HTML Report

nexus scan . --format html --out report.html

JSON Report

nexus scan . --format json --out report.json

SARIF

nexus scan . --format sarif --out report.sarif.json

شکست در برابر High / Critical

nexus scan . --fail-on-high

ساخت Graph

nexus graph . --out graph.json

Impact Analysis

nexus impact <query> .

تولید SBOM

nexus sbom . --out sbom.json

ساخت Snapshot

nexus snapshot .

بررسی Snapshot

nexus verify .nexus/snapshot.json .

ساخت Capsule

nexus capsule . --out analysis.nexus.zip

قرار دادن Source در Capsule

nexus capsule . --include-source

بررسی Capsule

nexus capsule-verify analysis.nexus.zip

اجرای Dashboard

nexus serve .

اجرای Dashboard با دسترسی Remote

nexus serve . --host 0.0.0.0 --port 8765 --allow-remote

اجرای MCP

nexus mcp .

استفاده از Local AI

nexus ask "Explain this project" .

استفاده از Deep Context

nexus ask "Explain the authentication architecture" . --deep

توضیح یک Security Rule

nexus explain NXS101

بررسی محیط

nexus doctor .

خلاصه Git

nexus git-summary .

نمایش نسخه

nexus --version

---

🧠 یک Workflow کامل نمونه

فرض کنید پروژه‌ای با نام "my-application" دارید.

وارد پروژه شوید:

cd my-application

NEXUS را Initialize کنید:

nexus init .

Index محلی را بسازید:

nexus index .

یک Scan اولیه انجام دهید:

nexus scan . --format html --out nexus-report.html

گزارش HTML را در مرورگر باز کنید.

سپس Architecture Graph:

nexus graph . --out nexus-graph.json

SBOM:

nexus sbom . --out sbom.json

Snapshot:

nexus snapshot .

داشبورد:

nexus serve .

سپس وارد:

http://127.0.0.1:8765

شوید.

اگر Ollama تنظیم شده باشد:

nexus ask "Explain how authentication works in this repository" .

در نهایت یک Capsule ایجاد کنید:

nexus capsule . --out nexus-analysis.nexus.zip

با این مراحل، از Discovery تا Analysis، Reporting و Archival یک Workflow کامل محلی خواهید داشت.

---

🔍 استفاده از NEXUS برای بررسی امنیتی

یک Workflow دفاعی پیشنهادی:

1. ایجاد Baseline

nexus snapshot .

2. ساخت Index

nexus index .

3. اجرای Scan سریع

nexus scan . --format html --out security.html

4. اجرای Scan عمیق

nexus scan . --deep --format sarif --out security.sarif.json

5. بررسی معماری

nexus graph . --out architecture.json

6. جست‌وجوی Components مهم

nexus search authentication .

7. تحلیل Impact

nexus impact authentication .

8. ساخت Dependency Inventory

nexus sbom . --out sbom.json

9. بررسی Integrity

nexus verify .nexus/snapshot.json .

10. نگهداری از نتایج تحلیل

nexus capsule . --out security-analysis.nexus.zip

---

🛡️ NEXUS برای چه کارهایی طراحی شده است؟

NEXUS برای موارد زیر مناسب است:

- بررسی امنیتی Source Code
- Audit کردن Repository
- بررسی معماری نرم‌افزار
- Workflowهای امنیتی توسعه‌دهندگان
- فرآیندهای DevSecOps
- Inventory وابستگی‌ها
- تولید SBOM
- بررسی Integrity Source
- مطالعه و درک Codebase
- پژوهش امنیتی روی کدهایی که مجوز بررسی آن‌ها را دارید
- تحلیل کد با کمک Local AI
- مستندسازی پروژه
- بررسی امنیتی قبل از Release

---

🚫 NEXUS چه چیزی نیست؟

NEXUS قرار نیست جایگزین موارد زیر باشد:

- پلتفرم کامل Dynamic Application Security Testing
- سیستم Monitoring زمان اجرا
- دیتابیس کامل آسیب‌پذیری Dependencyها
- پلتفرم Cloud Security
- بررسی دستی Source Code
- Formal Verification
- Penetration Testing

Static Analysis می‌تواند الگوهای مشکوک و امنیتی را شناسایی کند، اما هر Finding باید با توجه به Context واقعی توسط انسان بررسی شود.

---

⚠️ False Positive و بررسی انسانی

ماهیت Security Scan مبتنی بر Pattern است.

وجود یک Finding لزوماً به معنی این نیست که پروژه دارای یک Vulnerability قابل Exploit است.

هنگام بررسی هر Finding، موارد زیر را در نظر بگیرید:

Rule
Path
Line
Context
Severity
Confidence

قبل از تصمیم‌گیری امنیتی، Finding را به‌صورت دستی بررسی کنید.

از اطلاعات Remediation مرتبط با Rule برای هدایت بررسی خود استفاده کنید.

---

🔒 امنیت و حریم خصوصی

NEXUS بر پایهٔ معماری Local-First ساخته شده است.

به‌صورت پیش‌فرض:

- تحلیل به‌صورت محلی اجرا می‌شود
- Source Fileها به‌صورت محلی خوانده می‌شوند
- Web Dashboard روی Loopback قرار دارد
- AI Endpoint پیش‌فرض روی Loopback است
- برای تحلیل قطعی به Cloud API نیازی نیست

وقتی Local AI فعال باشد، NEXUS می‌تواند با Endpoint تنظیم‌شدهٔ Ollama ارتباط برقرار کند.

اگر Remote Endpoint را عمداً تنظیم کنید، بخشی از Context استخراج‌شده از پروژه ممکن است از سیستم شما خارج شود.

بنابراین قبل از تحلیل Repositoryهای حساس با سرویس‌های Remote، تنظیمات خود را بررسی کنید.

مستندات امنیتی:

- ""SECURITY.md"" (SECURITY.md)
- ""THREAT_MODEL.md"" (THREAT_MODEL.md)

---

🤝 مشارکت در پروژه

مشارکت در NEXUS REDFOX آزاد است.

قبل از مشارکت، ابتدا فایل زیر را مطالعه کنید:

CONTRIBUTING.md

برای توسعه:

python -m pip install -e .

پس از نصب می‌توانید Testهای پروژه را با Workflow تست مورد استفادهٔ پروژه اجرا کنید.

هنگام ارسال تغییرات، اهداف امنیتی، قابلیت حمل و Cross-Platform بودن پروژه را در نظر بگیرید.

---

📚 مستندات

مستندات تکمیلی در مسیر زیر قرار دارند:

docs/

فایل‌های مهم:

- ""docs/architecture.md"" (docs/architecture.md)
- ""docs/release.md"" (docs/release.md)
- ""docs/roadmap.md"" (docs/roadmap.md)
- ""SECURITY.md"" (SECURITY.md)
- ""THREAT_MODEL.md"" (THREAT_MODEL.md)
- ""CONTRIBUTING.md"" (CONTRIBUTING.md)

---

📦 یکپارچگی Release

Artifactهای Release با اطلاعات Integrity منتشر می‌شوند.

Repository شامل فایل‌هایی مانند موارد زیر است:

SHA256SUMS.txt
PROVENANCE.json
RELEASE-MANIFEST.json

هدف این فایل‌ها پشتیبانی از Verification و بررسی Provenance مربوط به Artifactهای منتشرشده است.

هنگام استفاده از Releaseها، Checksumها را بررسی کرده و در صورت وجود، اطلاعات Build Provenance منتشرشده را نیز مطالعه کنید.

---

📜 مجوز

کد NEXUS REDFOX تحت:

Apache License 2.0

منتشر شده است.

فایل مجوز:

""LICENSE"" (LICENSE)

نام و برند NEXUS متعلق به پروژه است.

برای اطلاعات مربوط به استفاده از نام و برند:

""TRADEMARKS.md"" (TRADEMARKS.md)

---

❤️ سخن پایانی

NEXUS REDFOX بر پایهٔ یک ایدهٔ ساده ساخته شده است:

«یک Codebase باید به‌عنوان یک سیستم قابل فهم باشد، نه فقط مجموعه‌ای از فایل‌ها.»

به‌جای استفاده از ابزارهای جداگانه برای:

- Security Scan
- Architecture Discovery
- Dependency Inventory
- Integrity Verification
- Reporting
- Local AI Analysis
- Project Inspection

NEXUS این قابلیت‌ها را در یک محیط Local-First کنار هم قرار می‌دهد.

برای شروع:

nexus init .
nexus index .
nexus scan .
nexus graph .
nexus sbom .
nexus serve .

برای Workflow پیشرفته‌تر:

nexus impact <query> .
nexus snapshot .
nexus verify .nexus/snapshot.json .
nexus capsule .
nexus capsule-verify <file>
nexus ask "Explain this project" .
nexus mcp .

کدبیس را بشناسید. ساختار را ببینید. ریسک‌ها را پیدا کنید. Artifactها را بررسی کنید. کنترل Workflow را در دست خودتان نگه دارید.

---

<p align="center">
  <strong>NEXUS REDFOX 0.2.0</strong><br>
  محیط Local-First برای هوشمندی کدبیس و تحلیل امنیتی
</p>
