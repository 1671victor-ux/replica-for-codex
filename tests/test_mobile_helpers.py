import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


doctor = load("mobile_doctor", ROOT / "skills/replica-test/mobile_doctor.py")
capture = load("mobile_capture", ROOT / "skills/replica-diff/mobile_capture.py")


class MobileDoctorTests(unittest.TestCase):
    def test_detects_expo_project_without_running_npx(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                json.dumps(
                    {
                        "dependencies": {
                            "expo": "latest",
                            "react-native": "latest",
                            "expo-dev-client": "latest",
                        }
                    }
                ),
                encoding="utf-8",
            )
            info = doctor.package_info(root)
        self.assertTrue(info["expo"])
        self.assertTrue(info["react_native"])
        self.assertTrue(info["expo_dev_client"])

    def test_missing_package_is_reported_without_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            info = doctor.package_info(Path(directory))
        self.assertFalse(info["present"])
        self.assertFalse(info["expo"])


class MobileCaptureTests(unittest.TestCase):
    @mock.patch.object(capture, "booted_ios_devices", return_value=["one", "two"])
    def test_requires_explicit_device_when_multiple_are_running(self, _devices):
        with self.assertRaisesRegex(RuntimeError, "pass --device"):
            capture.select_device("ios", None)

    def test_explicit_device_wins(self):
        self.assertEqual(capture.select_device("android", "serial-1"), "serial-1")


if __name__ == "__main__":
    unittest.main()
