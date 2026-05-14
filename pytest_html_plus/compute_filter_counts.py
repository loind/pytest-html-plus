from collections import Counter, defaultdict


def compute_filter_count(results):
    filters = Counter()
    marker_counts = defaultdict(int)

    for test in results:
        status = test.get("status")
        flaky = test.get("flaky", False)
        links = test.get("links", [])
        markers = test.get("markers", [])

        # xfailed render như failed về UI: gộp vào "failed" để filter chip
        # 'Show only failed tests' khớp banner 'Failures: N'.
        if status in ("failed", "xfailed") and not flaky:
            filters["failed"] += 1
        if status == "error":
            filters["error"] += 1
        if flaky:
            filters["flaky"] += 1
        if status == "skipped":
            filters["skipped"] += 1
        if not links:
            filters["untracked"] += 1

        for marker in markers:
            marker_counts[marker] += 1

    total = len(results)
    filters["total"] = total
    filters["passed"] = (
        total - filters["failed"] - filters["skipped"] - filters["error"]
    )

    filters["marker_counts"] = dict(marker_counts)
    return dict(filters)
