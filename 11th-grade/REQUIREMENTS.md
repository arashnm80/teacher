# Requirements — grade 11 site (طراح سایت)

Remember these on every later change. The classroom copy is the test.

## What this is

A static companion to the grade-11 textbook «طراح سایت» (رشته شبکه و نرم‌افزار رایانه). Students open it on lab PCs that have no internet.

## Must stay true

1. **Offline, including `file://`.** Copying the `site/` folder to a Windows PC and double-clicking `index.html` is the whole install. No web server, no `npm`, no internet.
2. **The `site/` folder is complete.** HTML, CSS, JavaScript, and images all live inside it. Do not link to `../converted-markdown-book/` or to anything outside `site/`. Symlinks break when the folder is copied to Windows.
3. **No remote dependencies.** No CDN, no Google Fonts, no analytics, no `fetch()` of a file (Chrome blocks `fetch` on `file://`). Ship data in a normal `<script>` file instead. Fonts are the ones already on school PCs (`Tahoma`, `Segoe UI`, `Consolas`).
4. **Relative links only** for anything the page needs in order to render.
5. **Both languages are the whole page, baked into the HTML.** Persian is the textbook transcription. English is a full transcription of the same sections (prose translated; code fences, inline code, and figure files unchanged). Each page carries both, and the switch only shows or hides them. Nothing is fetched. The choice is remembered in `localStorage` under `grade11-lang`. Default, including with JavaScript off, is Persian.
6. **One language control.** The فا / EN control is a single button. Clicking it anywhere, including the side that already looks selected, toggles the language.
7. **Sections follow the topic, not the printed پودمان length.** `outline.py` maps book pages into short sections. A section should be one sitting of reading. Callouts stay with the topic they belong to. The sidebar lists those sections under the module and the unit. Below 700 CSS pixels (a phone, or a Windows PC whose display scaling or browser zoom makes the window that narrow) the list collapses into a «فهرست درس‌ها» / Lessons hamburger button that opens it as an overlay. The button is prominent and fixed in the corner, so a narrow screen never shows a silent empty column where the sidebar used to be.
8. **Mixed Persian and English on one line must stay readable.** Persian paragraphs stay right-to-left. English words, code, and parentheses around them are isolated left-to-right. English paragraphs do the reverse for any Persian that remains. Code blocks are always left-to-right.
9. **Exercises and useful links are extra, and they look extra.** Each lesson ends with enough build tasks to cover that lesson (small lessons 3, big ones up to 7), ordered easy to hard. Every task names its file, its exact inputs, and what the finished result must look like, so nothing is ambiguous. Tasks ask for logic, understanding, and creativity — never memorizing trivia like pep8 numbers. The contents page (فهرست) has no practice panel. The book's own callouts (کنجکاوی / پروژه / نکته / فعالیت and their English twins) render as tinted boxes (`.callout`), built by `box_callouts()` in `build_site.py`, so they never look like stray lines. They are not printed book text. They sit in a green panel (`.extra`) after the lesson. Book text stays on the white lesson panel. A link in that panel may point at the public web; the page itself must still render offline. The cover and license pages (شناسنامه و مجوز) are not part of the site. The book's competency-scoring pages (ارزشیابی) are not part of the site either; a lesson that continues into that rubric stops before it.
10. **Offline zip, visible on the site.** The home page and the header both link to `grade11-offline.zip`. The file is the whole site. It unpacks to one folder, `grade11-site/`, and does not contain the zip itself. Students unzip it and open `index.html`. Nginx sends it as a download. Building the site writes this file; `deploy.sh` publishes it with the rest of `site/`. The «Useful links» page (`links`, module `more`) is a living page built by `links_html()`, not book text. Its thumbnails live in `extra-images/` and are copied into `site/images` at build time, so the page renders offline; the links themselves need internet only when clicked. That page also offers `teacher-playground-offline.zip` (Module 1 offline Python practice — unzip and run `شروع.bat`) and `evolution-of-trust-offline.zip` (period-4 trust game). Both live in `extras/` and are copied into `site/` at build time. The practice app source is the separate repo [arashnm80/teacher-playground](https://github.com/arashnm80/teacher-playground); keep `/root/Storage/teacher-playground` on this server matching GitHub when you refresh the zip.
11. **The pages themselves must not need a VPN.** Every stylesheet, script, font, and image that the page needs comes from this same site. Do not add Google Fonts, a CDN, or any other host required to render the page. Useful links may point outside, and those links need the network only if someone clicks them. The name `teacher.arashnm80.ir` is still a Cloudflare-proxied record unless that record is changed at Cloudflare. Proxied Cloudflare addresses are often blocked on Iranian networks, so the name may fail with no VPN even though the pages have no foreign assets. Direct origin is this machine, `65.109.200.45`, with the existing wildcard certificate. Turning the Cloudflare cloud grey, so the A record is that address, is the DNS change that lets the name open without passing through Cloudflare.
12. **Works with JavaScript off for reading.** Persian navigation and lesson pages must still open. JavaScript is only for the language switch and search.
13. **Rebuild and publish after every content update.** Persian comes from `converted-markdown-book/` sliced by `outline.py`. English lives in `sections/en/<id>.md` and must be updated when that slice changes. `repair_markdown.py` runs on both before HTML conversion: diagram labels must not sit in the middle of a sentence, and prose must not be a code block. Exercises for the green panel live in `practical.py`. From `11th-grade/`, run `python3 build_site.py` (needs the `markdown` package) and then `bash deploy.sh`. The update is not done until `deploy.sh` has copied `site/` to the live site.
14. **Public copy.** `https://teacher.arashnm80.ir` is this same `site/` folder, served by nginx on this machine. TLS on the origin is the existing wildcard certificate `/etc/nginx/ssl/arashnm80.ir/`. Nginx cannot read `/root`, so the published files live at `/var/www/teacher.arashnm80.ir`. Do not point the site at a CDN.
15. **Class notes live in `semester/`.** Four periods, all on one day. The first three follow the book. The fourth is mostly outside it: psychology, communication, soft skills, career, and things like the trust game. What already happened is in `semester/week-01.md` and the files after it. That folder is for the teacher, not a student page.

## Check before calling it done

- Open `site/index.html` from disk, not from a server, and click through a lesson, a figure, and the language switch.
- Generated HTML must not load a stylesheet or script from `http://` or `https://`.
- A figure that is missing on disk is a failed build.

## Known limits of version 1

- Some two-column tables in the PDF were read in a mixed order. The figure image is the reliable copy of those pages.
- Code samples that the book printed as screenshots are images, not retyped source.
- URLs in the references chapter are real links. They need internet only if someone clicks them. The page itself must still render offline.

## الزامات — نسخه فارسی

این‌ها را در تغییرهای بعدی نگه دارید. آزمون واقعی، کپی کردن پوشه در رایانه کلاس است.

1. **بدون اینترنت، حتی با باز کردن مستقیم فایل.** کل پوشه `site/` را کپی کنید و `index.html` را با دوبار کلیک باز کنید. سرور و اینترنت لازم نیست.
2. **پوشه `site/` خودش کامل است.** صفحه، سبک، اسکریپت و تصویرها داخل همان پوشه باشند. پیوند به بیرون پوشه یا میانبر (symlink) بعد از کپی در ویندوز می‌شکند.
3. **هیچ وابستگی دوری نباشد.** نه CDN، نه فونت گوگل، نه `fetch`. فونت همان قلم‌های موجود ویندوز مدرسه است (`Tahoma` و `Segoe UI`).
4. **هر دو زبان، کل صفحه هستند و داخل همان فایل HTML قرار دارند.** فارسی رونویسی کتاب است. انگلیسی رونویسی کامل همان بخش است. کد و تصویرها در هر دو یکی‌اند. دکمه زبان فقط نشان دادن و پنهان کردن است و چیزی از شبکه نمی‌گیرد.
5. **دکمه زبان یکی است.** با کلیک روی هر جای دکمه فا / EN زبان عوض می‌شود، حتی روی سمتی که از قبل انتخاب شده به نظر می‌رسد.
6. **بخش‌ها بر اساس موضوع کوتاه شده‌اند، نه به اندازه کل پودمان.** نقشه در `outline.py` است. هر بخش باید در یک نشست خوانده شود. در عرض کمتر از ۷۰۰ پیکسل (گوشی، یا رایانه‌ای که بزرگ‌نمایی ویندوز یا مرورگر عرضش را کم کرده) فهرست درس‌ها جمع می‌شود و دکمه «فهرست درس‌ها» در گوشه صفحه بازشو می‌ماند تا فهرست به‌صورت منوی بازشو باز شود؛ جای فهرست هیچ‌وقت خالی و بی‌دلیل نمی‌ماند.
7. **سطرهای مخلوط فارسی و انگلیسی باید درست خوانده شوند.** کد همیشه چپ‌به‌راست است. واژه انگلیسی داخل جمله فارسی جدا می‌ماند.
8. **تمرین و پیوند مفید اضافه بر کتاب‌اند و رنگ زمینه دیگری دارند** (قاب سبز بعد از درس). متن خود کتاب روی زمینه سفید می‌ماند. صفحه فهرست تمرین ندارد. صفحه‌های ارزشیابی (جدول نمره و شایستگی) روی سایت نیستند؛ اگر درسی به آن جدول برسد، همان‌جا قطع می‌شود. قاب‌های خود کتاب (کنجکاوی / پروژه / نکته / فعالیت) هم هر کدام رنگ زمینه خودشان را دارند.
9. **دانلود کل سایت** هم در صفحه اول و هم در بالای هر صفحه است. فایل `grade11-offline.zip` است. بعد از باز کردن، پوشه `grade11-site` و فایل `index.html` است. خود فایل فشرده داخل آرشیو نیست. صفحه برای دیده شدن نباید به فونت گوگل یا CDN وصل باشد. اگر نام سایت از کلادفلر (ابر نارنجی) رد شود، خیلی از شبکه‌های ایران بدون فیلترشکن آن را باز نمی‌کنند. مبدأ همین سرور با نشانی `65.109.200.45` است.
10. **بدون جاوااسکریپت هم بتوان درس فارسی را خواند.** زبان و جستجو با جاوااسکریپت کار می‌کنند.
11. **بعد از هر به‌روزرسانی محتوا** از پوشه `11th-grade/` دستور `python3 build_site.py` و سپس `bash deploy.sh` را اجرا کنید. کار وقتی تمام است که نسخه جدید روی سایت عمومی باشد. انگلیسی هر بخش در `sections/en/` است و اگر برش فارسی عوض شد باید همان را هم به‌روز کنید.
12. **نسخه عمومی** روی `https://teacher.arashnm80.ir` است. nginx فایل‌ها را از `/var/www/teacher.arashnm80.ir` می‌خواند، چون به پوشه `/root` دسترسی ندارد.
13. **صفحه «پیوندهای مفید»** جدا از متن کتاب است و در طول ترم بیشتر می‌شود. با `links_html()` ساخته می‌شود. تصویر بندانگشتی ویدیوها در `extra-images/` است و هنگام ساخت به `site/images` کپی می‌شود تا صفحه آفلاین هم باز شود؛ خود پیوندها فقط هنگام کلیک اینترنت می‌خواهند. از همین صفحه `teacher-playground-offline.zip` (تمرین آفلاین پایتون پودمان ۱ — بعد از باز کردن `شروع.bat`؛ سورس [arashnm80/teacher-playground](https://github.com/arashnm80/teacher-playground)) و `evolution-of-trust-offline.zip` هم دانلود می‌شود. هر دو در `extras/` هستند و هنگام ساخت به `site/` کپی می‌شوند.
14. **یادداشت کلاس در پوشه `semester/` است.** هر هفته چهار زنگ در یک روز است. سه زنگ اول کتاب است و زنگ چهارم بیشتر بیرون از کتاب (روان‌شناسی، ارتباط، مهارت نرم، مسیر شغلی). اتفاق‌های هر هفته در `semester/week-01.md` و فایل‌های بعدی است. این پوشه صفحه دانش‌آموز نیست.
