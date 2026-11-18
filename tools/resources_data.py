"""
Free AI resources (time.fade x FadeFlow).

To add a new resource: append a dict to RESOURCES, then run
    python tools/build_site.py
Every resource gets its own page at /resources/<slug>.html, a card on the
hub (/resources/), and entries in the sitemap and llms files.

Plain text everywhere (it is escaped when rendered). Section types:
  ("story",    {label, big, text, sub})
  ("steps",    {label, title, sub, steps: [(title, text)], note})
  ("prompt",   {label, title, sub, id, heading, text, after})
  ("examples", {label, title, sub, items: [text], note})
  ("faq",      {label, title, sub, items: [(q, a)]})
  ("bullets",  {label, title, sub, items: [(title, text)]})
  ("photo_input", {label, title, text})
  ("library",  {label, title, sub})      # renders LOOKS
  ("codes",    {label, title, sub, groups, search_placeholder, noun})  # renders BOOK_CODE_GROUPS
"""

PROFILE_ROAST_PROMPT = """Act as a sharp but fair profile reviewer. I’ll upload a screenshot of my Instagram or LinkedIn profile.

First, identify the platform. Review only what is actually visible in the screenshot. Do not invent my audience, business results, engagement, links, or content you cannot see. If my goal is unclear, ask me one short question: “What do you want this profile to achieve—followers, clients, job opportunities, or something else?”

Then give me:

1. THREE-SECOND TEST
In one sentence, say what a new visitor would understand about who I am, who this profile is for, and why they should follow or contact me. If the screenshot does not make that clear, say exactly what is missing.

2. TOP 5 FIXES
Rank the five changes with the biggest likely impact. For each, include:
- The exact element or wording you noticed
- A short, witty critique—direct, not insulting
- Why it may confuse visitors or reduce follows, enquiries, or opportunities
- The specific replacement or action

For Instagram, check the name, bio, profile photo, link and CTA, highlights, pinned posts, and whether visible Reel covers communicate a consistent topic.

For LinkedIn, check the photo, headline, banner, first visible About lines, Featured section, Experience preview, and contact CTA.

3. READY-TO-PASTE REWRITE
For Instagram, write one complete bio and a better display name if needed.
For LinkedIn, write one headline and the opening three lines of the About section.
Use only facts I provided or that are clearly visible. Put [PLACEHOLDER] where a necessary fact is missing. Include one clear CTA.

4. CHANGE ORDER
Give me a short checklist of what to change today, in order. Separate changes I can make from this screenshot from things that require another screenshot or more information.

Be honest and specific. Briefly acknowledge anything that already works. No generic branding advice, made-up proof, excessive praise, or harsh comments about my appearance."""

SCHEDULE_PROMPT = """Help me set up a real ChatGPT scheduled task.

Ask me these questions ONE AT A TIME, in simple language. Skip anything I have already answered:

1. What is your goal, and what would you like ChatGPT to do for you?
2. What result should ChatGPT send you when it runs? For example, a reminder, researched ideas, a summary, or a checklist.
3. When should it run? Ask for a time or time window, how often it should repeat, and when it should stop if relevant.
4. What city or time zone are you in?

Use my answers to write a clear task instruction. If my request needs web access, a connected app, or information you cannot access, tell me before scheduling it. Do not promise an action you cannot perform.

Briefly show me:
- What the task will do
- When it will run
- What result I will receive

Ask me to confirm or correct those details. Once I confirm, CREATE the scheduled task using ChatGPT’s scheduling feature. Do not merely write a prompt or say you will remember it. Show me the actual task confirmation, including its name, schedule, and time zone.

If scheduling is unavailable on my account, say so clearly and tell me where to check for the Scheduled feature.

Finally, tell me how to receive alerts. If push or email notifications are not enabled, direct me to Settings → Notifications to turn on Push, Email, or both. Do not claim to have enabled notifications unless you actually did."""

PHOTO_CORRECTION_PROMPT = """Keep the composition, outfit, and background from the previous result. Correct only [SPECIFIC ISSUE]. Use my uploaded photos to bring the face closer to my real appearance. Preserve my apparent age and natural skin tone. Generate the corrected image."""

# Shared identity instructions included in every profile-photo prompt.
PHOTO_IDENTITY = """Use the photos I uploaded as the identity reference for one person. Create a realistic, high-quality photograph of that same person.

Identity: keep their face shape, facial features, eyes, nose, lips, skin tone, hairline, hairstyle, facial hair, glasses (if any) and apparent age the same as in my photos. Do not beautify, slim, smooth the skin, change ethnicity, or make them look younger or older. Keep natural skin texture.

Quality: realistic proportions and natural hands if visible, sharp focus on the eyes, true-to-life colours. No extra people, no text, no logos, no watermarks, no brand marks."""

def photo_prompt(title, desc):
    return f"{PHOTO_IDENTITY}\n\nLook — {title}: {desc}\n\nGenerate one image."

PHOTO_CATEGORIES = [
    ("professional", "Professional"),
    ("creator", "Work & Creator"),
    ("everyday", "Casual & Everyday"),
    ("editorial", "Studio & Editorial"),
    ("platform", "Platform-specific"),
]

