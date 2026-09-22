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
7. **Sections follow the topic, not the printed پودمان length.** `outline.py` maps book pages into short sections. A section should be one sitting of reading. Callouts stay with the topic they belong to. The sidebar lists those sections under the module and the unit.
8. **Mixed Persian and English on one line must stay readable.** Persian paragraphs stay right-to-left. English words, code, and parentheses around them are isolated left-to-right. English paragraphs do the reverse for any Persian that remains. Code blocks are always left-to-right.
9. **Exercises and useful links are extra, and they look extra.** Each section ends with tasks that ask the student to build a page or a program, not to memorize or explain a definition. They are not printed book text. They sit in a green panel (`.extra`) after the lesson. Book text stays on the white lesson panel. A link in that panel may point at the public web; the page itself must still render offline. The cover and license pages (شناسنامه و مجوز) are not part of the site.
10. **Offline zip, visible on the site.** The home page and the header both link to `grade11-offline.zip`. The file is the whole site. It unpacks to one folder, `grade11-site/`, and does not contain the zip itself. Students unzip it and open `index.html`. Nginx sends it as a download. Building the site writes this file; `deploy.sh` publishes it with the rest of `site/`.
11. **The pages themselves must not need a VPN.** Every stylesheet, script, font, and image that the page needs comes from this same site. Do not add Google Fonts, a CDN, or any other host required to render the page. Useful links may point outside, and those links need the network only if someone clicks them. The name `teacher.arashnm80.ir` is still a Cloudflare-proxied record unless that record is changed at Cloudflare. Proxied Cloudflare addresses are often blocked on Iranian networks, so the name may fail with no VPN even though the pages have no foreign assets. Direct origin is this machine, `65.109.200.45`, with the existing wildcard certificate. Turning the Cloudflare cloud grey, so the A record is that address, is the DNS change that lets the name open without passing through Cloudflare.
12. **Works with JavaScript off for reading.** Persian navigation and lesson pages must still open. JavaScript is only for the language switch and search.
13. **Rebuild after markdown edits.** Persian comes from `converted-markdown-book/` sliced by `outline.py`. English lives in `sections/en/<id>.md` and must be updated when that slice changes. Exercises for the green panel live in `practical.py`. Run `python3 build_site.py` (needs the `markdown` package) and then `bash deploy.sh` from `11th-grade/`.
14. **Public copy.** `https://teacher.arashnm80.ir` is this same `site/` folder, served by nginx on this machine. TLS on the origin is the existing wildcard certificate `/etc/nginx/ssl/arashnm80.ir/`. Nginx cannot read `/root`, so the published files live at `/var/www/teacher.arashnm80.ir`. Do not point the site at a CDN.

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
6. **بخش‌ها بر اساس موضوع کوتاه شده‌اند، نه به اندازه کل پودمان.** نقشه در `outline.py` است. هر بخش باید در یک نشست خوانده شود.
7. **سطرهای مخلوط فارسی و انگلیسی باید درست خوانده شوند.** کد همیشه چپ‌به‌راست است. واژه انگلیسی داخل جمله فارسی جدا می‌ماند.
8. **تمرین و پیوند مفید اضافه بر کتاب‌اند و رنگ زمینه دیگری دارند** (قاب سبز بعد از درس). متن خود کتاب روی زمینه سفید می‌ماند.
9. **دانلود کل سایت** هم در صفحه اول و هم در بالای هر صفحه است. فایل `grade11-offline.zip` است. بعد از باز کردن، پوشه `grade11-site` و فایل `index.html` است. خود فایل فشرده داخل آرشیو نیست. صفحه برای دیده شدن نباید به فونت گوگل یا CDN وصل باشد. اگر نام سایت از کلادفلر (ابر نارنجی) رد شود، خیلی از شبکه‌های ایران بدون فیلترشکن آن را باز نمی‌کنند. مبدأ همین سرور با نشانی `65.109.200.45` است.
10. **بدون جاوااسکریپت هم بتوان درس فارسی را خواند.** زبان و جستجو با جاوااسکریپت کار می‌کنند.
11. **بعد از ویرایش مارک‌داون** دستور `python3 build_site.py` را اجرا کنید. انگلیسی هر بخش در `sections/en/` است و اگر برش فارسی عوض شد باید همان را هم به‌روز کنید. سپس `bash deploy.sh`.
12. **نسخه عمومی** روی `https://teacher.arashnm80.ir` است. nginx فایل‌ها را از `/var/www/teacher.arashnm80.ir` می‌خواند، چون به پوشه `/root` دسترسی ندارد.
