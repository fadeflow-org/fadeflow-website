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
]

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
