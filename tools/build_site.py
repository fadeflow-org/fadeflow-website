"""
FadeFlow static site builder.

    python tools/build_site.py

Generates the product/service/pricing/blog/resources/experiments pages,
refreshes the <head>, nav and footer of the hand-written pages
(index, about, contact, legal), and writes sitemap.xml, robots.txt,
rss.xml, site.webmanifest, llms.txt and llms-full.txt.

Free resources live in tools/resources_data.py.
"""
import io, re, sys, json, os, html
from email.utils import format_datetime
from datetime import datetime, timezone

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
from resources_data import RESOURCES, LOOKS, PHOTO_CATEGORIES, EXPERIMENTS, photo_prompt

R = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(TOOLS)
SITE = "https://fadeflow.in"
DATE = "2026-11-03"
OG = f"{SITE}/og-image.jpg"
OG_ALT = "FadeFlow: Less manual work. More flow. AI workflow automation for SMEs in the UAE & India"
APP = "https://application.fadelogistics.fadeflow.in/"
PHONE = "+971565814649"
PHONE_H = "+971 56 581 4649"

def esc(s): return html.escape(s, quote=True)
def strip(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(s))).strip()
def w(path, text):
    full = os.path.join(R, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, "w", encoding="utf-8", newline="\n").write(text)
def rd(path): return io.open(os.path.join(R, path), encoding="utf-8-sig").read()

ORG_DESC = ("FadeFlow builds AI products and custom AI workflow automation that reduce manual work for small and "
            "medium businesses (SMEs) in the United Arab Emirates and India. Its product FadeLogistics is workflow "
            "software for transport and logistics companies. Founded in 2023.")

ORG = {
  "@type": "Organization", "@id": f"{SITE}/#organization", "name": "FadeFlow", "url": f"{SITE}/",
  "logo": {"@type": "ImageObject", "url": f"{SITE}/icon-512.png", "width": 512, "height": 512},
  "image": OG, "description": ORG_DESC, "foundingDate": "2023",
  "email": "sales@fadeflow.in", "telephone": PHONE,
  "slogan": "Less manual work. More flow.",
  "areaServed": [{"@type": "Country", "name": "United Arab Emirates"}, {"@type": "Country", "name": "India"}],
  "knowsAbout": ["AI workflow automation", "Business process automation for SMEs", "Logistics workflow software",
                 "Invoice automation", "WhatsApp lead qualification", "Email filtering", "Document data extraction", "Claude AI"],
  "founder": {"@type": "Person", "@id": f"{SITE}/about.html#sayed-adinan", "name": "Sayed Adinan", "jobTitle": "Founder",
              "sameAs": ["https://www.linkedin.com/in/sayed-adinan/"]},
  "employee": [
    {"@type": "Person", "name": "Sayed Adinan", "jobTitle": "Founder"},
    {"@type": "Person", "name": "Muhammed KM", "jobTitle": "Co-founder, Software Engineer"},
    {"@type": "Person", "name": "Arshad Akl", "jobTitle": "Software Engineer"}],
  "sameAs": ["https://www.linkedin.com/company/fadeflow", "https://www.instagram.com/time.fade"],
  "contactPoint": [
    {"@type": "ContactPoint", "contactType": "sales", "email": "sales@fadeflow.in", "telephone": PHONE,
     "areaServed": ["AE", "IN"], "availableLanguage": ["English"]},
    {"@type": "ContactPoint", "contactType": "technical support", "email": "tech@fadeflow.in",
     "areaServed": ["AE", "IN"], "availableLanguage": ["English"]}],
}
WEBSITE = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "FadeFlow",
           "description": "AI workflow automation for SMEs in the UAE & India", "inLanguage": "en",
           "publisher": {"@id": f"{SITE}/#organization"}}

def faq_node(url, faqs):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}

def ldjson(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1).replace("</", "<\\/")

# ---------------------------------------------------------------- head
def head(title, desc, path, P, *, page_type="WebPage", crumbs=None, nodes=(), inner=True,
         og_type="website", article=None, noindex=False):
    url = SITE + path
    graph = [ORG, WEBSITE]
    page = {"@type": page_type, "@id": url + "#webpage", "url": url, "name": title, "description": desc,
            "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#organization"},
            "inLanguage": "en", "dateModified": DATE,
            "primaryImageOfPage": {"@type": "ImageObject", "url": OG, "width": 1200, "height": 630}}
    if crumbs:
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(crumbs)]})
    graph.insert(2, page)
    graph.extend(nodes)
    art = ""
    if article:
        art = (f'\n  <meta property="article:published_time" content="{article["date"]}T09:00:00+04:00" />'
               f'\n  <meta property="article:modified_time" content="{DATE}T09:00:00+04:00" />'
               f'\n  <meta property="article:author" content="FadeFlow Team" />'
               f'\n  <meta property="article:section" content="{esc(article["tag"])}" />')
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    css = f'  <link rel="stylesheet" href="{P}styles.css" />\n' + (f'  <link rel="stylesheet" href="{P}inner.css" />\n' if inner else "")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="{robots}" />
  <meta name="author" content="FadeFlow" />
  <meta name="application-name" content="FadeFlow" />
  <meta name="theme-color" content="#F5F2EA" />
  <meta name="format-detection" content="telephone=no" />

  <!-- Open Graph (WhatsApp, LinkedIn, Facebook) -->
  <meta property="og:site_name" content="FadeFlow" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{OG}" />
  <meta property="og:image:secure_url" content="{OG}" />
  <meta property="og:image:type" content="image/jpeg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{esc(OG_ALT)}" />
  <meta property="og:locale" content="en_US" />{art}

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{OG}" />
  <meta name="twitter:image:alt" content="{esc(OG_ALT)}" />

  <!-- Icons & app -->
  <link rel="icon" type="image/svg+xml" href="{P}favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="{P}favicon-32.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="{P}apple-touch-icon.png" />
  <link rel="manifest" href="{P}site.webmanifest" />
  <link rel="alternate" type="application/rss+xml" title="FadeFlow Blog" href="{SITE}/rss.xml" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
{css}
  <!-- Structured data -->
  <script type="application/ld+json">
{ldjson({"@context": "https://schema.org", "@graph": graph})}
  </script>
</head>'''

# ---------------------------------------------------------------- nav / footer / cta
NAV_ITEMS = [("fadelogistics", "fadelogistics.html", "FadeLogistics"), ("ai", "ai-automation.html", "AI automation"),
             ("pricing", "pricing.html", "Pricing"), ("blog", "blog/index.html", "Blog"),
             ("resources", "resources/index.html", "Free AI tools"),
             ("about", "about.html", "About"), ("contact", "contact.html", "Contact")]

def nav(P, active=None):
    links = "\n".join(f'        <a href="{P}{h}"{" class=\"active\" aria-current=\"page\"" if k == active else ""}>{t}</a>' for k, h, t in NAV_ITEMS)
    return f'''  <div class="scroll-progress" id="scroll-progress"></div>
  <div class="cursor" id="cursor" aria-hidden="true"></div>

  <!-- ===== NAVBAR ===== -->
  <header class="nav" id="navbar">
    <div class="nav-pill">
      <a href="{P}index.html" class="brand" aria-label="FadeFlow home">
        <img src="{P}logo.svg" alt="FadeFlow logo" width="25" height="28" />
        <span>FadeFlow</span>
      </a>
      <nav class="nav-links" id="nav-links" aria-label="Main">
{links}
      </nav>
      <a href="{P}contact.html" class="btn btn-ink nav-cta">Book a demo <span class="arrow">&rarr;</span></a>
      <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button>
    </div>
  </header>
'''

def footer(P):
    return f'''  <!-- ===== FOOTER ===== -->
  <footer class="footer" id="footer">
    <div class="wrap">
      <div class="footer-top">
        <div>
          <a href="{P}index.html" class="brand" aria-label="FadeFlow home"><img src="{P}logo-white.svg" alt="FadeFlow logo" width="25" height="28" /><span>FadeFlow</span></a>
          <p class="footer-tag">AI workflow automation for SMEs in the UAE &amp; India. Founded 2023.</p>
          <div class="footer-social">
            <a href="https://www.linkedin.com/company/fadeflow" aria-label="FadeFlow on LinkedIn" target="_blank" rel="noopener"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
            <a href="https://www.instagram.com/time.fade" aria-label="FadeFlow on Instagram (@time.fade)" target="_blank" rel="noopener"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
          </div>
        </div>
        <div class="footer-col">
          <h5>Product</h5>
          <ul>
            <li><a href="{P}fadelogistics.html">FadeLogistics</a></li>
            <li><a href="{P}ai-automation.html">AI Automation</a></li>
            <li><a href="{P}pricing.html">Pricing</a></li>
            <li><a href="{APP}" target="_blank" rel="noopener">Open the app &#8599;</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Company</h5>
          <ul>
            <li><a href="{P}about.html">About</a></li>
            <li><a href="{P}about.html#team">Team</a></li>
            <li><a href="{P}blog/index.html">Blog</a></li>
            <li><a href="{P}resources/index.html">Free AI resources</a></li>
            <li><a href="{P}experiments/index.html">time.fade experiments</a></li>
            <li><a href="{P}contact.html">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Get in touch</h5>
          <ul>
            <li><a href="mailto:sales@fadeflow.in">sales@fadeflow.in</a></li>
            <li><a href="mailto:tech@fadeflow.in">tech@fadeflow.in</a></li>
            <li><a href="tel:{PHONE}">{PHONE_H}</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-word" aria-hidden="true">FadeFlow</div>
    <div class="footer-bottom wrap">
      <span>&copy; 2023&ndash;2026 FadeFlow. All rights reserved.</span>
      <span><a href="{P}legal.html#privacy">Privacy</a> &middot; <a href="{P}legal.html#terms">Terms</a> &middot; <a href="{P}legal.html#cookies">Cookies</a></span>
    </div>
  </footer>
'''

def cta(P, title='Let&rsquo;s automate your <span class="serif">workflow.</span>',
        sub="Tell us how your team works today &mdash; we&rsquo;ll show you what we can take off their plate."):
    return f'''  <!-- ===== FINAL CTA ===== -->
  <section class="cta" id="cta">
    <div class="cta-spot" id="cta-spot"></div>
    <div class="wrap">
      <h2 class="split">{title}</h2>
      <p class="reveal">{sub}</p>
      <div class="cta-actions reveal">
        <a href="{P}contact.html" class="btn btn-yellow" data-magnetic>Book a demo <span class="arrow">&rarr;</span></a>
        <a href="{P}pricing.html" class="btn btn-line-light" data-magnetic>See pricing</a>
      </div>
      <div class="cta-mails reveal">
        <span>Sales &mdash; <a href="mailto:sales@fadeflow.in">sales@fadeflow.in</a></span>
        <span>Tech &mdash; <a href="mailto:tech@fadeflow.in">tech@fadeflow.in</a></span>
        <span>Call / WhatsApp &mdash; <a href="tel:{PHONE}">{PHONE_H}</a></span>
      </div>
    </div>
  </section>
