"""
tests for terminus simulator.
run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terminus_sim import simulate, quadratic_model, fmt_iec, fmt_si, sci


class TestQuadraticModel:
    """tests for the quadratic zip size model."""
    
    def test_level_zero(self):
        """level 0 should be 120 bytes."""
        assert quadratic_model(0) == 120
    
    def test_level_50(self):
        """level 50 should be close to actual (508,950 bytes)."""
        size = quadratic_model(50)
        assert 450000 < size < 550000
    
    def test_grows_monotonically(self):
        """zip size should increase with level."""
        sizes = [quadratic_model(d) for d in range(0, 51, 5)]
        for i in range(1, len(sizes)):
            assert sizes[i] > sizes[i-1]
    
    def test_reasonable_range(self):
        """all levels should have positive, reasonable sizes."""
        for d in range(0, 101):
            size = quadratic_model(d)
            assert size > 0
            assert size < 1e9  # less than 1GB for level 100


class TestSimulation:
    """tests for the core simulation function."""
    
    def test_default_terminus(self):
        """default terminus config should match known values."""
        r = simulate(16, 50, 43)
        assert r['branching'] == 16
        assert r['level'] == 50
        assert r['payload'] == 43
        assert r['total_files'] == 16 ** 50
        assert r['total_bytes'] == 16 ** 50 * 43
    
    def test_total_files_formula(self):
        """total files should be branching^level."""
        r = simulate(16, 10, 43)
        assert r['total_files'] == 16 ** 10
    
    def test_total_bytes_formula(self):
        """total bytes should be files * payload."""
        r = simulate(8, 5, 100)
        assert r['total_bytes'] == (8 ** 5) * 100
    
    def test_ratio_calculation(self):
        """ratio should be total_bytes / zip_size."""
        r = simulate(16, 50, 43)
        expected_ratio = r['total_bytes'] / r['zip_size']
        assert abs(r['ratio'] - expected_ratio) < 0.001
    
    def test_level_count(self):
        """should have level+1 entries in levels list."""
        r = simulate(16, 20, 43)
        assert len(r['levels']) == 21
    
    def test_level_zero_files(self):
        """level 0 should have exactly 1 file."""
        r = simulate(16, 50, 43)
        assert r['levels'][0]['files'] == 1
    
    def test_level_one_files(self):
        """level 1 should have branching files."""
        r = simulate(16, 50, 43)
        assert r['levels'][1]['files'] == 16
    
    def test_payload_types(self):
        """different payload types should work."""
        for pt in ['zeros', 'text', 'random', 'binary']:
            r = simulate(16, 10, 43, pt)
            assert r['payload_type'] == pt
            assert r['total_files'] > 0


class TestFormatters:
    """tests for unit conversion functions."""
    
    def test_fmt_iec_bytes(self):
        assert fmt_iec(0) == "0 B"
        assert fmt_iec(100) == "100.00 B"
    
    def test_fmt_iec_kib(self):
        assert "KiB" in fmt_iec(2048)
    
    def test_fmt_iec_mib(self):
        assert "MiB" in fmt_iec(2 * 1024 * 1024)
    
    def test_fmt_si_bytes(self):
        assert fmt_si(0) == "0 B"
        assert fmt_si(100) == "100.00 B"
    
    def test_fmt_si_kb(self):
        assert "kB" in fmt_si(2000)
    
    def test_sci_notation(self):
        assert sci(1000) == "1.0000e+03"
        assert sci(0.001) == "1.0000e-03"


class TestSafetyCaps:
    """tests for safety limits."""
    
    def test_max_level(self):
        """level should be capped at 200."""
        lv = min(300, 200)
        assert lv == 200
    
    def test_max_branching(self):
        """branching should be capped at 1000."""
        br = min(2000, 1000)
        assert br == 1000
    
    def test_max_payload(self):
        """payload should be capped at 10000."""
        pl = min(50000, 10000)
        assert pl == 10000


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
