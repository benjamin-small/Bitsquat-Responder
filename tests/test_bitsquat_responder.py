import unittest

from dnslib import DNSRecord

from bitsquat_responder import build_responses, rewrite_name


class RewriteNameTests(unittest.TestCase):
    def test_rewrites_each_configured_bitsquat(self):
        self.assertEqual(rewrite_name("squapme.com."), "squatme.com.")
        self.assertEqual(rewrite_name("www.squatmu.com."), "www.squatme.com.")

    def test_leaves_unrelated_lowercase_name_unchanged(self):
        self.assertEqual(rewrite_name("example.com."), "example.com.")


class BuildResponsesTests(unittest.TestCase):
    def test_regular_query_gets_one_configured_address_response(self):
        query = DNSRecord.question("example.com").pack()

        original, corrected, qname = build_responses(query)

        self.assertEqual(qname, "example.com.")
        self.assertIsNone(corrected)
        self.assertEqual(str(original.rr[0].rname), "example.com.")
        self.assertEqual(str(original.rr[0].rdata), "0.0.0.0")
        self.assertEqual(original.rr[0].ttl, 60)

    def test_bitsquatted_query_also_gets_corrected_response(self):
        query = DNSRecord.question("squapme.com").pack()

        original, corrected, _ = build_responses(query)

        self.assertEqual(str(original.rr[0].rname), "squapme.com.")
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected.questions, [])
        self.assertEqual(str(corrected.rr[0].rname), "squatme.com.")
        self.assertEqual(str(corrected.rr[0].rdata), "0.0.0.0")


if __name__ == "__main__":
    unittest.main()
