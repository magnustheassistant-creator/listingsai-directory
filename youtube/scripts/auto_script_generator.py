#!/usr/bin/env python3
"""
Auto-generate a video script from tool metadata.
Run: python3 auto_script_generator.py <tool-name>
"""
import json, sys, os, re

TOOLS_JSON = "/home/hermes/listingsai.directory/tools.json"
OUTPUT_DIR = "/home/hermes/brain-storm-corp/youtube/scripts"

def load_tools():
    with open(TOOLS_JSON) as f:
        return json.load(f)

def find_tool(tools, name):
    for t in tools:
        slug = t['name'].lower().replace(' ', '-').replace('/', '-')
        if slug == name or t['name'].lower().replace(' ', '-') == name.replace('_', '-'):
            return t
    # partial match
    for t in tools:
        if name.lower() in t['name'].lower() or t['name'].lower() in name.lower():
            return t
    return None

def generate_script(tool):
    name = tool['name']
    category = tool.get('category', 'productivity')
    desc = tool.get('description', '')
    affil = tool.get('affiliate_url', '')

    affil_block = ""
    if affil:
        affil_name = affil.split('/')[-2] if '/' in affil else name
        affil_block = f"\n**Affiliate:** {affil_name} — {affil}\n"

    slug = name.lower().replace(' ', '-').replace('/', '-')
    script = f"""# Video: {name}

**Status:** AUTO-GENERATED SCRIPT
**Tool:** {slug}
**Tool URL:** https://listingsai.directory/tools/{slug}.html{affil_block}
**Duration:** 90 seconds
**Category:** {category}

---

## Video Script

### HOOK (0-10s)
"Most {category} tools are confusing, expensive, or both. There's a free one that actually works — and today I'm showing you exactly how to use it."

### TOOL INTRO (10-20s)
"This is {name}. It helps real estate agents with {desc[:100]}. It's completely free, no signup required."

### DEMO (20-55s)
"Let's watch it in action. [Show the tool generating output]. Takes under 30 seconds. Look at the quality — this is what professional results look like."

### FEATURES (55-70s)
"Three things that make this stand out: First, it's instant. Second, it's free. Third, it actually works — no fluff, no watermarks."

### CTA (70-85s)
"Try it free — link in the description. No credit card, no signup, just results. If this helped you, subscribe and I'll see you in the next one."

### END CARD (85-90s)
"{name} — Free AI Tools for Real Estate. Visit listingsai.directory"
"""
    return script

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 auto_script_generator.py <tool-name>")
        sys.exit(1)

    tool_name = sys.argv[1]
    tools = load_tools()
    tool = find_tool(tools, tool_name)

    if not tool:
        print(f"Tool not found: {tool_name}")
        print("Available tools:")
        for t in tools[:20]:
            print(f"  {t['name']}")
        sys.exit(1)

    script = generate_script(tool)
    slug = tool['name'].lower().replace(' ', '-').replace('/', '-')
    out_file = os.path.join(OUTPUT_DIR, f"video-AUTO-{slug}.md")

    with open(out_file, 'w') as f:
        f.write(script)

    print(f"Generated: {out_file}")
    print(f"\nTool: {tool['name']}")
    print(f"Category: {tool.get('category')}")
    print(f"Description: {tool.get('description','')[:100]}")
