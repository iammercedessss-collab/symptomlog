"""
SymptomLog - Personal Health Tracker
By Mercedes Ebegbodi

A CLI tool to log symptoms over time and surface patterns.
No external libraries required - pure Python.
"""

import json
import os
from datetime import datetime
from collections import defaultdict


DATA_FILE = "symptom_log.json"


# ── DATA HELPERS ──────────────────────────────────────────────────────────────

def load_logs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_logs(logs):
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f, indent=2)


# ── FEATURES ──────────────────────────────────────────────────────────────────

def log_symptom(logs):
    print("\n── Log a Symptom ──────────────────────────────")
    symptom = input("Symptom name (e.g. headache, fatigue, nausea): ").strip().lower()
    if not symptom:
        print("No symptom entered. Returning to menu.")
        return

    while True:
        try:
            severity = int(input("Severity (1 = mild, 10 = severe): ").strip())
            if 1 <= severity <= 10:
                break
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    notes = input("Any notes? (press Enter to skip): ").strip()
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")

    entry = {
        "symptom": symptom,
        "severity": severity,
        "notes": notes,
        "date": date,
        "time": time
    }

    logs.append(entry)
    save_logs(logs)
    print(f"\n✓ Logged: {symptom} (severity {severity}) on {date} at {time}")


def view_history(logs):
    print("\n── Symptom History ────────────────────────────")
    if not logs:
        print("No symptoms logged yet.")
        return

    # Show most recent 20 entries
    recent = logs[-20:][::-1]
    print(f"{'DATE':<12} {'TIME':<8} {'SYMPTOM':<20} {'SEVERITY':<10} NOTES")
    print("-" * 70)
    for e in recent:
        notes_preview = (e['notes'][:20] + "...") if len(e['notes']) > 20 else e['notes']
        print(f"{e['date']:<12} {e['time']:<8} {e['symptom']:<20} {e['severity']:<10} {notes_preview}")


def view_summary(logs):
    print("\n── Summary & Patterns ─────────────────────────")
    if not logs:
        print("No symptoms logged yet.")
        return

    # Count frequency and average severity per symptom
    symptom_data = defaultdict(lambda: {"count": 0, "total_severity": 0})
    for entry in logs:
        s = entry["symptom"]
        symptom_data[s]["count"] += 1
        symptom_data[s]["total_severity"] += entry["severity"]

    print(f"\nTotal entries logged: {len(logs)}")
    print(f"Unique symptoms tracked: {len(symptom_data)}\n")

    print(f"{'SYMPTOM':<22} {'TIMES LOGGED':<15} {'AVG SEVERITY'}")
    print("-" * 52)

    # Sort by most frequent
    sorted_symptoms = sorted(symptom_data.items(), key=lambda x: x[1]["count"], reverse=True)
    for symptom, data in sorted_symptoms:
        avg = data["total_severity"] / data["count"]
        bar = "█" * int(avg)
        print(f"{symptom:<22} {data['count']:<15} {avg:.1f}/10  {bar}")

    # Most recent 7 days
    print("\n── Last 7 Days ────────────────────────────────")
    today = datetime.now()
    recent_symptoms = defaultdict(int)
    for entry in logs:
        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
        if (today - entry_date).days <= 7:
            recent_symptoms[entry["symptom"]] += 1

    if recent_symptoms:
        for symptom, count in sorted(recent_symptoms.items(), key=lambda x: x[1], reverse=True):
            print(f"  {symptom}: {count} time(s)")
    else:
        print("  No symptoms logged in the last 7 days.")


def search_symptom(logs):
    print("\n── Search Symptom ─────────────────────────────")
    query = input("Enter symptom to search: ").strip().lower()
    results = [e for e in logs if query in e["symptom"]]

    if not results:
        print(f"No entries found for '{query}'.")
        return

    print(f"\nFound {len(results)} entries for '{query}':\n")
    print(f"{'DATE':<12} {'SEVERITY':<10} NOTES")
    print("-" * 50)
    for e in results:
        print(f"{e['date']:<12} {e['severity']:<10} {e['notes'] or '—'}")

    avg_severity = sum(e["severity"] for e in results) / len(results)
    print(f"\nAverage severity: {avg_severity:.1f}/10 over {len(results)} log(s)")


# ── MAIN MENU ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  SymptomLog — Personal Health Tracker")
    print("  by Mercedes Ebegbodi")
    print("=" * 50)

    logs = load_logs()
    print(f"  {len(logs)} entries loaded.\n")

    menu = {
        "1": ("Log a symptom", log_symptom),
        "2": ("View history", view_history),
        "3": ("View summary & patterns", view_summary),
        "4": ("Search a symptom", search_symptom),
        "5": ("Exit", None),
    }

    while True:
        print("\n── Menu ────────────────────────────────────────")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "5":
            print("\nGoodbye! Stay healthy. 💙\n")
            break
        elif choice in menu:
            _, action = menu[choice]
            action(logs)
        else:
            print("Invalid choice. Please enter 1–5.")


if __name__ == "__main__":
    main()