'''

def crumbs_html(P, crumbs):
    parts = []
    for i, (n, p) in enumerate(crumbs):
        href = P + (p.lstrip("/") + "index.html" if p.endswith("/") else p.lstrip("/"))
        if i == len(crumbs) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{href}">{esc(n)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "".join(parts) + "</nav>"

def faq_html(faqs):
    items = "\n".join(f'''        <details class="faq-item reveal"{" open" if i == 0 else ""}>
          <summary>{q}<span class="faq-ico" aria-hidden="true"></span></summary>
          <div class="faq-a"><p>{a}</p></div>
        </details>''' for i, (q, a) in enumerate(faqs))
    return f'      <div class="faq">\n{items}\n      </div>'

def page(head_html, P, active, body, cta_html=None, scripts=""):
    return f'''{head_html}
<body>

{nav(P, active)}
  <main>
{body}
  </main>

{cta_html if cta_html is not None else cta(P)}
{footer(P)}
  <script src="{P}app.js"></script>{scripts}
</body>
</html>
'''

ICON = {
 "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
 "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "box": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
 "agent": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/><polyline points="16 11 18 13 22 9"/>',
 "money": '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
 "pulse": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
 "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
 "mail": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
 "chat": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
 "scan": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><circle cx="11.5" cy="14.5" r="2.5"/><line x1="13.3" y1="16.3" x2="15" y2="18"/>',
 "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/>',
 "reply": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 "bell": '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
 "bolt": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
}
def ico(k): return f'<div class="who-ico"><svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">{ICON[k]}</svg></div>'

def fgrid(items):
    out = []
    for k, t, d, *rest in items:
        lis = "".join(f"<li>{x}</li>" for x in rest[0]) if rest else ""
        out.append(f'        <div class="fcard reveal">{ico(k)}<h3>{t}</h3><p>{d}</p>{"<ul>" + lis + "</ul>" if lis else ""}</div>')
    return '      <div class="fgrid">\n' + "\n".join(out) + "\n      </div>"

# ================================================================ CONTENT
AI_USES = [
 ("doc", "Invoice generation", "Create accurate invoices automatically from job details, timesheets or delivery records &mdash; no retyping."),
 ("chart", "Business analytics", "Ask questions about your business in plain language and get clear answers on revenue, costs and trends."),
 ("mail", "Email filtering", "Sort incoming email by priority, route it to the right person and flag what needs a reply today."),
 ("chat", "WhatsApp lead qualifying", "Reply to WhatsApp enquiries instantly, ask the right questions and pass only qualified leads to your sales team."),
 ("scan", "Document data extraction", "Read POs, bills, receipts and shipping documents and enter the data into your system automatically."),
 ("pen", "Quotation drafting", "Turn a customer request into a ready-to-send quotation in minutes, using your own rates and templates."),
 ("reply", "Customer reply drafting", "Draft replies to common customer questions in your tone, ready for your team to review and send."),
 ("bell", "Payment follow-ups", "Track unpaid invoices and send polite, timely payment reminders without anyone chasing manually."),
 ("clock", "Daily summaries &amp; reports", "Get a short daily summary of jobs, sales and pending tasks delivered to your inbox or WhatsApp."),
]

LOGI_FEATURES = [
 ("doc", "Job cards", "Create and manage every logistics job in one place, from first request to final delivery.", ["Draft &rarr; ongoing &rarr; completed status", "One card per job, every detail attached", "Find any past job in seconds"]),
 ("pulse", "Status tracking", "Always know which jobs are pending, ongoing or done &mdash; without calling anyone.", ["Live overview of open work", "No more &ldquo;where is this shipment?&rdquo;", "Clear ownership per job"]),
 ("users", "Customers", "A full customer database &mdash; shipping lines, traders and companies &mdash; with every job card linked to each customer.", ["Complete job history per customer", "Contacts in one place, not five sheets"]),
 ("box", "Suppliers", "Manage suppliers and their costs, linked directly to the jobs they work on.", ["Supplier costs per job", "See who you work with most"]),
 ("agent", "Agents", "Manage your logistics agents across the UAE and India. Assign them to jobs and see who is handling what.", ["Assign agents to job cards", "Workload visible at a glance"]),
 ("money", "Trip &amp; operational expenses", "Track every operational and trip expense per job card so you never lose margin on a shipment.", ["Expenses linked to the job", "Spot unprofitable jobs early"]),
]

HOME_FAQ = [
 ("What does FadeFlow do?", "FadeFlow reduces manual work for small and medium businesses in the UAE and India. We offer FadeLogistics, workflow software for transport and logistics companies, and custom AI workflow automation that handles repetitive tasks like invoicing, email filtering, WhatsApp lead qualifying and daily reports."),
 ("What is FadeLogistics?", 'FadeLogistics is FadeFlow&rsquo;s workflow management software for transport and logistics companies. It brings job cards, status tracking, customers, suppliers, agents and trip expenses into one place. <a href="fadelogistics.html">See all features</a>.'),
 ("Do I need to replace my current software to use AI automation?", "No. We study how your team already works and build the AI automation around your existing tools &mdash; email, WhatsApp, spreadsheets and the software you use today. Nothing needs to be replaced."),
 ("Which AI does FadeFlow use?", "We build our automations with Claude AI by Anthropic, configured around your business rules, templates and data."),
 ("Where does FadeFlow work?", "FadeFlow serves small and medium businesses across the United Arab Emirates and India. Founded in 2023, our team works directly with each client."),
 ("How much does FadeFlow cost?", 'FadeLogistics starts from AED 125 per month (AED 1,499 per company per year). Custom packages are quoted after we understand your workflow. <a href="pricing.html">See pricing</a>.'),
]

LOGI_FAQ = [
 ("Who is FadeLogistics for?", "Transport and logistics companies in the UAE and India that manage jobs, customers, suppliers and agents &mdash; especially teams currently running operations on Excel sheets and WhatsApp groups."),
 ("How do I log in to FadeLogistics?", f'FadeLogistics runs in your browser at <a href="{APP}" target="_blank" rel="noopener">application.fadelogistics.fadeflow.in</a>. There is nothing to install.'),
 ("How much does FadeLogistics cost?", 'The Starter package starts from AED 125 per month (AED 1,499 per company per year) and includes training, workflow consulting and maintenance in the first year. <a href="pricing.html">See pricing</a>.'),
 ("Is training included?", "Yes. Full team training, workflow consulting, maintenance, updates and direct support are included in the first year of the Starter package."),
 ("Can I add AI automation later?", 'Yes. When you&rsquo;re ready, our custom package adds AI automation for invoices, follow-ups, reports and more on top of FadeLogistics. <a href="ai-automation.html">Learn about AI automation</a>.'),
 ("Is my data safe?", 'Your business data stays yours &mdash; we never sell or share it. Data is stored using industry-standard practices including encryption in transit and at rest. Read our <a href="legal.html#privacy">privacy policy</a>.'),
]

AI_FAQ = [
 ("What tasks can FadeFlow automate with AI?", "Common examples are invoice generation, business analytics in plain language, email filtering, WhatsApp lead qualifying, document data extraction, quotation drafting, customer reply drafting, payment follow-ups and daily summaries. If a task is repetitive and follows rules, it can usually be automated."),
 ("Do we have to change our software or systems?", "No. Our approach is to automate your current workflow without changing the systems you already use. Your team keeps working in the same tools."),
 ("Which AI model do you use?", "We build on Claude AI by Anthropic, set up with your business rules, templates, tone of voice and data."),
 ("Will the AI send things without our approval?", "You decide. Tasks can run fully automatically, or the AI can prepare drafts &mdash; replies, quotations, invoices &mdash; for your team to review and send."),
 ("How is AI automation priced?", 'AI automation is part of our custom package. We first study your workflow, then give you a quote that fits the work being automated. <a href="pricing.html">See pricing</a>.'),
 ("How do we get started?", 'Book a demo or email <a href="mailto:sales@fadeflow.in">sales@fadeflow.in</a>. We&rsquo;ll learn how your team works, identify the repetitive tasks and show you what can be automated first.'),
]

PRICING_FAQ = [
 ("How much does FadeLogistics cost?", "The FadeLogistics Starter package starts from AED 125 per month, which is AED 1,499 per company, per year."),
 ("What is included in the Starter package?", "All FadeLogistics features &mdash; job cards, status tracking, customers, suppliers, agents and expenses &mdash; with unlimited job cards, customers, suppliers and agents. Full team training, workflow consulting, maintenance, updates and direct support are included in the first year."),
 ("How is the Custom package priced?", "We study your current workflow and repetitive tasks first. Once we understand what needs to be built and automated, we send a quote that fits your business."),
 ("Is the price per user?", "The Starter price is per company, per year."),
 ("Can I see FadeLogistics before buying?", 'Yes. <a href="contact.html">Book a demo</a> and we&rsquo;ll walk you through the full workflow for your business.'),
 ("Which currency are prices in?", 'Prices are shown in UAE dirhams (AED). For anything else, email <a href="mailto:sales@fadeflow.in">sales@fadeflow.in</a>.'),
]

# ---------------------------------------------------------------- BLOG
POSTS = [
 dict(slug="ai-invoice-automation-for-smes", tag="AI Automation", date="2026-11-03",
  title="How SMEs Can Automate Invoicing with AI (Without New Software)",
  seo="Automate Invoicing with AI: A Guide for SMEs | FadeFlow",
  desc="How UAE and India SMEs can use AI to create invoices from job cards, timesheets and delivery notes, and chase payments, using the tools they already have.",
  lede="Invoicing is one of the most repetitive jobs in any small business. Here&rsquo;s how AI can take it over &mdash; without forcing you onto new accounting software.",
  body='''
<h2 id="why">Why invoicing eats so many hours</h2>
<p>In most SMEs, an invoice is the last step of a long chain. A job is agreed on WhatsApp, the details live in a spreadsheet or a job card, the delivery is confirmed by phone, and finally someone retypes all of it into an invoice template. Then someone else has to remember to chase the payment.</p>
<p>None of these steps is hard. They are just <strong>repetitive, easy to forget and easy to get wrong</strong> &mdash; a wrong amount, a missing reference number, an invoice that goes out a week late. That is exactly the kind of work AI is good at.</p>

<h2 id="what">What AI invoice automation actually does</h2>
<p>AI invoice automation is not a new accounting system. It is a set of automated steps that sits around the tools you already use:</p>
<ol>
<li><strong>Collects the source data</strong> &mdash; job details, timesheets, delivery records or a confirmed quotation.</li>
<li><strong>Fills your own invoice template</strong> with the right customer, line items, rates and references.</li>
<li><strong>Checks for gaps</strong> such as missing prices, duplicate invoices or amounts that don&rsquo;t match the quotation.</li>
<li><strong>Sends it for approval or straight to the customer</strong>, depending on the rules you set.</li>
<li><strong>Follows up on unpaid invoices</strong> with polite, timely reminders.</li>
</ol>

<h2 id="data">Where the invoice data comes from</h2>
<p>The key question is not &ldquo;which AI?&rdquo; but &ldquo;where does the information already live?&rdquo; For most businesses it is a mix of:</p>
<ul>
<li>Job cards or order records (for example in <a href="../fadelogistics.html">FadeLogistics</a>)</li>
<li>Excel or Google Sheets used for timesheets and rates</li>
<li>Delivery notes, POs and receipts arriving as PDFs or photos</li>
<li>Confirmations sent by email or WhatsApp</li>
</ul>
<p>AI can read structured data like spreadsheets and unstructured data like a scanned delivery note. That is what makes it possible to automate invoicing without first cleaning up every system you have.</p>

