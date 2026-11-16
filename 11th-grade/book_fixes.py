"""Hand fixes for places where the printed book itself is garbled.

The PDF prints a few code names and English phrases in the wrong order
(the typesetter's right-to-left layout broke them). The converter reproduces
the page faithfully, so the intended text is restored here. Each entry must
match exactly once; convert_book.py reports any that no longer match.
"""

# Figures whose crop picked up a neighbouring letter, caption or paragraph from the page.
# The crop rectangle (in PDF points, left, top, right, bottom) is moved inwards by these amounts.
IMAGE_CLIPS = {
    "p034-02.png": (5, 0, 0, 0),     # a letter from «if» at the left edge
    "p068-02.png": (8, 0, 0, -12),   # a letter at the left edge and the caption below
}

# A Persian paragraph from beside the figure, painted over in white (pixel rectangles
# x0, y0, x1, y1 of the 2.5x rendering). The output line under it stays untouched.
IMAGE_MASKS = {
    "p061-02.png": [(345, 0, 418, 300)],
}

FIXES = [
    # Tools table (back-end developer): the printed line is read left to right; as separate pieces the
    # brackets were split between the English words and the Persian text. The whole cell is kept as one
    # left-to-right span, with the same text as the book.
    # Printed table errors, checked against the page. The book prints these wrongly.
    # Table of built-in functions: print is written «Print», and float(5) is printed as 5.0.
    ("01-poodman-1-python/02-functions-and-modules.md", "`print(float(5))` | 50 |", "`print(float(5))` | 5.0 |"),
    ("01-poodman-1-python/02-functions-and-modules.md", "`Print(max(3, 9, 5))`", "`print(max(3, 9, 5))`"),
    ("01-poodman-1-python/02-functions-and-modules.md", "`Print(min(3, 9, 5))`", "`print(min(3, 9, 5))`"),
    ("01-poodman-1-python/02-functions-and-modules.md", "`Print(sum([2, 4, 6]))`", "`print(sum([2, 4, 6]))`"),
    # Comparison operators: < is «less than» and > is «more than» (the book's own examples say so);
    # the operators are printed with stray spaces.
    ("01-poodman-1-python/01-data-modeling.md", "| `! =` | مساوی نیست |", "| `!=` | مساوی نیست |"),
    ("01-poodman-1-python/01-data-modeling.md", "| `<` | بزرگ‌تر از |\n| `>` | کوچک‌تر از |", "| `<` | کوچک‌تر از |\n| `>` | بزرگ‌تر از |"),
    ("01-poodman-1-python/01-data-modeling.md", "| `> =` | بزرگ‌تر یا مساوی |", "| `>=` | بزرگ‌تر یا مساوی |"),
    ("01-poodman-1-python/01-data-modeling.md", "| `< =` | کوچک‌تر یا مساوی |", "| `<=` | کوچک‌تر یا مساوی |"),
    # Flex-direction table: the boxes were extracted as scrambled text; the picture shows box1 box2 box3.
    ("02-poodman-2-static-web/02-css.md", "box2box3<br>box1", "box1 box2 box3"),
    ("02-poodman-2-static-web/02-css.md", "box3box2box1", "box3 box2 box1"),
    # Two decorative arrows (CSS example, Poodman 2) were cropped without their outline:
    # only the letters inside them survived, as stray glyphs. The arrows add nothing to the
    # sentences around them, so the broken crops are removed.
    ("02-poodman-2-static-web/02-css.md", "> ![تصویر کتاب](../images/p125-03.png)\n>\n", ""),
    ("02-poodman-2-static-web/02-css.md", ">\n> ![تصویر کتاب](../images/p132-02.png)\n", ""),
    # Space lost before an inline code span (Module 1, data modeling).
    ("01-poodman-1-python/01-data-modeling.md", "ایجاد شده است`fruits", "ایجاد شده است `fruits"),
    ("01-poodman-1-python/01-data-modeling.md", "**دستور`input()`**", "**دستور `input()`**"),
    # (file, printed text, intended text)
    ("01-poodman-1-python/01-data-modeling.md", "`hello.py _ prog01`", "`prog01_hello.py`"),
    ("01-poodman-1-python/01-data-modeling.md", "اشتباه است: سلام py.", "اشتباه است: `سلام.py`"),
    ("01-poodman-1-python/01-data-modeling.md", "با پسوند py. در هر ویرایشگر", "با پسوند `.py` در هر ویرایشگر"),
    ("01-poodman-1-python/02-functions-and-modules.md", "نمایش عنوان :menu برای", "نمایش عنوان menu: برای"),
    ("01-poodman-1-python/02-functions-and-modules.md", "مقدار بازگشتی )**Return Value** )", "مقدار بازگشتی (**Return Value**)"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "**پروژه‌های MVP) minimum viable product**)", "**پروژه‌های MVP (minimum viable product)**"),
    ("02-poodman-2-static-web/01-html.md", "**نشانه‌گذاری عناصر در سند HTML: HTML**", "**نشانه‌گذاری عناصر در سند HTML:** HTML"),
    ("02-poodman-2-static-web/02-css.md", "ویژگی ;justify-content: space-between،", "ویژگی `justify-content: space-between;`،"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "وارد آدرس .icons `getbootstrap.com` شوید", "وارد آدرس `icons.getbootstrap.com` شوید"),
    ("03-poodman-3-interactive-web/02-javascript.md", "تعریف نشده یا )Undefined) خواهد", "تعریف نشده یا (Undefined) خواهد"),
    ("03-poodman-3-interactive-web/02-javascript.md", "در عبارت ( for (const name of firstNames چرا", "در عبارت `for (const name of firstNames)` چرا"),
    ("03-poodman-3-interactive-web/02-javascript.md", "به‌صورت نقطه‌ای .Math( )functionName امکان‌پذیر", "به‌صورت نقطه‌ای `Math.functionName()` امکان‌پذیر"),
    # Stacked fractions (4 over 12) come out of the PDF as scattered digits.
    ("03-poodman-3-interactive-web/01-bootstrap.md",
     "در دو اندازه \\_142\\_ و 12\n>\n> \\_8\\_ ایجاد می‌شود:",
     "در دو اندازه 4/12 و 8/12 ایجاد می‌شود:"),
    ("03-poodman-3-interactive-web/01-bootstrap.md",
     "> \\_4\\_ این دو ستون در دستگاه‌هایی با پهنای بزرگ‌تر یا مساوی 576 پیکسل در کنار هم و با اندازه‌های 12 \\_8\\_ نمایش داده می‌شوند. اما در دستگاه‌های کوچک‌تر، محتوای ستون‌ها روی هم قرار می‌گیرند و و 12\n>\n> در نتیجه",
     "> این دو ستون در دستگاه‌هایی با پهنای بزرگ‌تر یا مساوی 576 پیکسل در کنار هم و با اندازه‌های 4/12 و 8/12 نمایش داده می‌شوند. اما در دستگاه‌های کوچک‌تر، محتوای ستون‌ها روی هم قرار می‌گیرند و در نتیجه"),
    ("03-poodman-3-interactive-web/01-bootstrap.md",
     "> **پهنای دستگاه: بزرگ‌تر یا مساوی 576 پیکسل پهنای دستگاه: کمتر از 576 پیکسل**",
     "> **پهنای دستگاه: بزرگ‌تر یا مساوی 576 پیکسل** (تصویر اول) — **پهنای دستگاه: کمتر از 576 پیکسل** (تصویر دوم)"),
    ("03-poodman-3-interactive-web/01-bootstrap.md",
     "در اندازه \\_192\\_ و 12\n>\n> \\_3\\_ و در دستگاه‌های بزرگ‌تر با اندازه \\_142\\_ و 12\n>\n> \\_8\\_ نمایش داده می‌شوند.",
     "در اندازه 9/12 و 3/12 و در دستگاه‌های بزرگ‌تر با اندازه 4/12 و 8/12 نمایش داده می‌شوند."),
    ("03-poodman-3-interactive-web/01-bootstrap.md",
     "بزرگ‌تر برابر \\_142\\_، 12 و \\_132\\_ است. در پهنای 768 تا 992 پیکسل سهم هر ستون برابر 12\n>\n> \\_5\\_\n>\n> \\_4\\_ است و",
     "بزرگ‌تر برابر 4/12، 5/12 و 3/12 است. در پهنای 768 تا 992 پیکسل سهم هر ستون برابر 4/12 است و"),
    ("03-poodman-3-interactive-web/01-bootstrap.md",
     "> )شبکه توزیع محتوا( CDN: Content Delivery Networkـ۱",
     "> ۱ـ CDN: Content Delivery Network (شبکه توزیع محتوا)"),
    ("02-poodman-2-static-web/01-html.md",
     "| )Django، Python، Flask(، `JavaScript (Node.js)` |",
     "| `JavaScript (Node.js)`، Python (Django، Flask) |"),
    ("02-poodman-2-static-web/01-html.md",
     "**تگ `<Doctype html`**!&gt;: در ابتدای یک صفحه وب از تگ `<Doctype`! `html>` استفاده",
     "**تگ `<!Doctype html>`**: در ابتدای یک صفحه وب از تگ `<!Doctype html>` استفاده"),
    ("02-poodman-2-static-web/01-html.md",
     "**تگ `<html< :>html>`** تگ ریشه",
     "**تگ `<html>`**: تگ ریشه"),
    ("02-poodman-2-static-web/01-html.md",
     "عبارت`dir =\"trl\"` در تگ",
     "عبارت `dir=\"rtl\"` در تگ"),
    ("02-poodman-2-static-web/01-html.md",
     "با مقدار blank\\_ استفاده",
     "با مقدار `_blank` استفاده"),
    ("02-poodman-2-static-web/01-html.md",
     "برابر self\\_ است",
     "برابر `_self` است"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "کلمه important `!` در", "کلمه `!important` در"),
    # The CSS child combinator is «>».
    ("02-poodman-2-static-web/02-css.md", "انتخاب‌گر فرزند با نماد `<` و", "انتخاب‌گر فرزند با نماد `>` و"),
    ("02-poodman-2-static-web/02-css.md", "استفاده از علامت `<` باعث", "استفاده از علامت `>` باعث"),
    ("02-poodman-2-static-web/01-html.md",
     "> دانلود کتاب طراحی صفحات `<a href = \"./pdfs/books/web-design.pdf \" target=\"_blank\">` `</a>` وب",
     "> `<a href = \"./pdfs/books/web-design.pdf \" target=\"_blank\">` دانلود کتاب طراحی صفحات وب `</a>`"),
    # The percent sign is missing from the printed book.
    ("02-poodman-2-static-web/01-html.md",
     "از عبارتی مشابه `width=\"100\"` استفاده",
     "از عبارتی مشابه `width=\"100%\"` استفاده"),
    ("02-poodman-2-static-web/02-css.md",
     "شامل مقادیر lowercase، \ufffdupper cas، capitalize none، …",
     "شامل مقادیر uppercase، lowercase، capitalize، none و …"),
    ("02-poodman-2-static-web/02-css.md",
     "قوانین بالا به تگ‌های `<h2`&lt;، &gt;`h1>` و `<p>` اعمال",
     "قوانین بالا به تگ‌های `<h1>`، `<h2>` و `<p>` اعمال"),
    ("02-poodman-2-static-web/02-css.md", "**`nth()-child`**:", "**`nth-child()`**:"),
    ("02-poodman-2-static-web/02-css.md", ")( **first-child**:", "**`first-child`**:"),
    ("02-poodman-2-static-web/02-css.md", "**`last()-child`**:", "**`last-child`**:"),
    ("02-poodman-2-static-web/02-css.md", "`)padding:10px20.px`)", "(`padding:10px 20px`)"),
    ("02-poodman-2-static-web/02-css.md", "توسط انتخاب‌گر product-card a. انجام", "توسط انتخاب‌گر `.product-card a` انجام"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "<DOCTYPE`!&gt;،", "<!DOCTYPE html>`،"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "| سمت راست در `end( ltr)` |", "| سمت راست در ltr (end) |"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "| سمت چپ در `start( ltr)` |", "| سمت چپ در ltr (start) |"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "برابر با `p-3( 16px)` تعیین", "برابر با 16px (p-3) تعیین"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "| `shadow-none shadow-`<br>sm<br>shadow<br>`shadow-lg` |", "| `shadow-none`<br>`shadow-sm`<br>`shadow`<br>`shadow-lg` |"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "`danger-danger`", "`border-danger`"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "استایل‌دهی عناصر صفحه\n\nاستفاده می‌شوند", "استایل‌دهی عناصر صفحه استفاده می‌شوند"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "این کلاس‌ها نیازی به\n\nجاوا‌اسکریپت نیست", "این کلاس‌ها نیازی به جاوا‌اسکریپت نیست"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "دارای کلاس -list inline-item باشند", "دارای کلاس `list-inline-item` باشند"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "از کلاس -justify content-center در", "از کلاس `justify-content-center` در"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "به صورت -col breakpoint-size است", "به صورت `col-breakpoint-size` است"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "پارامترهای کلاس -col برای", "پارامترهای کلاس col- برای"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "انتخاب‌گر top-menu ul. با", "انتخاب‌گر `.top-menu ul` با"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "انتخابگر top-menu ul. را", "انتخابگر `.top-menu ul` را"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "در کلاس top-menu. نیست", "در کلاس `.top-menu` نیست"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "کادر f ilter", "کادر filter"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "توسط CSS و ۱ SASS امکان‌پذیر", "توسط CSS و SASS¹ امکان‌پذیر"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "هر ستون نیمی از ۶ ) را اشغال می‌نماید. \\_\\_ پهنای سطر (۱۲ B A |", "هر ستون نیمی از پهنای سطر (۶ از ۱۲) را اشغال می‌نماید. |"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "| B A D C کلاس row-cols-2", "| کلاس row-cols-2"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "به کلاس‌های \\*-d سپرده", "به کلاس‌های `d-*` سپرده"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "بعد از اضافه کردن کلاس‌های \\*-d، استایل", "بعد از اضافه کردن کلاس‌های `d-*`، استایل"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "ویژگی‌های عنصر bottom-toolbar. در فایل", "ویژگی‌های عنصر `.bottom-toolbar` در فایل"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "انتخاب‌گر bottom-toolbar. را حذف", "انتخاب‌گر `.bottom-toolbar` را حذف"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "همچون \\*-navbar-expand برای", "همچون `navbar-expand-*` برای"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "\\*-**navbar-expand**:", "**`navbar-expand-*`**:"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "با کلاس -navbar-toggler icon قرار", "با کلاس `navbar-toggler-icon` قرار"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "با شناسه navbar Collapse قرار", "با شناسه navbarCollapse قرار"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "با مقدار navbarCollapse# استفاده", "با مقدار `#navbarCollapse` استفاده"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "از کلاس nav-item. استفاده", "از کلاس nav-item استفاده"),
    ("03-poodman-3-interactive-web/02-javascript.md", "فایل `html.workshop1` را اجرا", "فایل `workshop1.html` را اجرا"),
    ("03-poodman-3-interactive-web/02-javascript.md", "در خط دوم و سوم\n>\n> باعث رخداد خطا", "در خط دوم و سوم باعث رخداد خطا"),
    ("04-poodman-4-python-oop/01-object-oriented.md", "از نمونه \\_my smartphone خوانده", "از نمونه `my_smartphone` خوانده"),
    ("05-poodman-5-django/02-develop-web-app.md", "به \\_delete city اشاره", "به `delete_city` اشاره"),
    ("01-poodman-1-python/02-functions-and-modules.md", "(import mojvle)", "(import module)"),
    ("04-poodman-4-python-oop/01-object-oriented.md", "به اختصار (.`O.O.P`) گفته", "به اختصار (`O.O.P.`) گفته"),
    ("01-poodman-1-python/01-data-modeling.md", "مثل (num, personl\\_ )", "مثل (`num`، `_personal`)"),
    # The printed symbol contradicts its own sentence; use the operator the sentence describes.
    ("01-poodman-1-python/01-data-modeling.md", "در این برنامه عملگر `<` برای بررسی شرط بیشتر بودن", "در این برنامه عملگر `>` برای بررسی شرط بیشتر بودن"),
    ("01-poodman-1-python/01-data-modeling.md", "در این برنامه عملگر `>` برای بررسی محدودیت سنی زیر", "در این برنامه عملگر `<` برای بررسی محدودیت سنی زیر"),
    ("01-poodman-1-python/01-data-modeling.md", "با عملگر `>=` مورد بررسی قرار گرفته است که تنها به تعداد ۵ یا کم", "با عملگر `<=` مورد بررسی قرار گرفته است که تنها به تعداد ۵ یا کم"),
    ("01-poodman-1-python/01-data-modeling.md", "با عملگر `=` `<` برقرار شده", "با عملگر `>=` برقرار شده"),
    ("01-poodman-1-python/01-data-modeling.md", "عملگرهای مقایسه `<=` به معنی بزرگ‌تر مساوی", "عملگرهای مقایسه `>=` به معنی بزرگ‌تر مساوی"),
    ("01-poodman-1-python/02-functions-and-modules.md", "`split()` `append()`", "`split()`، `append()`"),
    ("04-poodman-4-python-oop/02-object-oriented-development.md", "(یعنی برنامه py. شما)", "(یعنی برنامه `.py` شما)"),
    ("02-poodman-2-static-web/01-html.md", "نتیجه را در مرورگر مشاهده\n>\n> کنید.", "نتیجه را در مرورگر مشاهده کنید."),
    ("03-poodman-3-interactive-web/01-bootstrap.md", "در دستگاه دسکتاپ و موبایل\n>\n> به ترتیب 75%", "در دستگاه دسکتاپ و موبایل به ترتیب 75%"),
    # Comment labels printed one per line beside the code; keep them apart.
    ("02-poodman-2-static-web/02-css.md", "به حالت عمودی اشغال پهنای کامل برای هر عنصر لیست وسط چین کردن متن گزینه‌ها", "به حالت عمودی<br>اشغال پهنای کامل برای هر عنصر لیست<br>وسط چین کردن متن گزینه‌ها"),
    ("02-poodman-2-static-web/02-css.md", "ایجاد یک ستون واحد افزایش فاصله عمودی بین گزینه‌ها", "ایجاد یک ستون واحد<br>افزایش فاصله عمودی بین گزینه‌ها"),
    ("02-poodman-2-static-web/02-css.md", "# طراحی ظاهر صفحات وب  با CSS", "# طراحی ظاهر صفحات وب با CSS"),
]