# (category, best for, title, description)
LOOKS = [
    ("professional", "LinkedIn", "Clean professional profile", "Chest-up, plain dark jacket and neutral shirt, relaxed shoulders, direct gaze and slight smile. Warm-grey studio backdrop, even diffused light. Square crop, face centred and circle-safe."),
    ("professional", "LinkedIn", "Bright office portrait", "White open-collar shirt, standing near a window in an understated modern office. Soft daylight, blurred surroundings, natural expression. Square crop with comfortable headroom."),
    ("professional", "LinkedIn", "Founder portrait", "Navy overshirt or blazer over a light shirt, seated at a simple desk, hands resting naturally. Neutral background, warm side light, waist-up, 4:5."),
    ("professional", "LinkedIn", "Simple formal headshot", "Dark suit jacket, plain light shirt, no tie. Chest-up, straight posture, muted off-white background, balanced studio light, square crop."),
    ("professional", "LinkedIn", "Approachable team page", "Neutral knit top, gentle smile, pale-grey background, consistent bright light. Head and shoulders, square crop suitable for a company team grid."),
    ("professional", "LinkedIn", "Consultant profile", "Textured beige jacket over a dark shirt, seated slightly angled toward camera. Quiet office background, bright natural light, waist-up 4:5."),
    ("professional", "LinkedIn", "Portfolio introduction", "Charcoal button-up shirt, standing against a plain warm wall. Candid but composed expression, soft side light, portrait 4:5."),
    ("professional", "LinkedIn", "Speaker biography", "Dark jacket and open-collar shirt, mid-torso portrait, a simple stage curtain in soft focus without visible logos or audience. Gentle spot light, 4:5."),
    ("professional", "LinkedIn", "Resume headshot", "Plain collared shirt, light neutral background, even lighting, direct gaze, neutral friendly expression. Tight but not passport-sized square crop."),
    ("professional", "LinkedIn", "Company leader", "Dark blazer over a simple crew-neck, seated in a calm office with subtle architectural lines. Natural hands, confident but unforced pose, waist-up 4:5."),
    ("creator", "Instagram", "At the desk", "Neutral shirt, seated at a tidy desk with a closed laptop, eyes toward camera. Window light, realistic small workspace, mid-torso 4:5."),
    ("creator", "Instagram", "Working portrait", "Casual dark overshirt, standing beside a desk with notebook and laptop in soft focus. Friendly expression, natural light, 4:5."),
    ("creator", "Instagram", "Podcast portrait", "Plain dark top, seated beside a microphone without brand marks, warm low-key studio light, looking toward camera. Chest-up 4:5."),
    ("creator", "Instagram", "Video creator", "Simple light shirt in a minimal filming setup, camera and lamp softly blurred in the background, relaxed direct gaze, 4:5."),
    ("creator", "Instagram", "Writer portrait", "Earth-tone knit sweater, seated by a window holding a closed notebook, thoughtful but natural expression, soft daylight, 4:5."),
    ("creator", "Instagram", "Workshop facilitator", "Neutral jacket in a bright meeting room, blank whiteboard in the background, no writing or logos. Warm smile, waist-up 4:5."),
    ("creator", "Instagram", "Product founder", "Casual dark jacket in a modest startup workspace, blurred monitor behind showing only abstract colour, no fake interface. Mid-torso 4:5."),
    ("creator", "Instagram", "Customer-facing professional", "Light blue collared shirt, welcoming expression, clean reception-like background with no invented company branding. Square crop."),
    ("creator", "Instagram", "Remote worker", "Plain black sweater, seated by a home-office window, soft screen glow and daylight, eye contact, chest-up 4:5."),
    ("creator", "Instagram", "Creative professional", "Olive overshirt over white tee, standing before a simple warm wall with a small plant, expressive but natural posture, 4:5."),
    ("everyday", "casual", "Cafe window", "Dark casual shirt at a quiet cafe table, relaxed smile, daylight through window, background blurred, no branded cups, 4:5."),
    ("everyday", "casual", "Outdoor daylight", "Plain cream shirt in open shade on a city walkway, calm expression, softly blurred background, chest-up 4:5."),
    ("everyday", "casual", "Denim casual", "Simple denim jacket over neutral tee, relaxed standing pose on a quiet street, cloudy daylight, square crop."),
    ("everyday", "casual", "Park portrait", "Neutral overshirt near trees, natural smile and candid posture, soft evening light, waist-up 4:5."),
    ("everyday", "casual", "Travel profile", "Light overshirt and small backpack strap, standing in an airport-like interior with no identifiable signs, natural light, 4:5."),
    ("everyday", "casual", "Coastal daylight", "White linen shirt near the sea, gentle breeze, neutral relaxed expression, horizon softly blurred, 4:5."),
    ("everyday", "casual", "City evening", "Dark jacket outdoors at dusk, subtle distant street lights, face evenly lit and clearly recognisable, square crop."),
    ("everyday", "casual", "Weekend portrait", "Plain textured sweater on a bench in an uncluttered garden, soft overcast light, relaxed gaze, 4:5."),
    ("everyday", "casual", "Bookshop portrait", "Neutral top beside softly blurred shelves, daylight, natural smile, no readable book titles or signs, 4:5."),
    ("everyday", "casual", "Minimal everyday DP", "Plain dark t-shirt, off-white background, natural daylight, straightforward friendly expression, square centre crop."),
    ("editorial", "Instagram", "Dark studio", "Dark shirt against charcoal background, soft side light with gentle fill so both eyes remain visible, natural skin texture, square crop."),
    ("editorial", "Instagram", "Light studio", "Pale neutral shirt against warm-white background, diffused frontal light, natural expression, chest-up 4:5."),
    ("editorial", "Instagram", "Blue backdrop", "Plain dark crew-neck against muted deep-blue seamless backdrop, soft even studio light, direct gaze, square crop."),
    ("editorial", "Instagram", "Warm beige backdrop", "Simple dark jacket against matte beige studio wall, subtle warm side light and realistic shadows, 4:5."),
    ("editorial", "Instagram", "Monochrome portrait", "Plain dark shirt, tasteful black-and-white tonal treatment, diffused window light, natural features preserved, head and shoulders 4:5."),
    ("editorial", "Instagram", "Film texture", "Earth-tone shirt, warm neutral wall, subtle realistic film grain without changing face detail, candid half smile, 4:5."),
    ("editorial", "Instagram", "Editorial seated", "Charcoal jacket, sitting on a simple chair, hands resting naturally, quiet grey backdrop, broad soft key light, mid-torso 4:5."),
    ("editorial", "Instagram", "Soft rim light", "Dark knit top against dark-grey background, subtle edge light and clear front fill, natural expression, square crop."),
    ("editorial", "Instagram", "Warm spotlight", "Neutral shirt, soft oval pool of warm light on plain wall behind, balanced light on face, no strong glow effects, 4:5."),
    ("editorial", "Instagram", "Architectural lines", "Dark jacket in front of an understated modern wall, leading lines in soft focus, composed standing pose, 4:5."),
    ("platform", "LinkedIn", "LinkedIn avatar", "Chest-up dark blazer, neutral pale background, direct gaze, natural slight smile, square image with eyes and shoulders safe inside a circular crop."),
    ("platform", "Instagram", "Instagram avatar", "Casual dark overshirt, warm blurred background, bright eyes and relaxed smile, square image designed for a small circular icon."),
    ("platform", "WhatsApp", "WhatsApp business DP", "Light collared shirt, plain mid-grey background, approachable expression, sharp face at thumbnail size, square and circle-safe."),
    ("platform", "Instagram", "YouTube channel icon", "Plain dark tee with muted teal studio backdrop, energetic but natural smile, face large and central, square and circle-safe."),
    ("platform", "banner", "Personal website hero", "Dark jacket in a calm sunlit workspace, person on right third, clean negative space on left for real website text to be added later, landscape 16:9, no generated text."),
    ("platform", "LinkedIn banner", "LinkedIn banner", "Dark jacket, person on right third of a wide minimal office scene, left side clear for text and profile overlay; 4:1 wide format, no generated text."),
    ("platform", "Instagram", "Speaker event card", "Neutral blazer, subject on left half against warm plain background, blank space on right for real event details, portrait 4:5, no generated text."),
    ("platform", "Instagram", "Team directory", "Simple neutral top, consistent pale-grey studio backdrop, straight-on face, soft even light, square thumbnail-safe composition."),
    ("platform", "banner", "Portfolio case-study header", "Plain black shirt in softly blurred working environment, subject on left third, open space on right, landscape 16:9, no generated interface or text."),
    ("platform", "Instagram", "Newsletter author image", "Warm, approachable chest-up portrait with neutral shirt and soft studio background, square centre crop that works at small size."),
]

