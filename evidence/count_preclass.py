"""Đếm tái lập hành vi học viên từ bộ `data/preclass/` của BTC (dữ liệu thô đặt ở `data-btc/preclass/`, git-ignored).

Chạy: python evidence/count_preclass.py
"""
from __future__ import annotations

import csv
import json
import os
import subprocess
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRECLASS_DIR = os.path.join(ROOT, "data-btc", "preclass")
SOURCE_COMMIT = "6225f90"


def ensure_local_preclass_files() -> bool:
    """Nếu chưa có file trong data-btc/preclass/, trích cục bộ từ commit 6225f90 vào thư mục gitignored."""
    needed = ["events.csv", "learners.csv", "column_dictionary.csv"]
    if all(os.path.exists(os.path.join(PRECLASS_DIR, fn)) for fn in needed):
        return True
    try:
        subprocess.run(
            ["git", "-C", ROOT, "cat-file", "-e", f"{SOURCE_COMMIT}^{{commit}}"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return False

    os.makedirs(PRECLASS_DIR, exist_ok=True)
    for fn in needed:
        res = subprocess.run(
            ["git", "-C", ROOT, "show", f"{SOURCE_COMMIT}:data/preclass/{fn}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if res.returncode == 0 and res.stdout:
            with open(os.path.join(PRECLASS_DIR, fn), "w", encoding="utf-8", newline="\n") as f:
                f.write(res.stdout)
    return all(os.path.exists(os.path.join(PRECLASS_DIR, fn)) for fn in needed)


def mask_id(raw_id: str) -> str:
    s = (raw_id or "").strip()
    return f"{s[:6]}..." if len(s) > 6 else (s or "N/A")


def main() -> int:
    if not ensure_local_preclass_files():
        print("Chưa tìm thấy data-btc/preclass/events.csv. Hãy đặt bộ data/preclass của BTC vào data-btc/preclass/.")
        return 1

    events_path = os.path.join(PRECLASS_DIR, "events.csv")
    learners_path = os.path.join(PRECLASS_DIR, "learners.csv")

    with open(learners_path, encoding="utf-8-sig", newline="") as f:
        total_learners_table = sum(1 for _ in csv.DictReader(f))

    event_counts: Counter[str] = Counter()
    learners_all_events: set[str] = set()
    learners_lab_opened: set[str] = set()
    learners_lab_completed: set[str] = set()
    learners_lab_skipped: set[str] = set()

    lab_completed_total = 0
    lab_completed_skipped = 0
    chat_sent_total = 0
    chat_sent_with_lab_key = 0
    learners_chat_sent: set[str] = set()
    learners_chat_with_lab: set[str] = set()

    min_ts, max_ts = None, None
    ex_skipped: list[str] = []
    ex_chat_lab: list[str] = []
    ex_chat_nolab: list[str] = []

    with open(events_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        for idx, row in enumerate(reader, start=2):
            etype = (row.get("type") or row.get("event_type") or "").strip()
            lid = (row.get("hv") or row.get("learner_id") or "").strip()
            ts = (row.get("occurred_at") or row.get("received_at") or "").strip()
            lesson_id = (row.get("lesson_id") or "").strip()
            data_raw = (row.get("data") or "").strip()

            lab_key = ""
            skipped_val = ""
            if data_raw.startswith("{"):
                try:
                    payload = json.loads(data_raw)
                    if isinstance(payload, dict):
                        if "skipped" in payload:
                            skipped_val = str(payload.get("skipped")).strip().lower()
                        if payload.get("lab_key"):
                            lab_key = str(payload.get("lab_key")).strip()
                except Exception:
                    pass

            is_skipped = skipped_val in ("true", "1", "yes")

            event_counts[etype] += 1
            if lid:
                learners_all_events.add(lid)
            if ts:
                if min_ts is None or ts < min_ts:
                    min_ts = ts
                if max_ts is None or ts > max_ts:
                    max_ts = ts

            if etype == "lab_opened":
                if lid:
                    learners_lab_opened.add(lid)
            elif etype == "lab_completed":
                lab_completed_total += 1
                if lid:
                    learners_lab_completed.add(lid)
                if is_skipped:
                    lab_completed_skipped += 1
                    if lid:
                        learners_lab_skipped.add(lid)
                    if len(ex_skipped) < 3:
                        ex_skipped.append(
                            f"events.csv dòng {idx}: type=lab_completed, lesson_id={lesson_id or '-'}, "
                            f"lab_key={lab_key or '-'}, skipped=true, hv={mask_id(lid)}, occurred_at={ts[:19]}"
                        )
            elif etype == "chat_sent":
                chat_sent_total += 1
                if lid:
                    learners_chat_sent.add(lid)
                if lab_key:
                    chat_sent_with_lab_key += 1
                    if lid:
                        learners_chat_with_lab.add(lid)
                    if len(ex_chat_lab) < 1:
                        ex_chat_lab.append(
                            f"events.csv dòng {idx}: type=chat_sent (CÓ gắn lab_key={lab_key}), "
                            f"lesson_id={lesson_id or '-'}, hv={mask_id(lid)}, occurred_at={ts[:19]}"
                        )
                elif len(ex_chat_nolab) < 1:
                    ex_chat_nolab.append(
                        f"events.csv dòng {idx}: type=chat_sent (lab_key trống — chat ngoài ngữ cảnh lab), "
                        f"lesson_id={lesson_id or '-'}, hv={mask_id(lid)}, occurred_at={ts[:19]}"
                    )

    total_events = sum(event_counts.values())
    lab_opened_total = event_counts["lab_opened"]
    chat_without_lab = chat_sent_total - chat_sent_with_lab_key
    examples = ex_skipped + ex_chat_lab + ex_chat_nolab

    print("=== KẾT QUẢ ĐÀO DATA PRECLASS (TÁI LẬP TỰ ĐỘNG) ===")
    print(f"Các cột trong events.csv: {', '.join(columns)}")
    print(f"Khoảng thời gian sự kiện: {min_ts} -> {max_ts}")
    print(f"Tổng số dòng learners.csv: {total_learners_table} | Số học viên có sự kiện trong events.csv: {len(learners_all_events)}")
    print(f"Tổng số sự kiện (events.csv): {total_events}")
    print(f"- lab_opened: {lab_opened_total} sự kiện (trên {len(learners_lab_opened)}/{len(learners_all_events)} học viên có log = {len(learners_lab_opened)/max(len(learners_all_events),1)*100:.1f}%)")
    print(f"- lab_completed: {lab_completed_total} sự kiện (trên {len(learners_lab_completed)}/{len(learners_lab_opened)} học viên đã mở lab = {len(learners_lab_completed)/max(len(learners_lab_opened),1)*100:.1f}%)")
    print(f"- lab_completed với skipped=true: {lab_completed_skipped}/{lab_completed_total} ({lab_completed_skipped/max(lab_completed_total,1)*100:.1f}%) — liên quan tới {len(learners_lab_skipped)}/{len(learners_lab_completed)} học viên hoàn thành lab ({len(learners_lab_skipped)/max(len(learners_lab_completed),1)*100:.1f}%)")
    print(f"- chat_sent có gắn lab_key: {chat_sent_with_lab_key}/{chat_sent_total} ({chat_sent_with_lab_key/max(chat_sent_total,1)*100:.2f}%) trên {len(learners_chat_with_lab)}/{len(learners_chat_sent)} học viên dùng chat | không gắn lab_key: {chat_without_lab}/{chat_sent_total} ({chat_without_lab/max(chat_sent_total,1)*100:.2f}%)")
    print("\n5 dòng ví dụ đối chiếu (đã che mã ẩn danh):")
    for i, ex in enumerate(examples, start=1):
        print(f"  {i}. {ex}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