# Pages whose layout (dotted leaders, two columns) does not survive as text.
# Keyed by PDF page; the markdown replaces what the converter would write.
PAGE_OVERRIDES = {
    1: """## طراح سایت

رشتۀ شبکه و نرم‌افزار رایانه — گروه برق و رایانه — شاخه فنی و حرفه‌ای

پایۀ یازدهم دورۀ دوم متوسطه

![جلد کتاب](images/p001-01.png)
""",
    2: """این اثر تحت یک مجوز آزاد و بدون محدودیت منتشر شده است و استفاده از آن برای عموم آزاد و رایگان است. هرگونه استفاده از کتاب و اجزای آن، از جمله چاپ و انتشار نسخه‌های الکترونیکی، تکثیر، بازنشر، ترجمه، اقتباس، ویرایش، تبدیل، استفاده در آثار دیگر، نمایش، ارائه و انتشار در پایگاه‌های مجازی و سایر اشکال استفاده، بدون نیاز به کسب مجوز قبلی از پدیدآورنده یا ناشر مجاز است.

این اثر را می‌توان برای هر منظور، اعم از شخصی، آموزشی، پژوهشی و تجاری، استفاده، کپی، تغییر و بازنشر کرد.
""",
    4: """## فهرست

- **پودمان اول: برنامه‌نویسی پایتون** — صفحه ۱
  - واحد یادگیری ۱ـ مدل‌سازی داده — صفحه ۲
  - واحد یادگیری ۲ـ کار با توابع و ماژول‌ها — صفحه ۴۸
- **پودمان دوم: طراحی صفحات وب ایستا** — صفحه ۸۳
  - واحد یادگیری ۱ـ طراحی ساختار صفحات وب با HTML — صفحه ۸۴
  - واحد یادگیری ۲ـ طراحی ظاهر صفحات وب با CSS — صفحه ۱۱۶
- **پودمان سوم: تولید صفحات وب تعاملی** — صفحه ۱۴۵
  - واحد یادگیری ۱ـ توسعه صفحات وب تعاملی با بوت‌استرپ — صفحه ۱۴۶
  - واحد یادگیری ۲ـ طراحی صفحات وب تعاملی با جاوااسکریپت — صفحه ۱۹۲
- **پودمان چهارم: توسعه وب پایتون** — صفحه ۲۳۳
  - واحد یادگیری ۱ـ تولید برنامه شیءگرا — صفحه ۲۳۴
  - واحد یادگیری ۲ـ توسعه برنامه شیءگرا — صفحه ۲۵۴
- **پودمان پنجم: برنامه‌نویسی جنگو** — صفحه ۲۷۵
  - واحد یادگیری ۱ـ ایجاد وب‌اپلیکیشن — صفحه ۲۷۶
  - واحد یادگیری ۲ـ توسعه وب‌اپلیکیشن — صفحه ۲۹۵
- **منابع** — صفحه ۳۳۰
""",
    5: "",
    6: "",
    336: """## منابع

1. سایت مستندات رسمی پایتون نسخه ۳: https://docs.python.org/3/
2. منبع جنگو: سایت مستندات رسمی جنگو: https://docs.djangoproject.com/
3. https://getbootstrap.com/
4. https://developer.mozilla.org
5. https://www.w3schools.com/
""",
}

