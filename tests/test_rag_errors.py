from pathlib import Path
import tempfile
import unittest

from rag_tool import load_documents, search_knowledge_base

class TestRAGErrors(unittest.TestCase):
    def test_missing_documents_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            missing_directory = Path(temp) / "missing"

            with self.assertRaisesRegex(
                FileNotFoundError, "Knowledge-base directory not found."
            ):
                load_documents(missing_directory)

    def test_empty_documents_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(
                ValueError, "No non-empty .txt documents found",
            ):
                load_documents(temp)

    def test_empty_search_query(self):
        with self.assertRaisesRegex(
            ValueError, "Search query cannot be empty",
        ):
            search_knowledge_base("   ")

if __name__ =="__main__":
    unittest.main()