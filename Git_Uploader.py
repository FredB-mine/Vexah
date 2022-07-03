try:
    from subprocess import Popen, PIPE
    from parse import compile

except ImportError:
    from os import system
    __libs__ = [
        "subprocess",
        "parse"
    ]
    for name in __libs__:
        system("pip install " + name)

class Main:
    NormalBranch  = compile("  {}\n")
    CurrentBranch = compile("* {}\n")
    modifiedExpr  = compile("{}:   {}\n")
    def runAndGet(command:str) -> list:
        return Popen(
            command, shell = True, stdout = PIPE
        ).stdout.readlines()

    def checkBranch() -> list:
        # 返回(当前branch,其他branch)
        _ret = ["",[]]
        for reads in Main.runAndGet("git branch"):
            reads = reads.decode('utf-8')
            NormalParseResult  = Main.NormalBranch.parse(reads)
            SpecialParseResult = Main.CurrentBranch.parse(reads)
            if NormalParseResult != None:
                _ret[1].append(NormalParseResult[0])
            else:
                _ret[0] = SpecialParseResult[0]
        return _ret

    def findCommits() -> list:
        _ret = []
        commandOut = Main.runAndGet("git status")
        for line in commandOut:
            line = line.decode("utf-8")
            print(line)
            __ParseResult = Main.modifiedExpr.parse(line)
            if __ParseResult != None:
                _ret.append(__ParseResult[1])
        return _ret

    def main() -> None:
        print("欢迎来到Git上传工具")
        # 首先检查当前的分支:
        CheckResult = Main.checkBranch()
        currentBranch = CheckResult[0]
        otherBranches = CheckResult[1]
        print("当前分支: ",currentBranch)
        print("其他分支: ",otherBranches)
        IfChange = input("是否切换到其他分支? ")
        if IfChange == 'Y' or IfChange == 'y':
            WhichToChange = input("切换到哪个分支? ")
            if WhichToChange in otherBranches:
                Main.runAndGet("git checkout " + WhichToChange)
            else:
                print("NoSence!!!")
                return
        else:
            WhichToChange = currentBranch
        Main.runAndGet("git add .")
        # check which to commit
        commitResult = Main.findCommits()
        print("更改过的文件: ",commitResult)
        for name in commitResult:
            currentCommit = input("请输入对" + name + "的commit: ")
            Main.runAndGet("git commit " + name + " -m \"" + currentCommit + "\"")
        checkIfPush = input("是否推送到GitHub? ")
        if checkIfPush != 'N' and checkIfPush != 'n':
            Main.runAndGet("git push origin " + WhichToChange)
        if IfChange == 'Y' or IfChange == 'y':
            returnToBranch = input("是否回退到原来的分支? ")
            if returnToBranch != 'N' and returnToBranch != 'n':
                Main.runAndGet("git checkout " + currentBranch)
        return

if __name__ == '__main__':
    Main.main()
    exit(0)