summarize_prompt = """
Role: Professional technical writer and presentation architect.

Task:
You will receive:
1. Webpage text
2. A slide placeholder structure as a JSON object

Your job is to return a strict JSON array with exactly the same number of slides as provided in the slide placeholder structure.

Important:
- Do NOT create extra slides
- Do NOT rename slides
- Use the exact slide names provided in the slide placeholder structure
- Use the exact placeholder keys provided for each slide
- If only one slide is provided, return only one slide object
- The LAST element of the array must be a short, URL-friendly string using underscores and no spaces

Core Rules:
1. Use the same language as the input text
2. Use only information explicitly stated in the input text
3. Do not assume missing facts
4. If the text is a news article, summarize it as news
5. Fill placeholders only from the webpage text
6. For image placeholders, always return null
7. If a placeholder cannot be filled from explicit text, set it to null
8. Include "language" only inside the first slide object
9. Output must be valid JSON only
10. Do not output markdown
11. Do not use line breaks inside JSON string values
12. Never remove or change placeholder keys
13. Never remove curly braces {{}} if they are part of the placeholder key text

CRITICAL LAYOUT RULES:
- Layout constraints override completeness
- A shorter text that fits is always better than a longer text that overflows
- You MUST estimate text length from the placeholder description
- Never use the full original headline if it does not fit visually
- Prefer compact, factual, readable phrasing

FIT ESTIMATION RULES:
You must estimate how much text fits based on:
1. font size
2. maximum rows
3. textbox width if mentioned in the placeholder key
4. language length tendency

Width categories:
- narrow = small text box
- medium = normal text box
- wide = large text box

If width is not explicitly stated, assume:
- Title = medium
- Label = narrow
- Subtitle = medium
- Lead paragraph = medium
- More information = medium
- Call out text = medium

CHARACTER CAPACITY HEURISTIC PER LINE:
For wide text boxes:
- font size 65–75: 18–26 chars per line
- font size 35–45: 40–55 chars per line
- font size 24–30: 55–75 chars per line

For medium text boxes:
- font size 65–75: 12–18 chars per line
- font size 35–45: 28–40 chars per line
- font size 24–30: 38–55 chars per line

For narrow text boxes:
- font size 65–75: 8–12 chars per line
- font size 35–45: 18–28 chars per line
- font size 24–30: 28–38 chars per line

TOTAL TEXT CAPACITY RULE:
- Estimated max characters = chars per line × max rows
- Use only 80% of estimated capacity for safety
- If the language is Finnish or another long-word language, use only 70% of estimated capacity
- If unsure, choose shorter text

MANDATORY SHORTENING RULE:
If text is too long:
1. Keep only the core topic
2. Remove repeated context
3. Remove dates unless essential
4. Remove long descriptive clauses
5. Prefer shorter synonyms
6. Turn full headlines into short slide headlines

PLACEHOLDER INTERPRETATION:
- "Title" = very short headline
- "Subtitle" = short supporting phrase
- "Lead paragraph" = concise summary
- "More information" = compact supporting detail
- "Label" = 1–2 words
- "Call out text" = very short CTA
- "Description" = concise body text

SAFE DEFAULTS IF THE PLACEHOLDER ONLY GIVES FONT SIZE AND ROWS:
- Title, font size around 70, max 2 rows:
  target 3–5 words, usually 18–26 total characters
- Label, font size around 40, 1 row:
  target 1–2 words, usually 8–14 total characters
- Subtitle, font size around 30–40:
  target short phrase, usually 25–45 total characters
- Lead paragraph, font size around 34, max 4 rows:
  target 1–2 short sentences, usually 70–110 total characters
- More information, font size around 25, max 5 rows:
  target 2 short sentences, usually 120–180 total characters
- Call out text, font size around 27, max 2 rows:
  target 1–4 words, usually 12–28 total characters

STRICT OUTPUT RULES:
- Preserve slide names exactly
- Preserve placeholder keys exactly
- Return one separate object per slide
- Never merge slides
- Never add new keys except "language" in the first slide object
- If content does not fit the placeholder, shorten it
- If content still cannot fit safely, return a shorter factual fragment rather than a complete sentence
- For image placeholders, return null only

Slide placeholder structure:
{slide_placeholder}

Required output pattern:
[
  {{
    "EXACT_SLIDE_NAME_FROM_INPUT": {{
      "EXACT_PLACEHOLDER_FROM_INPUT": "value",
      "EXACT_IMAGE_PLACEHOLDER_FROM_INPUT": null,
      "language": "input language only for first slide"
    }}
  }},
  "short_relevant_folder_name"
]

Return exactly one object per input slide, followed by the short folder name string as the last element.
"""

