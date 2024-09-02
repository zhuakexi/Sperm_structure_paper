import subprocess
from pathlib import Path
ddir = "/shareb/ychi/repo/sperm_struct/notebooks/data"
batches = [
    #"GAM",
    "GAM_MR15_orphan",
    "GAM_MR15_ft4"
]
coolps = [
    # [
    #     "/shareb/ychi/repo/sperm_struct/notebooks/data2/Sperm_hg.gam.1m.cool",
    #     "/shareb/ychi/repo/sperm_struct/notebooks/data2/Sperm_hg.pileup.1k.mcool::resolutions/1000000"
    # ],
    [
        "/shareb/ychi/repo/sperm_struct/notebooks/data2/Sperm_hg.MR15.orphan__0_98.1m.cool",
        "/shareb/ychi/repo/sperm_struct/notebooks/data2/Sperm_hg.pileup.1k.mcool::resolutions/1000000"
    ],
    [
        "/shareb/ychi/repo/sperm_struct/notebooks/data2/Sperm_hg.MR15.fthres__4.1m.cool",
        "/shareb/ychi/repo/sperm_struct/notebooks/data2/Sperm_hg.pileup.1k.mcool::resolutions/1000000"
    ],
]
import subprocess

def run_command(command, cwd):
    print("command:", command)
    print("cwd:", cwd)
    """运行命令并返回输出"""
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
        )
    if result.returncode != 0:
        raise Exception(f"命令执行失败: {result.stderr}")
    return result.stdout.strip()
results = []
for cool_pair in coolps:
    # 运行 htrain 命令
    coolpA, coolpB = cool_pair
    htrain_cmd = f"hicreppy htrain -m 10000000 -b chrX,chrY {coolpA} {coolpB}"
    htrain_output = run_command(htrain_cmd, ddir)

    # 从 htrain 输出中获取整数参数
    v_param = int(htrain_output)

    # 运行 scc 命令
    scc_cmd = f"hicreppy scc -v {v_param} -m 10000000 -b chrX,chrY {coolpA} {coolpB}"
    scc_output = run_command(scc_cmd, ddir)

    # 输出 scc 命令的结果
    results.append(scc_output)
print(
    "results:\n",
    "\n".join(results)
    )
with open("scc_results.txt", "w") as f:
    for batch, result in zip(batches, results):
        f.write(f"{batch}\n{result}\n")