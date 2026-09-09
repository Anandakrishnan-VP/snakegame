"""
Comprehensive Unit Test Suite for Certification Journey & PDF Generator.
Tests data model, deduplication, step toggling, exact readiness score calculations line-by-line,
and PDF generation.
"""

import os
import sys
sys.path.insert(0, os.path.abspath("."))
import unittest
from backend.services.journey_service import start_journey, update_step_status, get_journey
from backend.services.journey_pdf import generate_roadmap_pdf

class TestJourneyService(unittest.TestCase):

    def test_01_start_journey_scheme1(self):
        """Tests starting a journey for IS 17803:2022 (Scheme-I, 6 steps)."""
        import uuid
        session_id = f"test-sess-fresh-{uuid.uuid4().hex[:8]}"
        res = start_journey(session_id, journey_type="get_certified", standard_id="IS 17803:2022")
        
        self.assertIsNotNone(res.get("journey_id"))
        self.assertEqual(res["journey_type"], "get_certified")
        self.assertEqual(res["scheme"], "Scheme-I")
        self.assertEqual(len(res["steps"]), 6)
        self.assertEqual(res["readiness_score"], 0)
        self.assertFalse(res.get("resumed", False))
        print("[PASS] Test 1: Journey initialization for Scheme-I (6 steps, 0% score)")

    def test_02_deduplication(self):
        """Tests that starting the same journey in the same session resumes instead of creating duplicate."""
        session_id = "test-sess-dedup"
        res1 = start_journey(session_id, journey_type="get_certified", standard_id="IS 17803:2022")
        res2 = start_journey(session_id, journey_type="get_certified", standard_id="IS 17803:2022")

        self.assertEqual(res1["journey_id"], res2["journey_id"])
        self.assertTrue(res2.get("resumed", True))
        print("[PASS] Test 2: Deduplication correctly resumes existing journey")

    def test_03_readiness_score_line_by_line(self):
        """
        Tests line-by-line step toggles and exact readiness score calculations:
        0% -> 17% -> 33% -> 50% -> 67% -> 83% -> 100% -> 83%
        """
        session_id = "test-sess-steps"
        journey = start_journey(session_id, journey_type="get_certified", standard_id="IS 17803:2022", force_new=True)
        journey_id = journey["journey_id"]
        self.assertEqual(journey["readiness_score"], 0)

        # Step 1: 1/6 = 16.666% -> 17%
        u1 = update_step_status(journey_id, "step-1", "done")
        self.assertIsNotNone(u1)
        self.assertEqual(u1["readiness_score"], 17, f"Expected 17%, got {u1['readiness_score']}%")

        # Step 2: 2/6 = 33.333% -> 33%
        u2 = update_step_status(journey_id, "step-2", "done")
        self.assertEqual(u2["readiness_score"], 33, f"Expected 33%, got {u2['readiness_score']}%")

        # Step 3: 3/6 = 50.000% -> 50%
        u3 = update_step_status(journey_id, "step-3", "done")
        self.assertEqual(u3["readiness_score"], 50, f"Expected 50%, got {u3['readiness_score']}%")

        # Step 4: 4/6 = 66.666% -> 67%
        u4 = update_step_status(journey_id, "step-4", "done")
        self.assertEqual(u4["readiness_score"], 67, f"Expected 67%, got {u4['readiness_score']}%")

        # Step 5: 5/6 = 83.333% -> 83%
        u5 = update_step_status(journey_id, "step-5", "done")
        self.assertEqual(u5["readiness_score"], 83, f"Expected 83%, got {u5['readiness_score']}%")

        # Step 6: 6/6 = 100.000% -> 100%
        u6 = update_step_status(journey_id, "step-6", "done")
        self.assertEqual(u6["readiness_score"], 100, f"Expected 100%, got {u6['readiness_score']}%")

        # Toggle back to pending (Step 6): 5/6 -> 83%
        u7 = update_step_status(journey_id, "step-6", "pending")
        self.assertEqual(u7["readiness_score"], 83, f"Expected 83%, got {u7['readiness_score']}%")

        print("[PASS] Test 3: Line-by-line readiness score calculations (0% -> 17% -> 33% -> 50% -> 67% -> 83% -> 100% -> 83%)")

    def test_04_voluntary_standard(self):
        """Tests that a voluntary standard produces a graceful single-step assessment."""
        session_id = "test-sess-vol"
        # IS 10500 or voluntary standard
        res = start_journey(session_id, journey_type="get_certified", standard_id="IS 10500:2012", force_new=True)
        self.assertEqual(len(res["steps"]), 1)
        self.assertEqual(res["steps"][0]["title"], "Voluntary Compliance Assessment")
        self.assertEqual(res["readiness_score"], 100)
        print("[PASS] Test 4: Voluntary standard handled gracefully as 1-step assessment")

    def test_05_consumer_verify_protect_journey(self):
        """Tests consumer Verify & Protect journey with grievance redressal."""
        session_id = "test-sess-cons"
        res = start_journey(session_id, journey_type="verify_protect", standard_id="CML1234567", force_new=True)
        self.assertEqual(res["journey_type"], "verify_protect")
        self.assertEqual(len(res["steps"]), 4)
        self.assertIn("Grievance", res["steps"][3]["title"])
        print("[PASS] Test 5: Consumer Verify & Protect journey initialized with 4 steps")

    def test_06_pdf_generation_0_and_100_percent(self):
        """Tests that ReportLab generates valid single-page PDF byte streams at both 0% and 100% scores."""
        session_id = "test-sess-pdf"
        journey = start_journey(session_id, journey_type="get_certified", standard_id="IS 17803:2022", force_new=True)
        
        # Test PDF at 0%
        pdf_bytes_0 = generate_roadmap_pdf(journey)
        self.assertTrue(len(pdf_bytes_0) > 1000)
        self.assertTrue(pdf_bytes_0.startswith(b"%PDF-"))

        # Mark all steps done and test PDF at 100%
        for i in range(1, 7):
            update_step_status(journey["journey_id"], f"step-{i}", "done")

        updated_journey = get_journey(journey["journey_id"])
        self.assertEqual(updated_journey["readiness_score"], 100)
        
        pdf_bytes_100 = generate_roadmap_pdf(updated_journey)
        self.assertTrue(len(pdf_bytes_100) > 1000)
        self.assertTrue(pdf_bytes_100.startswith(b"%PDF-"))
        print(f"[PASS] Test 6: ReportLab PDF generated cleanly at 0% ({len(pdf_bytes_0)} bytes) and 100% ({len(pdf_bytes_100)} bytes)")

    def test_07_standard_not_found_returns_clear_message_no_default_fallback(self):
        """Tests that a non-existent standard returns not_found instead of silently defaulting to Steel Flasks."""
        session_id = "test-sess-notfound"
        res = start_journey(session_id, journey_type="get_certified", standard_id="IS 99999", force_new=True)

        self.assertTrue(res.get("not_found"))
        self.assertEqual(res.get("requested_standard"), "IS 99999")
        self.assertIn("No data found", res.get("message", ""))
        self.assertIsNone(res.get("journey_id"))
        self.assertNotEqual(res.get("standard_id"), "IS 17803:2022")
        print("[PASS] Test 7: Non-existent standard explicitly returns not_found and refuses default fallback")

    def test_08_default_template_when_no_standard_selected(self):
        """Tests that a new user without a selected standard receives the generic Scheme-I template (not steel flasks)."""
        session_id = "test-sess-default-user"
        res = start_journey(session_id, journey_type="get_certified", standard_id=None, force_new=True)

        self.assertFalse(res.get("not_found", False))
        self.assertEqual(res.get("standard_id"), "Scheme-I Template")
        self.assertTrue(res.get("metadata", {}).get("is_default_template"))
        self.assertIn("General Product Certification Roadmap", res.get("metadata", {}).get("title", ""))
        self.assertNotEqual(res.get("metadata", {}).get("title"), "Stainless Steel Vacuum Flasks and Insulated Flask Containers - Specification")
        self.assertEqual(len(res.get("steps", [])), 6)
        print("[PASS] Test 8: Default roadmap provides generic Scheme-I template with 6 milestones")

if __name__ == "__main__":
    unittest.main()
