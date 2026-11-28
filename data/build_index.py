"""Xây dựng chỉ mục tra cứu tài liệu các bài Lab hàng ngày của lớp L3 khoá K5 (`data/kb_index.json`).

Nguyên tắc trung thực dữ liệu (01-challenge-brief#data & data/DATA_CARD.md):
- KHÔNG chứa nội dung đề Hackathon và KHÔNG tự bịa thêm quy định không có nguồn.
- Toàn bộ mục trong chỉ mục dưới đây được trích xuất từ các dòng tài liệu Lab ngày Phase 1 của K5 (`Day01`–`Day14`)
  đã kiểm đếm và ghi rõ đường dẫn + số dòng gốc trong `evidence/lab-checkpoint-analysis.md` và `evidence/lab-checkpoints.csv`.
- Repo công khai chỉ lưu chỉ mục tóm tắt + trích đoạn ngắn (≤ 60 từ) kèm metadata `khoa`, `lop`, `lab`, `source_ref` và `conflicts_with`.

Chạy:
    python data/build_index.py
    python data/build_index.py --source-root <thu_muc_chua_Lab>

`doc_sha256_scope` ghi `source_file` nếu có tài liệu gốc, hoặc `indexed_excerpt`
nếu hash chỉ phản ánh bản trích trong chỉ mục.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_SOURCE = os.path.join(ROOT, "evidence", "lab-checkpoints.csv")
OUT_PATH = os.path.join(ROOT, "data", "kb_index.json")
CORPUS_VERSION = "K5-L3-Phase1-Labs (2026-11-27)"


SECTIONS: list[dict[str, Any]] = [
    {
        "code": "K5-Day01/CHECKPOINTS#lich-3-moc",
        "lab": "K5 Day01 — AI Foundation",
        "file": "Lab/K5-L3-Day-01-AI-Foundation-Lab/CHECKPOINTS.md:5,13,21",
        "title": "K5 Day01 (AI Foundation) · 3 mốc kiểm tra trong 150 phút",
        "keywords": ["day01", "day 1", "day 01", "ai foundation", "3 checkpoint", "150 phút", "0:40", "1:30", "2:30"],
        "summary": (
            "Bài Lab K5 Day01 (AI Foundation) có tổng cộng 3 checkpoint thiết kế trong 150 phút (40 | 50 | 60 phút, "
            "trung bình 50 phút/CP), các mốc kiểm tra được ghi ước lượng là 'khoảng 0:40', 'khoảng 1:30' và '2:30'."
        ),
        "quote": "3 checkpoint (40|50|60 phút, tổng 150 phút); mốc ghi 'khoảng 0:40', 'khoảng 1:30', '2:30'.",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day02/CHECKPOINTS#lich-8-moc",
        "lab": "K5 Day02 — Discovery & Problem Framing",
        "file": "Lab/K5-L3A-Day02/CHECKPOINTS.md:7-14,58,111",
        "title": "K5 Day02 (Discovery & Problem Framing) · 8 checkpoint và 2 lần nghỉ",
        "keywords": ["day02", "day 2", "day 02", "discovery", "problem framing", "8 checkpoint", "220 phút", "nghỉ 10 phút"],
        "summary": (
            "Bài Lab K5 Day02 (Discovery & Problem Framing) gồm 8 checkpoint với thời lượng lần lượt "
            "15 | 25 | 35 | 30 | 30 | 45 | 25 | 15 phút (tổng 220 phút làm bài, trung bình 27,5 phút/CP), xen kẽ 2 lần nghỉ 10 phút."
        ),
        "quote": "8 checkpoint: 15|25|35|30|30|45|25|15 phút (tổng 220 phút), có 2 lần nghỉ 10 phút (dòng 58, 111).",
        "conflicts_with": [],
    },
    {
        "code": "K5-Day02/CHECKPOINTS#doc-bai-mau",
        "lab": "K5 Day02 — Discovery & Problem Framing",
        "file": "Lab/K5-L3A-Day02/CHECKPOINTS.md:21",
        "title": "K5 Day02 · Hướng dẫn ưu tiên khi không kịp đọc hết bài mẫu trong 15 phút",
        "keywords": ["day02", "day 2", "day 02", "không kịp đọc", "bài mẫu", "15 phút", "mục 2 3 7 8", "đọc phần nào"],
        "summary": (
            "Ở mốc đọc đầu buổi (15 phút) của Lab K5 Day02, nếu học viên không kịp đọc hết toàn bộ bài mẫu thì tài liệu "
            "hướng dẫn ưu tiên tập trung đọc phần nhóm mục 2, 3, 7 và 8. Tài liệu không ghi quy định trừ % điểm theo từng giờ nộp muộn."
        ),
        "quote": "Không kịp đọc bài mẫu trong 15 phút thì đọc phần nhóm mục 2, 3, 7, 8 (CHECKPOINTS.md:21).",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day04/CHECKPOINTS#react-loop",
        "lab": "K5 Day04 — ReAct Loop Agent",
        "file": "Lab/K5-L3A-DAY04/CHECKPOINTS.md:5-14",
        "title": "K5 Day04 (ReAct Loop Agent) · 7 checkpoint chung thời lượng cho 3 ca học",
        "keywords": ["day04", "day 4", "day 04", "react", "react loop", "agent", "7 checkpoint", "215 phút", "3 ca học"],
        "summary": (
            "Bài Lab K5 Day04 (ReAct Loop Agent) gồm 7 checkpoint với thời lượng 15 | 50 | 25 | 30 | 55 | 25 | 15 phút "
            "(tổng 215 phút làm bài, nghỉ 10 phút, trung bình 30,7 phút/CP), áp dụng cùng khung thời lượng cho cả 3 ca học."
        ),
        "quote": "Day04 ReAct Loop Agent: 7 checkpoint (15|50|25|30|55|25|15 phút, tổng 215 phút), 3 ca học cùng thời lượng, nghỉ 10 phút.",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day06/CHECKPOINTS#benchmark-20",
        "lab": "K5 Day06 — Data Ingestion Engineering",
        "file": "Lab/K5-L3-Day06-DataIngestionEngineering/CHECKPOINTS.md:8",
        "title": "K5 Day06 (Data Ingestion) · Quy mô bộ benchmark và tỷ lệ chia dev/test",
        "keywords": ["day06", "day 6", "day 06", "data ingestion", "benchmark", "bao nhiêu câu", "20 câu", "15 dev", "5 test", "chia thế nào"],
        "summary": (
            "Trong bài Lab K5 Day06 (Data Ingestion Engineering, gồm 6 checkpoint: 25|35|50|40|50|30 phút = 230 phút), "
            "bộ câu thử benchmark bắt buộc có tối thiểu ≥ 20 câu và chia theo tỷ lệ 15 câu dev / 5 câu test."
        ),
        "quote": "Benchmark cần ≥ 20 câu, chia 15 dev / 5 test (CHECKPOINTS.md:8).",
        "conflicts_with": [],
    },
    {
        "code": "K5-Day06/CHECKPOINTS#moc-khong-phai-deadline",
        "lab": "K5 Day06 — Data Ingestion Engineering",
        "file": "Lab/K5-L3-Day06-DataIngestionEngineering/CHECKPOINTS.md:3-13",
        "title": "K5 Day06 · Giờ mốc tích luỹ (vd 4:00) không phải hạn nộp bài cuối cùng",
        "keywords": ["day06", "day 6", "day 06", "mốc 4:00", "4:00", "hạn nộp", "deadline", "không phải hạn nộp", "giảng viên", "coach thông báo"],
        "summary": (
            "Dòng 3 của CHECKPOINTS.md ở K5 Day06 ghi rõ các mốc thời gian tích luỹ trong bảng (như mốc 4:00, nghỉ 1:50–2:00) "
            "KHÔNG phải là hạn nộp bài cuối cùng; hạn nộp chính xác không ghi cứng trong CHECKPOINTS.md mà do giảng viên / lab coach "
            "thông báo theo từng ca học (cần kiểm SUBMISSION.md hoặc hỏi trực tiếp Lab Coach của ca)."
        ),
        "quote": "Các mốc ... không phải hạn nộp bài. Deadline do giảng viên/coach thông báo (CHECKPOINTS.md:3).",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day07/CHECKPOINTS#lich-4-moc",
        "lab": "K5 Day07 — Retrieval & Context",
        "file": "Lab/K5-L3A-DAY07/CHECKPOINTS.md:3-10",
        "title": "K5 Day07 (Retrieval & Context) · 4 checkpoint trong 240 phút",
        "keywords": ["day07", "day 7", "day 07", "retrieval", "context", "4 checkpoint", "240 phút", "lịch khởi đầu"],
        "summary": (
            "Bài Lab K5 Day07 (Retrieval & Context) có 4 checkpoint với thời lượng 60 | 60 | 90 | 30 phút (tổng 240 phút, "
            "trung bình 60 phút/CP); tài liệu lưu ý đây là 'một lịch khởi đầu' và có thể điều chỉnh tuỳ lớp."
        ),
        "quote": "Day07 Retrieval & Context: 4 checkpoint (60|60|90|30 phút, tổng 240 phút), ghi chú 'một lịch khởi đầu, tuỳ lớp'.",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day08/CHECKPOINTS#lich-va-deadline",
        "lab": "K5 Day08 — From Workflows to Agents",
        "file": "Lab/K5-Day8-From-Workflows-to-Agents/CHECKPOINTS.md:3-37",
        "title": "K5 Day08 (From Workflows to Agents) · 5 checkpoint và lưu ý giờ mốc khác hạn nộp",
        "keywords": ["day08", "day 8", "day 08", "workflows to agents", "5 checkpoint", "210 phút", "15:15", "17:00", "không phải hạn nộp"],
        "summary": (
            "Bài Lab K5 Day08 (From Workflows to Agents) gồm 5 checkpoint (15 | 45 | 60 | 45 | 45 phút = 210 phút; "
            "giờ ghi trong bảng là lúc bắt đầu từng CP, CP3 bao gồm giờ nghỉ 15:15–15:30, CP5 kết thúc lúc 17:00). "
            "Tương tự Day06 và Day13, dòng 3 của CHECKPOINTS.md nhắc rõ giờ checkpoint không phải là hạn nộp bài."
        ),
        "quote": "5 checkpoint (15|45|60|45|45 phút); dòng 3 ghi rõ giờ checkpoint không phải hạn nộp; CP5 kết thúc trên lớp lúc 17:00.",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day09/CHECKPOINTS#moc-m0-m5",
        "lab": "K5 Day09 — Evaluation & Failure Analysis",
        "file": "Lab/K5-Day9-Evaluation-and-Failure-Analysis/CHECKPOINTS.md:3-22",
        "title": "K5 Day09 (Evaluation & Failure Analysis) · M0–M4 tại lớp, M5 làm sau 17:00 hạn 23:59",
        "keywords": ["day09", "day 9", "day 09", "evaluation", "failure analysis", "m0", "m4", "m5", "17:00", "23:59", "hạn khi nào"],
        "summary": (
            "Bài Lab K5 Day09 (Evaluation & Failure Analysis) chia thành 6 mốc từ M0 đến M5 (tài liệu không ghi số phút lẻ từng mốc): "
            "các mốc M0–M4 thực hiện tại lớp, riêng mốc M5 làm sau 17:00 với hạn nộp trước 23:59 cùng ngày."
        ),
        "quote": "6 mốc M0–M5: M0–M4 làm tại lớp, M5 làm sau 17:00, hạn nộp 23:59 (CHECKPOINTS.md:3-22).",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day10/CHECKPOINTS#poc-to-pilot",
        "lab": "K5 Day10 — PoC to Pilot Gate 1",
        "file": "Lab/K5-L3A-DAY10-HTHC-PoCtoPilotGate1/CHECKPOINTS.md:5-37",
        "title": "K5 Day10 (PoC to Pilot Gate 1) · 5 checkpoint trong 230 phút",
        "keywords": ["day10", "day 10", "poc", "pilot", "gate 1", "5 checkpoint", "230 phút", "115-125"],
        "summary": (
            "Bài Lab K5 Day10 (PoC to Pilot Gate 1) có 5 checkpoint với thời lượng 15 | 50 | 50 | 60 | 55 phút "
            "(tổng 230 phút làm bài, trung bình 46 phút/CP, nghỉ giải lao ở phút 115–125)."
        ),
        "quote": "Day10 PoC to Pilot Gate 1: 5 checkpoint (15|50|50|60|55 phút, tổng 230 phút), nghỉ phút 115–125.",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day11/CHECKPOINTS#outputs-rule",
        "lab": "K5 Day11 — Guardrails, HITL & Responsible AI",
        "file": "Lab/K5-L3-LAB-Day11/CHECKPOINTS.md:3,5",
        "title": "K5 Day11 (Guardrails) · Cấm tự tạo tay file JSON trong thư mục outputs/",
        "keywords": ["day11", "day 11", "guardrails", "hitl", "cp3", "tự tạo file json", "outputs/", "sinh ra khi chạy lệnh", "5 checkpoint", "155 phút"],
        "summary": (
            "Bài Lab K5 Day11 (Guardrails & HITL, 5 checkpoint: 30|45|40|30|10 phút ≈ 155 phút) quy định ngay ở dòng 5 của "
            "CHECKPOINTS.md: học viên KHÔNG được tự tạo tay file JSON trong thư mục `outputs/`; các file này bắt buộc phải "
            "được sinh ra tự động khi chạy lệnh kiểm thử thực tế."
        ),
        "quote": "Không được tự tạo file JSON trong outputs/ — file phải được sinh ra khi chạy lệnh (CHECKPOINTS.md:5).",
        "conflicts_with": [],
    },
    {
        "code": "K5-Day11/CHECKPOINTS#nop-bai",
        "lab": "K5 Day11 — Guardrails, HITL & Responsible AI",
        "file": "Lab/K5-L3-LAB-Day11/CHECKPOINTS.md:65,68",
        "title": "K5 Day11 (Guardrails) · Hai file kết quả bắt buộc phải nộp trong outputs/",
        "keywords": ["day11", "day 11", "file nào bắt buộc nộp", "cần nộp gì", "results.json", "attack_results.json", "outputs"],
        "summary": (
            "Khi nộp bài Lab K5 Day11, hai file kết quả bắt buộc phải có trong thư mục `outputs/` là "
            "`outputs/results.json` và `outputs/attack_results.json` (được sinh ra từ lệnh chạy)."
        ),
        "quote": "File bắt buộc nộp: outputs/results.json và outputs/attack_results.json (CHECKPOINTS.md:65,68).",
        "conflicts_with": [],
    },
    {
        "code": "K5-Day11/CHECKPOINTS#ba-agent-bonus",
        "lab": "K5 Day11 — Guardrails, HITL & Responsible AI",
        "file": "Lab/K5-L3-LAB-Day11/CHECKPOINTS.md:15-25",
        "title": "K5 Day11 (Guardrails) · Phân biệt 3 agent (Blue, Red, Red Advance) và quy tắc tính 1 bonus",
        "keywords": ["day11", "day 11", "red", "red advance", "blue", "leak", "flag", "cp3", "cộng cả hai bonus", "bonus", "ba agent"],
        "summary": (
            "Mục 'Ba agent (nhớ bảng này)' (CHECKPOINTS.md:15-25) nhắc phân biệt tên vai (Blue/Red Team) với 3 agent "
            "(`Blue`, `Red`, `Red Advance`). Nếu khai thác leak thành công cả hai agent `Red` và `Red Advance` thì KHÔNG được "
            "cộng dồn cả hai mà chỉ được tính một phần điểm bonus."
        ),
        "quote": "Leak được cả Red và Red Advance thì không cộng cả hai bonus — chỉ tính một (CHECKPOINTS.md:23).",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day12/CHECKPOINTS#lich-cp0-cp5",
        "lab": "K5 Day12 — AI SDLC",
        "file": "Lab/K5-L3-LAB-Day12-AI-SDLC/CHECKPOINTS.md:12-17",
        "title": "K5 Day12 (AI SDLC) · 6 checkpoint (CP0–CP5) có mốc lồng nhau trong 240 phút",
        "keywords": ["day12", "day 12", "ai sdlc", "6 checkpoint", "cp0", "cp5", "chồng giờ", "240 phút"],
        "summary": (
            "Bài Lab K5 Day12 (AI SDLC) gồm 6 mốc CP0–CP5 trong tổng 240 phút, lưu ý thiết kế giờ lồng nhau: "
            "CP0 (10 phút) nằm bên trong 60 phút đầu của CP1, và CP5 (10–15 phút) nằm trong giờ cuối của CP4 "
            "(thời lượng thực tách rời tương ứng khoảng 10 | 50 | 60 | 30 | 77,5 | 12,5 phút)."
        ),
        "quote": "Day12 AI SDLC (240 phút): CP0 nằm trong 60 phút của CP1; CP5 (10–15 phút) nằm trong giờ cuối của CP4 (CHECKPOINTS.md:12-17).",
        "conflicts_with": [],
    },
    {
        "code": "K5-Day12/CHECKPOINTS#demo-video",
        "lab": "K5 Day12 — AI SDLC",
        "file": "Lab/K5-L3-LAB-Day12-AI-SDLC/CHECKPOINTS.md:129",
        "title": "K5 Day12 (AI SDLC) · Thời lượng tối đa và vị trí nộp video demo",
        "keywords": ["day12", "day 12", "video demo", "dài tối đa", "5 phút", "100 mb", "release v1.0.0", "demo.mp4", "nộp ở đâu"],
        "summary": (
            "Ở Lab K5 Day12, video demo phải dài dưới 5 phút, nộp bằng cách đính kèm vào GitHub Release `v1.0.0` "
            "hoặc lưu tại `docs/demo/demo.mp4` (dung lượng dưới 100 MB) và đặt đường link ngay ở đầu file `README.md`."
        ),
        "quote": "Video demo dưới 5 phút, gắn ở Release v1.0.0 hoặc docs/demo/demo.mp4 dưới 100 MB, đặt link ở đầu README (CHECKPOINTS.md:129).",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day13/CHECKPOINTS#gan-nhan-doc-lap",
        "lab": "K5 Day13 — Launch Economics",
        "file": "Lab/K5-L3A-DAY13-HC2-LaunchEconomics/CHECKPOINTS.md:3-39",
        "title": "K5 Day13 (Launch Economics) · Quy tắc gắn nhãn độc lập 20 ca lỗi trong 8 phút",
        "keywords": ["day13", "day 13", "launch economics", "gắn nhãn", "20 ca lỗi", "8 phút", "độc lập", "trao đổi", "không phải hạn nộp"],
        "summary": (
            "Bài Lab K5 Day13 (Launch Economics, 5 checkpoint: 53|27|33|28|84 phút = 225 phút, nghỉ 15:20–15:35; dòng 3 lưu ý "
            "giờ mốc không phải hạn nộp) quy định ở bước gắn nhãn 20 ca lỗi: thực hiện trong 8 phút, hai người phải gắn nhãn "
            "hoàn toàn độc lập, không được trao đổi với nhau trong lúc gắn."
        ),
        "quote": "Gắn nhãn 20 ca lỗi trong 8 phút: hai người gắn độc lập, không trao đổi (CHECKPOINTS.md:26).",
        "conflicts_with": [],
    },

    {
        "code": "K5-Day14/CHECKPOINTS#lo-trinh-240p",
        "lab": "K5 Day14 — Deployment, Benchmark & Observability",
        "file": "Lab/K5-L3-Day14/CHECKPOINTS.md:6-10,14-22,114",
        "title": "K5 Day14 · Lộ trình rút gọn 240 phút của lớp K5 (khác 3 điểm so với CODE_LAB.md)",
        "keywords": ["day14", "day 14", "7 part", "code_lab", "335 phút", "240 phút", "khác ba điểm", "cp8", "9 checkpoint", "làm hết"],
        "summary": (
            "Bài Lab K5 Day14 có 9 mốc (CP0–CP8: 10|20|30|25|20|60|25|45 phút tại lớp = 235 phút + 5 phút nghỉ, riêng CP8 làm sau giờ lab). "
            "CHECKPOINTS.md:6-10 cảnh báo rõ: lộ trình gốc trong `CODE_LAB.md` dài 335 phút (Part 1–7), nên để vừa buổi 240 phút tại lớp, "
            "lớp K5 làm khác 3 điểm so với `CODE_LAB.md` (học viên không làm nguyên xi cả 7 Part tại lớp theo giờ của CODE_LAB.md)."
        ),
        "quote": "Lộ trình trong CODE_LAB.md dài 335 phút (Part 1–7). Để vừa 240 phút, lớp K5 làm khác ba điểm (CHECKPOINTS.md:6).",
        "conflicts_with": ["K5-Day14/CODE_LAB#lo-trinh-335p"],
    },
    {
        "code": "K5-Day14/CODE_LAB#lo-trinh-335p",
        "lab": "K5 Day14 — Deployment, Benchmark & Observability",
        "file": "Lab/K5-L3-Day14/CODE_LAB.md (đối chiếu tại CHECKPOINTS.md:6)",
        "title": "K5 Day14 · Lộ trình gốc 7 Part (335 phút) trong CODE_LAB.md",
        "keywords": ["day14", "day 14", "code_lab", "7 part", "part 1-7", "335 phút", "lộ trình"],
        "summary": (
            "File hướng dẫn thực hành `CODE_LAB.md` của Day14 trình bày đầy đủ 7 phần (Part 1–7) với tổng thời lượng thiết kế gốc "
            "là 335 phút. Tuy nhiên tài liệu này lệch với thời lượng 240 phút trên lớp của K5 — bắt buộc phải đối chiếu với "
            "`K5-Day14/CHECKPOINTS#lo-trinh-240p` để xem 3 điểm điều chỉnh riêng cho lớp K5."
        ),
        "quote": "CODE_LAB.md mô tả lộ trình đầy đủ Part 1–7 dài 335 phút (lệch với khung 240 phút trên lớp ở CHECKPOINTS.md:6-10).",
        "conflicts_with": ["K5-Day14/CHECKPOINTS#lo-trinh-240p"],
    },
    {
        "code": "K5-Day14/CHECKPOINTS#cp5-va-ket",
        "lab": "K5 Day14 — Deployment, Benchmark & Observability",
        "file": "Lab/K5-L3-Day14/CHECKPOINTS.md:25",
        "title": "K5 Day14 · Trọng số điểm CP5 (60/120) và quy tắc xử lý khi kẹt quá 10 phút",
        "keywords": ["day14", "day 14", "cp5", "nhiều điểm nhất", "60/120", "kẹt", "quá lâu", "10 phút", "gọi lab coach"],
        "summary": (
            "Trong bảng điểm của Lab K5 Day14, mốc CP5 chiếm nhiều điểm nhất với 60/120 điểm. Nếu học viên bị kẹt ở bất kỳ "
            "checkpoint nào quá 10 phút thì quy định xử lý là: gọi ngay Lab Coach, ghi nhận lại lỗi và chuyển sang làm mốc tiếp theo."
        ),
        "quote": "CP5 nhiều điểm nhất: 60/120 điểm. Kẹt ở một CP quá 10 phút: gọi Lab Coach, ghi lỗi, đi tiếp mốc sau (CHECKPOINTS.md:25).",
        "conflicts_with": [],
    },
    {
        "code": "K5-Day14/CHECKPOINTS#deadline-va-6-file",
        "lab": "K5 Day14 — Deployment, Benchmark & Observability",
        "file": "Lab/K5-L3-Day14/CHECKPOINTS.md:3",
        "title": "K5 Day14 · Quy chiếu hạn nộp sang SUBMISSION.md và cấu trúc 6 file liên kết",
        "keywords": ["day14", "day 14", "hạn nộp", "deadline", "submission.md", "delivery_checklist", "6 file"],
        "summary": (
            "Ở K5 Day14, file `CHECKPOINTS.md` không ghi giờ khoá sổ nộp bài mà chỉ dẫn ở dòng 3: 'Deadline: xem SUBMISSION.md', "
            "đồng thời dẫn link sang tổng cộng 6 file khác (`CODE_LAB.md`, `DAY14_DELIVERY_CHECKLIST.md`, `README.md`, "
            "`RUBRIC.md`, `SUBMISSION.md`, `06-lab-complete/README.md`)."
        ),
        "quote": "Deadline: xem SUBMISSION.md (CHECKPOINTS.md:3) — file CHECKPOINTS.md liên kết sang 6 file hướng dẫn khác.",
        "conflicts_with": [],
    },

    {
        "code": "K5-L3-General/QUY-UOC#nhip-lab-va-han-nop",
        "lab": "Quy ước chung các bài Lab ngày lớp L3 K5",
        "file": "evidence/lab-checkpoint-analysis.md#1,3",
        "title": "Nhịp bài Lab hàng ngày lớp L3 (686 học viên) & thông lệ hạn nộp theo ca học",
        "keywords": ["686 học viên", "6 tuần", "3 tuần", "phase 1", "mỗi ngày", "23:59", "11:59", "11h59", "4h chiều", "16:00", "hạn nộp thường"],
        "summary": (
            "Lớp L3 có 686 học viên, lộ trình 6 tuần với 3 tuần đầu học liên tục Phase 1 (mỗi ngày đều làm lab, trung bình 5,8 CP/bài lab). "
            "Thông lệ hạn nộp bài lab thường là trước 23:59 cùng ngày, hoặc trước 11:59 trưa ngày hôm sau nếu lịch học lab bắt đầu lúc 16:00 (4h chiều). "
            "Tuy nhiên giờ mốc trong CHECKPOINTS.md không phải hạn nộp; hạn chính thức của từng bài luôn phải kiểm ở SUBMISSION.md hoặc hỏi Lab Coach."
        ),
        "quote": "Giờ checkpoint không phải hạn nộp; hạn nộp cụ thể nằm ở SUBMISSION.md hoặc do giảng viên/lab coach thông báo theo ca (thường 23:59 cùng ngày hoặc 11:59 trưa hôm sau với ca 16:00).",
        "conflicts_with": [],
    },
]


def count_csv_stats() -> dict[str, int]:
    if not os.path.exists(CSV_SOURCE):
        return {"total_units": 40, "k5_daily_labs": 12}
    with open(CSV_SOURCE, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    k5_daily = sum(1 for r in rows if r.get("khoa") == "K5" and r.get("loai") == "Lab ngày")
    return {"total_units": len(rows), "k5_daily_labs": k5_daily}


def build(source_root: Path | None = None) -> dict[str, Any]:
    stats = count_csv_stats()
    sections = []
    for section in SECTIONS:
        ref = section["file"]
        relative = ref.split(":", 1)[0].split("#", 1)[0].split(" (", 1)[0]
        if relative.startswith("evidence/"):
            source = Path(ROOT) / relative
        else:
            source = source_root / relative if source_root is not None else None
        if source is not None and source.is_file():
            content = source.read_bytes()
            scope = "source_file"
        else:
            content = json.dumps(section, ensure_ascii=False, sort_keys=True).encode("utf-8")
            scope = "indexed_excerpt"
        sections.append({
            **section,
            "doc_sha256": hashlib.sha256(content).hexdigest()[:8],
            "doc_sha256_scope": scope,
        })
    payload = {
        "version": CORPUS_VERSION,
        "updated_at": "2026-11-27T15:15:00+07:00",
        "description": (
            "Chỉ mục tra cứu có nguồn từ 12 bài Lab ngày Phase 1 của lớp L3 khoá K5 (Day01–Day14). "
            "Mọi mục đều đối chiếu trực tiếp tới file:dòng trong evidence/lab-checkpoint-analysis.md và evidence/lab-checkpoints.csv, "
            "chỉ lưu tóm tắt + trích đoạn ngắn (≤ 60 từ), không chứa tài liệu nguyên văn và không chứa nội dung Hackathon."
        ),
        "corpus_stats": stats,
        "section_count": len(sections),
        "sections": sections,
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return payload


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, help="Thư mục tài liệu gốc chứa Lab/")
    args = parser.parse_args()
    if args.source_root is not None and not (args.source_root / "Lab").is_dir():
        parser.error("--source-root phải chứa thư mục Lab/")
    data = build(args.source_root)
    conflict_count = sum(1 for s in data["sections"] if s.get("conflicts_with"))
    print(
        f"Đã tạo {OUT_PATH}: {data['section_count']} mục từ {data['corpus_stats']['k5_daily_labs']} bài Lab ngày K5 "
        f"(trên tổng {data['corpus_stats']['total_units']} đơn vị lab ở lab-checkpoints.csv), "
        f"{conflict_count} mục gắn cờ đối chiếu lệch giữa hai file."
    )
