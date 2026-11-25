import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("sync_skills", Path(__file__).resolve().parents[1] / "sync-skills.py")
sync_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_skills)


class SyncSkillsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.skills = self.root / "source"
        self.plugin = self.root / "plugin"
        for source_name, target_name in sync_skills.MAPPING.items():
            source = self.skills / "skills" / source_name
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text(f"---\nname: {source_name}\ndescription: source {source_name}\n---\n\n# {source_name}\n")
            target = self.plugin / "skills" / target_name
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text(f"---\nname: {target_name}\nuser-invocable: false\n---\n\nold {target_name}\n")
            (target / "stale.txt").write_text("stale")
        (self.plugin / ".claude-plugin").mkdir()
        (self.plugin / ".claude-plugin/plugin.json").write_text('{"name":"scrapfly"}')
        for name in ("scrapfly", "mcp-server"):
            target = self.plugin / "skills" / name
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text(f"---\nname: {name}\n---\n\nplugin-specific\n")

    def tearDown(self):
        self.temp.cleanup()

    def test_sync_replaces_only_the_mapped_product_skills(self):
        self.assertEqual(sync_skills.sync(self.skills, self.plugin, False), 0)

        for source_name, target_name in sync_skills.MAPPING.items():
            target = self.plugin / "skills" / target_name / "SKILL.md"
            text = target.read_text()
            self.assertTrue(text.startswith("---\nname:"), text[:80])
            self.assertIn(f"name: {target_name}\n", text)
            self.assertIn("description: 'Load first", text)
            self.assertNotIn("description: source", text)
            self.assertIn("user-invocable: false", text)
            self.assertIn(f"# {source_name}", text)
            self.assertNotIn(f"old {target_name}", text)
            self.assertFalse((target.parent / "stale.txt").exists())
        self.assertEqual((self.plugin / ".claude-plugin/plugin.json").read_text(), '{"name":"scrapfly"}')
        for name in ("scrapfly", "mcp-server"):
            self.assertIn("plugin-specific", (self.plugin / "skills" / name / "SKILL.md").read_text())

    def test_check_reports_drift_without_writing_then_passes_after_sync(self):
        before = (self.plugin / "skills/web-scraping-api/SKILL.md").read_text()

        self.assertEqual(sync_skills.sync(self.skills, self.plugin, True), 1)
        self.assertEqual((self.plugin / "skills/web-scraping-api/SKILL.md").read_text(), before)
        self.assertEqual(sync_skills.sync(self.skills, self.plugin, False), 0)
        self.assertEqual(sync_skills.sync(self.skills, self.plugin, True), 0)

    def test_a_missing_source_leaves_the_plugin_untouched(self):
        before = (self.plugin / "skills/web-scraping-api/SKILL.md").read_text()
        (self.skills / "skills/scrapfly-scraper/SKILL.md").unlink()

        with self.assertRaises(sync_skills.SyncError):
            sync_skills.sync(self.skills, self.plugin, False)

        self.assertEqual((self.plugin / "skills/web-scraping-api/SKILL.md").read_text(), before)

    def test_invalid_front_matter_leaves_the_plugin_untouched(self):
        before = (self.plugin / "skills/web-scraping-api/SKILL.md").read_text()
        (self.skills / "skills/scrapfly-scraper/SKILL.md").write_text("no front matter\n")

        with self.assertRaises(sync_skills.SyncError):
            sync_skills.sync(self.skills, self.plugin, False)

        self.assertEqual((self.plugin / "skills/web-scraping-api/SKILL.md").read_text(), before)

    def test_unmapped_source_skills_are_not_copied(self):
        (self.skills / "skills/scrapfly-cli").mkdir()
        (self.skills / "skills/scrapfly-cli/SKILL.md").write_text("---\nname: scrapfly-cli\n---\n")

        self.assertEqual(sync_skills.sync(self.skills, self.plugin, False), 0)

        self.assertFalse((self.plugin / "skills/scrapfly-cli").exists())

    def test_claude_rules_are_appended_without_changing_the_source(self):
        self.assertEqual(sync_skills.sync(self.skills, self.plugin, False), 0)

        browser = (self.plugin / "skills/cloud-browser/SKILL.md").read_text()
        extraction = (self.plugin / "skills/extraction-api/SKILL.md").read_text()
        self.assertIn("## Claude Code rules", browser)
        self.assertIn("take_snapshot", browser)
        self.assertIn("extraction_model", extraction)
        self.assertNotIn("## Claude Code rules", (self.skills / "skills/scrapfly-browser/SKILL.md").read_text())

    def snapshot(self):
        return {str(path.relative_to(self.plugin)): path.read_bytes() for path in self.plugin.rglob("*") if path.is_file()}

    def test_a_source_symlink_is_refused_without_touching_the_plugin(self):
        before = self.snapshot()
        os.symlink(self.plugin / ".claude-plugin/plugin.json", self.skills / "skills/scrapfly-scraper/config-link")

        with self.assertRaises(sync_skills.SyncError):
            sync_skills.sync(self.skills, self.plugin, False)

        self.assertEqual(self.snapshot(), before)

    def test_a_publication_failure_restores_every_target(self):
        before = self.snapshot()
        original = sync_skills.shutil.copytree

        failed = False

        def fail_on_screenshot(source, target, *args, **kwargs):
            nonlocal failed
            if not failed and Path(target) == self.plugin / "skills" / "screenshot-api":
                failed = True
                raise OSError("injected publication failure")
            return original(source, target, *args, **kwargs)

        sync_skills.shutil.copytree = fail_on_screenshot
        try:
            with self.assertRaises(OSError):
                sync_skills.sync(self.skills, self.plugin, False)
        finally:
            sync_skills.shutil.copytree = original

        self.assertEqual(self.snapshot(), before)

    def test_a_new_target_is_removed_when_a_later_publication_fails(self):
        shutil = sync_skills.shutil
        shutil.rmtree(self.plugin / "skills/web-scraping-api")
        before = self.snapshot()
        original = shutil.copytree

        failed = False

        def fail_on_screenshot(source, target, *args, **kwargs):
            nonlocal failed
            if not failed and Path(target) == self.plugin / "skills" / "screenshot-api":
                failed = True
                raise OSError("injected publication failure")
            return original(source, target, *args, **kwargs)

        shutil.copytree = fail_on_screenshot
        try:
            with self.assertRaises(OSError):
                sync_skills.sync(self.skills, self.plugin, False)
        finally:
            shutil.copytree = original

        self.assertEqual(self.snapshot(), before)

    def test_a_backup_failure_keeps_the_original_target_intact(self):
        before = self.snapshot()
        original = sync_skills.shutil.copytree

        def fail_on_backup(source, target, *args, **kwargs):
            if "claude-plugin-backup-" in str(target) and Path(target).name == "web-scraping-api":
                raise OSError("injected backup failure")
            return original(source, target, *args, **kwargs)

        sync_skills.shutil.copytree = fail_on_backup
        try:
            with self.assertRaises(OSError):
                sync_skills.sync(self.skills, self.plugin, False)
        finally:
            sync_skills.shutil.copytree = original

        self.assertEqual(self.snapshot(), before)

    def test_front_matter_guards_leave_the_plugin_untouched(self):
        before = self.snapshot()
        cases = {
            "opening delimiter": "no front matter\n",
            "closing delimiter": "---\nname: scrapfly-scraper\n",
            "missing name": "---\ndescription: x\n---\n",
            "duplicate name": "---\nname: x\nname: y\n---\n",
            "missing description": "---\nname: x\n---\n",
        }
        for label, content in cases.items():
            with self.subTest(label=label):
                (self.skills / "skills/scrapfly-scraper/SKILL.md").write_text(content)
                with self.assertRaises(sync_skills.SyncError):
                    sync_skills.sync(self.skills, self.plugin, False)
                self.assertEqual(self.snapshot(), before)

    def test_an_existing_invocable_flag_is_always_false(self):
        (self.skills / "skills/scrapfly-scraper/SKILL.md").write_text("---\nname: scrapfly-scraper\ndescription: source\nuser-invocable: true\n---\n")

        self.assertEqual(sync_skills.sync(self.skills, self.plugin, False), 0)

        text = (self.plugin / "skills/web-scraping-api/SKILL.md").read_text()
        self.assertIn("user-invocable: false", text)
        self.assertNotIn("user-invocable: true", text)


if __name__ == "__main__":
    unittest.main()
