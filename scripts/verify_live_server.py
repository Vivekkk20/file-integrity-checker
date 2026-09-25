"""
Verification script for the live File Integrity Checker Flask server.
"""

import urllib.request
import urllib.parse
import json

def run_checks():
    base_url = "http://127.0.0.1:5000"
    print(f"=== Verifying Live Web Server at {base_url} ===")

    # 1. Check Index HTML
    try:
        req = urllib.request.urlopen(f"{base_url}/")
        assert req.status == 200, f"Expected 200, got {req.status}"
        body = req.read().decode("utf-8")
        print("[PASS] GET / -> HTTP 200 OK")
        
        # Verify all 5 core screens are present in the HTML DOM
        screens = ["screenHome", "screenAnalyze", "screenResult", "screenHistory", "screenAbout"]
        for s in screens:
            assert f'id="{s}"' in body, f"Screen element id='{s}' missing from index.html"
            print(f"       + Screen section #{s} verified present in HTML")

    except Exception as e:
        print(f"[FAIL] GET / -> {e}")
        return False

    # 2. Check Static Assets
    for asset, mime_type in [("style.css", "text/css"), ("js/app.js", "javascript")]:
        try:
            req = urllib.request.urlopen(f"{base_url}/static/css/{asset}" if asset.endswith(".css") else f"{base_url}/static/{asset}")
            assert req.status == 200
            content = req.read()
            assert len(content) > 100
            print(f"[PASS] GET static asset {asset} -> HTTP 200 ({len(content)} bytes)")
        except Exception as e:
            print(f"[FAIL] GET static asset {asset} -> {e}")
            return False

    # 3. Check /api/stats
    try:
        req = urllib.request.urlopen(f"{base_url}/api/stats")
        assert req.status == 200
        stats_data = json.loads(req.read().decode("utf-8"))
        assert stats_data.get("success") is True
        print(f"[PASS] GET /api/stats -> HTTP 200 (Active Baselines: {stats_data['stats']['total_baselines']}, Verifications: {stats_data['stats']['total_verifications']})")
    except Exception as e:
        print(f"[FAIL] GET /api/stats -> {e}")
        return False

    # 4. Check /api/analyze with live file
    try:
        payload = json.dumps({"file_path": "AGENTS.md"}).encode("utf-8")
        post_req = urllib.request.Request(
            f"{base_url}/api/analyze",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(post_req)
        assert res.status == 200
        data = json.loads(res.read().decode("utf-8"))
        assert data.get("success") is True
        assert len(data.get("sha256", "")) == 64
        print(f"[PASS] POST /api/analyze (AGENTS.md) -> HTTP 200 (SHA-256: {data['sha256'][:16]}...)")
    except Exception as e:
        print(f"[FAIL] POST /api/analyze -> {e}")
        return False

    # 5. Check /api/verify with live file
    try:
        payload = json.dumps({"file_path": "AGENTS.md"}).encode("utf-8")
        post_req = urllib.request.Request(
            f"{base_url}/api/verify",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(post_req)
        assert res.status == 200
        data = json.loads(res.read().decode("utf-8"))
        assert data.get("success") is True
        result = data.get("result", {})
        assert result.get("status") in ["MATCHED", "MODIFIED"]
        print(f"[PASS] POST /api/verify (AGENTS.md) -> HTTP 200 (Verdict: {result['status']})")
    except Exception as e:
        print(f"[FAIL] POST /api/verify -> {e}")
        return False

    # 6. Check /api/history
    try:
        req = urllib.request.urlopen(f"{base_url}/api/history")
        assert req.status == 200
        history_data = json.loads(req.read().decode("utf-8"))
        assert history_data.get("success") is True
        assert len(history_data.get("history", [])) > 0
        latest = history_data["history"][0]
        print(f"[PASS] GET /api/history -> HTTP 200 ({len(history_data['history'])} log entries found, latest #{latest['id']} status: {latest['status']})")
    except Exception as e:
        print(f"[FAIL] GET /api/history -> {e}")
        return False

    print("\n=== ALL LIVE SERVER ENDPOINTS VERIFIED SUCCESSFULLY ===")
    return True

if __name__ == "__main__":
    run_checks()
