"""Host-only, local→local checks of the exact activation check template."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
FILTERS=['--exclude','**/.git/objects/**/tmp_obj_*','--exclude','**/.git/objects/tmp_obj_*',
         '--exclude','/.git/objects/**/tmp_obj_*','--exclude','/.git/objects/tmp_obj_*']

def filter_argv(excludes): return ['--exclude-from',str(excludes),*FILTERS,'--links']

def check_argv(source,destination,excludes,run,download=False):
    run=Path(run)
    return ['/opt/homebrew/bin/rclone','check',str(source),str(destination),'--one-way',
            *filter_argv(excludes),'--combined',str(run/'combined.txt'),
            '--differ',str(run/'differ.txt'),'--missing-on-dst',str(run/'missing-on-dst.txt'),
            '--error',str(run/'error.txt'),'--log-file',str(run/'check.log'),'--log-level','DEBUG',
            '--log-format','date,time','--stats','0','--retries','1',*(['--download'] if download else [])]

def main():
    from run_py39_coverage import validate_host
    from verify_check import inspect
    validate_host(sys.version_info[:3],os.getpriority(os.PRIO_PROCESS,0),os.environ)
    home=Path(os.environ['HOME']).resolve()
    run=Path(sys.argv[1]).resolve()
    run.relative_to(HERE)
    if not home.is_relative_to(Path('/private/tmp')):
        raise RuntimeError('content fixture HOME must be inside isolated /private/tmp runtime')
    run.mkdir()
    def call(directory,label,argv):
        with (directory/(label+'.stdout.txt')).open('w') as out,(directory/(label+'.stderr.txt')).open('w') as err:
            proc=subprocess.run(argv,text=True,stdout=out,stderr=err,timeout=120)
        (directory/(label+'.exit_code.txt')).write_text(str(proc.returncode)+'\n')
        (directory/(label+'.command.json')).write_text(json.dumps(dict(argv=argv,cwd=str(Path.cwd()),
            interpreter=sys.executable,niceness=os.getpriority(os.PRIO_PROCESS,0),env={'HOME':str(home)},
            source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (Path(__file__),HERE/'verify_check.py',ROOT/'tools/backup_mirror.excludes')}),indent=2)+'\n')
        return proc.returncode
    config=call(run,'config',['/opt/homebrew/bin/rclone','config','file'])
    if config: raise RuntimeError('rclone config file failed')
    config_path=Path((run/'config.stdout.txt').read_text().strip().splitlines()[-1]).resolve()
    config_path.relative_to(home)
    if call(run,'remotes',['/opt/homebrew/bin/rclone','listremotes']) or (run/'remotes.stdout.txt').read_text():
        raise RuntimeError('isolated config must have no remotes')
    results=[]
    for case in ('same_size_corruption','excluded_only','symlink','clean'):
        directory=run/case; directory.mkdir()
        # All content fixtures live under isolated HOME, including symlink targets.
        fixture=home/('content_'+case); fixture.mkdir()
        source=fixture/'source'; source.mkdir()
        (source/'alpha.txt').write_text('same-size-A\n')
        if case=='symlink': (source/'alpha.link').symlink_to('alpha.txt')
        (source/'.cache').mkdir(); (source/'.cache/ignored.txt').write_text('source cache')
        destination=fixture/'destination'; shutil.copytree(source,destination,symlinks=True)
        if case=='same_size_corruption': (destination/'alpha.txt').write_text('same-size-B\n')
        if case=='excluded_only': (destination/'.cache/ignored.txt').write_text('different excluded content')
        excludes=ROOT/'tools/backup_mirror.excludes'
        argv=['/opt/homebrew/bin/rclone','lsf',str(source),'--recursive','--files-only',*filter_argv(excludes)]
        code=call(directory,'inventory',argv)
        (directory/'inventory.txt').write_bytes((directory/'inventory.stdout.txt').read_bytes())
        if code: raise RuntimeError('fixture inventory failed')
        argv=check_argv(source,destination,excludes,directory)
        code=call(directory,'check',argv)
        for name in ('stdout','stderr','exit_code'):
            (directory/(name+'.txt')).write_bytes((directory/('check.'+name+'.txt')).read_bytes())
        verdict=inspect(directory)
        (directory/'verifier.json').write_text(json.dumps(verdict,indent=2)+'\n')
        expected=case!='same_size_corruption'
        passed=verdict['pass']==expected and (expected or 'alpha.txt' in verdict['failed_objects'])
        results.append(dict(case=case,expected_verifier_pass=expected,actual=verdict,accepted=passed,check_exit=code))
    value=dict(cases=results,success=all(x['accepted'] for x in results))
    (run/'result.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(value,indent=2)); return 0 if value['success'] else 1

if __name__=='__main__': sys.exit(main())