<h2 id="rollout">A simple four-step rollout</h2>
<ol>
<li><strong>Map today&rsquo;s process.</strong> Write down every step from &ldquo;job done&rdquo; to &ldquo;payment received&rdquo;, and who does it.</li>
<li><strong>Pick one invoice type.</strong> Start with your most common, most predictable invoices.</li>
<li><strong>Run in draft mode first.</strong> Let the AI prepare invoices that a person approves. Compare them with what your team would have sent.</li>
<li><strong>Automate the follow-ups.</strong> Once drafts are reliable, add automatic payment reminders &mdash; often the quickest win.</li>
</ol>

<h2 id="human">What should stay human</h2>
<p>Good automation keeps people in charge of decisions. Your team should still approve unusual invoices, handle disputes and agree special terms with key customers. Your invoices must also follow local tax rules such as UAE VAT or India GST, so keep your accountant involved when setting up templates.</p>
<blockquote>Automate the typing and the chasing. Keep the judgement.</blockquote>

<h2 id="mistakes">Common mistakes to avoid</h2>
<ul>
<li><strong>Replacing systems first.</strong> You rarely need new software to automate invoicing.</li>
<li><strong>Skipping the draft phase.</strong> Trust is built by checking the first batches.</li>
<li><strong>Forgetting follow-ups.</strong> Sending invoices faster helps; collecting payment faster helps more.</li>
</ul>

<h2 id="start">Getting started</h2>
<p>FadeFlow builds AI invoice automation for SMEs in the UAE and India using Claude AI, around the tools you already have. <a href="../ai-automation.html">See how our AI workflow automation works</a> or <a href="../contact.html">book a demo</a> to talk through your invoicing process.</p>
'''),
 dict(slug="whatsapp-lead-qualification-with-ai", tag="Sales", date="2026-11-03",
  title="WhatsApp Lead Qualification with AI: A Practical Guide for SMEs",
  seo="WhatsApp Lead Qualification with AI for SMEs | FadeFlow",
  desc="Most SME enquiries in the UAE and India arrive on WhatsApp. How AI can reply instantly, qualify leads and pass only serious buyers to your sales team.",
  lede="Your customers already message you on WhatsApp. The problem is answering every enquiry quickly, asking the right questions and spotting the serious buyers. AI can do the first part for you.",
  body='''
<h2 id="why">Why WhatsApp is where your leads are</h2>
<p>For small and medium businesses in the UAE and India, WhatsApp is often the main sales channel. Customers find your number on a website, a listing or a business card and send a message instead of filling in a form.</p>
<p>That&rsquo;s great for customers &mdash; and hard for your team. Messages arrive at all hours, in different formats, mixed in with existing customers, suppliers and staff. Some enquiries are ready to buy. Many just want a price. A few are not a fit at all.</p>

<h2 id="slow">The real cost of slow replies</h2>
<p>When a reply takes hours, a buyer has often already messaged two competitors. When your salesperson spends the day answering the same five questions, they have less time for the customers who are ready to decide. Slow or inconsistent first replies quietly lose business.</p>

<h2 id="qualify">What &ldquo;qualifying&rdquo; a lead means</h2>
<p>Qualifying means finding out quickly whether an enquiry is worth your sales team&rsquo;s time. Define your own criteria first. Typical ones are:</p>
<ul>
<li><strong>Need</strong> &mdash; what service or product do they want?</li>
<li><strong>Location</strong> &mdash; is it an area you serve?</li>
<li><strong>Size or budget</strong> &mdash; is the job in your range?</li>
<li><strong>Timeline</strong> &mdash; do they need it this week or &ldquo;sometime&rdquo;?</li>
</ul>

<h2 id="how">How an AI qualification flow works</h2>
<ol>
<li><strong>Instant, friendly reply</strong> in your business&rsquo;s tone, any time of day.</li>
<li><strong>A few smart questions</strong> based on your criteria &mdash; asked naturally, not like a form.</li>
<li><strong>Answers common questions</strong> such as services, areas covered or what information you need for a quote.</li>
<li><strong>Scores the lead</strong> against your rules.</li>
<li><strong>Hands over qualified leads</strong> to the right salesperson with a short summary, so nobody has to scroll back through the chat.</li>
</ol>

<h2 id="human">Keep it human</h2>
<p>AI should open the conversation, not close the deal. Make it easy for a customer to reach a person, let your team take over a chat at any point, and review conversations regularly to improve the questions. Customers care about quick, useful answers &mdash; not about whether the first reply was typed by a person.</p>

<h2 id="checklist">Setup checklist</h2>
<ul>
<li>Write down your qualification criteria and the questions that reveal them.</li>
<li>Collect your ten most common customer questions and the right answers.</li>
<li>Decide who receives which type of lead.</li>
<li>Agree when the AI should hand over to a person immediately.</li>
<li>Review a sample of conversations every week for the first month.</li>
</ul>

<h2 id="start">Getting started</h2>
<p>WhatsApp lead qualifying is one of the AI automations FadeFlow builds for SMEs, alongside email filtering and customer reply drafting. <a href="../ai-automation.html">Explore AI workflow automation</a> or <a href="../contact.html">talk to us</a> about your enquiry flow.</p>
'''),
 dict(slug="logistics-job-cards-excel-vs-software", tag="Logistics", date="2026-11-03",
  title="Logistics Job Cards: Why Excel Breaks and What to Use Instead",
  seo="Logistics Job Cards: Excel vs Job Card Software | FadeFlow",
  desc="Running logistics jobs on Excel and WhatsApp works until it doesn't. Where spreadsheets fail, and what a job card system like FadeLogistics changes.",
  lede="Almost every small logistics company starts with a spreadsheet and a WhatsApp group. It works &mdash; until the business grows and nobody is sure which version of the sheet is right.",
  body='''
<h2 id="what">What is a logistics job card?</h2>
<p>A job card is the single record of one logistics job: the customer, the route or shipment details, the supplier and agent involved, the status and every cost along the way. When it&rsquo;s complete, anyone in the team can answer &ldquo;where are we with this job?&rdquo; without asking around.</p>

<h2 id="today">How most small logistics companies run jobs today</h2>
<p>Typically, a request arrives on WhatsApp or by phone. Someone adds a row to an Excel sheet. Updates are shared in a group chat. Expenses are noted on paper or in a separate file. At month-end, someone tries to put it all together.</p>

<h2 id="breaks">Five places where Excel breaks</h2>
<ol>
<li><strong>Versions.</strong> <em>jobs_final_v3.xlsx</em> on one laptop, <em>jobs_final_v4.xlsx</em> on another. Nobody knows which is right.</li>
<li><strong>Status is unclear.</strong> A cell that says &ldquo;ongoing&rdquo; was last updated three days ago &mdash; or was it?</li>
<li><strong>Expenses are disconnected.</strong> Trip and operational costs live somewhere else, so you only learn a job lost money weeks later.</li>
<li><strong>Suppliers and agents are scattered.</strong> Who handled which job, at what cost, is buried in chats.</li>
<li><strong>No history.</strong> When a customer asks about a job from last year, finding it takes an afternoon.</li>
</ol>

<h2 id="should">What a job card system should do</h2>
<ul>
<li>Create one job card per job, with a clear status from draft to ongoing to completed.</li>
<li>Link every job to its customer, supplier and agent.</li>
<li>Record trip and operational expenses against the job, so margin is visible.</li>
<li>Show the whole team what is pending, ongoing and done.</li>
<li>Keep a searchable history of every job.</li>
</ul>

<h2 id="fadelogistics">How FadeLogistics handles it</h2>
<p><a href="../fadelogistics.html">FadeLogistics</a> is FadeFlow&rsquo;s workflow software built for exactly this. It brings job cards, status tracking, customers, suppliers, agents and trip expenses into one place, and runs in the browser, so there&rsquo;s nothing to install. Teams across the UAE and India use it to replace the spreadsheet-and-WhatsApp routine.</p>

<h2 id="switch">Switching without disrupting operations</h2>
<ol>
<li>Start with new jobs only &mdash; don&rsquo;t try to migrate years of history on day one.</li>
<li>Add your active customers, suppliers and agents first.</li>
<li>Agree as a team that job status is updated in one place only.</li>
<li>Review open jobs together weekly for the first month.</li>
</ol>
<p>FadeLogistics Starter includes team training and workflow consulting in the first year. <a href="../pricing.html">See pricing</a> or <a href="../contact.html">book a demo</a>.</p>
'''),
 dict(slug="repetitive-tasks-smes-can-automate", tag="AI Automation", date="2026-11-03",
  title="9 Repetitive Tasks Every SME Can Automate with AI",
  seo="9 Repetitive Tasks SMEs Can Automate with AI | FadeFlow",
  desc="From invoices and quotations to WhatsApp enquiries and daily reports: nine everyday tasks small and medium businesses in the UAE and India can hand to AI first.",
  lede="You don&rsquo;t need a big transformation project to benefit from AI. Start with the boring, repetitive work your team does every day. Here are nine places to begin.",
  body='''
<h2 id="list">The nine tasks</h2>
<h3>1. Invoice generation</h3>
<p>Create invoices automatically from job details, timesheets or delivery records instead of retyping them. <a href="ai-invoice-automation-for-smes.html">Read our invoicing guide</a>.</p>
<h3>2. Business analytics</h3>
<p>Ask questions like &ldquo;which customers brought the most revenue this quarter?&rdquo; in plain language and get a clear answer, without building reports by hand.</p>
<h3>3. Email filtering</h3>
<p>Sort incoming email by priority, route it to the right person and flag what needs a reply today.</p>
<h3>4. WhatsApp lead qualifying</h3>
<p>Reply to enquiries instantly, ask the right questions and pass only qualified leads to sales. <a href="whatsapp-lead-qualification-with-ai.html">See how it works</a>.</p>
<h3>5. Document data extraction</h3>
<p>Read POs, bills, receipts and shipping documents and enter the data into your system automatically.</p>
<h3>6. Quotation drafting</h3>
<p>Turn a customer request into a ready-to-send quotation in minutes, using your own rates and templates.</p>
<h3>7. Customer reply drafting</h3>
<p>Draft replies to common questions in your tone, ready for your team to review and send.</p>
<h3>8. Payment follow-ups</h3>
<p>Track unpaid invoices and send polite, timely reminders without anyone chasing manually.</p>
<h3>9. Daily summaries and reports</h3>
<p>Receive a short daily summary of jobs, sales and pending tasks in your inbox or on WhatsApp.</p>

<h2 id="choose">How to choose your first automation</h2>
<p>Pick the task that scores highest on these three questions:</p>
<ul>
<li><strong>How often does it happen?</strong> Daily tasks pay back faster than monthly ones.</li>
<li><strong>How rule-based is it?</strong> The clearer the rules, the easier to automate reliably.</li>
<li><strong>How painful is a mistake or delay?</strong> Late invoices and missed leads cost real money.</li>
</ul>
<div class="callout">For many SMEs, payment follow-ups, email filtering or WhatsApp lead replies are the quickest wins: frequent, rule-based and directly tied to revenue.</div>

