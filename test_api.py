import urllib.request
import json

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("Testing NexusAI API endpoints...")

    # 1. Test Homepage
    req = urllib.request.urlopen(f"{BASE_URL}/")
    assert req.status == 200, f"Expected 200 from /, got {req.status}"
    print("[PASS] Homepage (/) returned 200 OK")

    # 2. Test /api/categories
    req = urllib.request.urlopen(f"{BASE_URL}/api/categories")
    assert req.status == 200
    data = json.loads(req.read().decode('utf-8'))
    assert data['status'] == 'success'
    assert len(data['categories']) == 7
    print(f"[PASS] /api/categories returned {len(data['categories'])} categories")

    # 3. Test /api/tools
    req = urllib.request.urlopen(f"{BASE_URL}/api/tools")
    assert req.status == 200
    data = json.loads(req.read().decode('utf-8'))
    assert data['status'] == 'success'
    initial_count = data['count']
    assert initial_count >= 20, f"Expected >= 20 tools, got {initial_count}"
    print(f"[PASS] /api/tools returned {initial_count} tools")

    # 4. Test Category Filter
    req = urllib.request.urlopen(f"{BASE_URL}/api/tools?category=coding-dev")
    data = json.loads(req.read().decode('utf-8'))
    assert data['status'] == 'success'
    assert data['count'] > 0
    for t in data['tools']:
        assert t['category_slug'] == 'coding-dev'
    print(f"[PASS] Category filter (coding-dev) returned {data['count']} coding tools")

    # 5. Test Search Filter
    req = urllib.request.urlopen(f"{BASE_URL}/api/tools?q=cursor")
    data = json.loads(req.read().decode('utf-8'))
    assert data['status'] == 'success'
    assert any(t['name'] == 'Cursor' for t in data['tools'])
    print(f"[PASS] Search query 'cursor' successfully matched Cursor tool")

    # 6. Test Pricing Filter
    req = urllib.request.urlopen(f"{BASE_URL}/api/tools?pricing=Free")
    data = json.loads(req.read().decode('utf-8'))
    assert data['status'] == 'success'
    for t in data['tools']:
        assert t['pricing_type'].lower() == 'free'
    print(f"[PASS] Pricing filter (Free) returned {data['count']} free tools")

    # 7. Test Single Tool Details
    req = urllib.request.urlopen(f"{BASE_URL}/api/tools/1")
    data = json.loads(req.read().decode('utf-8'))
    assert data['status'] == 'success'
    assert data['tool']['id'] == 1
    print(f"[PASS] /api/tools/1 returned details for: {data['tool']['name']}")

    # 8. Test Upvote API
    tool_1_votes_before = data['tool']['upvotes']
    post_req = urllib.request.Request(f"{BASE_URL}/api/tools/1/upvote", data=b'', method='POST')
    res = urllib.request.urlopen(post_req)
    upvote_data = json.loads(res.read().decode('utf-8'))
    assert upvote_data['status'] == 'success'
    assert upvote_data['upvotes'] == tool_1_votes_before + 1
    print(f"[PASS] Upvote incremented votes from {tool_1_votes_before} to {upvote_data['upvotes']}")

    # 9. Test Tool Submission API
    new_tool_payload = json.dumps({
        "name": "Devin AI",
        "tagline": "The world's first autonomous AI software engineer",
        "description": "Devin is an autonomous agent that can solve engineering problems end-to-end.",
        "category_id": 1,
        "website_url": "https://cognition.ai",
        "pricing_type": "Paid",
        "pricing_details": "Enterprise subscription",
        "tags": ["Autonomous", "Agent", "Software Engineer"],
        "features": ["End-to-end coding", "Terminal control", "Self-learning"]
    }).encode('utf-8')

    submit_req = urllib.request.Request(
        f"{BASE_URL}/api/tools/submit",
        data=new_tool_payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    submit_res = urllib.request.urlopen(submit_req)
    submit_data = json.loads(submit_res.read().decode('utf-8'))
    assert submit_data['status'] == 'success'
    assert submit_data['tool']['name'] == 'Devin AI'
    print(f"[PASS] Tool Submission succeeded: created tool with ID {submit_data['tool']['id']}")

    # 10. Test Stats API
    stats_req = urllib.request.urlopen(f"{BASE_URL}/api/stats")
    stats_data = json.loads(stats_req.read().decode('utf-8'))
    assert stats_data['status'] == 'success'
    assert stats_data['stats']['total_tools'] == initial_count + 1
    print(f"[PASS] Stats API verified: total tools now {stats_data['stats']['total_tools']}")

    print("\nSUCCESS: ALL 10 REST API AND DATABASE TESTS PASSED!")

if __name__ == '__main__':
    test_api()