GROCERY_PRICE_PROMPT = """I want to compare grocery prices across supermarkets and find the cheapest way to buy my shopping list.

First, ask me only these two questions:

1. What grocery items do you want to buy? Ask me to include quantities, sizes, and preferred brands if possible.
2. Which city or area should I search in?

After I answer, search the internet for current grocery prices and offers at supermarkets near that location.

Check stores such as LuLu, Nesto, Carrefour, Sharjah Coop, and other available supermarkets.

For each supermarket:
- List every item and its price.
- Mention whether it is an offer price or regular price.
- Compare equivalent brands, sizes, and quantities.
- Calculate the total cost of the complete shopping list.

After comparing the stores, tell me which supermarket has the cheapest complete basket.

Also check whether buying different items from different supermarkets would reduce the total cost. Consider extra travel or delivery costs before recommending that option.

Important:
- Use real, current prices from reliable sources.
- Prefer official supermarket websites and current catalogues.
- Include source links and the date prices were checked.
- Never guess or invent prices, offers, or availability.
- If a price cannot be verified, write "Price unavailable".
- Clearly distinguish live website prices from catalogue prices.
- Do not calculate missing prices as zero.
- If some prices are unavailable, show a partial total and explain what is missing.

Present the results in a simple comparison table and give me a clear recommendation."""

BOOK_CODES_PROMPT = """I read books with codes. When my message starts with a code below, do exactly what it says. Codes aren't case sensitive. Use the book I attached or pasted in this chat, or the book I name after the code. If I add a chapter (like /visualnotes chapter 3), only do that part. I can stack codes, like /chaptermap /quotes. Work from the book's text when you have it, and never make up quotes or events. If I only gave a title, say once that attaching the book gets better results, then do your best. Codes that need my answers (like /quizme and /debate) keep going until I say stop. If I use a code that isn't on this list, work out what it means from its name. If I paste this into a chat, reply only: "Codes ready. Which book are we reading?"

THE 4 FROM THE VIDEO
/visualnotes: Turn the entire book into short visual notes I can scan in minutes: one block per big idea with a bold heading, an emoji icon, two or three short bullets and a simple diagram or table where it helps.
/mentalmodels: Pull out the book's biggest ideas and turn them into a visual map of how they all connect: one line on each idea, then a diagram with arrows showing how they link.
/chaptermap: Break the book down one chapter at a time: what happens or what's argued, the key point and how it links to the rest. End with a simple map of how it all fits together.
/themes: Find every major theme running through the book: what it is, where it shows up (characters, events, examples) and what the book is really saying, so I get the deeper meaning.

GET THE GIST
/tldr: The whole book in five sentences.
/onepager: The whole book on one page: the big idea, the key points and the best takeaways.
/bigidea: The one idea the whole book is built on, in one sentence, then why it matters.
/worthit: Ask what I want from it, then tell me honestly if it's worth my time and who should skip it.
/skimguide: Which chapters to read closely, which to skim and which to skip, and why.
/beforeyouread: What to know before I start: the author, when and why it was written, what to look out for. No spoilers.

GO DEEPER
/characters: Every main character: who they are, what they want and how they change.
/timeline: Every key event in order, with the chapter it happens in.
/symbols: The symbols and recurring images, and what each one stands for.
/argument: The author's main argument, the evidence behind it and the weak spots.
/keyterms: Every important term or idea in the book, in plain words.
/simplify: Rewrite the passage I paste in plain, everyday words.
/ending: What the ending really means, and the main ways people read it.
/critique: The strongest criticisms of the book and where the author might be wrong.

REMEMBER IT
/quotes: The 10 best lines, word for word from the text, with the chapter and what each one means. If you don't have the text, say so instead of guessing.
/flashcards: Flashcards of the key ideas. Run me through them one at a time.
/recall: Ask me what I remember from the chapter first, then fill in what I missed.
/sketchnote: Make one image: the book's big ideas as a hand-drawn sketchnote page I can save.
/savenotes: Everything from this chat as clean notes I can paste into my notes app.

USE IT
/actionsteps: Turn the book into a short list of things to actually do, starting this week.
/applytome: Ask me a few questions about my life and goals, then show how the book's ideas apply to me.
/challenge: A 30-day challenge to put the book into practice, one small task a day.
/examples: An everyday, real-life example of each big idea.
/asktheauthor: Answer my questions the way the author would, based only on the book. Say when it doesn't cover something.
/advice: I'll bring a real problem. Give me advice using only this book's ideas.

STUDY IT
/quizme: Quiz me one question at a time. Tell me if I'm right and why, and keep score.
/studyguide: A full study guide: summary, characters or key ideas, themes, quotes and likely test questions.
/essayideas: Five essay topics, each with a thesis and the evidence from the book to back it up.
/vocab: The hard words from the chapter, with simple meanings and an example sentence.
/sofar: Recap everything up to the chapter I name. No spoilers past it.

BOOK CLUB AND BEYOND
/bookclub: Ten discussion questions for a book club, from easy to deep.
/debate: Argue the opposite side of the book's main idea with me, one point at a time.
/compare: Compare it to another book I name: where they agree, where they clash and which to read first.
/readnext: Five real books to read next based on this one, and why each fits.

FOR KIDS
/kidsversion: Retell it for a kid of the age I give, in simple words, keeping the big lessons.
/kidsquestions: Questions to ask my kid as we read it together, chapter by chapter."""

