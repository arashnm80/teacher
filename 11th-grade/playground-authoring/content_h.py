"""Batch h: NEW problems p76–p88 — if/else examples and basic functions."""


def out(*lines):
    """Expected stdout: every value on its own line."""
    return "".join(f"{x}\n" for x in lines)


ITEMS = {}

ITEMS["p76"] = dict(
    number=0, topic="شرط‌ها", conceptId="if-else", difficulty=1, mode="stdio",
    title="مثبت، منفی یا صفر", constraints=None,
    statement=(
        "یک عدد صحیح `n` بخوانید.\n\n"
        "اگر `n` مثبت بود کلمه `positive`، اگر منفی بود `negative` و اگر صفر بود `zero` را چاپ کنید."
    ),
    starter="",
    hints=[
        "اول بررسی کنید `n` بزرگ‌تر از صفر است یا نه.",
        "با `elif` می‌توانید حالت منفی را بعد از مثبت بنویسید.",
    ],
    tests=[
        {"stdin": "5\n", "stdout": out("positive")},
        {"stdin": "-3\n", "stdout": out("negative")},
        {"stdin": "0\n", "stdout": out("zero")},
    ],
    guideTitle="مثبت، منفی یا صفر — if و elif",
    mistakes=["فراموش کردن حالت صفر: عدد صفر هیچ چاپی نمی‌دهد."],
    solutions=[
        dict(
            name="روش ۱: if و elif و else",
            steps=[
                "عدد را می‌خوانیم و به عدد تبدیل می‌کنیم.",
                "اگر بزرگ‌تر از صفر بود، `positive` را چاپ می‌کنیم.",
                "اگر کوچک‌تر از صفر بود، `negative` و در غیر این صورت `zero` را چاپ می‌کنیم.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# اگر n مثبت است
if n > 0:
    print("positive")
# اگر n منفی است
elif n < 0:
    print("negative")
# در غیر این صورت n صفر است
else:
    print("zero")
''',
            explain=[
                "شرط‌ها به ترتیب بررسی می‌شوند. اگر هیچ‌کدام درست نبود، بخش `else` اجرا می‌شود و چون عدد نه مثبت است و نه منفی، پس صفر است.",
            ],
        ),
        dict(
            name="روش ۲: سه if جدا",
            steps=[
                "عدد را می‌خوانیم.",
                "هر سه حالت را جدا بررسی می‌کنیم؛ فقط یکی از آن‌ها درست است.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# بررسی مثبت بودن
if n > 0:
    print("positive")

# بررسی منفی بودن
if n < 0:
    print("negative")

# بررسی صفر بودن
if n == 0:
    print("zero")
''',
            explain=[
                "در این روش سه شرط مستقل نوشته‌ایم. چون فقط یکی از آن‌ها برای هر عدد درست است، خروجی یک خط بیشتر ندارد.",
            ],
        ),
    ],
)

ITEMS["p77"] = dict(
    number=0, topic="شرط‌ها", conceptId="if-else", difficulty=1, mode="stdio",
    title="بزرگ‌ترین از دو عدد", constraints=None,
    statement=(
        "دو عدد صحیح `a` و `b` را هر کدام در یک خط بخوانید.\n\n"
        "**عدد بزرگ‌تر** را چاپ کنید. اگر دو عدد برابر بودند، همان عدد را چاپ کنید."
    ),
    starter="",
    hints=[
        "مقایسه‌ی `a > b` را با `if` بنویسید.",
        "برای حالت برابر بودن، هر کدام از دو عدد همان جواب است.",
    ],
    tests=[
        {"stdin": "3\n7\n", "stdout": out(7)},
        {"stdin": "9\n2\n", "stdout": out(9)},
        {"stdin": "4\n4\n", "stdout": out(4)},
    ],
    guideTitle="بزرگ‌ترین از دو عدد — if",
    mistakes=["استفاده از `>=` بدون نیاز: خروجی حالت برابر فرقی ندارد، اما منطق را سخت‌تر می‌کند."],
    solutions=[
        dict(
            name="روش ۱: if و else",
            steps=[
                "دو عدد را می‌خوانیم.",
                "اگر `a` بزرگ‌تر بود، `a` را چاپ می‌کنیم؛ وگرنه `b` را چاپ می‌کنیم.",
            ],
            code='''# دو عدد ورودی را می‌خوانیم
a = int(input())
b = int(input())

# اگر a بزرگ‌تر بود
if a > b:
    print(a)
# در غیر این صورت b بزرگ‌تر یا برابر است
else:
    print(b)
''',
            explain=[
                "اگر `a` بزرگ‌تر باشد همان را چاپ می‌کنیم. در غیر این صورت `b` بزرگ‌تر است یا با `a` برابر است؛ در هر دو حالت `b` جواب درست است.",
            ],
        ),
        dict(
            name="روش ۲: با یک متغیر کمکی",
            steps=[
                "فرض می‌کنیم `a` بزرگ‌ترین است.",
                "اگر `b` از آن بزرگ‌تر بود، متغیر را به `b` تغییر می‌دهیم.",
                "در پایان متغیر را چاپ می‌کنیم.",
            ],
            code='''# دو عدد ورودی را می‌خوانیم
a = int(input())
b = int(input())

# فرض اولیه: a بزرگ‌ترین است
biggest = a
# اگر b از آن بزرگ‌تر بود، بزرگ‌ترین را عوض می‌کنیم
if b > biggest:
    biggest = b

# بزرگ‌ترین را چاپ می‌کنیم
print(biggest)
''',
            explain=[
                "با یک متغیر کمکی همان نتیجه را می‌گیریم. این الگو را بعداً برای پیدا کردن بزرگ‌ترین در یک لیست هم به کار می‌بریم.",
            ],
        ),
    ],
)

ITEMS["p78"] = dict(
    number=0, topic="شرط‌ها", conceptId="if-else", difficulty=1, mode="stdio",
    title="قدرمطلق بدون abs", constraints={"forbid": ["abs"]},
    statement=(
        "یک عدد صحیح `n` بخوانید و **قدرمطلق** آن را چاپ کنید.\n\n"
        "نباید از تابع `abs` استفاده کنید؛ با `if` حساب کنید."
    ),
    starter="",
    hints=[
        "اگر عدد منفی باشد، قدرمطلقش همان عدد ضربدر منفی یک است.",
        "اگر عدد مثبت یا صفر باشد، همان عدد جواب است.",
    ],
    tests=[
        {"stdin": "5\n", "stdout": out(5)},
        {"stdin": "-7\n", "stdout": out(7)},
        {"stdin": "0\n", "stdout": out(0)},
    ],
    guideTitle="قدرمطلق با if",
    mistakes=["نوشتن `abs(n)`: این مسئله آن را ممنوع کرده است."],
    solutions=[
        dict(
            name="روش ۱: اگر منفی بود، برعکسش",
            steps=[
                "عدد را می‌خوانیم.",
                "اگر کمتر از صفر بود، آن را با `-n` چاپ می‌کنیم.",
                "وگرنه همان عدد را چاپ می‌کنیم.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# اگر n منفی است
if n < 0:
    # قدرمطلق آن برابر منفی n است
    print(-n)
# در غیر این صورت n مثبت یا صفر است
else:
    print(n)
''',
            explain=[
                "منفی یک عدد منفی، عدد مثبت می‌شود. پس برای عدد منفی `-n` را چاپ می‌کنیم و برای بقیه خود `n` را.",
            ],
        ),
        dict(
            name="روش ۲: مقایسه با صفر",
            steps=[
                "عدد را می‌خوانیم.",
                "اگر بزرگ‌تر یا برابر صفر بود، همان را چاپ می‌کنیم؛ وگرنه `0 - n`.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# اگر n نامنفی است، همان جواب است
if n >= 0:
    print(n)
# در غیر این صورت قدرمطلق برابر صفر منهای n است
else:
    print(0 - n)
''',
            explain=[
                "صفر منهای یک عدد منفی، همان عدد مثبت است. این روش هم دقیقاً همان قدرمطلق را می‌دهد.",
            ],
        ),
    ],
)

ITEMS["p79"] = dict(
    number=0, topic="شرط‌ها", conceptId="if-else", difficulty=1, mode="stdio",
    title="قبول یا مردود", constraints=None,
    statement=(
        "یک نمره‌ی صحیح بین ۰ و ۲۰ بخوانید.\n\n"
        "اگر نمره **۱۰ یا بیشتر** بود کلمه `pass` و در غیر این صورت `fail` را چاپ کنید."
    ),
    starter="",
    hints=[
        "شرط قبولی یعنی نمره بزرگ‌تر یا برابر ۱۰ باشد.",
        "اگر نمره کمتر از ۱۰ بود، بخش `else` جواب مردودی است.",
    ],
    tests=[
        {"stdin": "10\n", "stdout": out("pass")},
        {"stdin": "9\n", "stdout": out("fail")},
        {"stdin": "20\n", "stdout": out("pass")},
        {"stdin": "0\n", "stdout": out("fail")},
    ],
    guideTitle="قبول یا مردود — if و else",
    mistakes=["نوشتن `score > 10`: نمره‌ی ۱۰ قبول است و باید `pass` شود."],
    solutions=[
        dict(
            name="روش ۱: if و else",
            steps=[
                "نمره را می‌خوانیم.",
                "اگر بزرگ‌تر یا برابر ۱۰ بود `pass` و در غیر این صورت `fail` را چاپ می‌کنیم.",
            ],
            code='''# نمره را از ورودی می‌خوانیم
score = int(input())

# اگر نمره به ۱۰ رسید یا از آن گذشت
if score >= 10:
    print("pass")
# در غیر این صورت مردود است
else:
    print("fail")
''',
            explain=[
                "شرط `score >= 10` دقیقاً مرز قبولی را می‌گیرد؛ یعنی ۱۰ هم قبول است.",
            ],
        ),
        dict(
            name="روش ۲: متغیر جواب",
            steps=[
                "جواب را ابتدا `fail` می‌گذاریم.",
                "اگر نمره کافی بود، جواب را `pass` می‌کنیم.",
                "در پایان جواب را چاپ می‌کنیم.",
            ],
            code='''# نمره را از ورودی می‌خوانیم
score = int(input())

# فرض اولیه: مردود
result = "fail"
# اگر نمره به ۱۰ رسید، قبول است
if score >= 10:
    result = "pass"

# نتیجه را چاپ می‌کنیم
print(result)
''',
            explain=[
                "همان منطق با یک متغیر کمکی. فقط یک بار `print` داریم که آسان‌تر خوانده می‌شود.",
            ],
        ),
    ],
)

ITEMS["p80"] = dict(
    number=0, topic="شرط‌ها", conceptId="if-else", difficulty=1, mode="stdio",
    title="بخش‌پذیر بر ۳؟", constraints=None,
    statement=(
        "یک عدد صحیح `n` بخوانید.\n\n"
        "اگر `n` بر ۳ بخش‌پذیر بود `yes` و در غیر این صورت `no` را چاپ کنید. "
        "(عدد صفر بر ۳ بخش‌پذیر است.)"
    ),
    starter="",
    hints=[
        "عدد بر ۳ بخش‌پذیر است اگر باقی‌مانده‌ی `n % 3` صفر باشد.",
        "شرط را با `==` بسنجید.",
    ],
    tests=[
        {"stdin": "9\n", "stdout": out("yes")},
        {"stdin": "10\n", "stdout": out("no")},
        {"stdin": "0\n", "stdout": out("yes")},
        {"stdin": "-3\n", "stdout": out("yes")},
    ],
    guideTitle="بخش‌پذیری با %",
    mistakes=["نوشتن `n / 3 == 0`: تقسیم عددهای اعشاری نتیجه‌ی دیگری می‌دهد؛ باید باقی‌مانده را بسنجیم."],
    solutions=[
        dict(
            name="روش ۱: باقی‌مانده مساوی صفر",
            steps=[
                "عدد را می‌خوانیم.",
                "اگر `n % 3` برابر صفر بود `yes` و وگرنه `no` را چاپ می‌کنیم.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# اگر باقی‌مانده‌ی تقسیم بر ۳ صفر است
if n % 3 == 0:
    print("yes")
# در غیر این صورت بخش‌پذیر نیست
else:
    print("no")
''',
            explain=[
                "`n % 3` باقی‌مانده‌ی تقسیم `n` بر ۳ است. وقتی صفر باشد، یعنی عدد بر ۳ بخش‌پذیر است. این روش برای عددهای منفی هم درست کار می‌کند.",
            ],
        ),
        dict(
            name="روش ۲: ذخیره‌ی باقی‌مانده",
            steps=[
                "باقی‌مانده را در متغیر `r` می‌ریزیم.",
                "اگر `r` صفر بود `yes` و وگرنه `no` را چاپ می‌کنیم.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# باقی‌مانده‌ی تقسیم بر ۳ را حساب می‌کنیم
r = n % 3

# اگر باقی‌مانده صفر بود، بخش‌پذیر است
if r == 0:
    print("yes")
# در غیر این صورت نیست
else:
    print("no")
''',
            explain=[
                "این روش همان کار را با یک متغیر کمکی انجام می‌دهد تا منطق روشن‌تر دیده شود.",
            ],
        ),
    ],
)

ITEMS["p81"] = dict(
    number=0, topic="شرط‌ها", conceptId="if-else", difficulty=1, mode="stdio",
    title="بین ۱۰ و ۲۰ (شامل هر دو)", constraints={"require": ["and"]},
    statement=(
        "یک عدد صحیح `n` بخوانید.\n\n"
        "اگر `n` **بین ۱۰ و ۲۰** بود، شامل خود ۱۰ و ۲۰، کلمه `yes` و در غیر این صورت `no` را چاپ کنید. "
        "برای این کار از **and** استفاده کنید."
    ),
    starter="",
    hints=[
        "دو شرط را با `and` کنار هم بگذارید: `n` بزرگ‌تر یا برابر ۱۰ و کوچک‌تر یا برابر ۲۰ باشد.",
        "مرزهای ۱۰ و ۲۰ هم قبول هستند.",
    ],
    tests=[
        {"stdin": "15\n", "stdout": out("yes")},
        {"stdin": "10\n", "stdout": out("yes")},
        {"stdin": "20\n", "stdout": out("yes")},
        {"stdin": "9\n", "stdout": out("no")},
        {"stdin": "21\n", "stdout": out("no")},
    ],
    guideTitle="بازه‌ی عددها با and",
    mistakes=["استفاده از `or`: هیچ عددی همزمان کوچک‌تر از ۱۰ و بزرگ‌تر از ۲۰ نیست؛ شرط باید `and` باشد."],
    solutions=[
        dict(
            name="روش ۱: یک if با and",
            steps=[
                "عدد را می‌خوانیم.",
                "شرط `n >= 10 and n <= 20` را می‌سنجیم.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# اگر n هم بزرگ‌تر یا برابر ۱۰ است و هم کوچک‌تر یا برابر ۲۰
if n >= 10 and n <= 20:
    print("yes")
# در غیر این صورت بیرون بازه است
else:
    print("no")
''',
            explain=[
                "`and` یعنی هر دو شرط باید درست باشند. اگر یکی از آن‌ها غلط باشد، عدد بیرون بازه است.",
            ],
        ),
        dict(
            name="روش ۲: متغیر شرط",
            steps=[
                "شرط را در متغیر `inside` می‌گذاریم.",
                "اگر `inside` درست بود `yes` و وگرنه `no` را چاپ می‌کنیم.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# شرط بازه را در یک متغیر می‌ریزیم
inside = n >= 10 and n <= 20

# بر اساس نتیجه، جواب را چاپ می‌کنیم
if inside:
    print("yes")
else:
    print("no")
''',
            explain=[
                "نتیجه‌ی مقایسه‌ی `and` هم یک مقدار درست یا غلط است. می‌توانیم آن را در متغیر بریزیم و بعد بررسی کنیم.",
            ],
        ),
    ],
)

ITEMS["p82"] = dict(
    number=0, topic="شرط‌ها", conceptId="if-else", difficulty=2, mode="stdio",
    title="نام روز هفته با elif", constraints={"require": ["elif"]},
    statement=(
        "یک عدد `n` بخوانید. اگر `n` از ۱ تا ۷ بود، نام روز را به انگلیسی چاپ کنید:\n\n"
        "- ۱ ← `Saturday`\n"
        "- ۲ ← `Sunday`\n"
        "- ۳ ← `Monday`\n"
        "- ۴ ← `Tuesday`\n"
        "- ۵ ← `Wednesday`\n"
        "- ۶ ← `Thursday`\n"
        "- ۷ ← `Friday`\n\n"
        "برای هر عدد دیگری کلمه `invalid` را چاپ کنید. برای این کار **elif** لازم است."
    ),
    starter="",
    hints=[
        "هر حالت را یک `elif` جدا بنویسید؛ ترتیب شرط‌ها مهم نیست ولی هر عدد فقط یک شرط را برآورده می‌کند.",
        "حالت‌های خارج از ۱ تا ۷ را در `else` بگذارید.",
    ],
    tests=[
        {"stdin": "1\n", "stdout": out("Saturday")},
        {"stdin": "4\n", "stdout": out("Tuesday")},
        {"stdin": "7\n", "stdout": out("Friday")},
        {"stdin": "8\n", "stdout": out("invalid")},
        {"stdin": "0\n", "stdout": out("invalid")},
    ],
    guideTitle="نام روز با if و elif",
    mistakes=["نوشتن `if` برای همه‌ی حالت‌ها: همه‌ی شرط‌ها بررسی می‌شوند و ممکن است چند چاپ شود."],
    solutions=[
        dict(
            name="روش ۱: زنجیره‌ی if و elif",
            steps=[
                "عدد را می‌خوانیم.",
                "با `if` و `elif` هر عدد را به یک نام روز وصل می‌کنیم.",
                "در `else` کلمه‌ی `invalid` را چاپ می‌کنیم.",
            ],
            code='''# عدد n را از ورودی می‌خوانیم
n = int(input())

# هر عدد به یک روز هفته وصل است
if n == 1:
    print("Saturday")
elif n == 2:
    print("Sunday")
elif n == 3:
    print("Monday")
elif n == 4:
    print("Tuesday")
elif n == 5:
    print("Wednesday")
elif n == 6:
    print("Thursday")
elif n == 7:
    print("Friday")
# هر عدد دیگری معتبر نیست
else:
    print("invalid")
''',
            explain=[
                "`elif` یعنی اگر شرط قبلی درست نبود، این شرط بررسی شود. از بالا به پایین بررسی می‌شود و اولین شرط درست اجرا می‌شود؛ بقیه کنار گذاشته می‌شوند.",
            ],
        ),
    ],
)

ITEMS["p83"] = dict(
    number=0, topic="توابع", conceptId="functions", difficulty=1, mode="function",
    functionName="square", constraints=None,
    title="تابع مربع",
    statement=(
        "تابعی به نام `square(x)` بنویسید که **مربع** عدد `x` را با `return` برگرداند.\n\n"
        "این مسئله **آزمون تابع** است: فقط تابع را بنویسید؛ نیازی به `input` یا `print` نیست."
    ),
    starter="def square(x):\n    pass\n",
    hints=[
        "مربع یک عدد، همان عدد ضربدر خودش است.",
        "با `return` مقدار را برگردانید؛ `print` جواب تابع را نمی‌دهد.",
    ],
    tests=[
        {"call": {"args": [3], "expected": 9}},
        {"call": {"args": [0], "expected": 0}},
        {"call": {"args": [-4], "expected": 16}},
        {"call": {"args": [2.5], "expected": 6.25}},
    ],
    guideTitle="تابع مربع — return",
    mistakes=["استفاده از `print` به‌جای `return`: تابع مقداری برنمی‌گرداند."],
    solutions=[
        dict(
            name="روش ۱: ضرب در خودش",
            steps=[
                "پارامتر `x` را می‌گیریم.",
                "`x * x` را با `return` برمی‌گردانیم.",
            ],
            code='''# مربع x را محاسبه و برمی‌گردانیم
def square(x):
    # x را در خودش ضرب می‌کنیم
    return x * x
''',
            explain=[
                "تابع ورودی را می‌گیرد، حساب را انجام می‌دهد و با `return` جواب را بیرون می‌فرستد.",
            ],
        ),
        dict(
            name="روش ۲: توان دو",
            steps=[
                "پارامتر `x` را می‌گیریم.",
                "با `**` توان ۲ را حساب و برمی‌گردانیم.",
            ],
            code='''# مربع x را با توان دو حساب می‌کنیم
def square(x):
    # x به توان ۲ می‌رسد
    return x ** 2
''',
            explain=[
                "عملگر `**` توان می‌دهد. `x ** 2` همان مربع است.",
            ],
        ),
    ],
)

ITEMS["p84"] = dict(
    number=0, topic="توابع", conceptId="functions", difficulty=1, mode="function",
    functionName="add", constraints=None,
    title="تابع جمع دو عدد",
    statement=(
        "تابعی به نام `add(a, b)` بنویسید که **حاصل جمع** دو عدد را با `return` برگرداند.\n\n"
        "این مسئله **آزمون تابع** است."
    ),
    starter="def add(a, b):\n    pass\n",
    hints=[
        "دو پارامتر را با `+` جمع کنید.",
        "نتیجه را با `return` بدهید.",
    ],
    tests=[
        {"call": {"args": [2, 3], "expected": 5}},
        {"call": {"args": [-1, 1], "expected": 0}},
        {"call": {"args": [0, 0], "expected": 0}},
        {"call": {"args": [2.5, 0.5], "expected": 3.0}},
    ],
    guideTitle="تابع جمع — پارامترها",
    mistakes=["نوشتن `return a - b` به‌جای جمع."],
    solutions=[
        dict(
            name="روش ۱: یک خط return",
            steps=[
                "دو پارامتر `a` و `b` را می‌گیریم.",
                "`a + b` را برمی‌گردانیم.",
            ],
            code='''# جمع دو عدد را برمی‌گرداند
def add(a, b):
    # حاصل جمع را بیرون می‌فرستیم
    return a + b
''',
            explain=[
                "تابع دو ورودی را می‌گیرد و جمع آن‌ها را با `return` می‌دهد.",
            ],
        ),
        dict(
            name="روش ۲: با متغیر میانی",
            steps=[
                "جمع را در متغیر `total` می‌ریزیم.",
                "`total` را برمی‌گردانیم.",
            ],
            code='''# جمع دو عدد را برمی‌گرداند
def add(a, b):
    # جمع را در متغیر total می‌ریزیم
    total = a + b
    # و آن را برمی‌گردانیم
    return total
''',
            explain=[
                "همان جواب، با یک مرحله‌ی میانی. این شکل برای خواندن بعدی آسان‌تر است.",
            ],
        ),
    ],
)

ITEMS["p85"] = dict(
    number=0, topic="توابع", conceptId="functions", difficulty=1, mode="function",
    functionName="is_even", constraints=None,
    title="تابع زوج بودن",
    statement=(
        "تابعی به نام `is_even(n)` بنویسید که اگر `n` زوج بود `True` و در غیر این صورت `False` برگرداند.\n\n"
        "این مسئله **آزمون تابع** است."
    ),
    starter="def is_even(n):\n    pass\n",
    hints=[
        "عدد زوج است اگر باقی‌مانده‌ی `n % 2` صفر باشد.",
        "نتیجه‌ی مقایسه‌ی `==` خودش `True` یا `False` است.",
    ],
    tests=[
        {"call": {"args": [4], "expected": True}},
        {"call": {"args": [7], "expected": False}},
        {"call": {"args": [0], "expected": True}},
        {"call": {"args": [-2], "expected": True}},
    ],
    guideTitle="تابع زوج بودن با %",
    mistakes=["برگرداندن `\"True\"` به‌صورت متن به‌جای `True`."],
    solutions=[
        dict(
            name="روش ۱: if و return",
            steps=[
                "باقی‌مانده‌ی `n % 2` را بررسی می‌کنیم.",
                "اگر صفر بود `True` و وگرنه `False` را برمی‌گردانیم.",
            ],
            code='''# بررسی زوج بودن n
def is_even(n):
    # اگر باقی‌مانده‌ی تقسیم بر ۲ صفر است
    if n % 2 == 0:
        # عدد زوج است
        return True
    # در غیر این صورت فرد است
    return False
''',
            explain=[
                "با `if` دو حالت را جدا جواب داده‌ایم. هر کدام با `return` تمام می‌شود.",
            ],
        ),
        dict(
            name="روش ۲: برگرداندن نتیجه‌ی مقایسه",
            steps=[
                "مقایسه‌ی `n % 2 == 0` را انجام می‌دهیم.",
                "همان نتیجه را برمی‌گردانیم.",
            ],
            code='''# بررسی زوج بودن n
def is_even(n):
    # نتیجه‌ی مقایسه خودش True یا False است
    return n % 2 == 0
''',
            explain=[
                "مقایسه یک مقدار درست یا غلط می‌دهد. پس می‌توانیم همان را مستقیم برگردانیم.",
            ],
        ),
    ],
)

ITEMS["p86"] = dict(
    number=0, topic="توابع", conceptId="functions", difficulty=1, mode="function",
    functionName="sign", constraints=None,
    title="تابع علامت عدد",
    statement=(
        "تابعی به نام `sign(n)` بنویسید که اگر `n` مثبت بود `\"positive\"`، اگر منفی بود `\"negative\"` "
        "و اگر صفر بود `\"zero\"` برگرداند.\n\n"
        "این مسئله **آزمون تابع** است."
    ),
    starter="def sign(n):\n    pass\n",
    hints=[
        "سه حالت را با `if`، `elif` و `else` جدا کنید.",
        "هر حالت باید با `return` متن مناسب را برگرداند.",
    ],
    tests=[
        {"call": {"args": [5], "expected": "positive"}},
        {"call": {"args": [-5], "expected": "negative"}},
        {"call": {"args": [0], "expected": "zero"}},
    ],
    guideTitle="تابع علامت عدد — if و return",
    mistakes=["استفاده از `print` به‌جای `return`: تابع مقداری برنمی‌گرداند."],
    solutions=[
        dict(
            name="روش ۱: if و elif و else",
            steps=[
                "اگر `n` بزرگ‌تر از صفر بود، `positive` را برمی‌گردانیم.",
                "اگر کوچک‌تر از صفر بود، `negative` و در غیر این صورت `zero` را برمی‌گردانیم.",
            ],
            code='''# علامت n را به‌صورت متن برمی‌گرداند
def sign(n):
    # اگر n مثبت است
    if n > 0:
        return "positive"
    # اگر n منفی است
    elif n < 0:
        return "negative"
    # در غیر این صورت صفر است
    else:
        return "zero"
''',
            explain=[
                "هر شاخه با `return` جواب را بیرون می‌دهد. با رسیدن به اولین `return` تابع تمام می‌شود.",
            ],
        ),
        dict(
            name="روش ۲: return‌های جدا",
            steps=[
                "اول حالت مثبت را بررسی می‌کنیم و در صورت درست بودن برمی‌گردانیم.",
                "بعد حالت منفی و در پایان صفر را برمی‌گردانیم.",
            ],
            code='''# علامت n را به‌صورت متن برمی‌گرداند
def sign(n):
    # اگر مثبت بود، همین‌جا جواب می‌دهیم
    if n > 0:
        return "positive"
    # اگر منفی بود، همین‌جا جواب می‌دهیم
    if n < 0:
        return "negative"
    # به اینجا که رسیدیم n صفر است
    return "zero"
''',
            explain=[
                "چون `return` تابع را تمام می‌کند، نیازی به `else` نیست: اگر به خط آخر رسیدیم، حالت‌های قبلی درست نبوده‌اند.",
            ],
        ),
    ],
)

ITEMS["p87"] = dict(
    number=0, topic="رشته‌ها", conceptId="strings", difficulty=1, mode="function",
    functionName="word_length", constraints=None,
    title="تابع طول رشته",
    statement=(
        "تابعی به نام `word_length(text)` بنویسید که **تعداد حرف‌های** رشته‌ی `text` را برگرداند "
        "(فاصله‌ها هم شمرده می‌شوند).\n\n"
        "این مسئله **آزمون تابع** است."
    ),
    starter="def word_length(text):\n    pass\n",
    hints=[
        "تابع `len` طول یک رشته را می‌دهد.",
        "اگر بخواهید بدون `len` حساب کنید، روی رشته با `for` بچرخید و بشمارید.",
    ],
    tests=[
        {"call": {"args": ["python"], "expected": 6}},
        {"call": {"args": [""], "expected": 0}},
        {"call": {"args": ["a b"], "expected": 3}},
        {"call": {"args": ["سلام"], "expected": 4}},
    ],
    guideTitle="طول رشته — len",
    mistakes=["شمردن فاصله‌ها نادیده گرفته شود: طول `a b` سه است، نه دو."],
    solutions=[
        dict(
            name="روش ۱: تابع len",
            steps=[
                "رشته را به `len` می‌دهیم.",
                "نتیجه را برمی‌گردانیم.",
            ],
            code='''# طول رشته را برمی‌گرداند
def word_length(text):
    # len تعداد حرف‌های رشته را می‌دهد
    return len(text)
''',
            explain=[
                "`len` تعداد عضوهای یک رشته را می‌شمارد. هر حرف، از جمله فاصله، یک عضو است.",
            ],
        ),
        dict(
            name="روش ۲: شمردن با for",
            steps=[
                "شمارنده را از صفر شروع می‌کنیم.",
                "به ازای هر حرف، شمارنده را یکی زیاد می‌کنیم.",
                "شمارنده را برمی‌گردانیم.",
            ],
            code='''# طول رشته را با شمردن حرف‌ها به دست می‌آورد
def word_length(text):
    # شمارنده از صفر شروع می‌شود
    count = 0
    # به ازای هر حرف یکی اضافه می‌کنیم
    for ch in text:
        count = count + 1
    # تعداد حرف‌ها را برمی‌گردانیم
    return count
''',
            explain=[
                "با `for` روی رشته می‌چرخیم و هر حرف را می‌شماریم. نتیجه همان طول است، بدون استفاده از `len`.",
            ],
        ),
    ],
)

ITEMS["p88"] = dict(
    number=0, topic="توابع", conceptId="functions", difficulty=1, mode="function",
    functionName="larger", constraints=None,
    title="تابع بزرگ‌تر از دو عدد",
    statement=(
        "تابعی به نام `larger(a, b)` بنویسید که **عدد بزرگ‌تر** را برگرداند. "
        "اگر برابر بودند، همان عدد را برگردانید.\n\n"
        "این مسئله **آزمون تابع** است."
    ),
    starter="def larger(a, b):\n    pass\n",
    hints=[
        "با `if a > b` بررسی کنید کدام بزرگ‌تر است.",
        "جواب را با `return` برگردانید.",
    ],
    tests=[
        {"call": {"args": [3, 7], "expected": 7}},
        {"call": {"args": [9, 2], "expected": 9}},
        {"call": {"args": [4, 4], "expected": 4}},
    ],
    guideTitle="تابع بزرگ‌تر — if و return",
    mistakes=["فراموش کردن `return` در یکی از شاخه‌ها: تابع `None` برمی‌گرداند."],
    solutions=[
        dict(
            name="روش ۱: if و else با return",
            steps=[
                "اگر `a` بزرگ‌تر بود، `a` را برمی‌گردانیم.",
                "در غیر این صورت `b` را برمی‌گردانیم.",
            ],
            code='''# عدد بزرگ‌تر را برمی‌گرداند
def larger(a, b):
    # اگر a بزرگ‌تر است
    if a > b:
        return a
    # در غیر این صورت b بزرگ‌تر یا برابر است
    else:
        return b
''',
            explain=[
                "اگر `a` بزرگ‌تر بود همان را برمی‌گردانیم. در غیر این صورت `b` جواب است، چه بزرگ‌تر و چه برابر.",
            ],
        ),
        dict(
            name="روش ۲: متغیر بزرگ‌ترین",
            steps=[
                "فرض می‌کنیم `a` بزرگ‌ترین است.",
                "اگر `b` بزرگ‌تر بود، متغیر را به `b` می‌دهیم.",
                "در پایان آن را برمی‌گردانیم.",
            ],
            code='''# عدد بزرگ‌تر را برمی‌گرداند
def larger(a, b):
    # فرض اولیه: a بزرگ‌تر است
    m = a
    # اگر b از m بزرگ‌تر بود، m را عوض می‌کنیم
    if b > m:
        m = b
    # بزرگ‌ترین را برمی‌گردانیم
    return m
''',
            explain=[
                "این الگو را بعداً برای پیدا کردن بزرگ‌ترین عدد در یک فهرست هم به کار می‌بریم.",
            ],
        ),
    ],
)