<h2 id="start">Getting started</h2>
<p>FadeFlow learns your company&rsquo;s repetitive tasks and automates them with Claude AI, without changing the systems you already use. <a href="../ai-automation.html">Explore AI workflow automation</a> or <a href="../contact.html">book a demo</a>.</p>
'''),
 dict(slug="ai-automation-without-replacing-systems", tag="Strategy", date="2026-11-03",
  title="AI Automation Without Replacing Your Systems: How It Works",
  seo="AI Automation Without Replacing Your Systems | FadeFlow",
  desc="You don't need new software to benefit from AI. How FadeFlow automates work around the email, WhatsApp, spreadsheets and apps your team already uses.",
  lede="Many SMEs put off automation because they think it means replacing everything. It doesn&rsquo;t. The best automation often fits around the tools your team already knows.",
  body='''
<h2 id="trap">The replacement trap</h2>
<p>The usual pitch is: move everything onto one new platform and your problems disappear. In practice, switching systems means months of setup, retraining, migrated data and staff who quietly go back to their old spreadsheets. For a small or medium business, that disruption can cost more than the manual work it was meant to remove.</p>

<h2 id="around">The alternative: automate around what works</h2>
<p>Your team already has a way of working &mdash; email, WhatsApp, Excel or Google Sheets, and maybe accounting or industry software. Most of the manual effort sits in the <strong>gaps between those tools</strong>: copying data from a message into a sheet, from a sheet into an invoice, from an inbox into a task list. AI is very good at filling exactly those gaps.</p>

<h2 id="how">How FadeFlow does it</h2>
<ol>
<li><strong>Learn.</strong> We study how your team works today and find the repetitive tasks.</li>
<li><strong>Automate.</strong> We build AI automation, using Claude AI, around your existing workflow.</li>
<li><strong>Keep your systems.</strong> No new software to switch to. Your current tools stay as they are.</li>
</ol>

<h2 id="connects">What it typically connects to</h2>
<ul>
<li>Email inboxes, for filtering, routing and reply drafts</li>
<li>WhatsApp, for instant replies and lead qualifying</li>
<li>Spreadsheets, for data entry, reporting and analytics</li>
<li>Documents such as POs, bills and receipts, for data extraction</li>
<li>The business software you already run</li>
</ul>

<h2 id="team">What changes for your team</h2>
<p>Very little, on the surface &mdash; and that&rsquo;s the point. People keep using the same tools, but the copying, chasing and sorting happens automatically. Drafts appear ready for review. Leads arrive already qualified. Reports land in the inbox each morning.</p>

<h2 id="when">When new software does make sense</h2>
<p>Sometimes there is no system to build around &mdash; for example a logistics company running every job on paper and chat. In that case a focused tool helps. That&rsquo;s why we built <a href="../fadelogistics.html">FadeLogistics</a> for transport and logistics teams, and why AI automation can be added on top of it later.</p>

<h2 id="start">Next step</h2>
<p>Tell us how your team works today and we&rsquo;ll show you what can be automated first. <a href="../ai-automation.html">See AI workflow automation</a> or <a href="../contact.html">book a demo</a>.</p>
'''),
]
for p in POSTS:
    p["words"] = len(strip(p["body"]).split())
    p["mins"] = max(3, round(p["words"] / 200))
    p["toc"] = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p["body"])

def nice_date(d): return datetime.strptime(d, "%Y-%m-%d").strftime("%d %b %Y").lstrip("0")

def post_card(p, P, featured=False):
    return f'''        <a href="{P}{p["slug"]}.html" class="post-card reveal{" featured" if featured else ""}">
          <span class="post-tag">{p["tag"]}</span>
          <h3>{p["title"]}</h3>
          <p>{strip(p["desc"])}</p>
          <div class="post-meta"><span>{nice_date(p["date"])} &middot; {p["mins"]} min read</span><span class="post-go" aria-hidden="true">&rarr;</span></div>
        </a>'''

# ================================================================ PAGES
def hero(P, crumbs, label, title, sub, actions=""):
    return f'''    <section class="page-hero">
      <div class="container">
        {crumbs_html(P, crumbs)}
        <div class="page-hero-label">{label}</div>
        <h1 class="page-hero-title split">{title}</h1>
        <p class="page-hero-sub reveal">{sub}</p>{f'{chr(10)}        <div class="page-hero-actions reveal">{actions}</div>' if actions else ""}
      </div>
    </section>
