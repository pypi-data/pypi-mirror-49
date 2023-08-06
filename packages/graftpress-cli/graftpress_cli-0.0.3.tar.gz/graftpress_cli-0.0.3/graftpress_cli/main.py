import sys
import cookiecutter
from cookiecutter.main import cookiecutter
import os

import graftpress_cli.compile_elm as ce
import graftpress_cli.rust_json as rj
import json
from typing import List


VERSION = "0.1.0"


def main():
    if len(sys.argv) == 1:
        print(
            f"""\
Hi, thank you for trying out graftpress-cli {VERSION} . I hope you like it!

----------------------------------------------------------------------------
I highly recommend walking throught https://www.graftpress.com to get
started. It teaches many important concepts, including how to use graftpress-cli
in terminal.
----------------------------------------------------------------------------

The most common commonds are:

    graftpress-cli init <proj_name>
        create a new project graftpress project.

    graftpress-cli build
         build the current graftpress project.

    graftpress-cli run
         run the current graftpress project.

Be sure to ask on https://gitter.im/amitu/graftpress if you run into trouble! Folks
are friendly and happy to help out. They hang out there because it is fun, so
be kind to get best results!
        """
        )
        return

    if sys.argv[1] == "version":
        handle_version()
    elif sys.argv[1] == "init":
        handle_init()
    elif sys.argv[1] == "debug":
        handle_debug()
    elif sys.argv[1] == "publish":
        if len(sys.argv) >= 3:
            o_path = sys.argv[2]
        else:
            o_path = "docs"
        
        
        if not o_path.startswith("/"):
            o_path = os.getcwd() + "/" + o_path
        if not os.path.isdir(o_path):
            os.makedirs(o_path)
        handle_publish(o_path)
    elif sys.argv[1] == "build":
        handle_build()
    elif sys.argv[1] == "test":
        publish_test()
    
    else:
        print(f"unknown command: {sys.argv[1]}")


def handle_version():
    print(VERSION)


def publish_test():
    handle_publish("tests/publish/test_res", "tests/publish/test_arg/cms")
    lis_r = []
    for root, dirs, files in os.walk("tests/publish/test_res"):
        for file in files:
            lis_r.append((root.split("tests/publish/test_res")[1], file))


    lis_t = []
    for root, dirs, files in os.walk("tests/publish/test_tar"):
        for file in files:
            lis_t.append((root.split("tests/publish/test_tar")[1], file))
    
    set_res = set(lis_r)
    set_tar = set(lis_t)
    print(set_res)
    print(set_tar)
    print("diff",set_res - set_tar)
    assert(lis_r == lis_t)
def handle_init():
    pass


def handle_debug():
    
    pass

def handle_build():
    if not os.path.isdir("node_modules"):
        os.system("yarn add package.json")
    curr_dir: str = os.getcwd()
    print("curr_dir, ", curr_dir)
    
    bin_path: str = os.path.join(curr_dir, "node_modules", ".bin")
    
    elm_path: str = os.path.join(bin_path, "elm")
    
    elm_format_path: str = os.path.join(bin_path, "elm-format")
    
    elm_dest_dir: str = "static/realm/elatest"
    if not os.path.isdir(elm_dest_dir):
        os.system("mkdir -p " + elm_dest_dir)
    
    
    with open("static/realm/latest.txt", "w+") as file:
        file.write("elatest")
    
    with open("static/realm/elatest/deps.json", "w+") as file:
        file.write("{}")

    
    elm_src_dirs: List[str] = ["frontend"]

    ce.check_conflicts(elm_src_dirs)
    for src_dir in elm_src_dirs:
        ce.compile_all_elm(src_dir, elm_dest_dir, elm_path, elm_format_path, "")


def format_url(u):
    if u == "/":
        return ""
    return u

def handle_publish(publish_folder, read_folder = "cms"):
    #handle absence of publish_folder
    lis_walk = []
    for root, dirs, files in os.walk(read_folder):
        lis_walk.append((root, dirs, files))
    print("lis_walk", lis_walk)
    
    for root, dirs, files in lis_walk:
        url_path = root.split(read_folder)[1]
        if not url_path.endswith("/"):
            url_path += "/"
        
        if "include" in root:
            continue
            
            
        
        for file in files:
            if file == "index.graft":
                output_folder = publish_folder.rstrip("/") + "/" + format_url(url_path)
                
                output_path = output_folder +"index.html"
            else:
                file_name, ext = os.path.splitext(file)
                
                if ext != "graft":
                    pass
                output_folder = publish_folder.rstrip("/") + "/" + format_url(url_path) + file_name
                
                output_path = output_folder.rstrip("/") + "/" + "index.html"
            
            
            if not os.path.isdir(output_folder):
                print(output_folder)
                os.makedirs(output_folder)
                
            os.system("wget -m 127.0.0.1:3000/" + url_path.lstrip("/") + " -O " + output_path)
            
    

            
