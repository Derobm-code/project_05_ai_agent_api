import unittest

from rag_tool import search_knowledge_base

class TestRAGRetrieval(unittest.TestCase):

    def test_automation_query_finds_automation_document(self):
        results = search_knowledge_base(
            "What tasks can Python automate, such as files and APIs?"
        )
        self.assertIn("Source: automation.txt", results)

    def test_database_query_fnds_databases_document(self):
        results = search_knowledge_base(
            "What is the difference between relational and NoSQL databases?"
        )
        self.assertIn("Source: databases.txt", results)

if __name__ == "__main__":
    unittest.main()