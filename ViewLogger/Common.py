def run(excuter):
    import subprocess
    PIPE = subprocess.PIPE
    p = subprocess.Popen(excuter, stdout=PIPE, stderr=PIPE, shell=True)
    out = ""
    while p.poll() is None:
        line = "".join(p.stdout.readlines())
        out += line
    return out
