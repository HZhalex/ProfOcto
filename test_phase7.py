#!/usr/bin/env python3
"""
Phase 7 UX Features - Validation Test
Verify that all new modules load and work together.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import config

def test_module_imports():
    """Test that all Phase 7 modules can be imported."""
    print("Testing Phase 7 module imports...")
    
    modules_to_test = [
        ('output.phd_startup_cli', 'run_startup'),
        ('output.cost_estimator', 'estimate_cost_for_gaps'),
        ('output.gap_dashboard', 'show_gap_dashboard'),
        ('output.elevator_pitch', 'generate_elevator_pitch'),
        ('output.pdf_exporter', 'export_for_advisor'),
        ('output.batch_processor', 'BatchProcessor'),
        ('utils.bookmark_history', 'get_bookmark_manager'),
    ]
    
    for module_name, class_or_func in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_or_func])
            getattr(module, class_or_func)
            print(f"  ✓ {module_name}.{class_or_func}")
        except Exception as e:
            print(f"  ✗ {module_name}.{class_or_func}: {e}")
            return False
    
    return True


def test_config_flags():
    """Test that all Phase 7 config flags exist."""
    print("\nTesting Phase 7 config flags...")
    
    flags = [
        'QUICK_START_MODE',
        'INTERACTIVE_SETUP',
        'MINIMAL_OUTPUT',
        'DETAILED_OUTPUT',
        'FAST_MODE',
        'ESTIMATE_API_COST',
        'SHOW_TOP_GAP_DASHBOARD',
        'ENABLE_BOOKMARKING',
        'ENABLE_RUN_HISTORY',
        'ENABLE_PDF_EXPORT',
        'ENABLE_ELEVATOR_PITCH',
        'ENABLE_BATCH_MODE',
        'BOOKMARK_FILE',
        'HISTORY_FILE',
        'ADVISOR_EXPORT_DIR',
        'BATCH_FILE',
        'BATCH_RESULTS_DIR',
    ]
    
    missing = []
    for flag in flags:
        if not hasattr(config, flag):
            missing.append(flag)
            print(f"  ✗ Missing: {flag}")
        else:
            print(f"  ✓ {flag}")
    
    return len(missing) == 0


def test_cost_estimator():
    """Test cost estimator functionality."""
    print("\nTesting cost estimator...")
    
    try:
        from output.cost_estimator import CostEstimator
        
        estimator = CostEstimator()
        
        # Test for 5 gaps
        estimate = estimator.estimate_for_gaps(5)
        assert estimate['num_gaps'] == 5
        assert estimate['estimated_cost_usd'] > 0
        assert estimate['estimated_time_seconds'] > 0
        
        print(f"  ✓ Estimate for 5 gaps: ${estimate['estimated_cost_usd']}, {estimate['estimated_time_readable']}")
        
        # Test cost confirmation logic
        should_confirm = estimator.should_confirm_cost(estimate)
        print(f"  ✓ Should confirm cost: {should_confirm}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_bookmark_system():
    """Test bookmarking system."""
    print("\nTesting bookmark system...")
    
    try:
        from utils.bookmark_history import GapBookmarkManager, RunHistoryManager
        
        # Create test managers (temporary)
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            bookmark_file = f.name
        
        mgr = GapBookmarkManager(bookmark_file)
        
        # Test bookmark
        test_gap = {
            'gap_title': 'Test Gap',
            'iclr_readiness_score': 80,
            'recommendation': 'Highly recommended',
            'timeline_assessment': {'total_timeline_months': 6}
        }
        
        success = mgr.bookmark('Test Gap', test_gap, 'This is a test')
        assert success
        print(f"  ✓ Bookmarked test gap")
        
        # Test retrieval
        bookmarks = mgr.get_bookmarks()
        assert len(bookmarks) > 0
        print(f"  ✓ Retrieved {len(bookmarks)} bookmarks")
        
        # Cleanup
        os.unlink(bookmark_file)
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_elevator_pitch():
    """Test elevator pitch generation."""
    print("\nTesting elevator pitch generator...")
    
    try:
        from output.elevator_pitch import generate_elevator_pitch
        
        test_gap = {
            'gap_title': 'Novel approach to transformer efficiency',
            'problem_statement': 'Current transformers are computationally expensive',
            'novelty_score': 75,
            'feasibility_assessment': {'feasibility_score': 70},
            'timeline_assessment': {'total_timeline_months': 8},
            'key_innovations': ['Low-rank approximation', 'Dynamic compression'],
            'recommendation': 'Ready for PhD pursuit'
        }
        
        pitch = generate_elevator_pitch(test_gap, seconds=30)
        
        assert 'short' in pitch
        assert 'medium' in pitch
        assert 'detailed' in pitch
        assert 'bullet_points' in pitch
        
        print(f"  ✓ Generated pitch with {len(pitch['bullet_points'])} bullet points")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_dashboard():
    """Test gap dashboard."""
    print("\nTesting gap dashboard...")
    
    try:
        from output.gap_dashboard import show_gap_dashboard
        
        test_gaps = [
            {
                'gap_title': 'Gap 1',
                'iclr_readiness_score': 85,
                'novelty_score': 80,
                'feasibility_assessment': {'feasibility_score': 85},
                'timeline_assessment': {'total_timeline_months': 6},
                'recommendation': 'Excellent'
            },
            {
                'gap_title': 'Gap 2',
                'iclr_readiness_score': 65,
                'novelty_score': 60,
                'feasibility_assessment': {'feasibility_score': 70},
                'timeline_assessment': {'total_timeline_months': 10},
                'recommendation': 'Good'
            }
        ]
        
        dashboard = show_gap_dashboard(test_gaps, 'Test Topic')
        
        assert 'GAP ANALYSIS DASHBOARD' in dashboard
        assert 'Gap 1' in dashboard
        print(f"  ✓ Generated dashboard ({len(dashboard)} chars)")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_pdf_exporter():
    """Test PDF exporter."""
    print("\nTesting PDF exporter...")
    
    try:
        from output.pdf_exporter import AdvisorExporter
        import tempfile
        
        exporter = AdvisorExporter(os.path.join(tempfile.gettempdir(), 'test_export'))
        
        test_gap = {
            'gap_title': 'Test Export Gap',
            'problem_statement': 'This is a test gap',
            'iclr_readiness_score': 75,
            'novelty_score': 70,
            'feasibility_assessment': {'feasibility_score': 80},
            'timeline_assessment': {
                'literature_review_weeks': 4,
                'problem_formalization_weeks': 2,
                'solution_development_months': 4,
                'experimentation_months': 3,
                'paper_writing_weeks': 4,
                'total_timeline_months': 8
            },
            'key_innovations': ['Innovation 1', 'Innovation 2'],
            'key_risks': ['Risk 1', 'Risk 2'],
            'next_steps_for_researcher': ['Step 1', 'Step 2'],
            'required_resources': ['GPU', 'Data'],
            'recommendation': 'Recommended'
        }
        
        filepath = exporter.export_gap_analysis(test_gap, format='txt')
        assert os.path.exists(filepath)
        print(f"  ✓ Exported to {filepath}")
        
        # Cleanup
        os.unlink(filepath)
        os.rmdir(exporter.export_dir)
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("="*70)
    print("Phase 7 UX Features - Validation Test Suite")
    print("="*70)
    
    results = []
    
    # Run tests
    results.append(("Module Imports", test_module_imports()))
    results.append(("Config Flags", test_config_flags()))
    results.append(("Cost Estimator", test_cost_estimator()))
    results.append(("Bookmark System", test_bookmark_system()))
    results.append(("Elevator Pitch", test_elevator_pitch()))
    results.append(("Dashboard", test_dashboard()))
    results.append(("PDF Exporter", test_pdf_exporter()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