# (group key, group name, [(code, what it does)])
BOOK_CODE_GROUPS = [
    ("video", "From the video", [
        ("/visualnotes", "Turn the whole book into short visual notes: one block per big idea with a heading, an icon, two or three bullets and a simple diagram."),
        ("/mentalmodels", "Turn the biggest ideas into a visual map, with arrows showing how they connect."),
        ("/chaptermap", "Go chapter by chapter: what happens or is argued, the key point, and how it links to the rest."),
        ("/themes", "Find the major themes, where they show up and what the book is really saying."),
    ]),
    ("gist", "Get the gist", [
        ("/tldr", "The whole book in five sentences."),
        ("/onepager", "The big idea, key points and best takeaways on one page."),
        ("/bigidea", "The one idea the whole book is built on, and why it matters."),
        ("/worthit", "Ask what you want, then say honestly if it's worth your time and who should skip it."),
        ("/skimguide", "Which chapters to read closely, skim or skip, and why."),
        ("/beforeyouread", "The author, when and why it was written, and what to look out for. No spoilers."),
    ]),
    ("deeper", "Go deeper", [
        ("/characters", "Every main character: who they are, what they want and how they change."),
        ("/timeline", "Every key event in order, with the chapter it happens in."),
        ("/symbols", "Recurring symbols and images, and what each one stands for."),
        ("/argument", "The main argument, the evidence behind it and the weak spots."),
        ("/keyterms", "Every important term or idea in plain words."),
        ("/simplify", "Rewrite a confusing passage in everyday language."),
        ("/ending", "What the ending really means and the main ways people read it."),
        ("/critique", "The strongest criticisms of the book and where the author might be wrong."),
    ]),
    ("remember", "Remember it", [
        ("/quotes", "The 10 best lines word for word, with the chapter and what each one means. Needs the book's text."),
        ("/flashcards", "Flashcards of the key ideas, run through one at a time."),
        ("/recall", "Asks what you remember first, then fills in what you missed."),
        ("/sketchnote", "One hand-drawn style image of the book's big ideas that you can save."),
        ("/savenotes", "Everything from the chat as clean notes for your notes app."),
    ]),
    ("use", "Use it", [
        ("/actionsteps", "A short list of things to do, starting this week."),
        ("/applytome", "Asks about your life and goals, then applies the book's ideas to you."),
        ("/challenge", "A 30-day challenge, with one small task each day."),
        ("/examples", "An everyday, real-life example of each big idea."),
        ("/asktheauthor", "Answers your questions the way the author would, based only on the book."),
        ("/advice", "Bring a real problem and get advice using only this book's ideas."),
    ]),
    ("study", "Study it", [
        ("/quizme", "One question at a time, with explanations, scoring and no stopping until you say so."),
        ("/studyguide", "Summary, characters or key ideas, themes, quotes and likely test questions."),
        ("/essayideas", "Five essay topics with a thesis and evidence from the book."),
        ("/vocab", "Hard words from the chapter, with simple meanings and example sentences."),
        ("/sofar", "A recap up to your current chapter, with no spoilers past it."),
    ]),
    ("club", "Book club & beyond", [
        ("/bookclub", "Ten discussion questions, from easy to deep."),
        ("/debate", "Argues the opposite side of the main idea, one point at a time."),
        ("/compare", "Compares another book you name: where they agree, clash and which to read first."),
        ("/readnext", "Five real books to read next based on this one, and why each fits."),
    ]),
    ("kids", "For kids", [
        ("/kidsversion", "Retells the book for a kid of the age you give, keeping the big lessons."),
        ("/kidsquestions", "Questions to ask your kid as you read together, chapter by chapter."),
    ]),
]