# Pattern fixes: (file, regex, replacement).
REGEX_FIXES = [
    # Tools table (back-end developer): the printed line reads left to right; the brackets were split
    # between the English words and the Persian text. The whole cell becomes one left-to-right span.
    ("02-poodman-2-static-web/01-html.md", r"`JavaScript \(Node\.js\)`، Python \(Django، Flask\)", '<span dir="ltr">JavaScript (Node.js)، (Flask، Python، Django)</span>'),
    # The group row of the selector table was taken as the header of its own table.
    # It is a body row, under the same header as the simple-selector table.
    ("02-poodman-2-static-web/02-css.md", r"\| گروهی\(Group\) \| (.*)\n\| --- \| --- \|\n", "| نوع انتخاب‌گر | عملکرد |\n| --- | --- |\n| گروهی(Group) | \\1\n"),
    # A sentence cut by the page break (the next page starts with it).
    ("03-poodman-3-interactive-web/02-javascript.md", r"(با توجه به اینکه)\n\n(<!-- page 212 -->)\n\n([^\n]+)", r"\1 \3\n\n\2"),
    # «-justify content-center» is how the book prints «justify-content-center».
    ("03-poodman-3-interactive-web/01-bootstrap.md", r"(?<=\s)-([a-z]+) ([a-z]+-[a-z]+)\b", r"`\1-\2`"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", r"(?<=\s)-(modal|carousel) (header|item)\b", r"`\1-\2`"),
    ("03-poodman-3-interactive-web/01-bootstrap.md", r"-data `bs-interval=\"2000\"`", r"`data-bs-interval=\"2000\"`"),
    # Table cells print «rounded-1» as «1ـ rounded».
    ("03-poodman-3-interactive-web/01-bootstrap.md", r"\| ([0-5]) ?ـ (rounded|border) \|", r"| `\2-\1` |"),
]
