#!/usr/bin/env python3

import os
import subprocess
import sys
import platform


def input_int(prompt: str, lower: int, upper: int) -> int:
    while True:
        try:
            i = int(input(prompt))
            if i >= lower and i <= upper:
                return i
        except KeyboardInterrupt as e:
            raise e
        except ValueError:
            pass


def input_yn(prompt: str, default: str) -> bool:
    yn_string = ""
    if default == "y" or default == "Y":
        yn_string = "Y/n"
    elif default == "n" or default == "N":
        yn_string = "y/N"
    else:
        yn_string = "y/n"

    while True:
        try:
            r = input("{} ({}): ".format(prompt, yn_string))
            if r == "":
                if default == "y" or default == "Y":
                    return True
                if default == "n" or default == "N":
                    return False
            elif r == "y" or r == "Y":
                return True
            elif r == "n" or r == "N":
                return False
        except KeyboardInterrupt as e:
            raise e


if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(__file__)
        target_dir = os.path.join(script_dir, "targets")
        host_dir = os.path.join(script_dir, "hosts")
    
        files = os.listdir(target_dir)
        targets = []
        for f in files:
            if f.endswith(".config"):
                targets.append(f)
        targets.sort()

        files = os.listdir(host_dir)
        hosts = []
        for f in files:
            if f.endswith(".config"):
                hosts.append(f)
        hosts.sort()

        if platform.system() != "Linux":
            print("ERROR: Only building on linux is supported!")
            exit(1)

        print("================================================================================")
        print("Targets")
        print("================================================================================")
        for i in range(len(targets)):
            print("    {}: {}".format(i, targets[i]))
        sel_target = targets[input_int("Select Target: ", 0, len(targets) - 1)]
        print("================================================================================")
        print()

        print("================================================================================")
        print("Hosts")
        print("================================================================================")
        for i in range(len(hosts)):
            print("    {}: {}".format(i, hosts[i]))
        sel_host = hosts[input_int("Select Host: ", 0, len(hosts) - 1)]
        print("================================================================================")
        print()


        print("================================================================================")
        print("Selected Configuration:")
        print("================================================================================")
        print("    Target: {}".format(sel_target))
        print("    Host:   {}".format(sel_host))
        print("================================================================================")
        print()

        if os.path.exists(os.path.join(script_dir, ".config")):
            os.remove(os.path.join(script_dir, ".config"))
        with open(os.path.join(script_dir, ".config"), 'w') as cf:
            cf.write("# Target configuration")
            cf.write(os.linesep)
            with open(os.path.join(target_dir, sel_target)) as tf:
                cf.write(tf.read())
            cf.write(os.linesep)
            cf.write(os.linesep)
            cf.write("# Host configuration")
            cf.write(os.linesep)
            with open(os.path.join(host_dir, sel_host)) as hf:
                cf.write(hf.read())

        print("================================================================================")
        print("ct-ng menuconfig")
        print("================================================================================")
        print("Press enter to run ct-ng menuconfig.")
        print("It is recommended to disable 'render readonly' under 'paths and misc options'.")
        print("Then, save as '.config' and exit.")
        input()
        try:
            p = subprocess.Popen(["ct-ng", "menuconfig"], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, bufsize=0)
            if p.wait() != 0:
                print("ct-ng menuconfig exited with non-zero return code.")
                exit(1)
        except FileNotFoundError:
            print("ct-ng not found!")
            exit(1)
        print("================================================================================")
        print()

        print("================================================================================")
        print("ct-ng build")
        print("================================================================================")
        ncores = input_int("Build threads: ", 1, 999999)
        try:
            p = subprocess.Popen(["ct-ng", "build.{}".format(ncores)], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, bufsize=0)
            if p.wait() != 0:
                print("ct-ng build exited with non-zero return code.")
                exit(1)
        except FileNotFoundError:
            print("ct-ng not found!")
            exit(1)
        print("================================================================================")
    except KeyboardInterrupt:
        exit(1)