RESOURCES = [
    dict(
        slug="profile-roast-prompt",
        tag="Prompt",
        card_title="Roast my profile, then fix it",
        card_desc="One prompt that reviews a screenshot of your LinkedIn or Instagram profile, ranks the top 5 fixes and writes a ready-to-paste bio or headline.",
        meta="1 prompt · Instagram & LinkedIn",
        seo="Free LinkedIn & Instagram Profile Roast Prompt | FadeFlow",
        desc="Copy a free AI prompt that reviews a screenshot of your LinkedIn or Instagram profile, ranks the top 5 fixes and writes a ready-to-paste bio or headline.",
        kicker="time.fade / Resources · Profile growth",
        title="Roast my profile. Then [fix] it.",
        sub="A sharp but fair AI review of your Instagram or LinkedIn profile: what visitors understand in three seconds, the five fixes that matter most, and a rewrite you can paste today.",
        hero_cta=("Copy the prompt", "#prompt"),
        hero_note="Works with ChatGPT, Claude, Gemini or any AI that can read a screenshot.",
        sections=[
            ("steps", dict(label="01 / Get started", title="Four steps. One honest review.",
                sub="Takes about two minutes.",
                steps=[("Take a screenshot", "Capture the top of your profile: photo, name, bio or headline, link, highlights or banner, and the first posts or About lines."),
                       ("Open your AI chat", "Start a new chat in ChatGPT, Claude, Gemini or another AI that accepts images."),
                       ("Paste the prompt + upload", "Copy the complete prompt below, paste it, attach your screenshot and send."),
                       ("Answer one question, then fix", "If it asks what the profile should achieve, answer in one line. Then work through the change order it gives you.")],
                note="Hide anything private (phone numbers, emails, messages) before you upload a screenshot.")),
            ("prompt", dict(label="02 / Copy & paste", title="Your review prompt", sub="Copy it all. Upload your screenshot with it.",
                id="prompt", heading="The complete prompt", text=PROFILE_ROAST_PROMPT,
                after="Want a second round? Upload a new screenshot after your changes and paste the same prompt again.")),
            ("bullets", dict(label="03 / What you get", title="Four clear outputs.", sub="",
                items=[("Three-second test", "What a new visitor understands about who you are, who it’s for and why they should follow or contact you."),
                       ("Top 5 fixes", "Ranked by impact, each with what was noticed, a witty critique, why it matters and the exact replacement."),
                       ("Ready-to-paste rewrite", "A full Instagram bio and display name, or a LinkedIn headline and opening About lines, with one clear CTA."),
                       ("Change order", "A short checklist of what to change today, in order.")])),
        ],
    ),
    dict(
        slug="chatgpt-scheduled-tasks",
        tag="Guide",
        card_title="Give ChatGPT a task to do later",
        card_desc="A five-step guide and setup prompt to schedule research, summaries, reminders and checklists in ChatGPT.",
        meta="5 steps · 1 setup prompt",
        seo="How to Schedule Tasks in ChatGPT (Free Prompt) | FadeFlow",
        desc="Give ChatGPT a task to do later. A 5-step guide and copy-ready setup prompt to schedule research, summaries, reminders and checklists in ChatGPT.",
        kicker="time.fade / Guides · A little setup. A useful routine.",
        title="Give ChatGPT a task to do [later].",
        sub="Tell it what you need, choose when it should run, and get the result in ChatGPT.",
        hero_cta=("Copy the setup prompt", "#prompt"),
        hero_note="More than a reminder: schedule research, summaries, checklists, and other supported tasks.",
        sections=[
            ("story", dict(label="The real-life starting point", big="AED 50",
                text="My fine for missing a daily video. So I scheduled ChatGPT to research content ideas for me.",
                sub="Your task can be something completely different.")),
            ("steps", dict(label="01 / Get started", title="Five steps. One useful task.",
                sub="Start with what would help you. Let the prompt handle the questions.",
                steps=[("Open ChatGPT", "Start a new chat."),
                       ("Paste the setup prompt", "Copy the complete prompt below and paste it into ChatGPT."),
                       ("Answer the simple questions", "Explain your goal, the result you want, and when it should run."),
                       ("Review and confirm", "Review the task details and confirm them. Make sure ChatGPT shows an actual scheduled-task confirmation."),
                       ("Check Scheduled and alerts", "Find the task in Scheduled. To receive alerts, check Settings → Notifications and enable Push, Email, or both.")],
                note="Free ChatGPT accounts may have a limited number of active tasks and flexible time windows. Exact delivery times and some advanced actions depend on the plan and account. A scheduled task can use only information and tools available to it.")),
            ("prompt", dict(label="02 / Copy & paste", title="Your setup prompt",
                sub="Copy it all. ChatGPT will ask you one question at a time.",
                id="prompt", heading="The complete prompt", text=SCHEDULE_PROMPT,
                after="After copying, open a new ChatGPT chat and paste the prompt. This guide itself does not create a task.")),
            ("examples", dict(label="03 / Make it yours", title="What could you schedule?",
                sub="Examples to get you started — not guaranteed outcomes.",
                items=["Find three relevant content ideas each morning, with source links.",
                       "Search for newly posted jobs that match my role and location each day.",
                       "Summarise important news in my industry every morning.",
                       "Remind me of a deadline and give me a short action checklist."],
                note="Web research depends on accessible sources. Connected-account tasks require the relevant connection and permissions.")),
            ("faq", dict(label="04 / A little help", title="Before you go",
                sub="A few things to check if your task or alerts aren't working.",
                items=[("Where do I see my task?", "Look for Scheduled in ChatGPT’s menu. Confirmed tasks appear there, where you can review, pause, edit or delete them. The exact location can vary between the app and the website."),
                       ("Why didn’t I get an alert?", "Check that ChatGPT showed a real scheduled-task confirmation, then open Settings → Notifications and enable Push, Email, or both. On your phone, also make sure notifications are allowed for the ChatGPT app."),
                       ("Can I set an exact time for free?", "Free accounts may have a limited number of active tasks and flexible time windows, so a task may run close to, rather than exactly at, the time you chose. Exact delivery depends on your plan and account."),
                       ("Can it do anything I ask?", "No. A scheduled task can use only the information and tools available to it. Web research depends on accessible sources, and tasks that use connected accounts need that connection and its permissions.")])),
        ],
    ),
    dict(
        slug="ai-profile-photo-prompts",
        tag="Prompt library",
        card_title="Make a profile photo with AI",
        card_desc="Upload two clear selfies, pick one of 50 looks and copy a complete prompt. LinkedIn, Instagram, WhatsApp, banners and more.",
        meta="50 prompts · Vol. 01",
        seo="50 AI Profile Photo Prompts for ChatGPT | FadeFlow",
        desc="Make a LinkedIn, Instagram or WhatsApp profile photo with AI. Upload two selfies, pick one of 50 looks and copy a complete ChatGPT prompt.",
        kicker="time.fade / Resources · The profile photo collection · Vol. 01",
        title="Make a profile photo with [AI].",
        sub="Upload two clear selfies. Pick a look. Copy a prompt.",
        hero_cta=("Choose a look", "#library"),
        hero_note="50 complete prompts · No special commands or settings",
        sections=[
            ("steps", dict(label="01 / Start here", title="Two photos. One full prompt.", sub="A quick guide",
                steps=[("Open ChatGPT", "Start a new chat. Choose a chat where image generation is available. Free access and limits can vary."),
                       ("Upload two clear selfies", "Of yourself or someone who has agreed: one front-facing and one slight side angle. Use natural light, visible face, no sunglasses, strong filters, or other people in the frame. You may add a third angle if available; two are enough to try."),
                       ("Copy one prompt", "Scroll to a look you want. Tap Copy prompt on that card, paste the complete text with your photos, and send. You need only ONE prompt per image."),
                       ("Inspect and correct", "Check the face, hands, clothes and crop. If something is wrong, reply: “Keep everything else. Correct only [the issue]. Match my uploaded face more closely.” You can regenerate if needed."),
                       ("Save and use it", "Use square portraits for Instagram, LinkedIn and WhatsApp DPs; a wide banner prompt for LinkedIn cover. Generated images can differ from your real appearance. Avoid presenting a fictional setting as a real event or workplace.")],
                note="Image generation availability and usage limits depend on your account. /slash names are not built-in ChatGPT commands; the full prompts do the work.")),
            ("photo_input", dict(label="Input guidance", title="A clear face. Natural light.",
                text="Photo A = clear front selfie. Photo B = the same person at a slight angle. These diagrams illustrate input quality; they are not example results.")),
            ("library", dict(label="02 / The prompt library", title="Pick your next look.",
                sub="Each prompt below is complete. Upload your photos and copy just ONE full prompt. The shared identity instructions are already included.")),
            ("prompt", dict(label="03 / Make an adjustment", title="Fix the result.",
                sub="Inspect the face, hands, clothes and crop. Replace [SPECIFIC ISSUE] with what needs fixing.",
                id="correction", heading="Correction prompt", text=PHOTO_CORRECTION_PROMPT, after="")),
        ],
    ),
    dict(
        slug="grocery-price-checker",
        tag="Prompt",
        card_title="Find the cheapest grocery basket",
        card_desc="One prompt compares your whole shopping list across supermarkets near you: live prices, offers, full-basket totals and travel costs.",
        meta="1 prompt · ChatGPT with web search",
        seo="AI Grocery Price Checker: Compare Supermarket Prices | FadeFlow",
        desc="Compare grocery prices across supermarkets with AI. Copy a prompt that checks current prices and offers, compares full baskets and recommends the cheapest place to shop.",
        kicker="time.fade / Resources · Everyday savings",
        title="Cheaper groceries, [checked by AI].",
        sub="One prompt compares your complete shopping list across supermarkets near you — offers, sizes, totals and travel costs included.",
        hero_cta=("Copy the prompt", "#prompt"),
        hero_note="Use ChatGPT with web search available. Results depend on which supermarket prices are published online.",
        sections=[
            ("steps", dict(label="01 / Get started", title="Five steps. One cheapest basket.",
                sub="Copy the prompt, answer two questions, compare the results.",
                steps=[("Open ChatGPT", "Start a new chat with web search available."),
                       ("Copy and paste the prompt", "Copy the full prompt below, paste it into ChatGPT and send it."),
                       ("Enter your grocery list", "Include quantities, sizes and preferred brands if you have them."),
                       ("Enter your location", "Give a city or area, for example Rolla, Sharjah."),
                       ("Compare the results", "ChatGPT searches for prices near you, compares the complete baskets and identifies the cheapest option.")],
                note="Online prices may differ from in-store prices. Always verify the final price and stock with the supermarket before purchasing.")),
            ("prompt", dict(label="02 / Copy & paste", title="Your grocery price checker",
                sub="Copy it all. ChatGPT will ask for your items and your location first.",
                id="prompt", heading="The complete prompt", text=GROCERY_PRICE_PROMPT,
                after="The prompt asks for only two answers before it searches: your shopping list and your city or area.")),
            ("examples", dict(label="03 / Try the example", title="Use this sample list.",
                sub="Paste it when ChatGPT asks what you want to buy.",
                items=["Onion — 1 kg", "Carrot — 1 kg", "Laundry detergent powder — 2 kg",
                       "Cooking oil — 1 litre", "Whole chicken — 1 kg", "Location: Rolla, Sharjah"],
                note="The point of the demo: compare the complete basket across supermarkets, instead of looking at individual discounts only.")),
            ("bullets", dict(label="04 / What it checks", title="What the comparison includes.", sub="",
                items=[("Every item, every store", "Lists each item and its price at each supermarket, marked as an offer or regular price."),
                       ("Fair comparisons", "Matches equivalent brands, sizes and quantities before comparing."),
                       ("Complete basket cost", "Calculates the total cost of the full shopping list at each store."),
                       ("Cheapest complete basket", "Names the supermarket with the lowest total, not just the best-looking discount."),
                       ("Mixed-store option", "Checks whether buying different items at different stores saves money after extra travel or delivery costs."),
                       ("Verified sources", "Prefers official websites and current catalogues, with source links and the date checked."),
                       ("Honest gaps", "Writes “Price unavailable” when a price cannot be verified, shows a partial total and never counts missing items as zero.")])),
            ("faq", dict(label="05 / A little help", title="Before you go.",
                sub="A few things to know about online grocery prices.",
                items=[("Do I need ChatGPT with web search?", "Yes. The comparison uses internet search for current supermarket prices and offers. Without it, ChatGPT cannot check what is being sold near you right now."),
                       ("Which supermarkets does it check?", "The prompt asks for LuLu, Nesto, Carrefour, Sharjah Coop and other available supermarkets near your location. What appears depends on which stores publish prices online for that area."),
                       ("What if a price is unavailable?", "The prompt tells ChatGPT to write “Price unavailable”, show a partial total and explain what is missing. Missing prices are never treated as zero."),
                       ("Are catalogue prices the same as live website prices?", "Not always. The prompt asks ChatGPT to clearly distinguish live website prices from catalogue prices and to include source links and the date each price was checked."),
                       ("Can I use this outside Sharjah?", "Yes. Give any city or area when ChatGPT asks. Results depend on what that area’s supermarkets publish online."),
                       ("Should I buy everything at the cheapest store?", "Not automatically. Check the mixed-store comparison too: a few dirhams saved can be lost on extra travel or delivery costs. The prompt asks for those costs before recommending a split basket.")])),
        ],
    ),
    dict(
        slug="chatgpt-book-codes",
        tag="Guide",
        card_title="4 ChatGPT codes for any book",
        card_desc="Paste one setup prompt, attach a book and type /visualnotes, /mentalmodels, /chaptermap or /themes. Plus 36 more book codes for notes, study and book clubs.",
        meta="40 codes · 1 setup prompt",
        seo="40 ChatGPT Book Codes: /visualnotes, /mentalmodels & More | FadeFlow",
        desc="Paste one prompt into ChatGPT, attach a book and type /visualnotes, /mentalmodels, /chaptermap or /themes. Includes 40 book codes for notes, study, quotes and book clubs.",
        kicker="time.fade / Free guides · Read a book with codes",
        title="Read any book with [codes].",
        sub="One setup prompt teaches ChatGPT 40 shortcuts. Attach a book, type /visualnotes and get visual notes you can scan in minutes.",
        hero_cta=("Copy the setup prompt", "#prompt"),
        hero_note="Works in ChatGPT on any plan, including free. Web, desktop or the phone app.",
        sections=[
            ("steps", dict(label="01 / How it works", title="Three steps. Start with four codes.",
                sub="Run them in the same chat, so ChatGPT already has the book every time.",
                steps=[("Paste the setup prompt", "Open a new chat in ChatGPT, paste the prompt below and send it. It should reply “Codes ready. Which book are we reading?”"),
                       ("Give ChatGPT the book", "Attach the PDF with + → Add photos & files, paste in a chapter, or just name a title. An attached book or pasted text works best; a title alone can be inaccurate and cannot produce exact quotes."),
                       ("Type your first code", "Send /visualnotes, then /mentalmodels, /chaptermap and /themes in the same chat. Each code is a shortcut for a full instruction."),
                       ("Zoom in or stack codes", "Use /visualnotes chapter 3 for one part, or /chaptermap /quotes to get two outputs at once."),
                       ("Keep the codes in every chat", "A pasted setup prompt lasts for that chat only. For every new chat, paste it again or save it under Settings → Personalization → Custom instructions.")],
                note="Codes are plain text shortcuts, not built-in ChatGPT commands. If a / menu pops up while typing, ignore it and keep typing.")),
            ("prompt", dict(label="02 / Copy & paste", title="Teach ChatGPT every code",
                sub="Copy it all into a new chat and send. Takes ten seconds.",
                id="prompt", heading="The setup prompt", text=BOOK_CODES_PROMPT,
                after="If the reply isn’t “Codes ready”, paste the prompt again at the top of the chat.")),
            ("examples", dict(label="03 / The routine", title="Your four codes, in order.",
                sub="This is the exact routine from the video. Do all four in one chat.",
                items=["/visualnotes — short visual notes of the whole book, with headings, icons and simple diagrams.",
                       "/mentalmodels — a visual map of the biggest ideas and how they connect.",
                       "/chaptermap — every chapter, its key point and how it fits into the whole book.",
                       "/themes — the major themes, where they appear and what they really mean."],
                note="Want to keep it? /sketchnote makes one saveable image of the big ideas, and /savenotes gives you clean notes for your notes app.")),
            ("codes", dict(label="04 / The full list", title="All 40 [codes].",
                sub="Search or filter by group. Copy a code, then paste it into ChatGPT with your book.",
                groups=BOOK_CODE_GROUPS, search_placeholder="Search codes, e.g. quotes or quizme", noun="codes")),
            ("faq", dict(label="05 / Quick fixes", title="If a code [doesn’t] land.",
                sub="The usual problems, and what to do.",
                items=[("ChatGPT doesn’t know a code", "Paste the setup prompt at the top of the chat, or save it in your custom instructions so it is there every time."),
                       ("The codes worked yesterday, but not in a new chat", "A pasted setup prompt only lasts for that chat. Save it under Settings → Personalization → Custom instructions."),
                       ("A menu pops up when I type /", "Ignore it and keep typing. The code still works."),
                       ("The notes are vague or skip chapters", "The book is probably too long for one go. Add the chapter after the code, like /visualnotes chapter 6, or give it one chapter at a time."),
                       ("The file won’t upload", "Paste the text of a chapter instead, or split the PDF into smaller parts."),
                       ("It’s getting details wrong", "It is probably working from the title alone. Attach the book or paste a chapter, and say “stick to the text.”"),
                       ("/quotes won’t give exact quotes", "It needs the actual text. Attach the book or paste the chapter first."),
                       ("I don’t want spoilers", "Use /sofar with the chapter you are on, or add “no spoilers past chapter 8” to any code."),
                       ("The map comes out as a plain list", "Say “draw it as a diagram with arrows.”"),
                       ("/quizme stops after one question", "Type /quizme again or say “keep going, one question at a time.”")])),
        ],
    ),
]

