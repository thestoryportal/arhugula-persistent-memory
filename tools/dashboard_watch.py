"""Program-session watcher (run under Monitor): one line per change in the team's state, so the lead can act at once —
a session starts waiting for an answer, stalls (no new step for 15 min while working), stops after an error, recovers,
or finishes (a 'Worked for' line after working). Every 60 s; never touches a session.
Usage: /usr/bin/python3 -B tools/dashboard_watch.py
"""
import os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dashboard_live as L  # noqa: E402


def main():
    memory, alerts, working = {}, set(), {}
    while True:
        names = [n for n in L.team_sessions(L.sh("tmux", "list-sessions", "-F", "#{session_name}").split()) if n != "program"]
        screens = {n: L.sh("tmux", "capture-pane", "-p", "-t", n) for n in names}
        now = set(L.session_alerts(screens, memory, time.time()))
        for a in sorted(now - alerts):
            print(f"ALERT {a}", flush=True)
        for a in sorted(alerts - now):
            print(f"CLEARED {a}", flush=True)
        alerts = now
        for n, screen in screens.items():
            busy = "esc to interrupt" in screen
            if working.get(n) and not busy:
                print(f"FINISHED {n}" + (" (DONE)" if "DONE" in screen else " (no DONE line: read its report)"), flush=True)
            working[n] = busy
        time.sleep(60)


if __name__ == "__main__":
    main()
