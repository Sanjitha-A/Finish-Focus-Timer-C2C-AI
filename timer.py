import json
from datetime import date
from pathlib import Path
from time import monotonic


LOG_FILE = Path(__file__).with_name("focus_log.json")


def load_sessions(path=LOG_FILE):
    if not path.exists():
        return []

    with path.open(encoding="utf-8") as log_file:
        sessions = json.load(log_file)

    if not isinstance(sessions, list):
        raise ValueError(f"Focus log must contain a JSON list: {path}")
    return sessions


def save_sessions(sessions, path=LOG_FILE):
    with path.open("w", encoding="utf-8") as log_file:
        json.dump(sessions, log_file, indent=2)
        log_file.write("\n")


def show_daily_summary(sessions):
    today = date.today().isoformat()
    today_sessions = [session for session in sessions if session["date"] == today]
    if not today_sessions:
        print("No focus sessions logged today.")
        return

    minutes_by_name = {}
    for session in today_sessions:
        name = session["name"]
        minutes_by_name[name] = minutes_by_name.get(name, 0) + session["minutes"]

    for name, minutes in minutes_by_name.items():
        print(f"{name}: {minutes:.1f} min")

    grand_total = sum(minutes_by_name.values())
    print(f"Total: {grand_total:.1f} min")


def start_focus_session():
    name = input("Enter a name for this focus session: ")
    print("Session started. Press Enter to stop the timer.")
    started_at = monotonic()
    input()
    elapsed_minutes = (monotonic() - started_at) / 60

    return {
        "name": name,
        "date": date.today().isoformat(),
        "minutes": round(elapsed_minutes, 1),
    }


def main(log_path=LOG_FILE):
    sessions = load_sessions(log_path)

    while True:
        print("\n1. Start a focus session")
        print("2. Show today's summary")
        print("3. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            session = start_focus_session()
            sessions.append(session)
            save_sessions(sessions, log_path)
        elif choice == "2":
            show_daily_summary(sessions)
        elif choice == "3":
            print("Quitting FocusTimer.")
            break
        else:
            print("Not a valid choice")


if __name__ == "__main__":
    main()