FLIGHT_TRACKER_PROMPT = """--- ✈️ YOUR TRIP SETUP (EDIT THESE) ---
• FROM & TO: Dubai (DXB) to Kozhikode (CCJ)
• DATE WINDOW: Dec 1 to Jan 31
• MAX BUDGET: Under AED 600
• DAILY ALERT TIME: 8:00 AM  (Optional: leave blank or delete if you want an instant one-time check)
---------------------------------------

Use Google Flights to search for flights matching my FROM & TO route and DATE WINDOW above.

If DAILY ALERT TIME is provided, schedule this action to run automatically every day at that exact time and send me a mobile push notification. If no time is provided, run the check right now.

Requirements:
1. Prioritize non-stop / direct flights under my MAX BUDGET.
2. If no flights meet the budget, find the absolute cheapest available direct dates across the entire window.
3. For every match, list:
   - Travel Date & Day
   - Airline & Flight Timings
   - Exact Ticket Price
   - Direct Google Flights booking link"""

# Shared by direct link only (DMs). Not on the hub, sitemap or llms files; noindex.
RESOURCES.append(dict(
    slug="gemini-flight-tracker",
    unlisted=True,
    tag="Prompt",
    card_title="Automated flight deal tracker",
    card_desc="Set your route, dates and budget once. Gemini checks Google Flights and sends you the cheapest direct flights.",
    meta="1 prompt · Google Gemini",
    seo="Automated Flight Deal Tracker Prompt for Gemini | time.fade",
    desc="Copy a Google Gemini prompt that checks Google Flights for your route, dates and budget, daily or right now, and lists the cheapest direct flights with booking links.",
    kicker="time.fade / Resources · Flight deal tracker",
    title="Track cheap flights with [Gemini].",
    sub="Set your route, dates and budget once. Gemini searches Google Flights and sends you the best direct deals, every day or right now.",
    hero_cta=("Copy the prompt", "#prompt"),
    hero_note="Here is the exact automated flight tracker setup for Google Gemini.",
    sections=[
        ("steps", dict(label="01 / How to set it up", title="Four steps. Daily deal alerts.",
            sub="Edit the top four lines, then send.",
            steps=[("Open Gemini", "Open the Google Gemini app on your phone (iOS or Android) or go to gemini.google.com in your browser."),
                   ("Customize your trip details", "Copy the prompt below and edit the top 4 lines: FROM & TO, DATE WINDOW, MAX BUDGET and DAILY ALERT TIME."),
                   ("Hit send", "Gemini will confirm your schedule (e.g., “Scheduled daily at 8:00 AM”)."),
                   ("Receive your daily deal alert", "Every morning at your chosen time, Gemini scans Google Flights in the background and sends a push notification to your phone lock screen showing the lowest prices and direct links to book!")],
            note="Pro tip: you can view, pause, or cancel your active trackers anytime inside the Gemini app by tapping the left menu and selecting Scheduled.")),
        ("prompt", dict(label="02 / Copy & paste", title="Your flight tracker prompt",
            sub="Copy it all, edit the trip setup at the top, then send it to Gemini.",
            id="prompt", heading="Your trip setup + prompt", text=FLIGHT_TRACKER_PROMPT,
            after="Scheduled actions, alert times and notifications depend on your Gemini app, plan and region. Prices come from Google Flights at the time of each check, so always confirm the fare on the booking page.")),
        ("bullets", dict(label="03 / Edit these", title="Your top four lines.", sub="",
            items=[("FROM & TO", "Your departure and arrival airport codes or cities (e.g., Abu Dhabi to Kochi, Dubai to Mumbai)."),
                   ("DATE WINDOW", "The range of dates you are willing to fly (e.g., Nov 15 to Dec 20, or specific dates)."),
                   ("MAX BUDGET", "Your ideal maximum price (e.g., Under AED 500)."),
                   ("DAILY ALERT TIME", "For a daily notification on your lock screen, put your preferred time (e.g., 8:00 AM, 7:30 PM). For an instant one-time scan, leave this line blank or delete it!")])),
    ],
))

EXPERIMENTS = [
    dict(n="01", title="The AED 50 fine", status="Shipped as a guide",
         text="I fined myself AED 50 for every missed daily video. Instead of relying on willpower, I scheduled ChatGPT to research content ideas for me every day.",
         link="chatgpt-scheduled-tasks"),
    dict(n="02", title="Roasting profiles with AI", status="Shipped as a prompt",
         text="Can one prompt give an honest, specific profile review without inventing facts? We built a reviewer that only judges what’s visible and ends with a ready-to-paste rewrite.",
         link="profile-roast-prompt"),
    dict(n="03", title="AI profile photos from two selfies", status="Shipped as a library",
         text="How far can two clear selfies go? We wrote 50 complete looks with identity rules built in, plus a correction prompt for when something is off.",
         link="ai-profile-photo-prompts"),
]
