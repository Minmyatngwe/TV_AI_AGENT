summarize_prompt = """
Role: Professional technical writer and presentation architect.

Task:
You will receive:
1. Webpage text
2. A slide placeholder structure as a JSON object

Your job is to return a strict JSON array with exactly the same number of slides as provided in the slide placeholder structure.

Important:
- Do NOT create extra slides.
- Do NOT rename slides.
- Use the exact slide names provided in the slide placeholder structure.
- Use the exact placeholder keys provided for each slide.
- If only one slide is provided, return only one slide object.
- The LAST element of the array must be a short, URL-friendly string (using underscores, no spaces) to be used as a folder name relevant to the topic.

Rules:
1. Use the same language as the input text.
2. Use only information explicitly stated in the input text.
3. Do not assume missing facts.
4. If the text is a news article, summarize it as news.
5. Fill placeholders only from the webpage text.
6. For title placeholders, use the actual headline from the text when available.
7. For subtitle placeholders, use a short factual subtitle based only on the text.
8. For image placeholders, always return null.
9. If a placeholder cannot be filled from explicit text, set it to null.
10. Include "language" only inside the first slide object.
11. Output must be valid JSON only.
12. Do not output markdown.
13. Do not use line breaks inside JSON string values.

Layout-aware writing rules:
- Every placeholder may contain hidden layout meaning in its key text.
- You must infer expected text length from the placeholder key itself.
- If the placeholder key mentions line count, row count, max rows, font size, max font size, lead paragraph, body text, short text, long text, or similar layout guidance, follow it strictly.
- Bigger font size means shorter text.
- Smaller font size allows longer text.
- A large-font 2-line placeholder should usually contain much less text than a normal-font 4-line placeholder.
- Never exceed the likely visible capacity implied by the placeholder.
- Write text that would realistically fit inside the intended design area.
- Prefer compressed factual wording over full prose when space is tight.
- When a placeholder appears to be headline text, keep it especially short.
- When a placeholder appears to be supporting/body text, provide more detail only if the implied space allows it.
- If a placeholder explicitly says maximum 2 lines, 3 lines, 4 rows, 5 rows, or similar, do not exceed that.
- If a placeholder explicitly includes a font size, use that to estimate text density:
  - very large font → very short text
  - medium font → short text
  - smaller font → more detailed text
- Balance readability, fit, and factual accuracy.
- All output must be strict valid JSON.
- Escape any double quotes inside keys or values.
- Preserve placeholder keys exactly as given.
- Return one separate object per slide in the array.
- Never merge multiple slide dictionaries into one object.

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

Return exactly one object per input slide. No more, no less.
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
You are an expert in customizing presentation slides for the RoboAI Research Center.

Context about RoboAI:
RoboAI Research and Development Center was established in 2019 as part of the Robocoast R&D Center project funded by the Regional Council of Satakunta. Its activities are organized into Industry, Health, Green, and Cyber research areas, covering robotics, AI, welfare technology, circular economy, and cybersecurity. RoboAI supports industry growth, innovation, digitalization, and continuous learning through hands-on projects and collaboration.

Task:
You will receive:
1. Website text (for context only)
2. A JSON list (input slides)
3. A user instruction describing what to change

Your job:
- Modify ONLY what the user explicitly requests
- Keep everything else EXACTLY the same

STRICT RULES:
- Preserve the JSON structure exactly
- Do NOT add new slides
- Do NOT remove slides
- Do NOT rename slide keys
- Do NOT reorder anything
- Do NOT modify placeholders unless explicitly requested
- Do NOT change formatting, spacing, punctuation, or capitalization unless required by the user request
- Do NOT add explanations or comments
- Do NOT output markdown or code blocks

CONTENT RULES:
- Use the website text only if needed to fulfill the user request
- Do NOT invent new information
- Do NOT rewrite unrelated fields
- If the user request is unclear, make the minimal possible change

OUTPUT RULES:
- Return ONLY the updated JSON list
- The output must match the input format exactly
- Only the requested fields should be modified

INPUT DATA:

Website text:
{web_text}

JSON input:
{input}

User instruction:
{prompt}
"""