'''

# ---- FadeLogistics
P = ""
path = "/fadelogistics.html"
title = "FadeLogistics: Logistics Job Card Software | FadeFlow"
desc = "Job cards, status tracking, customers, suppliers, agents and trip expenses in one place. Logistics workflow software for SMEs in the UAE & India."
crumbs = [("Home", "/"), ("FadeLogistics", path)]
software = {"@type": "SoftwareApplication", "@id": f"{SITE}/fadelogistics.html#software", "name": "FadeLogistics",
  "applicationCategory": "BusinessApplication", "applicationSubCategory": "Logistics workflow management",
  "operatingSystem": "Web browser", "url": f"{SITE}/fadelogistics.html", "installUrl": APP,
  "description": desc, "image": f"{SITE}/app-screenshot.jpg", "screenshot": f"{SITE}/app-screenshot.jpg",
  "featureList": ["Job cards with draft, ongoing and completed status", "Status tracking", "Customer database",
                  "Supplier management", "Agent management across UAE and India", "Trip and operational expense tracking"],
  "publisher": {"@id": f"{SITE}/#organization"}, "areaServed": ["AE", "IN"],
  "offers": {"@type": "Offer", "name": "FadeLogistics Starter", "price": "1499", "priceCurrency": "AED",
             "url": f"{SITE}/pricing.html", "availability": "https://schema.org/InStock",
             "priceSpecification": {"@type": "UnitPriceSpecification", "price": "1499", "priceCurrency": "AED",
                                    "unitText": "per company per year", "billingDuration": "P1Y"}}}
body = hero(P, crumbs, "Product &middot; Logistics workflow software",
  'Every logistics job. One calm <span class="serif">place.</span>',
  "FadeLogistics is workflow software for transport &amp; logistics companies. Job cards, status tracking, customers, suppliers, agents and trip expenses &mdash; no more chasing WhatsApp groups and Excel sheets.",
  f'<a href="{APP}" class="btn btn-ink" target="_blank" rel="noopener" data-magnetic>Open FadeLogistics <span class="arrow">&rarr;</span></a><a href="pricing.html" class="btn btn-line" data-magnetic>From AED 125/month</a>') + f'''
    <section class="page-content">
      <div class="container">
        <div class="block reveal">
          <div class="shot-frame">
            <div class="browser"><div class="browser-bar"><i></i><i></i><i></i><span>application.fadelogistics.fadeflow.in</span></div>
            <img src="app-screenshot.jpg" alt="FadeLogistics dashboard showing active jobs, quotations, invoices and business overview" width="1600" height="900" loading="lazy" /></div>
          </div>
        </div>

        <div class="block">
          <div class="block-head">
            <div><div class="label reveal">Features</div><h2 class="split">Everything your operations team <span class="serif">handles.</span></h2></div>
            <p class="reveal">Built for how logistics SMEs in the UAE and India actually work &mdash; jobs, people, partners and costs, connected.</p>
          </div>
{fgrid(LOGI_FEATURES)}
        </div>

        <div class="block">
          <div class="block-head">
            <div><div class="label reveal">How it works</div><h2 class="split">From request to <span class="serif">delivered.</span></h2></div>
            <p class="reveal">A simple flow your whole team can follow from day one.</p>
          </div>
          <div class="numbered">
            <div class="reveal"><h3>Create the job card</h3><p>Log the request the moment it comes in &mdash; customer, details and status in one card.</p></div>
            <div class="reveal"><h3>Assign the team</h3><p>Link the supplier and agent handling it, so ownership is clear.</p></div>
            <div class="reveal"><h3>Track status &amp; costs</h3><p>Move the job from draft to ongoing, and log trip expenses as they happen.</p></div>
            <div class="reveal"><h3>Complete &amp; review</h3><p>Close the job with its full history and see whether it made money.</p></div>
          </div>
        </div>

        <div class="block">
          <div class="block-head">
            <div><div class="label reveal">Add AI when ready</div><h2 class="split">Then let AI take the <span class="serif">paperwork.</span></h2></div>
            <p class="reveal">Upgrade to our custom package and automate invoices, follow-ups, reports and more on top of FadeLogistics. <a class="link-u" href="ai-automation.html">See AI automation</a></p>
          </div>
        </div>

        <div class="block">
          <div class="block-head">
            <div><div class="label reveal">FAQ</div><h2 class="split">Questions about <span class="serif">FadeLogistics.</span></h2></div>
          </div>
{faq_html(LOGI_FAQ)}
        </div>
      </div>
    </section>'''
w("fadelogistics.html", page(head(title, desc, path, P, crumbs=crumbs, nodes=[software, faq_node(SITE + path, LOGI_FAQ)]), P, "fadelogistics", body,
  cta(P, 'Run your logistics on <span class="serif">FadeLogistics.</span>', "Start from AED 125 a month (AED 1,499 per company per year), with training and support included in the first year.")))

# ---- AI automation
path = "/ai-automation.html"
title = "AI Workflow Automation for SMEs, UAE & India | FadeFlow"
desc = "We learn your repetitive tasks and automate them with Claude AI: invoices, WhatsApp leads, email, quotations and reports, without changing your systems."
crumbs = [("Home", "/"), ("AI Automation", path)]
service = {"@type": "Service", "@id": f"{SITE}/ai-automation.html#service", "name": "AI Workflow Automation",
  "serviceType": "Business process automation with AI", "provider": {"@id": f"{SITE}/#organization"},
  "areaServed": [{"@type": "Country", "name": "United Arab Emirates"}, {"@type": "Country", "name": "India"}],
  "audience": {"@type": "BusinessAudience", "name": "Small and medium businesses (SMEs)"},
  "description": desc, "url": f"{SITE}/ai-automation.html",
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "AI automation use cases", "itemListElement": [
     {"@type": "Offer", "itemOffered": {"@type": "Service", "name": strip(t), "description": strip(d)}} for _, t, d in AI_USES]}}
uses_html = "\n".join(f'          <div class="use reveal"><span class="use-n">/{i+1:02d}</span><h3>{t}</h3><p>{d}</p><span class="use-arrow" aria-hidden="true">&rarr;</span></div>' for i, (_, t, d) in enumerate(AI_USES))
body = hero(P, crumbs, "Service &middot; Powered by Claude AI",
  'Automate the work. Keep your <span class="serif">systems.</span>',
  "We learn your company&rsquo;s repetitive tasks, then automate your current workflow with AI &mdash; without changing the systems you already use.",
  '<a href="contact.html" class="btn btn-ink" data-magnetic>Book a demo <span class="arrow">&rarr;</span></a><a href="#use-cases" class="btn btn-line" data-magnetic>See use cases</a>') + f'''
    <section class="page-content">
      <div class="container">
        <div class="block">
          <article class="offer offer-ai reveal">
            <div class="offer-ai-top">
              <div><div class="offer-num">OUR PROCESS</div><h2 style="font-size:clamp(2rem,4vw,3.2rem);font-weight:700;letter-spacing:-0.05em;line-height:1">Three steps. No disruption.</h2></div>
              <p>Most manual work sits in the gaps between your tools. That&rsquo;s exactly where we put AI to work.</p>
            </div>
            <div class="steps">
              <div class="steps-line"><i></i></div>
              <div class="step"><div class="step-dot">01</div><h3 style="font-size:1.5rem;font-weight:700;letter-spacing:-0.03em;margin-bottom:8px">Learn</h3><p>We study how your team works today and find the repetitive tasks.</p></div>
              <div class="step"><div class="step-dot">02</div><h3 style="font-size:1.5rem;font-weight:700;letter-spacing:-0.03em;margin-bottom:8px">Automate</h3><p>We build AI automation around your existing workflow using Claude AI.</p></div>
              <div class="step"><div class="step-dot">03</div><h3 style="font-size:1.5rem;font-weight:700;letter-spacing:-0.03em;margin-bottom:8px">Keep your systems</h3><p>No new software to switch to. Your current tools stay as they are.</p></div>
            </div>
          </article>
        </div>

        <div class="block" id="use-cases">
          <div class="block-head">
            <div><div class="label reveal">Use cases</div><h2 class="split">Where AI gives your team its <span class="serif">hours</span> back.</h2></div>
            <p class="reveal">Nine places we put AI to work for SMEs. Have a different repetitive task? <a class="link-u" href="mailto:sales@fadeflow.in?subject=AI%20Automation%20Enquiry">Tell us about it</a></p>
          </div>
          <div class="uses">
{uses_html}
          </div>
        </div>

        <div class="block">
          <div class="block-head">
            <div><div class="label reveal">Works with</div><h2 class="split">Fits the tools you <span class="serif">already</span> use.</h2></div>
            <p class="reveal">We connect AI to where your work already happens, so your team doesn&rsquo;t have to learn anything new.</p>
          </div>
          <div class="chips-light reveal">
            <span class="chip-light">Email inboxes</span><span class="chip-light">WhatsApp</span><span class="chip-light">Excel</span><span class="chip-light">Google Sheets</span><span class="chip-light">PDF documents &amp; scans</span><span class="chip-light">Your existing business software</span><span class="chip-light">FadeLogistics</span>
          </div>
        </div>

        <div class="block">
          <div class="block-head">
            <div><div class="label reveal">FAQ</div><h2 class="split">Questions about AI <span class="serif">automation.</span></h2></div>
          </div>
{faq_html(AI_FAQ)}
        </div>
      </div>
    </section>'''
w("ai-automation.html", page(head(title, desc, path, P, crumbs=crumbs, nodes=[service, faq_node(SITE + path, AI_FAQ)]), P, "ai", body))

# ---- Pricing
path = "/pricing.html"
title = "Pricing: FadeLogistics from AED 125/month | FadeFlow"
desc = "FadeLogistics Starter from AED 125/month (AED 1,499 per company per year), with training and support in year one. Custom packages built around your workflow."
crumbs = [("Home", "/"), ("Pricing", path)]
offers = {"@type": "OfferCatalog", "@id": f"{SITE}/pricing.html#plans", "name": "FadeFlow pricing", "itemListElement": [
  {"@type": "Offer", "name": "FadeLogistics Starter", "price": "1499", "priceCurrency": "AED", "url": f"{SITE}/pricing.html",
   "description": "All FadeLogistics features, unlimited job cards, customers, suppliers and agents. Training, workflow consulting and maintenance included in year one.",
   "itemOffered": {"@id": f"{SITE}/fadelogistics.html#software"},
   "priceSpecification": {"@type": "UnitPriceSpecification", "price": "1499", "priceCurrency": "AED", "unitText": "per company per year", "billingDuration": "P1Y"}},
  {"@type": "Offer", "name": "Custom Package", "url": f"{SITE}/pricing.html",
   "description": "A system customised to your workflow, with AI automation. Priced by quote after a study of your workflow.",
   "priceSpecification": {"@type": "PriceSpecification", "priceCurrency": "AED", "description": "Custom quote"}}]}
body = hero(P, crumbs, "Pricing", 'Simple, honest <span class="serif">pricing.</span>',
  "Start with our ready-made package, or let us build the system around the way you already work.") + f'''
    <section class="page-content">
      <div class="container">
        <div class="block">
          <div class="plans">
            <div class="plan plan-dark reveal">
              <span class="plan-badge">Most popular</span>
              <div class="plan-tag">Starter package</div>
              <h2>FadeLogistics</h2>
              <p class="plan-desc">Everything a logistics team needs to run jobs in one place.</p>
              <div class="plan-price"><small>AED</small><b>125</b><span>/month</span></div>
              <p class="plan-note">Starting price &middot; AED 1,499 per company, per year.</p>
              <ul>
                <li>All FadeLogistics features &mdash; job cards, customers, suppliers, agents &amp; expenses</li>
                <li>Unlimited job cards, customers, suppliers &amp; agents</li>
                <li>Full team training (first year)</li>
                <li>Workflow consulting (first year)</li>
                <li>Maintenance, updates &amp; direct support (first year)</li>
              </ul>
              <a href="{APP}" class="btn btn-yellow" target="_blank" rel="noopener" data-magnetic>Get started <span class="arrow">&rarr;</span></a>
            </div>
            <div class="plan reveal">
              <div class="plan-tag">Custom package</div>
              <h2>Built around your workflow</h2>
              <p class="plan-desc">We learn your flow, customise the system and automate it.</p>
              <div class="plan-price"><b class="txt">Custom quote</b></div>
              <p class="plan-note">You get a quote once we understand your needs.</p>
              <ul>
                <li>A study of your current workflow &amp; repetitive tasks</li>
                <li>System customised to the way your team works</li>
                <li>AI automation &mdash; invoices, analytics, email, WhatsApp leads &amp; more</li>
                <li>Works with the systems you already use</li>
                <li>Dedicated support from our team</li>
              </ul>
              <a href="mailto:sales@fadeflow.in?subject=Custom%20Package%20-%20Request%20a%20Quote" class="btn btn-ink" data-magnetic>Request a quote <span class="arrow">&rarr;</span></a>
            </div>
          </div>
        </div>

        <div class="block">
          <div class="block-head">
            <div><div class="label reveal">Compare</div><h2 class="split">What&rsquo;s <span class="serif">included.</span></h2></div>
          </div>
          <div class="table-wrap reveal">
            <table class="compare">
              <thead><tr><th scope="col">Feature</th><th scope="col">Starter</th><th scope="col">Custom</th></tr></thead>
              <tbody>
                <tr><td>Job cards &amp; status tracking</td><td class="y">&#10003;</td><td class="y">&#10003;</td></tr>
                <tr><td>Customers, suppliers &amp; agents</td><td class="y">Unlimited</td><td class="y">Unlimited</td></tr>
                <tr><td>Trip &amp; operational expenses</td><td class="y">&#10003;</td><td class="y">&#10003;</td></tr>
                <tr><td>Team training &amp; workflow consulting</td><td class="y">First year</td><td class="y">&#10003;</td></tr>
                <tr><td>Maintenance, updates &amp; support</td><td class="y">First year</td><td class="y">Dedicated</td></tr>
                <tr><td>System customised to your workflow</td><td class="n">&mdash;</td><td class="y">&#10003;</td></tr>
                <tr><td>Automation of repetitive tasks</td><td class="n">&mdash;</td><td class="y">&#10003;</td></tr>
                <tr><td>Works with your existing systems</td><td class="n">&mdash;</td><td class="y">&#10003;</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="block">
          <div class="block-head">
            <div><div class="label reveal">FAQ</div><h2 class="split">Pricing <span class="serif">questions.</span></h2></div>
          </div>
{faq_html(PRICING_FAQ)}
        </div>
      </div>
    </section>'''
w("pricing.html", page(head(title, desc, path, P, crumbs=crumbs, nodes=[offers, faq_node(SITE + path, PRICING_FAQ)]), P, "pricing", body,
  cta(P, 'Not sure which fits? <span class="serif">Ask us.</span>', "Tell us how your team works and we&rsquo;ll recommend the right package &mdash; no pressure.")))

# ---- Blog index
P = "../"
path = "/blog/"
title = "Blog: AI Automation Guides for SMEs | FadeFlow"
desc = "Practical guides on AI workflow automation, WhatsApp lead handling, invoicing and logistics operations for small and medium businesses in the UAE and India."
crumbs = [("Home", "/"), ("Blog", path)]
blog_node = {"@type": "Blog", "@id": f"{SITE}/blog/#blog", "name": "FadeFlow Blog", "url": f"{SITE}/blog/", "description": desc,
  "publisher": {"@id": f"{SITE}/#organization"}, "inLanguage": "en",
  "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/blog/{p['slug']}.html", "datePublished": p["date"]} for p in POSTS]}
cards = "\n".join(post_card(p, "", i == 0) for i, p in enumerate(POSTS))
body = hero(P, crumbs, "Blog", 'Guides for running a business with less manual <span class="serif">work.</span>',
  "Practical, no-hype articles on AI automation, sales, invoicing and logistics operations for SMEs in the UAE &amp; India.") + f'''
    <section class="page-content">
      <div class="container">
        <div class="post-grid">
{cards}
        </div>
      </div>
    </section>'''
w("blog/index.html", page(head(title, desc, path, P, page_type="CollectionPage", crumbs=crumbs, nodes=[blog_node]), P, "blog", body))

# ---- Blog posts
for p in POSTS:
    path = f"/blog/{p['slug']}.html"
    url = SITE + path
    crumbs = [("Home", "/"), ("Blog", "/blog/"), (strip(p["title"]), path)]
    art = {"@type": "BlogPosting", "@id": url + "#article", "headline": strip(p["title"]), "description": p["desc"],
           "image": {"@type": "ImageObject", "url": OG, "width": 1200, "height": 630},
           "datePublished": p["date"], "dateModified": DATE, "wordCount": p["words"], "articleSection": p["tag"],
           "inLanguage": "en", "mainEntityOfPage": {"@id": url + "#webpage"},
           "author": {"@type": "Organization", "name": "FadeFlow Team", "url": f"{SITE}/about.html"},
           "publisher": {"@id": f"{SITE}/#organization"}, "isPartOf": {"@id": f"{SITE}/blog/#blog"}}
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in p["toc"])
    related = [q for q in POSTS if q is not p][:3]
    rel = "\n".join(post_card(q, "") for q in related)
    body = f'''    <article>
      <header class="post-hero">
        <div class="container">
          {crumbs_html(P, crumbs)}
          <span class="post-tag reveal" style="display:inline-block">{p["tag"]}</span>
          <h1 class="split">{p["title"]}</h1>
          <p class="lede reveal">{p["lede"]}</p>
          <div class="post-info reveal"><span>By <b>FadeFlow Team</b></span><span>Published <b><time datetime="{p["date"]}">{nice_date(p["date"])}</time></b></span><span><b>{p["mins"]} min</b> read</span></div>
        </div>
      </header>
      <div class="container">
        <div class="post-layout">
          <div class="prose">
{p["body"].strip()}
          </div>
          <aside class="post-aside">
            <div class="aside-box"><h4>In this article</h4><ol>{toc}</ol></div>
            <div class="aside-box aside-cta"><h4>FadeFlow</h4><p>Want this automated in your business?</p><a href="../contact.html" class="btn btn-yellow">Book a demo <span class="arrow">&rarr;</span></a></div>
          </aside>
        </div>
      </div>
    </article>
    <section class="related">
      <div class="container">
        <h2>Keep reading</h2>
        <div class="post-grid">
{rel}
        </div>
      </div>
    </section>'''
    w(f"blog/{p['slug']}.html", page(head(p["seo"], p["desc"], path, P, crumbs=crumbs, nodes=[art], og_type="article", article=p), P, "blog", body))

# ================================================================ FREE RESOURCES (time.fade)
INSTA = "https://www.instagram.com/time.fade"

def acc(t):
    """Escape plain text; [word] becomes the serif accent."""
    return re.sub(r"\[(.+?)\]", r'<span class="serif">\1</span>', esc(t))

def plain(t): return t.replace("[", "").replace("]", "")

def block_head(label, title, sub=""):
    return f'''          <div class="block-head">
            <div><div class="label reveal">{esc(label)}</div><h2 class="split">{acc(title)}</h2></div>
            {f'<p class="reveal">{esc(sub)}</p>' if sub else ""}
          </div>'''

def copy_btn(target, label="Copy prompt", cls=""):
    return f'<button type="button" class="copy-btn{cls}" data-copy="{target}"><span class="copy-label">{label}</span> <span aria-hidden="true">&#8599;</span></button>'

def r_story(d):
    return f'''        <div class="block">
          <div class="story-card reveal">
            <div class="label">{esc(d["label"])}</div>
            <div class="story-big">{esc(d["big"])}</div>
            <p class="story-text">{esc(d["text"])}</p>
            <p class="story-sub">{esc(d["sub"])}</p>
          </div>
        </div>'''

def r_steps(d):
    steps = "\n".join(f'            <div class="how-step reveal"><span class="how-n">{i+1:02d}</span><div><h3>{esc(t)}</h3><p>{esc(x)}</p></div></div>'
                      for i, (t, x) in enumerate(d["steps"]))
    note = f'\n          <p class="res-note reveal">{esc(d["note"])}</p>' if d.get("note") else ""
    return f'''        <div class="block" id="start">
{block_head(d["label"], d["title"], d.get("sub", ""))}
          <div class="how-steps">
{steps}
          </div>{note}
        </div>'''

def r_prompt(d):
    after = f'\n          <p class="res-note reveal">{esc(d["after"])}</p>' if d.get("after") else ""
    pid = d["id"]
    return f'''        <div class="block" id="{pid}">
{block_head(d["label"], d["title"], d.get("sub", ""))}
          <div class="prompt-box reveal">
            <div class="prompt-head"><span>{esc(d["heading"])}</span>{copy_btn(pid + "-text")}</div>
            <pre id="{pid}-text">{esc(d["text"])}</pre>
          </div>{after}
        </div>'''

def r_examples(d):
    items = "\n".join(f'            <div class="ex-card reveal"><span class="how-n">{i+1:02d}</span><p>{esc(t)}</p></div>' for i, t in enumerate(d["items"]))
    note = f'\n          <p class="res-note reveal">{esc(d["note"])}</p>' if d.get("note") else ""
    return f'''        <div class="block">
{block_head(d["label"], d["title"], d.get("sub", ""))}
          <div class="ex-grid">
{items}
          </div>{note}
        </div>'''

def r_faq(d):
    return f'''        <div class="block">
{block_head(d["label"], d["title"], d.get("sub", ""))}
{faq_html([(esc(q), esc(a)) for q, a in d["items"]])}
        </div>'''

def r_bullets(d):
    items = "\n".join(f'            <div class="reveal"><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for t, x in d["items"])
    return f'''        <div class="block">
{block_head(d["label"], d["title"], d.get("sub", ""))}
          <div class="numbered">
{items}
          </div>
        </div>'''

FACE = {
 "front": '<circle cx="60" cy="52" r="26"/><circle cx="51" cy="49" r="2.6" class="f"/><circle cx="69" cy="49" r="2.6" class="f"/><path d="M52 62q8 6 16 0"/><path d="M22 118c4-22 20-32 38-32s34 10 38 32"/>',
 "angle": '<ellipse cx="62" cy="52" rx="23" ry="26"/><circle cx="58" cy="49" r="2.6" class="f"/><circle cx="74" cy="49" r="2.4" class="f"/><path d="M84 52l5 6-5 2"/><path d="M60 63q7 5 13 0"/><path d="M24 118c4-22 20-32 38-32s34 10 38 32"/>',
}
def r_photo_input(d):
    def card(k, tag, title):
        return f'''            <figure class="photo-card reveal">
              <svg viewBox="0 0 120 120" aria-hidden="true">{FACE[k]}</svg>
              <figcaption><span>{tag}</span><b>{title}</b></figcaption>
            </figure>'''
    return f'''        <div class="block">
          <div class="photo-input">
            <div>
              <div class="label reveal">{esc(d["label"])}</div>
              <h2 class="split" style="font-size:clamp(2rem,4.4vw,3.4rem);font-weight:700;letter-spacing:-0.05em;line-height:1;margin:14px 0 18px">{acc(d["title"])}</h2>
              <p class="reveal" style="color:var(--muted)">{esc(d["text"])}</p>
            </div>
{card("front", "Photo A / Front-facing", "Clear front selfie")}
{card("angle", "Photo B / Slight angle", "Same person, slight side angle")}
          </div>
        </div>'''

def r_library(d):
    chips = '<button type="button" class="lib-chip active" data-filter="all">All</button>' + "".join(
        f'<button type="button" class="lib-chip" data-filter="{k}">{esc(n)}</button>' for k, n in PHOTO_CATEGORIES)
    groups = []
    n = 0
    for key, name in PHOTO_CATEGORIES:
        looks = [l for l in LOOKS if l[0] == key]
        cards = []
        for cat, best, title, desc in looks:
            n += 1
            lid = f"look-{n:02d}"
            text = f"{title} {desc} {best} {name}".lower()
            cards.append(f'''              <article class="look-card" data-cat="{key}" data-text="{esc(text)}">
                <div class="look-top"><span class="look-n">{n:02d}</span><span class="look-best">Best for {esc(best)}</span></div>
                <h3>{esc(title)}</h3>
                <p>{esc(desc)}</p>
                <details class="look-full"><summary>Read full prompt</summary><pre id="{lid}">{esc(photo_prompt(title, desc))}</pre></details>
                {copy_btn(lid, cls=" light")}
              </article>''')
        first, last = n - len(looks) + 1, n
        groups.append(f'''          <section class="look-group" data-group="{key}">
            <div class="look-group-head"><h3>{esc(name)}</h3><span>{first:02d}&mdash;{last:02d}</span></div>
            <div class="look-grid">
{chr(10).join(cards)}
            </div>
          </section>''')
    return f'''        <div class="block" id="library">
{block_head(d["label"], d["title"], d.get("sub", ""))}
          <div class="lib-tools reveal">
            <label class="lib-search"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.5" y2="16.5"/></svg><input id="look-search" type="search" placeholder="Search titles, e.g. studio or LinkedIn" aria-label="Search looks" autocomplete="off" /></label>
            <div class="lib-chips">{chips}</div>
            <div class="lib-count"><span id="look-count">{len(LOOKS)} of {len(LOOKS)} looks</span><button type="button" id="look-reset">Reset filters &#8634;</button></div>
          </div>
{chr(10).join(groups)}
          <p class="lib-empty" id="look-empty" hidden>No looks match that search. <button type="button" class="link-u" id="look-reset-2">Reset filters</button></p>
        </div>'''

RENDER = {"story": r_story, "steps": r_steps, "prompt": r_prompt, "examples": r_examples, "faq": r_faq,
          "bullets": r_bullets, "photo_input": r_photo_input, "library": r_library}

def credit(P):
    return f'''        <div class="res-credit reveal">
          <a href="{INSTA}" target="_blank" rel="noopener">Guide by <b>@time.fade</b> &#8599;</a>
          <span>Make room for the work that matters.</span>
          <a href="{P}index.html">FadeFlow &mdash; software &amp; AI automation for businesses &#8599;</a>
        </div>'''

def resource_cta(P):
    return f'''  <!-- ===== FINAL CTA ===== -->
  <section class="cta" id="cta">
    <div class="cta-spot" id="cta-spot"></div>
    <div class="wrap">
      <h2 class="split">More free AI guides on <span class="serif">@time.fade.</span></h2>
      <p class="reveal">Follow for the next experiment &mdash; and if you want AI to handle your business&rsquo;s repetitive work, FadeFlow builds it.</p>
      <div class="cta-actions reveal">
        <a href="{INSTA}" class="btn btn-yellow" target="_blank" rel="noopener" data-magnetic>Follow @time.fade <span class="arrow">&rarr;</span></a>
        <a href="{P}resources/index.html" class="btn btn-line-light" data-magnetic>All free resources</a>
      </div>
    </div>
  </section>
