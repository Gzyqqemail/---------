import os
import py_compile
import shutil
from pathlib import Path

def compile_python_files(source_dir, output_dir):
    """
    将源目录中的Python文件编译为Pyc文件，并保留目录结构
    
    参数:
    source_dir (str): 源Python文件所在目录
    output_dir (str): 编译后Pyc文件的输出目录
    """
    # 确保源目录存在
    if not os.path.exists(source_dir):
        print(f"错误: 源目录 '{source_dir}' 不存在")
        return
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历源目录中的所有文件和子目录
    for root, dirs, files in os.walk(source_dir):
        # 计算相对路径，用于在输出目录中创建相同的目录结构
        relative_path = os.path.relpath(root, source_dir)
        output_subdir = os.path.join(output_dir, relative_path)
        
        # 创建对应的输出子目录
        os.makedirs(output_subdir, exist_ok=True)
        
        # 处理每个文件
        for file in files:
            if file.endswith('.py'):
                # 源文件路径
                source_file = os.path.join(root, file)
                # 输出的pyc文件路径 (将.py替换为.pyc)
                pyc_file = os.path.join(output_subdir, file.replace('.py', '.pyc'))
                
                try:
                    # 编译Python文件
                    py_compile.compile(
                        source_file, 
                        cfile=pyc_file, 
                        doraise=True
                    )
                    print(f"已编译: {source_file} -> {pyc_file}")
                except Exception as e:
                    print(f"编译失败: {source_file} - 错误: {str(e)}")
            else:
                # 非Python文件，直接复制
                source_file = os.path.join(root, file)
                dest_file = os.path.join(output_subdir, file)
                shutil.copy2(source_file, dest_file)
                print(f"已复制: {source_file} -> {dest_file}")

if __name__ == "__main__":
    # 源目录：存放Python代码的目录
    SOURCE_DIR = "/media/gzy/移动硬盘/python_program/双色球抽奖/"
    
    # 输出目录：编译后的Pyc文件将存放在此目录
    OUTPUT_DIR = "/media/gzy/移动硬盘/python_program/python代码封装"
    
    # 执行编译
    compile_python_files(SOURCE_DIR, OUTPUT_DIR)
    
    print("\n编译完成!")
    print(f"Pyc文件已保存到: {OUTPUT_DIR}")    