#encoding=utf-8
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from pathlib import Path
import shutil
import sys, os


class MyBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent
        target_dir = build_dir if not self.inplace else root_dir
        target_dir = target_dir / 'sqless'
        print("[build_dir]  : ", build_dir)
        print("[root_dir]   : ", root_dir)
        print("[target_dir] : ", target_dir)
        # 处理目录
        for module in my_packages:
            if module.split('.')[0] in exclude_dir:
                continue
            module = module.replace(".","/")
            module_path = Path(module)
            print(">>find modeule path:" + str(module_path))
            # 头文件
            self.copy_file(module_path / '__init__.py', root_dir, target_dir)
            for p in module_path.iterdir():
                # 已加密py文件
                if p.is_file() and p.rglob("*.py") and p.rglob("*.pyc"):
                    print('[Done] ',p)
                # 非py文件
                if p.is_file() and p.suffix not in [".py", ".pyc"] and p.name not in exclude_list:
                    print('[Copy] ',p)
                    self.copy_file(p, root_dir, target_dir)
                # 不需要加密py文件
                if p.is_file() and p.name in exclude_list:
                    print('[Skip] ',p)
                    self.copy_file(p, root_dir, target_dir)
        # 拷贝根目录其他文件
        for p in Path('.').iterdir():
            # 其他文件
            if p.is_file() and p.suffix not in [".py", ".pyc"] and p.name not in exclude_list:
                print('[Copy] ',p)
                self.copy_file(p, root_dir, target_dir)
            # 不需要加密py文件
            if p.is_file() and p.name in exclude_list:
                print('[Skip] ',p)
                self.copy_file(p, root_dir, target_dir)
        print("copy end")

    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


def find_scrips():
    scrips_list = []

    for p in Path('.').iterdir():
        if p.is_file() and (p.name not in exclude_list):
            if p.suffix in [".py"] and (not p.name.startswith(".")):
                scrips_list.append(p.name)
    print("scrips_list",scrips_list)
    print("exclude_list",exclude_list)
    return scrips_list


if __name__ == "__main__":
    my_project_name = "sqless"
    my_build_dir = "build"
    my_clang = "gcc "

    print("===============start=================")
    exclude_list = ["encrypt.py", "app.py", "setup.py"]
    exclude_dir = ["init", "logs", "quickstart", "saas", "save", "scripts", "test"]
    os.environ["CC"]=my_clang
    my_packages = find_packages()
    print("packages:",my_packages)

    ext=[]
    #找到所有的package
    for module in my_packages:
        module = module.replace(".","/")
        #print(module)
        ext.append(Extension(module + ".*", [module + "/*.py"]))
    #找到根目录下的脚本
    ext.extend(find_scrips())
    print("Extension:",ext)

    setup(
        name=my_project_name,
        ext_modules=cythonize(
            ext,
            build_dir=my_build_dir,
            language_level="3",
            compiler_directives=dict(
                always_allow_keywords=True
            )),
        cmdclass=dict(
            build_ext=MyBuildExt
        ),
        packages=[]
    )
    print("===============end=================")