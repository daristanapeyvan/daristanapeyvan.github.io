# -*- coding: utf-8 -*-
import os
import csv
import json
import unicodedata

# --- YENİ GRUPLAMA İÇİN GEREKLİ KLASÖR OLUŞTURMA BAŞLANGICI ---
# Kelimeleri ilk harfine göre gruplamak için yeni dizin klasörünü oluşturma
base_dir = os.path.dirname(os.path.abspath(__file__))
dizin_folder_path = os.path.join(base_dir, "dizin")
if not os.path.exists(dizin_folder_path):
    os.mkdir(dizin_folder_path)
# --- YENİ GRUPLAMA İÇİN GEREKLİ KLASÖR OLUŞTURMA BİTİŞİ ---


# klasör yolu oluşturma
base_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(base_dir, "sayfalar")
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

csv_path = os.path.join(base_dir, "veriler.csv")
with open(csv_path, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    all_data = sorted(list(reader), key=lambda x: x[0].lower())

# csv kısaltmaları tam biçimlerine çevirme
wordtype_map = {
    "n": "nav - isim",
    "v": "lêker - fiil",
    "adj": "rengdêr - sıfat",
    "adv": "hoker - zarf",
    "pron": "cînav - zamir",
    "prep": "daçek - edat",
    "conj": "girêdek - bağlaç",
    "interj": "ünlem",
    "num": "sayı",
    "exp": "ifade",
    "color": "renk",
}

def normalize_word(k):
    # uyumsuz karakterleri düzeltme fonksiyonu
    k = k.split(",")[0].strip()
    return ''.join(c for c in unicodedata.normalize('NFKD', k) if not unicodedata.combining(c)).lower().replace(" ", "_")

# --- YENİ GRUPLAMA VE DİZİN VERİ HAZIRLIĞI BAŞLANGICI ---
# Kelimeleri Kürtçe kelimenin ilk harfine göre gruplama
grouped_data = {}
for data in all_data:
    kurdish_word = data[0].strip()
    first_char = kurdish_word[0].upper() 
    
    if first_char not in grouped_data:
        grouped_data[first_char] = []
    
    grouped_data[first_char].append(data)

# Harfleri alfabetik sıraya göre al
sorted_letters = sorted(grouped_data.keys()) 
# --- YENİ GRUPLAMA VE DİZİN VERİ HAZIRLIĞI BİTİŞİ ---

# ortak CSS
joint_css = """
<style>

    html {
    overscroll-behavior: none;
    font-size: 100%;
    }

    body {
        font-family: 'Tahoma', "Geneva", sans-serif;
        font-size: 1rem;
        margin: 0;
        background-color: #EBEAE6;
        color: #21421e;
        overflow: scroll;
        overscroll-behavior: none;
    }
    body::-webkit-scrollbar {
        display: none;
    }
    .navbar {
    background-image: linear-gradient(180deg, #21421e, #122010);
    color: white;
    padding: 15px 30px; 
    display: flex;
    justify-content: space-between; 
    align-items: center;
    flex-wrap: wrap; 
    gap: 10px;
    box-shadow: 0 4px .0px #708A58;
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
    .nav-links {
    display: flex;
    align-items: center;
    gap: 20px; 
}
        .nav-links a {
        color: #e6e6e6;
        text-decoration: none;
        margin-left: 20px;
        font-size: 1rem;
    }
    .nav-links a:hover {
        color: #ffffff;
    }
    .container {
        max-width: 900px;
        margin: 40px auto;
        padding: 30px;
        background: #FFFFFFE6;
        border-radius: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .footer {
        text-align:center;
        font-size: 16px;
    }
    .footer a {
        color: #21421e;
        text-decoration: none;
        margin: 0 10px;
    }
</style>
"""

# sözlük sayfalarını oluştur
for data in all_data:
    kurdish, wordtype, turkish, extra = data
    extra = extra.replace("<es>", "<h3>Hevoka Mînak - Örnek Cümle</h3>")
    file_name = normalize_word(kurdish)
    # csv kısaltmalarını çözme
    wordtype_full = wordtype_map.get(wordtype.strip().lower(), wordtype)
    file_path = os.path.join(folder_path, f"{file_name}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{kurdish} - {turkish} Daristana Peyvan</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="manifest" href="manifest.json">
    <link rel="icon" type="image/svg+xml" href="../resources/favicon.svg">
    <meta name="description" content="Kürtçe {kurdish} Türkçe ne demek? Türkçe {turkish} Kürtçe ne demek? Anlamı, manası, kelimeleri bul ve keşfet. ">
    <meta name="keywords" content="Kürtçe {kurdish} Türkçe ne demek?, Türkçe {turkish} Kürtçe ne demek?, anlam, kelime, kürtçe - türkçe sözlük, {turkish} kürtçe nasıl denir">
    <meta name="robots" content="index, follow">
    {joint_css}
    <style>
        h1 {{ font-size: 2.2rem; }}
        .wordtype {{ font-style: italic; color: #21421e; font-size: 1rem; margin-bottom: 20px; }}
        p {{ font-size: 1.2rem; line-height: 1.6em; }}

        .extra h3 {{
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 1.15rem;
        }}

        .extra {{
            margin-top: 30px;
            font-size: 1rem;
            background: #21421e08;
            padding: 15px;
            border-radius: 24px;
            color: #21421e;
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
            color: #21421e;
        }}
        .title-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        a {{
            color: #21421e;
            text-decoration: none;
            font-weight: bold;
        }}

        .navbarnew {{
            background-image: linear-gradient(180deg, #21421e, #122010);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: center; 
            align-items: center;
            box-shadow: 0 4px .0px #708A58;
        }}

        .home-link {{
    display: flex;
    align-items: end;
    gap: 8px;
    text-decoration: none;
    color: #e6e6e6;
    font-size: 16px;
    font-weight: bold;
    margin: 5px;
        }}

        .home-link img {{
    vertical-align: middle;
    filter: invert(85%);
    transition: 0.2s ease;
}}

.home-link img:hover {{
    filter: invert(100%);
    transform: scale(1.1);
}}

.home-link:hover span {{
    color: #ffffff;
}}
    </style>
</head>
<body>
    <div class="navbarnew">
    <a href="../index.html" class="home-link" title="Ana Sayfa">
    <img src="../resources/homepage.svg" alt="Ana Sayfa" width="22" height="22">
    <span>Ana Sayfa</span>
</a>
    </div>
    <div class="container">
        <div class="title-bar">
            <h1>{kurdish}</h1>
            <button class="copy-btn" onclick="copyPageUrl()" title="Bağlantıyı Kopyala">
                <img src="../resources/copy.svg" alt="Kopyala" width="24" height="24">
                <span class="checkmark" style="display:none;">✅</span>
            </button>
        </div>
        <div class="wordtype">{wordtype_full}</div>
        <p>{turkish}</p>
        <div class="extra">{extra}</div>
    </div>
    <div class="footer">
        <a href="../hakkinda.html">Hakkında</a> |
        <a href="../iletisim.html">İletişim</a>
    </div>

    <script>
        function copyPageUrl() {{
            const url = window.location.href;
            const checkmark = document.querySelector('.copy-btn .checkmark');
            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(url).then(() => showCheckmark()).catch(() => {{
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
                document.execCommand('copy');
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
            navigator.serviceWorker.register('service-worker.js');
        }}
    </script>
</body>
</html>""")

for letter in sorted_letters:
    letter_data = grouped_data[letter]
    
    list_items = []
    for kurdish, _, turkish, _ in letter_data:
        file_name = normalize_word(kurdish) 
        list_items.append(f'<li><a href="../sayfalar/{file_name}.html">{kurdish} </a><span style="color:#666;">({turkish})</span></li>')
    
    list_html = '\n'.join(list_items)
    
    dizin_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>'{letter}' Harfiyle Başlayan Kürtçe Kelimeler - Daristana Peyvan</title>
    <meta name="robots" content="index, follow">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {joint_css}
    <style>
        .container a {{ text-decoration: none; color: #21421e; font-weight: bold; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 8px; font-size: 1.1rem; }}
        h1 {{ text-align: center; margin-bottom: 30px; }}
        .navbarnew {{
            background-image: linear-gradient(180deg, #21421e, #122010);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px .0px #708A58;
        }}
        
        .home-link {{
    display: flex;
    align-items: end;
    gap: 8px;
    text-decoration: none;
    color: #e6e6e6;
    font-size: 16px;
    font-weight: bold;
    margin: 5px;
        }}

        .home-link img {{
    vertical-align: middle;
    filter: invert(85%);
    transition: 0.2s ease;
}}

.home-link img:hover {{
    filter: invert(100%);
    transform: scale(1.1);
}}

.home-link:hover span {{
    color: #ffffff;
}}

    </style>
</head>
<body>
    <div class="navbarnew">
        <a href="../index.html" class="home-link" title="Ana Sayfa">
            <img src="../resources/homepage.svg" alt="Ana Sayfa" width="22" height="22">
            <span>Ana Sayfa</span>
        </a>
    </div>
    <div class="container">
        <h1>'{letter}' Harfiyle Başlayan Kelimeler ({len(letter_data)})</h1>
        <ul>
            {list_html}
        </ul>
    </div>
</body>
</html>
    """
    
    file_path = os.path.join(dizin_folder_path, f"{letter.lower()}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(dizin_html)

alfabetik_dizin_links = []
for letter in sorted_letters:
    count = len(grouped_data[letter])
    # Linkler /dizin klasöründeki harf sayfalarını işaret etmeli
    alfabetik_dizin_links.append(f'<a href="dizin/{letter.lower()}.html">{letter} ({count})</a>')

dizin_links_html = '\n'.join(alfabetik_dizin_links)

alfabetik_dizin_html_content = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Alfabetik Sözlük Dizinleri - Daristana Peyvan</title>
    <meta name="robots" content="index, follow">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {joint_css}
    <style>
        h1 {{ text-align: center; margin-bottom: 30px; }}
        .letter-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 12px;
            justify-content: center;
            text-align: center;
            margin-top: 30px;
        }}
        .letter-grid a {{
            display: block;
            padding: 15px 5px;
            background-color: #33662e;
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: bold;
            transition: background-color 0.2s;
            font-size: 1.1rem;
        }}
        .letter-grid a:hover {{
            background-color: #4a8045;
        }}
        .navbarnew {{
            background-image: linear-gradient(180deg, #21421e, #122010);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px .0px #708A58;
        }}
        .home-link {{
            display: flex;
            align-items: end;
            gap: 8px;
            text-decoration: none;
            color: #e6e6e6;
            font-size: 16px;
            font-weight: bold;
            margin: 5px;
        }}
        
        .home-link img {{
    vertical-align: middle;
    filter: invert(85%);
    transition: 0.2s ease;
}}

.home-link img:hover {{
    filter: invert(100%);
    transform: scale(1.1);
}}

.home-link:hover span {{
    color: #ffffff;
}}
    </style>
</head>
<body>
    <div class="navbarnew">
        <a href="./index.html" class="home-link" title="Ana Sayfa">
            <img src="resources/homepage.svg" alt="Ana Sayfa" width="22" height="22">
            <span>Ana Sayfa</span>
        </a>
    </div>
    <div class="container">
        <h1>Alfabetik Kelime Dizinleri</h1>
        <p style="text-align: center; font-size: 1.1rem;">Aşağıdaki harflerden birini seçerek ilgili kelimelere kolayca ulaşabilirsiniz.</p>
        <div class="letter-grid">
            {dizin_links_html}
        </div>
    </div>
</body>
</html>
"""
with open(os.path.join(base_dir, "alfabetik_dizin.html"), "w", encoding="utf-8") as f:
    f.write(alfabetik_dizin_html_content)
# --- YENİ KOD BİTİŞİ ---

# all_data.js oluştur
data_json_path = os.path.join(base_dir, "all_data.js")
with open(data_json_path, "w", encoding="utf-8") as f:
    f.write("const all_data = " + json.dumps(all_data, ensure_ascii=False) + ";")

toplam_kelime_sayisi = len(all_data)

# index.html oluştur
index_path = os.path.join(base_dir, "index.html")
with open(index_path, "w", encoding="utf-8") as index:
    index.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Daristana Peyvan, Kürtçe-Türkçe dilleri arası dijital sözlük hizmeti sağlar...">
    <meta name="keywords" content="Kürtçe-Türkçe, Sözlük, kürtçe-türkçe sözlük, daristana peyvan">
    <meta name="robots" content="index, follow">
    <title>Daristana Peyvan Kürtçe - Türkçe Sözlük</title>
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="resources/favicon.svg" type="image/svg+xml">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {joint_css}
    <style>
        h2 {{ font-size: 1.75rem; }}
        .switcher {{
        display: flex; gap: 15px; justify-content: center; align-items: center; margin-bottom: 25px;
        }}

        .lang-label {{
        font-weight: normal; color: #666; font-size: 0.875rem;
        }}

        #label-kurd.active, #label-turkish.active {{
        font-weight: bold; color: #21421e;
        }}

.toggle-switch {{
    position: relative;
    display: inline-block;
    width: 58px; 
    height: 18px; 
}}


.toggle-switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}


.slider {{
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc; 
    transition: .4s;
    border-radius: 34px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}


.slider:before {{
    position: absolute;
    content: "";
    height: 10px;
    width: 10px;
    left: 6px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}}


input:checked + .slider {{
    background-color: #33662e; 
}}


input:checked + .slider:before {{
    transform: translateX(36px); 
}}
        #search::placeholder {{
        color: #21421e;  
        opacity: 1;
}}
        .main-heading {{
        text-align: center;
        margin-bottom: 25px;
        color: #21421e;
        }}

        .logo-svg {{
    display: block;             
    margin: 0 auto 14px;        
    height: auto;               
    max-height: 140px;
    opacity: 0.5;   
    margin-top: 5px;            
}}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 12px 0; }}
        a {{ text-decoration: none; color: #21421e;}}
        #suggested_word {{
            margin-top: 30px;
            font-size: 1.1rem;
        }}
        .iconbox {{
        vertical-align: bottom;
        }}

        #search {{
        width: 50%;
        margin: 0 auto 25px auto;
        display: block;
        padding: 12px 16px;
        border: 2px solid #33662e;
        border-radius: 24px;
        outline: none;
        background-image: url('./resources/searchicon.png'); 
        background-position: 10px 10px; 
        background-repeat: no-repeat;
        background-size: 20px;
        padding: 12px 20px 12px 40px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        @media (max-width: 600px) {{
        .navbar {{
            flex-direction: column;
            align-items: center;
        }}

        .nav-links {{
            margin-top: 10px;
        }}

        .nav-links a {{
            margin-left: 10px;
            font-size: 15px;
        }}

        .title-text {{
            font-size: 22px;
        }}
        #search {{
        width: 80%; 
    }}
    }}

    </style>
</head>
<body>
    <div class="navbar">
        <h1 class="title-text">Daristana Peyvan</h1>
        <div class="nav-links">
            <a href="kelimekutusu.html"><img class="iconbox" src="./resources/kutu.svg" alt="Kelime Kutusu" width="22" height="22"></a>
            <a href="hakkinda.html">Hakkında</a>
            <a href="iletisim.html">İletişim</a>
            <a href="https://github.com/daristanapeyvan/daristanapeyvan.github.io">GitHub</a>
        </div>
    </div>
    <div class="container">
        <img src="resources/banner.png" alt="Daristana Peyvan logosu" class="logo-svg">
        <h2 class="main-heading">Kürtçe - Türkçe Sözlük</h2>
<div class="switcher">
    <span class="lang-label" id="label-kurd">Kürtçe (Kurmanci)</span>
    
    <label class="toggle-switch">
        <input type="checkbox" id="lang-toggle" checked onchange="toggle_lang()">
        <span class="slider"></span>
    </label>
    <span class="lang-label" id="label-turkish">Türkçe</span>
</div>
        <input type="text" id="search" placeholder="Aramak için bir sözcük girin..." oninput="search()">
        <div style="text-align:center; font-size: 0.9375rem; color: #21421e; padding-top: 15px; font-weight: bold;">Toplam Kelime Sayısı: {toplam_kelime_sayisi} | BETA</div>
        <div id="suggested_word"></div>
        <ul id="results"></ul>
    </div>
    <div class="footer">
    <div style="text-align:center; font-size: 0.875rem; color: #999;">Sevgi ile hazırlandı<br>Bi hezkirin hate amede kirin ❤️</div>
    <script src="all_data.js"></script>
    <script>
    let search_mode = "kurdish";
    
    function normalize_word(str) {{
        return str.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/ /g, "_");
    }}
    
    function toggle_lang() {{
        const isChecked = document.getElementById("lang-toggle").checked;
        const btnKurd = document.getElementById("label-kurd");
        const btnTurkish = document.getElementById("label-turkish");
        
        if (isChecked) {{
            // Anahtar AÇIK (Sağda) ise Kürtçe
            search_mode = "kurdish";
            btnKurd.classList.add("active");
            btnTurkish.classList.remove("active");
            
        }} else {{
            // Anahtar KAPALI (Solda) ise Türkçe
            search_mode = "turkish";
            btnKurd.classList.remove("active");
            btnTurkish.classList.add("active");
        }}
        
        search(); 
    }}
    
    
    function search() {{
        const q = document.getElementById("search").value.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ /g, "_");
        const ul = document.getElementById("results");
        ul.innerHTML = "";
        if(q.length < 2) return;
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
    
    window.onload = function() {{
        const random_word = all_data[Math.floor(Math.random() * all_data.length)];
        const kurdish = random_word[0];
        const filename = normalize_word(kurdish.split(",")[0].trim());
        const link = '<strong>Göz at:</strong> <a href="sayfalar/' + filename + '.html">' + kurdish + '</a>';
        document.getElementById("suggested_word").innerHTML = link;
        
        document.getElementById("label-kurd").classList.add("active");
    }}
    if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('service-worker.js');
    }}
    </script>
</body>
</html>""")

# veriler.csv'deki belirtilen kelime türleri için özel sayfalar oluştur
categories = {
    "exp": {
        "title": "İfadeler & Günlük Konuşma",
        "filename": "exp.html",
    },
    "color": {
        "title": "Renkler",
        "filename": "renkler.html",
    },
    "num": {
        "title": "Rakamlar & Sayılar",
        "filename": "sayilar.html",
    },
}

for key, info in categories.items():
    filtered = [d for d in all_data if d[1].strip().lower() == key]
    if not filtered:
        continue

    rows_html = "\n".join(f"<tr><td>{k}</td><td>{t}</td></tr>" for k, _, t, _ in filtered)

    file_path = os.path.join(base_dir, info["filename"])
    with open(file_path, "w", encoding="utf-8") as cat_file:
        cat_file.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{info["title"]} - Daristana Peyvan</title>
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="./favicon.svg" type="image/svg+xml">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {joint_css}
    <style>
        h1 {{
            font-size: 32px;
            text-align: center;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            border-radius: 12px;
            overflow: hidden;
        }}
        th, td {{
            padding: 16px;
            font-size: 1rem;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #21421e;
            color: white;
            text-align: left;
        }}
        tr:hover {{
            background-color: #f1f1f1;
        }}
        .home-link {{
            display: flex;
            align-items: end;
            gap: 8px;
            text-decoration: none;
            color: #e6e6e6;
            font-size: 16px;
            font-weight: bold;
            margin: 5px;
        }}
        .home-link img {{
            vertical-align: middle;
            filter: invert(85%);
            transition: 0.2s ease;
        }}
        .home-link img:hover {{
            filter: invert(100%);
            transform: scale(1.1);
        }}
        .home-link:hover span {{
            color: #ffffff;
        }}
        .navbarnew {{
            background-image: linear-gradient(180deg, #21421e, #122010);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: center; 
            align-items: center;
            box-shadow: 0 4px .0px #708A58;
        }}
    </style>
</head>
<body>
    <div class="navbarnew">
        <a href="./index.html" class="home-link" title="Ana Sayfa">
            <img src="./resources/homepage.svg" alt="Ana Sayfa" width="22" height="22">
            <span>Ana Sayfa</span>
        </a>
    </div>
    <div class="container">
        <h1>{info["title"]}</h1>
        <table>
            <thead>
                <tr>
                    <th>Kürtçe</th>
                    <th>Türkçe</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</body>
<script>
   if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('service-worker.js');
   }}
</script>
</html>""")

# kelime türleri sayfasını bağlayan ana sayfa oluştur
kelimekutusu_path = os.path.join(base_dir, "kelimekutusu.html")
with open(kelimekutusu_path, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Kelime Kutusu - Daristana Peyvan</title>
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="./favicon.svg" type="image/svg+xml">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {joint_css}
    <style>
        body {{
            font-family: 'Tahoma', "Geneva", sans-serif;
            margin: 0;
            background-color: #EBEAE6;
            color: #21421e;
            overflow: scroll;
            text-align: center;
        }}
        body::-webkit-scrollbar {{
            display: none;
        }}
        .navbarnew {{
            background-image: linear-gradient(180deg, #21421e, #122010);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: center; 
            align-items: center;
            box-shadow: 0 4px .0px #708A58;
        }}
        .home-link {{
            display: flex;
            align-items: end;
            gap: 8px;
            text-decoration: none;
            color: #e6e6e6;
            font-size: 16px;
            font-weight: bold;
            margin: 5px;
        }}
        .home-link img {{
            vertical-align: middle;
            filter: invert(85%);
            transition: 0.2s ease;
        }}
        .home-link img:hover {{
            filter: invert(100%);
            transform: scale(1.1);
        }}
        .home-link:hover span {{
            color: #ffffff;
        }}
        .container {{
            max-width: 900px;
            margin: 40px auto;
            padding: 30px;
            background: #FFFFFFE6;
            border-radius: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        h1 {{
            font-size: 32px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .container a {{
            display: block;
            font-size: 1rem;
            margin: 10px 0;
            color: #21421e;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.2s ease;
        }}
        .container a:hover {{
            color: #000;
        }}
    </style>
</head>
<body>
    <div class="navbarnew">
        <a href="./index.html" class="home-link" title="Ana Sayfa">
            <img src="./resources/homepage.svg" alt="Ana Sayfa" width="22" height="22">
            <span>Ana Sayfa</span>
        </a>
    </div>
    <div class="container">
        <h1>Kelime Kutusu 🎁</h1>
        <a href="./exp.html">İfadeler ve Günlük Konuşma</a>
        <a href="./renkler.html">Renkler</a>
        <a href="./sayilar.html">Rakam & Sayılar</a>
        <a href="./alfabetik_dizin.html">Alfabetik Dizin</a> </div>
<script>
   if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('service-worker.js');
   }}
</script>
</body>
</html>""")


# sabit sayfaları oluştur
for page, title, content, extracontent in [
    ("hakkinda.html", "Hakkında", "<b>Daristana Peyvan Kürtçe - Türkçe Sözlük</b><br> Kürtçe - Türkçe Sözlük ihtiyacına sunulan çözümlerden birisi olmak amacıyla geliştirilen, kar amacı gütmeyen bir projedir. Misyonumuz hem Kürtçe'yi dijital ortamlarda daha görünür kılmak, hem de Kürtçe dili ile çalışma yapmak isteyen veya bu dili öğrenen kullanıcılara erişilebilir, güncel ve güvenilir bir sözlük kaynağı sunmaktır.", "<b> Özellikler </b> <br> <ul> <li>Kürtçe (Kurmanci) veya Türkçe dillerinde girdi araması yapabilirsiniz.</li> <li>Şapkasız harfleri şapkalı karşılıklarına dönüştüren karakter dönüştürme özelliği sayesinde, Kürtçe girdileri aramak için özel Kürtçe harfleri kullanmanız zorunlu değildir.</li> <li>Kelime Kutusu özelliği ile, çeşitli kelimeleri kategorize edilmiş şekilde görüntüleyebilirsiniz.</li> <li>PWA desteğiyle, Web sayfasını cihazınıza bir Web uygulaması olarak yükleyip, hızlı erişim sağlayabilirsiniz.</li> </ul>"),
    ("iletisim.html", "İletişim", "İletişim adreslerini bu hususlarda kullanabilirsiniz.<ul><li>Geliştirici(ler) ile irtibata geçmek.</li><li>Proje ile ilgili öneri, soru, talepler vs.</li><li>Sözlük içeriği ile ilgili hataları ve düzeltmeleri sağlamak.</li></ul>", "Bizimle iletişime geçin: <a href='mailto:projectxurme@gmail.com'>projectxurme@gmail.com</a><br>Geri bildirimleriniz için Google Formlar adresini de kullanabilirsiniz: <a href='https://forms.gle/rzmShxf7H4sY8ycU7'>Google Formlar</a>")
]:
    with open(os.path.join(base_dir, page), "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="resources/favicon.svg" type="image/xml+svg">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {joint_css}
    <style>
        h1 {{ font-size: 32px; margin-bottom: 20px; }}
        p {{ font-size: 1rem; line-height: 1.6em; }}
             .navbarnew {{
            background-image: linear-gradient(180deg, #21421e, #122010);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: center; 
            align-items: center;
            box-shadow: 0 4px .0px #708A58;
        }}

.home-link {{
    display: flex;
    align-items: end;
    gap: 8px;
    text-decoration: none;
    color: #e6e6e6;
    font-size: 16px;
    font-weight: bold;
    margin: 5px;
        }}

.home-link img {{
    vertical-align: middle;
    filter: invert(85%);
    transition: 0.2s ease;
}}

.home-link img:hover {{
    filter: invert(100%);
    transform: scale(1.1);
}}

.home-link:hover span {{
    color: #ffffff;
}}
a {{
color: #21823f;
}}

ul li {{
    margin-bottom: 10px;
}}

    </style>
</head>
<body>
    <div class="navbarnew">
    <a href="./index.html" class="home-link" title="Ana Sayfa">
    <img src="resources/homepage.svg" alt="Ana Sayfa" width="22" height="22">
    <span>Ana Sayfa</span>
</a>
    </div>
    <div class="container">
        <h1>{title}</h1>
        <p>{content}</p>
        <p>{extracontent}</p>
    </div>
</body>
<script>
   if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('service-worker.js');
   }}
</script>
</html>""")

# manifest.json oluştur
manifest_json = {
  "name": "Daristana Peyvan",
  "short_name": "Ferheng",
  "start_url": "https://daristanapeyvan.github.io/",
  "scope": "https://daristanapeyvan.github.io/",
  "display": "standalone",
  "background_color": "#21421e",
  "theme_color": "#21421e",
  "icons": [
    {
      "src": "https://daristanapeyvan.github.io/resources/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "https://daristanapeyvan.github.io/resources/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}

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