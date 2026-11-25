#!/usr/bin/env python3
"""Sync the Claude plugin's product skills from a checkout of scrapfly/skills."""

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

MAPPING = {
    "scrapfly-scraper": "web-scraping-api",
    "scrapfly-screenshot": "screenshot-api",
    "scrapfly-extraction": "extraction-api",
    "scrapfly-browser": "cloud-browser",
}

DESCRIPTIONS = {
    "web-scraping-api": 'Load first for any request to scrape, fetch or read the content of a URL ("scrape this page", "get this page", "fetch the JSON at", "read this site in markdown"), before calling web_get_page or web_scrape. Covers Scrapfly\'s Web Scraping API: which tool and settings cost least, JavaScript rendering, proxy pool and country, the Unblocker, headers, cookies, POST bodies, browser scenarios, cache, output formats and error codes.',
    "screenshot-api": 'Load first for any request to screenshot or capture a web page or one of its elements ("screenshot this page", "capture the header of", "show me what this site looks like on mobile"), before calling the MCP tool screenshot. Covers Scrapfly\'s Screenshot API: format, full page or selector capture, resolution, country, waits, banner blocking, dark mode, accessibility simulations, costs and error codes.',
    "extraction-api": 'Load first for any request to extract, parse or get structured data (names, prices, a list, fields, JSON, a table) from a web page or a document, before fetching it ("extract the products from", "get the price and name as JSON", "parse this HTML into fields"). Covers Scrapfly\'s Extraction API on a URL through the MCP tool web_scrape, or on HTML, markdown, text or XML at hand over HTTP: an LLM prompt, a predefined AI model (product, article, review_list, job_posting and more) or a template of selectors, their costs and error codes.',
    "cloud-browser": 'Load first for any request to open a browser, click, fill a form, log in or move through pages ("open a browser on", "click the second product", "log in and", "automate this site with Playwright", "give my agent a browser"), before calling the Cloud Browser tools. Covers Scrapfly\'s Cloud Browser: the MCP session tools, CDP from Playwright, Puppeteer, Browser Use and Stagehand, session parameters, bandwidth savings, costs and error codes.',
}


class SyncError(Exception):
    pass


def synchronized_skill(source: Path, target_name: str) -> str:
    text = source.read_text()
    if not text.startswith("---\n"):
        raise SyncError(f"{source}: missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise SyncError(f"{source}: unterminated front matter")
    lines = text[4:end].splitlines()
    names = [i for i, line in enumerate(lines) if line.startswith("name:")]
    if len(names) != 1:
        raise SyncError(f"{source}: expected one name field")
    lines[names[0]] = f"name: {target_name}"
    descriptions = [i for i, line in enumerate(lines) if line.startswith("description:")]
    if len(descriptions) != 1:
        raise SyncError(f"{source}: expected one description field")
    description_end = next((i for i in range(descriptions[0] + 1, len(lines)) if lines[i].startswith("user-invocable:")), len(lines))
    del lines[descriptions[0] + 1:description_end]
    lines[descriptions[0]] = "description: '" + DESCRIPTIONS[target_name].replace("'", "''") + "'"
    invocable = [i for i, line in enumerate(lines) if line.startswith("user-invocable:")]
    if invocable:
        lines[invocable[0]] = "user-invocable: false"
    else:
        lines.append("user-invocable: false")
    content = "---\n" + "\n".join(lines) + text[end:]
    override = Path(__file__).parent / "skill-overrides" / f"{target_name}.md"
    if override.is_file():
        content = content.rstrip() + "\n\n" + override.read_text()
    return content


def refuse_symlinks(skill_dir: Path) -> None:
    for current, directories, files in os.walk(skill_dir, followlinks=False):
        for name in directories + files:
            path = Path(current) / name
            if path.is_symlink():
                raise SyncError(f"{path}: source symlinks are not published")


def build(skills_dir: Path, output_dir: Path) -> Path:
    if not (skills_dir / "skills").is_dir():
        raise SyncError(f"{skills_dir}: no skills/ directory")
    refuse_symlinks(skills_dir)
    stage = Path(tempfile.mkdtemp(prefix="claude-plugin-sync-")) / "plugin"
    shutil.copytree(output_dir, stage)
    for source_name, target_name in MAPPING.items():
        source = skills_dir / "skills" / source_name / "SKILL.md"
        if not source.is_file():
            raise SyncError(f"{source}: missing skill")
        content = synchronized_skill(source, target_name)
        target = stage / "skills" / target_name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source.parent, target)
        (target / "SKILL.md").write_text(content)
    return stage


def differs(stage: Path, output_dir: Path) -> list[str]:
    changed = []
    for target_name in MAPPING.values():
        left = stage / "skills" / target_name
        right = output_dir / "skills" / target_name
        left_files = {str(path.relative_to(left)): path.read_bytes() for path in left.rglob("*") if path.is_file()}
        right_files = {str(path.relative_to(right)): path.read_bytes() for path in right.rglob("*") if path.is_file()} if right.exists() else {}
        if left_files != right_files:
            changed.append(target_name)
    return changed


def sync(skills_dir: Path, output_dir: Path, check: bool) -> int:
    stage = build(skills_dir, output_dir)
    changed = differs(stage, output_dir)
    if check:
        if changed:
            print("out of date: " + ", ".join(changed))
            return 1
        return 0
    backup_root = Path(tempfile.mkdtemp(prefix="claude-plugin-backup-"))
    backups = {name: backup_root / name for name in MAPPING.values()}
    created = set()
    backed_up = set()
    try:
        for target_name in MAPPING.values():
            target = output_dir / "skills" / target_name
            if target.exists():
                shutil.copytree(target, backups[target_name])
                backed_up.add(target_name)
                shutil.rmtree(target)
            else:
                created.add(target_name)
            shutil.copytree(stage / "skills" / target_name, target)
    except Exception:
        for target_name in MAPPING.values():
            target = output_dir / "skills" / target_name
            if target_name in backed_up:
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(backups[target_name], target)
            elif target_name in created and target.exists():
                shutil.rmtree(target)
        raise
    finally:
        shutil.rmtree(backup_root, ignore_errors=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", required=True, type=Path, help="a checkout of scrapfly/skills")
    parser.add_argument("--out", required=True, type=Path, help="the Claude plugin checkout")
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args()
    try:
        return sync(args.skills, args.out, args.check)
    except SyncError as error:
        print(error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