'''

P = "../"
for r in RESOURCES:
    path = f"/resources/{r['slug']}.html"
    url = SITE + path
    crumbs = [("Home", "/"), ("Free AI resources", "/resources/"), (r["card_title"], path)]
    nodes = [{"@type": "CreativeWork", "@id": url + "#resource", "name": plain(r["title"]), "headline": r["card_title"],
              "description": r["desc"], "isAccessibleForFree": True, "inLanguage": "en", "learningResourceType": r["tag"],
              "author": {"@type": "Organization", "name": "time.fade by FadeFlow", "url": INSTA},
              "publisher": {"@id": f"{SITE}/#organization"}, "datePublished": DATE, "dateModified": DATE,
              "mainEntityOfPage": {"@id": url + "#webpage"}}]
    for kind, d in r["sections"]:
        if kind == "steps":
            nodes.append({"@type": "HowTo", "@id": url + "#howto", "name": plain(r["title"]), "description": r["desc"],
                          "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": x} for i, (t, x) in enumerate(d["steps"])]})
        if kind == "faq":
            nodes.append(faq_node(url, d["items"]))
    has_prompt = any(k == "prompt" and d["id"] == "prompt" for k, d in r["sections"])
    label, href = r["hero_cta"]
    primary = (copy_btn("prompt-text", label, " copy-btn-lg") if has_prompt
               else f'<a href="{href}" class="btn btn-ink" data-magnetic>{esc(label)} <span class="arrow">&darr;</span></a>')
    actions = primary + '<a href="#start" class="btn btn-line" data-magnetic>See the steps <span class="arrow">&darr;</span></a>'
    sections = "\n\n".join(RENDER[k](d) for k, d in r["sections"])
    body = f'''    <section class="page-hero">
      <div class="container">
        {crumbs_html(P, crumbs)}
        <div class="page-hero-label">{esc(r["kicker"])}</div>
        <h1 class="page-hero-title split">{acc(r["title"])}</h1>
        <p class="page-hero-sub reveal">{esc(r["sub"])}</p>
        <div class="page-hero-actions reveal">{actions}</div>
        <p class="res-hero-note reveal">{esc(r["hero_note"])}</p>
      </div>
    </section>

    <section class="page-content">
      <div class="container">
{sections}

