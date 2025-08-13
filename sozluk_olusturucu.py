# -*- coding: utf-8 -*-
import os
import csv
import json
import unicodedata

#klasor yolu olusturma
base_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(base_dir, "sayfalar")
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

csv_path = os.path.join(base_dir, "veriler.csv")
with open(csv_path, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    all_data = sorted(list(reader), key=lambda x: x[0].lower())

def normalize_word(k):
    # uyumsuz karakterleri duzeltme fonksiyonu
    k = k.split(",")[0].strip()
    return ''.join(c for c in unicodedata.normalize('NFKD', k) if not unicodedata.combining(c)).lower().replace(" ", "_")

# olusturulan sayfaların ortak css dosyası
joint_css = """
<style>
    body {
        font-family: 'Tahoma', "Geneva", sans-serif;
        margin: 0;
        background-color: #f4f4f4;
        color: #222;
        overflow: scroll;
    }

    body::-webkit-scrollbar {
    display: none;
    }
    .navbar {
        background: #203a3d;
        color: white;
        padding: 15px 20px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .navbar .title-text {
        color: #e6e6e6;
        text-transform: capitalize;
        white-space: nowrap;
        font-size: clamp(24px, 4vw, 28px);
        overflow: hidden;
        text-overflow: ellipsis;
        margin: 0;
    }

    .container {
        max-width: 900px;
        margin: 40px auto;
        padding: 30px;
        background: white;
        border-radius: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 0.5); 
    }
    .footer {
        text-align:center;
        padding: 30px 0;
        font-size: 16px;
    }
    .footer a {
        color: #31595E;
        text-decoration: none;
        margin: 0 10px;
    }
</style>
"""

# sözlük sayfalarını oluştur
for data in all_data:
    kurdish, wordtype, turkish, extra = data
    file_name = normalize_word(kurdish)
    file_path = os.path.join(folder_path, f"{file_name}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{kurdish} - Daristana Peyvan</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="manifest" href="manifest.json">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    {joint_css}
    <style>
        h1 {{ font-size: 42px; }}
        .wordtype {{ font-style: italic; color: gray; font-size: 18px; margin-bottom: 20px; }}
        p {{ font-size: 22px; line-height: 1.6em; }}
        .extra {{
            margin-top: 30px;
            font-size: 18px;
            background: #1f3a3d17;
            padding: 15px;
            border-left: 5px solid #1f3a3d;
            border-radius: 24px;
            color: #222;
        }}
        .copy-btn {{
      background: none;
      border: none;
      font-size: 20px;
      cursor: pointer;
      padding: 4px;
      color: #365e58;
    }}

    .copy-btn:hover {{
      color: #203a3d;
    }}

    .title-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    </style>
</head>
<body>
    <div class="navbar">
        <a href="../index.html" style="text-decoration: none; color: #e6e6e6; font-size: 16px; font-weight: bold;">Ana Sayfa</a>
    </div>
    <div class="container">
    <div class="title-bar">
        <h1>{kurdish}</h1>
        <button class="copy-btn" onclick="copyPageUrl()" title="Bağlantıyı Kopyala"><img src="../copy.svg" alt="Kopyala" width="24" height="24"><span class="checkmark" style="display:none;">✅</span></button>
        </div>
        <div class="wordtype">{wordtype}</div>
        <p>{turkish}</p>
        <div class="extra">{extra}</div>
    </div>
    <div class="footer">
        <a href="../hakkinda.html">Hakkında</a> |
        <a href="../iletisim.html">İletişim</a>
    </div>

    <script>
    // kopyalama fonksiyonu
     function copyPageUrl() {{
    const url = window.location.href;
    const checkmark = document.querySelector('.copy-btn .checkmark');
    // tarayıcılar için uyumluluk ve kullanıcı geri bildirimleri
    if (navigator.clipboard && window.isSecureContext) {{
      navigator.clipboard.writeText(url).then(() => {{
        showCheckmark();
      }}).catch(() => {{
        fallbackCopy(url);
        showCheckmark();
      }});
    }} else {{
      fallbackCopy(url);
      showCheckmark();
    }}

    function fallbackCopy(text) {{
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.setAttribute('readonly', '');
      textarea.style.position = 'absolute';
      textarea.style.left = '-9999px';
      document.body.appendChild(textarea);
      textarea.select();
      try {{
        document.execCommand('copy');
      }} catch (e) {{
      }}
      document.body.removeChild(textarea);
    }}

    function showCheckmark() {{
      checkmark.style.display = 'inline';
      setTimeout(() => {{
        checkmark.style.display = 'none';
      }}, 1000);
    }}
  }}

   if ('serviceWorker' in navigator) {{
    navigator.serviceWorker.register('service-worker.js').then(function(registration) {{
      console.log('Service Worker kayıtlı:', registration.scope);
    }}).catch(function(error) {{
      console.log('Service Worker kaydı başarısız:', error);
    }});
  }}
  </script>
</body>
</html>""")

# all_data.js oluştur (sözlük verilerini aramada kullanmak için)
data_json_path = os.path.join(base_dir, "all_data.js")
with open(data_json_path, "w", encoding="utf-8") as f:
    f.write("const all_data = " + json.dumps(all_data, ensure_ascii=False) + ";")

# index.html oluştur (sözlük anasayfası)
index_path = os.path.join(base_dir, "index.html")
with open(index_path, "w", encoding="utf-8") as index:
    index.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Daristana Peyvan, Kürtçe-Türkçe dilleri arası dijital sözlük hizmeti sağlar...">
    <meta name="keywords" content="Kürtçe-Türkçe, Sözlük">
    <title>Daristana Peyvan Kürtçe - Türkçe Sözlük</title>
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="./favicon.svg" type="image/svg+xml">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {joint_css}
    <style>
        h2 {{ font-size: 28px; }}
        .switcher {{ display: flex; gap: 20px; justify-content:center; margin-bottom: 20px; }}
        .switcher button {{
            padding: 8px 20px;
            border: none;
            border-radius: 24px;
            background: #315b5e;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }}
        .switcher button.active {{ background: #203b3d; }}
        #search {{
            width: 60%;
            padding: 12px 16px;
            margin: 0 auto 25px auto;
            font-size: 18px;
            border: 1px solid #ccc;
            border-radius: 24px;
            display: block;
            outline: none;
        }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 12px 0; }}
        a {{ text-decoration: none; color: #1f4037; font-size: 20px; }}
        a:hover {{ text-decoration: underline; }}
        #suggested_word {{
            font-size: 18px;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="navbar">
        <h1 class="title-text">Daristana Peyvan</h1>
    </div>
    <div class="container">
        <div class="switcher">
            <button id="btn-kurd" class="active" onclick="change_lang('kurdish')">Kürtçe (Kurmanci)</button>
            <button id="btn-turkish" onclick="change_lang('turkish')">Türkçe</button>
        </div>
        <input type="text" id="search" placeholder="Ara..." oninput="search()">
        <div id="suggested_word"></div>
        <ul id="results"></ul>
    </div>
    <div class="footer">
        <a href="hakkinda.html">Hakkında</a> |
        <a href="iletisim.html">İletişim</a>
    </div>
    <div style="text-align:center; font-size: 14px; color: #999; margin-top: 20px;">Sevgi ile hazırlandı <br> Bi hezkirin hate amede kirin ❤️</div>
    <script src="all_data.js"></script>
    <script>
        let search_mode = "kurdish";
        // uyumlu bir arama deneyimi için kelimelerin normalize edilmesi
        function normalize_word(str) {{
            return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/ /g, "_");
        }}
        // iki dilli arama değiştirme fonksiyonu
        function change_lang(mod) {{
            search_mode = mod;
            document.getElementById("btn-kurd").classList.toggle("active", mod === "kurdish");
            document.getElementById("btn-turkish").classList.toggle("active", mod === "turkish");
            search();
        }}
        // arama fonksiyonu
        function search() {{
            const q = document.getElementById("search").value.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/ /g, "_");
            const ul = document.getElementById("results");
            ul.innerHTML = "";
            // girdi en az 2 harf taşımalı
            if(q.length < 2) return;
        // verilerin şekillendirilmesi ve kullanıcıya sunumu
            all_data.forEach(v => {{
                const kurdish = normalize_word(v[0]);
                const turkishword = normalize_word(v[2]);
                if((search_mode === "kurdish" && kurdish.includes(q)) || (search_mode === "turkish" && turkishword.includes(q))) {{
                    let shown = search_mode === "kurdish" ? v[0] : v[2];
                    const filename = normalize_word(kurdish.split(",")[0].trim());
                    const li = document.createElement("li");
                    li.innerHTML = '<a href="sayfalar/' + filename + '.html">' + shown + '</a>';
                    ul.appendChild(li);
                }}
            }});
        }}
        // rastgele kelime sunumu
        window.onload = function() {{
            const random_word = all_data[Math.floor(Math.random() * all_data.length)];
            const kurdish = random_word[0];
            const filename = normalize_word(kurdish.split(",")[0].trim());
            const link = '<strong>Göz at:</strong> <a href="sayfalar/' + filename + '.html">' + kurdish + '</a>';
            document.getElementById("suggested_word").innerHTML = link;
        }}
           if ('serviceWorker' in navigator) {{
    navigator.serviceWorker.register('service-worker.js').then(function(registration) {{
      console.log('Service Worker kayıtlı:', registration.scope);
    }}).catch(function(error) {{
      console.log('Service Worker kaydı başarısız:', error);
    }});
  }}
    </script>
</body>
</html>""")

# sabit sayfaları oluştur
for page, title, content, extracontent in [
    ("hakkinda.html", "Hakkında", "<b>Daristana Peyvan Kürtçe - Türkçe Sözlük</b><br> Kürtçe - Türkçe Sözlük ihtiyacına sunulan çözümlerden birisi olmak amacıyla geliştirilen, kar amacı gütmeyen bir projedir. Misyonumuz hem Kürtçe'yi dijital ortamlarda daha görünür kılmak, hem de Kürtçe dili ile çalışma yapmak isteyen veya bu dili öğrenen kullanıcılara erişilebilir, güncel ve güvenilir bir sözlük kaynağı sunmaktır.", "Bu proje açık kaynak kodludur. Projenin kaynak kodlarına ve ana sayfasına ulaşmak için:  <a href='https://github.com/projectxurme/projectxurme.github.io'>Proje Ana Sayfası - GitHub</a>"),
    ("iletisim.html", "İletişim", "Geliştirici ekibimizle iletişime geçmek; soru ve taleplerinizi bildirmek için ilgili iletişim adresini kullanabilirsiniz.", "Bizimle iletişime geçin: <a href='mailto:projectxurme@gmail.com'>projectxurme@gmail.com</a>")
]:
    with open(os.path.join(base_dir, page), "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="../favicon.svg" type="image/xml+svg">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {joint_css}
    <style>
        h1 {{ font-size: 32px; margin-bottom: 20px; }}
        p {{ font-size: 18px; line-height: 1.6em; }}
    </style>
</head>
<body>
    <div class="navbar">
        <a href="index.html" style="text-decoration: none; color: #e6e6e6; font-size: 16px; font-weight: bold;">Ana Sayfa</a>
    </div>
    <div class="container">
        <h1>{title}</h1>
        <p>{content}</p>
        <p>{extracontent}</p>
    </div>
</body>
<script>
   if ('serviceWorker' in navigator) {{
    navigator.serviceWorker.register('service-worker.js').then(function(registration) {{
      console.log('Service Worker kayıtlı:', registration.scope);
    }}).catch(function(error) {{
      console.log('Service Worker kaydı başarısız:', error);
    }});
  }}
</script>
</html>""")

# manifest.json oluştur
manifest_json = {
    "name": "Daristana Peyvan",
    "short_name": "Sözlük",
    "start_url": "index.html",
    "display": "standalone",
    "background_color": "#f4f4f4",
    "theme_color": "#203a3d",
    "icons": [
        {
            "src": "icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

import json
with open(os.path.join(base_dir, "manifest.json"), "w", encoding="utf-8") as mf:
    json.dump(manifest_json, mf, ensure_ascii=False, indent=2)

# service-worker.js oluştur
with open(os.path.join(base_dir, "service-worker.js"), "w", encoding="utf-8") as sw:
    sw.write("""self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('sozluk-cache').then(function(cache) {
      return cache.addAll([
        '/index.html',
        '/style.css',
        '/all_data.js'
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});""")