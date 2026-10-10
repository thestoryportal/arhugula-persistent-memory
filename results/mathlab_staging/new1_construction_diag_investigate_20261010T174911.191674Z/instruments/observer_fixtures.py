import json
import os
import signal
import subprocess
import sys
import time
import unittest


class SignalFixture(unittest.TestCase):
    def test_alarm(self):
        class Fired(Exception): pass
        previous = signal.getsignal(signal.SIGALRM)
        real_signal, real_alarm = signal.signal, signal.setitimer
        mask = signal.pthread_sigmask(signal.SIG_BLOCK, [])
        seen = []
        start = time.monotonic()
        def known_handler(number, frame):
            seen.append(time.monotonic()-start)
            raise Fired('known alarm')
        signal.signal(signal.SIGALRM, known_handler)
        try:
            signal.setitimer(signal.ITIMER_REAL, .04)
            with self.assertRaises(Fired): time.sleep(.2)
            self.assertEqual(len(seen), 1)
            self.assertGreater(seen[0], .02)
            self.assertLess(seen[0], .25)
            self.assertIs(signal.getsignal(signal.SIGALRM), known_handler)
            self.assertIs(signal.signal, real_signal)
            self.assertIs(signal.setitimer, real_alarm)
            self.assertEqual(signal.getitimer(signal.ITIMER_REAL), (0.,0.))
            self.assertEqual(signal.pthread_sigmask(signal.SIG_BLOCK, []), mask)
            print(json.dumps({'known_alarm_s':seen[0],'expected_s':.04,'handler_unchanged':True}))
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)

    def test_failure(self): self.fail('known failure')

    def test_native_exit(self): os._exit(37)

    def test_owned_child(self):
        process = subprocess.run([sys.executable,'-B','-c','import os;os._exit(23)'], capture_output=True)
        self.assertEqual(process.returncode, 23)

    def test_clear_observer_profile(self): sys.setprofile(None)