{credit(P)}
      </div>
    </section>'''
    w(f"resources/{r['slug']}.html", page(head(r["seo"], r["desc"], path, P, crumbs=crumbs, nodes=nodes), P, "resources", body, resource_cta(P)))

def res_card(r, P):
    return f'''          <a href="{P}{r["slug"]}.html" class="post-card reveal">
            <span class="post-tag">{esc(r["tag"])}</span>
            <h3>{esc(r["card_title"])}</h3>
            <p>{esc(r["card_desc"])}</p>
            <div class="post-meta"><span>{esc(r["meta"])}</span><span class="post-go" aria-hidden="true">&rarr;</span></div>
          </a>'''

# ---- Resources hub
path = "/resources/"
title = "Free AI Resources & Prompts by time.fade | FadeFlow"
desc = "Free, copy-ready AI prompts and step-by-step guides from @time.fade: profile roasts, ChatGPT scheduled tasks, AI profile photos and more. No sign-up."
crumbs = [("Home", "/"), ("Free AI resources", path)]
hub_nodes = [{"@type": "ItemList", "@id": SITE + path + "#list", "name": "Free AI resources", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/resources/{r['slug']}.html", "name": r["card_title"]} for i, r in enumerate(RESOURCES)]}]
cards = "\n".join(res_card(r, "") for r in RESOURCES)
body = f'''    <section class="page-hero">
      <div class="container">
        {crumbs_html(P, crumbs)}
        <div class="page-hero-label">time.fade &times; FadeFlow &middot; Resource center</div>
        <h1 class="page-hero-title split">Free AI resources. Copy, paste, <span class="serif">done.</span></h1>
        <p class="page-hero-sub reveal">Copy-ready prompts and step-by-step guides from @time.fade. Free, no sign-up &mdash; every prompt has its own copy button.</p>
        <div class="page-hero-actions reveal"><a href="#all" class="btn btn-ink" data-magnetic>Browse resources <span class="arrow">&darr;</span></a><a href="{INSTA}" class="btn btn-line" target="_blank" rel="noopener" data-magnetic>Follow @time.fade</a></div>
      </div>
    </section>

    <section class="page-content">
      <div class="container">
        <div class="block" id="all">
{block_head("All resources", f"{len(RESOURCES)} free [tools] so far.", "New guides are added after each experiment on @time.fade.")}
          <div class="post-grid">
{cards}
          </div>
        </div>

        <div class="block">
          <a href="{P}experiments/index.html" class="exp-teaser reveal">
            <div><div class="label label-light">Behind the guides</div><h2>See the <span class="serif">time.fade</span> experiments center.</h2><p>Where every free resource starts: a real problem, tested with AI in public.</p></div>
            <span class="post-go" aria-hidden="true">&rarr;</span>
          </a>
        </div>
      </div>
    </section>'''
w("resources/index.html", page(head(title, desc, path, P, page_type="CollectionPage", crumbs=crumbs, nodes=hub_nodes), P, "resources", body, resource_cta(P)))

# ---- Experiments (time.fade)
path = "/experiments/"
title = "time.fade Experiments: Testing AI in Public | FadeFlow"
desc = "time.fade is FadeFlow's experiments center: we test AI on real everyday problems, share them on Instagram and turn what works into free guides."
crumbs = [("Home", "/"), ("time.fade experiments", path)]
by_slug = {r["slug"]: r for r in RESOURCES}
exps = "\n".join(f'''          <article class="exp-card reveal">
            <div class="exp-top"><span class="look-n">EXP {e["n"]}</span><span class="exp-status">{esc(e["status"])}</span></div>
            <h3>{esc(e["title"])}</h3>
            <p>{esc(e["text"])}</p>
            <a class="link-u" href="{P}resources/{e["link"]}.html">Open: {esc(by_slug[e["link"]]["card_title"])} &rarr;</a>
          </article>''' for e in EXPERIMENTS)
body = f'''    <section class="page-hero">
      <div class="container">
        {crumbs_html(P, crumbs)}
        <div class="page-hero-label">time.fade &middot; by FadeFlow</div>
        <h1 class="page-hero-title split">The time.fade experiments <span class="serif">center.</span></h1>
        <p class="page-hero-sub reveal">time.fade is where FadeFlow tests AI on real, everyday problems &mdash; in public, on Instagram. What works becomes a free guide in our resource center.</p>
        <div class="page-hero-actions reveal"><a href="{INSTA}" class="btn btn-ink" target="_blank" rel="noopener" data-magnetic>Follow @time.fade <span class="arrow">&rarr;</span></a><a href="{P}resources/index.html" class="btn btn-line" data-magnetic>Free resources</a></div>
      </div>
    </section>

    <section class="page-content">
      <div class="container">
        <div class="block">
{block_head("How it works", "Problem. Test. [Share.]")}
          <div class="numbered three">
            <div class="reveal"><h3>Pick a real problem</h3><p>Something that wastes time or keeps getting skipped &mdash; at work or in daily life.</p></div>
            <div class="reveal"><h3>Test it with AI, in public</h3><p>We try it, document what happens and share it on @time.fade.</p></div>
            <div class="reveal"><h3>Ship what works</h3><p>The useful parts become a free, copy-ready guide anyone can use.</p></div>
          </div>
        </div>

        <div class="block">
{block_head("Experiment log", "What we&rsquo;ve [tried].".replace("&rsquo;", "’"))}
          <div class="exp-grid">
{exps}
          </div>
        </div>
      </div>
    </section>'''
w("experiments/index.html", page(head(title, desc, path, P, crumbs=crumbs), P, None, body, resource_cta(P)))

# ---- 404
P = ""
body = '''    <section class="page-hero" style="min-height:70vh;display:flex;align-items:center">
      <div class="container">
        <div class="page-hero-label">Error 404</div>
        <h1 class="page-hero-title split">This page has <span class="serif">faded.</span></h1>
        <p class="page-hero-sub reveal">The page you&rsquo;re looking for doesn&rsquo;t exist or has moved.</p>
        <div class="page-hero-actions reveal"><a href="index.html" class="btn btn-ink">Back to home <span class="arrow">&rarr;</span></a><a href="blog/index.html" class="btn btn-line">Read the blog</a></div>
      </div>
    </section>'''
w("404.html", page(head("Page not found | FadeFlow", "The page you are looking for could not be found.", "/404.html", P, noindex=True), P, None, body))

# ================================================================ EXISTING PAGES
def swap_shell(name, P, active, head_html):
    s = rd(name)
    s = re.sub(r"^.*?</head>", lambda m: head_html, s, count=1, flags=re.S)
    s = re.sub(r'  <div class="scroll-progress".*?</header>\n', lambda m: nav(P, active), s, count=1, flags=re.S)
    s = re.sub(r'  <!-- ===== FOOTER ===== -->.*?</footer>\n', lambda m: footer(P), s, count=1, flags=re.S)
    return s

# ---- Home
path = "/"
s = swap_shell("index.html", "", None, head(
  "FadeFlow: AI Workflow Automation for SMEs in UAE & India",
  "FadeFlow helps SMEs in the UAE & India cut manual work with FadeLogistics and custom AI automation for invoices, WhatsApp leads, email and reports.",
  path, "", nodes=[faq_node(SITE + "/", HOME_FAQ)], inner=False))
s = s.replace('src="app_screenshot.png" alt="FadeLogistics dashboard" loading="lazy"',
              'src="app-screenshot.jpg" alt="FadeLogistics dashboard showing active jobs, quotations and invoices" width="1600" height="900" loading="lazy"')
s = s.replace('<p class="offer-note">Add AI automation whenever you&rsquo;re ready.</p>',
              '<p class="offer-note">Add AI automation whenever you&rsquo;re ready &middot; <a href="fadelogistics.html">Explore features</a> &middot; <a href="pricing.html">See pricing</a></p>')
if "offer-more" not in s:
    s = s.replace('''              <p>No new software to switch to. Your current tools stay as they are.</p>
            </div>
          </div>
        </article>''', '''              <p>No new software to switch to. Your current tools stay as they are.</p>
            </div>
          </div>
          <a href="ai-automation.html" class="btn btn-ink offer-more" data-magnetic>How AI automation works <span class="arrow">&rarr;</span></a>
        </article>''')
if 'id="faq"' not in s:
    extra = f'''    <!-- ===== BLOG ===== -->
    <section class="section" id="blog" style="padding-bottom:40px">
      <div class="wrap">
        <div class="sec-head">
          <div>
            <div class="label reveal">05 &mdash; From the blog</div>
            <h2 class="split">Guides for less manual <span class="serif">work.</span></h2>
          </div>
          <p class="reveal">Practical articles on AI automation, sales and logistics operations. <a class="link-u" href="blog/index.html">All articles</a></p>
        </div>
        <div class="post-grid">
{chr(10).join(post_card(p, "blog/") for p in POSTS[:3])}
        </div>
      </div>
    </section>

    <!-- ===== FAQ ===== -->
    <section class="section" id="faq">
      <div class="wrap home-faq">
        <div class="sec-head">
          <div class="label reveal">06 &mdash; FAQ</div>
          <h2 class="split">Questions, <span class="serif">answered.</span></h2>
          <p class="reveal">Can&rsquo;t find what you need? Email <a class="link-u" href="mailto:sales@fadeflow.in">sales@fadeflow.in</a></p>
        </div>
{faq_html(HOME_FAQ)}
      </div>
    </section>