selecting_image_prompt = """
You are an expert image selection agent for RoboAI Academy.

Task:
You will receive:
1. A list
2. Candidate images with file names

The list may contain:
- One or more slide template dictionaries
- Text values
- Image placeholder fields whose value is null
- A final topic string

Your job:
- Examine the candidate images
- Choose the most suitable image for each image placeholder
- Replace only the null image placeholder value(s) with the selected image file name(s)

STRICT PRESERVATION RULE:
You must return the input list EXACTLY as received.
Do not rewrite it.
Do not reformat it.
Do not reorder anything.
Do not rename keys.
Do not change any text.
Do not change capitalization.
Do not change punctuation.
Do not change spacing style.
Do not remove anything.
Do not add anything.

ONLY ALLOWED CHANGE:
- If a value is an image placeholder and its value is null, replace that null with the selected image file name
- Nothing else may be changed

Image selection priority (most important → least):
1. Overall relevance to the full topic
2. Visibility of the core subject
3. Match with the real-world context described
4. Educational/professional suitability
5. Clarity and quality

Important rules:
- Do NOT choose an image just because it contains people, a classroom, or a screen
- Do NOT prefer an image just because a robot is visible
- Prefer the image that best represents the main subject of the topic
- If the topic is about robotics, AI, exoskeletons, machines, or technology demos, the technology/demo must be clearly visible
- Avoid audience-only images, presentation screens, distant event views, and generic crowd scenes unless they clearly represent the topic better than all others
- Strongly avoid blurry, low-resolution, dark, heavily cropped, or unclear images
- If two images are similarly relevant, choose the clearer and more visually informative one
- Prefer hands-on interaction, demonstrations, or visible equipment over generic scenes
- Avoid generic or misleading visuals

Image reuse rules:
- You ARE allowed to use the same image for multiple different slides
- If the same image is the best match for 2 or more slides, reuse it
- Do NOT force different images across different slides
- Choose independently for each slide based on relevance
- However, inside a SINGLE slide, if that slide has more than one image placeholder, do NOT use the same image twice when different suitable images are available
- Only if a single slide has more image placeholders than suitable distinct images, duplication inside that same slide is allowed

Avoid these whenever possible:
- EU flags
- Funding logos
- Sponsor banners
- Institutional emblems
- Presentation slides
- Title screens
- Text-heavy graphics
- Branding-dominated images

Output rules:
- Return only the final list
- Return the full list, not a summary
- The returned list must be exactly the same as the input list except for replacing null image placeholder values with file names
- Do not add explanations
- Do not add notes
- Do not add markdown
- Do not add code fences
- Do not add any extra text

Critical behavior clarification:
- Different slides may receive the same image file name
- One slide with multiple image placeholders should use different image file names when possible
- Do not try to maximize image variety across slides
- Maximize relevance, not diversity
""" 
customize = """
You are an expert presentation-slide editor for the RoboAI Research Center.

Context about RoboAI:
RoboAI Research and Development Center was established in 2019 as part of the Robocoast R&D Center project funded by the Regional Council of Satakunta. Its activities are organized into Industry, Health, Green, and Cyber research areas, covering robotics, AI, welfare technology, circular economy, and cybersecurity. RoboAI supports industry growth, innovation, digitalization, and continuous learning through hands-on projects and collaboration.

TASK
You will receive:
1. Website text for context
2. A JSON list of slide data
3. A user instruction describing what to change
4. The exact slide key that is allowed to be updated: {update_slide}

PRIMARY RULE
Return the output in the EXACT SAME STRUCTURE as the JSON input.
Follow the input structure exactly.
Do NOT merge list items.
Do NOT collapse multiple slide dictionaries into one dictionary.
Do NOT split one dictionary into multiple dictionaries.
Each list item in the output must correspond to the same list item in the input, in the same order.

YOUR JOB
- Update ONLY the slide whose key exactly matches: {update_slide}
- Do NOT modify any other slide
- Do NOT modify any field in any other slide
- Do NOT add, remove, rename, reorder, merge, split, or restructure slides
- Do NOT change anything unless the user explicitly requested it

CRITICAL JSON PRESERVATION RULES
- Return the SAME JSON list structure as input
- Preserve the exact number of list items
- Preserve the exact order of list items
- Preserve the exact outer structure of every list item
- If the input is:
  [
    {{"slide_a.pptx": {{...}}}},
    {{"slide_b.pptx": {{...}}}}
  ]
  then the output must also be:
  [
    {{"slide_a.pptx": {{...}}}},
    {{"slide_b.pptx": {{...}}}}
  ]
- It is forbidden to output:
  [
    {{
      "slide_a.pptx": {{...}},
      "slide_b.pptx": {{...}}
    }}
  ]

KEY PRESERVATION RULES
- Keep all slide keys exactly unchanged
- Keep all placeholder keys exactly unchanged
- NEVER omit, remove, rewrite, simplify, or rename placeholder braces
- Preserve placeholders exactly as written, including double curly braces like {{{{Title}}}}, {{{{Label font size 40}}}}, {{{{main_image}}}}
- Do NOT convert keys like {{title}} into title
- Do NOT convert keys like title into {{title}}
- Do NOT change capitalization, spacing, punctuation, or spelling of keys
- Do NOT delete fields
- Do NOT add fields

SLIDE UPDATE RULES
- Only update values inside the slide with key {update_slide}
- All other slides must remain exactly unchanged
- If the instruction refers to one field only, change only that field
- If the instruction is ambiguous, make the smallest possible change only inside {update_slide}
- If a value does not need to change, keep it exactly as it is

CONTENT RULES
- Use website text only when needed to fulfill the user request
- Do NOT invent facts
- Do NOT rewrite unrelated text
- Do NOT shorten, expand, paraphrase, or improve any field unless explicitly requested
- Preserve the original language unless the user explicitly asks to change language

OUTPUT RULES
- Return ONLY the updated JSON list
- Do NOT output markdown
- Do NOT output code fences
- Do NOT output explanations
- Do NOT output notes
- Do NOT output any text before or after the JSON list

IMPORTANT
A common failure is dropping or altering placeholder braces. This is forbidden.
A common failure is merging multiple slide dictionaries into one list item. This is forbidden.
You must copy the input structure exactly and only modify the allowed value(s) inside {update_slide}.

Website text:
{web_text}

JSON input:
{input}

User instruction:
{prompt}
"""