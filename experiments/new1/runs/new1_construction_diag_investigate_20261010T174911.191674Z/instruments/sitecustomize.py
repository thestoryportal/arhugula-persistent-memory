import os
if os.environ.get('NEW1_OBSERVE_DIR') and os.environ.get('NEW1_OBSERVE_LAUNCHER_PID',str(os.getppid())) == str(os.getppid()):
    import state_observer
    state_observer.install()