'''
    s = s.replace("    <!-- ===== FINAL CTA ===== -->", extra + "    <!-- ===== FINAL CTA ===== -->", 1)
s = s.replace('<a href="https://application.fadelogistics.fadeflow.in/" class="btn btn-line-light" target="_blank" rel="noopener" data-magnetic>Open FadeLogistics &#8599;</a>',
              '<a href="pricing.html" class="btn btn-line-light" data-magnetic>See pricing</a>')
w("index.html", s)

# ---- About
about_nodes = [{"@type": "Person", "@id": f"{SITE}/about.html#sayed-adinan", "name": "Sayed Adinan", "jobTitle": "Founder",
                "worksFor": {"@id": f"{SITE}/#organization"}, "image": f"{SITE}/assets/team-sayed.jpg", "sameAs": ["https://www.linkedin.com/in/sayed-adinan/"]},
               {"@type": "Person", "name": "Muhammed KM", "jobTitle": "Co-founder, Software Engineer", "worksFor": {"@id": f"{SITE}/#organization"}, "image": f"{SITE}/assets/team-muhammed.jpg"},
               {"@type": "Person", "name": "Arshad Akl", "jobTitle": "Software Engineer", "worksFor": {"@id": f"{SITE}/#organization"}, "image": f"{SITE}/assets/team-arshad.jpg"}]
s = swap_shell("about.html", "", "about", head(
  "About FadeFlow: Founded 2023 | Team & Mission",
  "FadeFlow was founded in 2023 to take manual work off SMEs in the UAE and India. Meet founder Sayed Adinan and the team building FadeLogistics and AI automation.",
  "/about.html", "", page_type="AboutPage", crumbs=[("Home", "/"), ("About", "/about.html")], nodes=about_nodes))
w("about.html", s)

# ---- Contact
s = swap_shell("contact.html", "", "contact", head(
  "Contact FadeFlow: Book a Demo | UAE & India",
  f"Talk to FadeFlow: book a demo, request a quote or get support. Sales: sales@fadeflow.in, tech support: tech@fadeflow.in, phone/WhatsApp: {PHONE_H}.",
  "/contact.html", "", page_type="ContactPage", crumbs=[("Home", "/"), ("Contact", "/contact.html")]))
w("contact.html", s)

# ---- Legal
s = swap_shell("legal.html", "", None, head(
  "Privacy Policy, Terms & Cookie Policy | FadeFlow",
  "FadeFlow's privacy policy, terms of service and cookie policy, written to be simple and transparent. Your business data stays yours.",
  "/legal.html", "", crumbs=[("Home", "/"), ("Legal", "/legal.html")]))
w("legal.html", s)

# ================================================================ SEO FILES
pages = [("/", "1.0", "weekly"), ("/fadelogistics.html", "0.9", "monthly"), ("/ai-automation.html", "0.9", "monthly"),
         ("/pricing.html", "0.9", "monthly"), ("/about.html", "0.7", "monthly"), ("/contact.html", "0.7", "yearly"),
         ("/blog/", "0.8", "weekly")] + [(f"/blog/{p['slug']}.html", "0.7", "monthly") for p in POSTS] + \
        [("/resources/", "0.8", "weekly")] + [(f"/resources/{r['slug']}.html", "0.7", "monthly") for r in RESOURCES] + \
        [("/experiments/", "0.6", "monthly"), ("/legal.html", "0.3", "yearly")]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for u, pr, cf in pages:
    img = ""
    if u == "/fadelogistics.html":
        img = f"\n    <image:image><image:loc>{SITE}/app-screenshot.jpg</image:loc></image:image>"
    sm.append(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{DATE}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>{img}\n  </url>")
sm.append("</urlset>\n")
w("sitemap.xml", "\n".join(sm))

w("robots.txt", f"""# FadeFlow — robots.txt
# Search engines and AI assistants are welcome to read and learn from this site.

User-agent: *
Allow: /
Disallow: /404.html

# AI crawlers (explicitly allowed)
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

Sitemap: {SITE}/sitemap.xml

# Plain-text summaries for large language models
# {SITE}/llms.txt
# {SITE}/llms-full.txt
""")

w("site.webmanifest", json.dumps({"name": "FadeFlow: AI Workflow Automation for SMEs", "short_name": "FadeFlow",
  "description": "AI workflow automation and FadeLogistics for SMEs in the UAE & India", "start_url": "/", "display": "standalone",
  "background_color": "#F5F2EA", "theme_color": "#0D7B63",
  "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=2) + "\n")

# RSS
items = []
for p in POSTS:
    d = datetime.strptime(p["date"], "%Y-%m-%d").replace(hour=9, tzinfo=timezone.utc)
    items.append(f"""    <item>
      <title>{esc(strip(p['title']))}</title>
      <link>{SITE}/blog/{p['slug']}.html</link>
      <guid isPermaLink="true">{SITE}/blog/{p['slug']}.html</guid>
      <pubDate>{format_datetime(d)}</pubDate>
      <category>{esc(p['tag'])}</category>
      <description>{esc(p['desc'])}</description>
    </item>""")
w("rss.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>FadeFlow Blog</title>
    <link>{SITE}/blog/</link>
    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml" />
    <description>Guides on AI workflow automation, sales, invoicing and logistics operations for SMEs in the UAE &amp; India.</description>
    <language>en</language>
    <lastBuildDate>{format_datetime(datetime.strptime(DATE, "%Y-%m-%d").replace(hour=9, tzinfo=timezone.utc))}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
""")

# llms.txt
def md(s):
    def link(m):
        href = m.group(1)
        if not href.startswith(("http", "mailto")):
            href = SITE + "/" + href.replace("../", "")
        return "[" + m.group(2) + "](" + href + ")"
    s = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', link, s)
    return strip(s)

llms = f"""# FadeFlow

> FadeFlow is a company founded in 2023 that builds AI products and custom AI workflow automation to reduce manual work for small and medium businesses (SMEs) in the United Arab Emirates (UAE) and India. Its product, FadeLogistics, is web-based workflow and job card software for transport and logistics companies. Its service, AI Workflow Automation, uses Claude AI to automate repetitive tasks such as invoicing, WhatsApp lead qualifying and email filtering without replacing a company's existing systems.

Key facts:
- Name: FadeFlow (website: {SITE})
- Founded: 2023
- Markets: United Arab Emirates and India
- Customers: small and medium businesses (SMEs)
- Product: FadeLogistics, from AED 125 per month / AED 1,499 per company per year (app: {APP})
- Service: AI Workflow Automation (custom quote), built with Claude AI by Anthropic
- Founder: Sayed Adinan
- Contact: sales@fadeflow.in (sales, demos, quotes), tech@fadeflow.in (technical support, privacy), {PHONE_H} (phone/WhatsApp)
- Tagline: "Less manual work. More flow."

## Main pages

- [Home]({SITE}/): Overview of FadeFlow, FadeLogistics, AI automation use cases, clients and FAQ
- [FadeLogistics]({SITE}/fadelogistics.html): Logistics workflow software with job cards, status tracking, customers, suppliers, agents and trip expenses
- [AI Workflow Automation]({SITE}/ai-automation.html): How FadeFlow learns and automates repetitive tasks with Claude AI, with nine use cases
- [Pricing]({SITE}/pricing.html): FadeLogistics Starter from AED 125/month (AED 1,499/year) and the Custom package by quote
- [About]({SITE}/about.html): Company story, mission, vision and team
- [Contact]({SITE}/contact.html): Sales, support, demo booking and contact details

## Blog

{chr(10).join(f"- [{strip(p['title'])}]({SITE}/blog/{p['slug']}.html): {p['desc']}" for p in POSTS)}

## Free AI resources (time.fade)

- [Free AI resources hub]({SITE}/resources/): Free, copy-ready AI prompts and guides from @time.fade, FadeFlow's Instagram
{chr(10).join(f"- [{r['card_title']}]({SITE}/resources/{r['slug']}.html): {r['desc']}" for r in RESOURCES)}
- [time.fade experiments center]({SITE}/experiments/): Where FadeFlow tests AI on everyday problems in public before turning them into free guides

## Optional

- [Full detailed information for LLMs]({SITE}/llms-full.txt): Complete facts, features, pricing, FAQs and policies in one file
- [Legal]({SITE}/legal.html): Privacy policy, terms of service and cookie policy
- [Sitemap]({SITE}/sitemap.xml)
"""
w("llms.txt", llms)

def faq_md(faqs): return "\n\n".join(f"### {strip(q)}\n{md(a)}" for q, a in faqs)
full = f"""# FadeFlow: complete information for AI assistants and LLMs

> This file gives large language models and AI assistants detailed, accurate information about FadeFlow. Last updated: {DATE}. Canonical website: {SITE}

## 1. Company overview

- **Name:** FadeFlow
- **What it does:** Builds AI products and custom AI workflow automation that reduce manual work for small and medium businesses (SMEs).
- **Founded:** 2023
- **Markets served:** United Arab Emirates (UAE) and India
- **Target customers:** SMEs that still run on WhatsApp, Excel and paper, including trading & distribution companies, service businesses, contractors & maintenance companies, logistics & transport companies, manpower & staffing agencies and other growing SMEs.
- **Offerings:** (1) FadeLogistics, a product; (2) AI Workflow Automation, a custom service.
- **AI technology:** Claude AI by Anthropic.
- **Tagline:** "Less manual work. More flow."
- **Positioning:** FadeFlow is a multi-product AI company for SMEs, not only a logistics company. FadeLogistics is its logistics product.

## 2. Team

- **Sayed Adinan:** Founder ([LinkedIn](https://www.linkedin.com/in/sayed-adinan/))
- **Muhammed KM:** Co-founder, Software Engineer
- **Arshad Akl:** Software Engineer

## 3. Contact

- Sales, demos and quotes: sales@fadeflow.in
- Technical support and privacy/data requests: tech@fadeflow.in
- Phone / WhatsApp: {PHONE_H}
- LinkedIn: https://www.linkedin.com/company/fadeflow
- Instagram: https://www.instagram.com/time.fade (@time.fade)
- Response time: within 24 hours
- Contact page: {SITE}/contact.html

## 4. Product: FadeLogistics

FadeLogistics is web-based workflow management software for transport and logistics companies. It runs in the browser at {APP}, with nothing to install. Page: {SITE}/fadelogistics.html

### Features
{chr(10).join(f"- **{strip(t)}:** {strip(d)}" + (" " + "; ".join(strip(x) for x in rest[0]) + "." if rest else "") for _, t, d, *rest in LOGI_FEATURES)}

### How it works
1. Create the job card when a request comes in.
2. Assign the supplier and agent handling it.
3. Track status (draft, ongoing, completed) and log trip expenses.
4. Complete the job and review its full history and margin.

AI automation can be added on top of FadeLogistics through the Custom package.

## 5. Service: AI Workflow Automation

FadeFlow learns a company's repetitive tasks, then automates its current workflow with AI (Claude AI), without changing the systems it already uses. Page: {SITE}/ai-automation.html

### Process
1. **Learn:** study how the team works today and find the repetitive tasks.
2. **Automate:** build AI automation around the existing workflow.
3. **Keep your systems:** no new software to switch to; current tools stay as they are.

### Use cases
{chr(10).join(f"- **{strip(t)}:** {strip(d)}" for _, t, d in AI_USES)}

### Works with
Email inboxes, WhatsApp, Excel, Google Sheets, PDF documents and scans, the business software a company already uses, and FadeLogistics.

## 6. Pricing

Page: {SITE}/pricing.html. Prices are in UAE dirhams (AED).

### FadeLogistics Starter: from AED 125 per month (AED 1,499 per company, per year)
- All FadeLogistics features: job cards, customers, suppliers, agents and expenses
- Unlimited job cards, customers, suppliers and agents
- Full team training (first year)
- Workflow consulting (first year)
- Maintenance, updates and direct support (first year)

### Custom package: priced by custom quote
- A study of the current workflow and repetitive tasks
- System customised to the way the team works
- AI automation: invoices, analytics, email, WhatsApp leads and more
- Works with the systems the company already uses
- Dedicated support
A quote is given once FadeFlow understands the company's needs.

## 7. Clients

FadeFlow works with businesses in the UAE and India including Moving Line, Route Star, Cool Life Technical Services L.L.C and Al Rawda Technical Services, plus others that cannot be named publicly.

## 8. Frequently asked questions

{faq_md(HOME_FAQ)}

{faq_md(LOGI_FAQ[0:2] + LOGI_FAQ[3:])}

{faq_md(AI_FAQ)}

{faq_md(PRICING_FAQ[1:])}

## 9. Data, privacy and policies

- Customer business data remains owned by the customer. FadeFlow does not sell, share or monetise business data.
- Data is stored using industry-standard practices including encryption in transit and at rest.
- Users can request account deletion and data removal at any time via tech@fadeflow.in; requests are processed within 30 days.
- Full policies: {SITE}/legal.html (privacy policy, terms of service, cookie policy).

## 10. Blog articles

{chr(10).join(f"- [{strip(p['title'])}]({SITE}/blog/{p['slug']}.html) ({p['tag']}): {p['desc']}" for p in POSTS)}

## 11. Free AI resources and time.fade

time.fade (Instagram @time.fade, {INSTA}) is FadeFlow's experiments center: it tests AI on real everyday problems in public and turns what works into free, copy-ready guides at {SITE}/resources/ (no sign-up).

{chr(10).join(f"- [{r['card_title']}]({SITE}/resources/{r['slug']}.html) ({r['tag']}, {r['meta']}): {r['desc']}" for r in RESOURCES)}

## 12. Mission and vision

- **Mission:** Give SMEs back the hours lost to manual work. FadeFlow helps small and medium businesses automate repetitive work with practical software and AI, so their teams can focus on customers and growth instead of paperwork.
- **Vision:** Every SME running on automated workflows. Automation should be within reach of every growing business in the UAE and India, not just large enterprises; it should fit the tools they already use and be priced for the size they are.
"""
w("llms-full.txt", full)
print("built:", len(POSTS), "posts")
