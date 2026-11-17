"""Check that a plain second visit (no hard reload) loads a changed script.
Needs the test servers (restart_judge.sh, restart_server.sh) and Playwright. It edits js/ai.js
temporarily and rebuilds the site, then restores both. Run from anywhere."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "accounts-server"))
from playwright.sync_api import sync_playwright
import json, urllib.request, http.cookiejar
BASE="http://127.0.0.1:8800"
jar=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
body=json.dumps({"phone":"09123456789","nationalCode":"0499370899","classCode":"201","fullName":"علی احمدی","password":"abc12345"}).encode()
try: op.open(urllib.request.Request(BASE+"/api/student/register",data=body,headers={"Content-Type":"application/json"}))
except Exception: op.open(urllib.request.Request(BASE+"/api/student/login",data=json.dumps({"phone":"09123456789","password":"abc12345"}).encode(),headers={"Content-Type":"application/json"}))
cookies=[{"name":c.name,"value":c.value,"url":BASE} for c in jar]
AI=os.path.join(HERE, "playground/app/js/ai.js")
def build(): subprocess.run(["python3",os.path.join(HERE,"build_site.py")],capture_output=True,cwd=HERE)
orig=open(AI,encoding="utf-8").read()
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(); ctx.add_cookies(cookies); page=ctx.new_page()
    page.goto(BASE+"/playground/",wait_until="domcontentloaded"); page.wait_for_selector(".problem-link",timeout=60000)
    print("first visit marker:", page.evaluate("window.__marker||null"))
    try:
        open(AI,"w",encoding="utf-8").write(orig+"\nwindow.__marker = 'new-build';\n"); build()
        page.goto(BASE+"/playground/",wait_until="domcontentloaded"); page.wait_for_selector(".problem-link",timeout=60000)
        print("plain second visit (no hard reload) marker:", page.evaluate("window.__marker||null"))
    finally:
        open(AI,"w",encoding="utf-8").write(orig); build()
    b.close()
