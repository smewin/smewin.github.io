#!/usr/bin/env python3

import subprocess
import random
import re
import os
import sys
import time

class SimpleExpressionTester:
    def __init__(self, interpreter_path="./build/riscv32-nemu-interpreter"):
        self.interpreter_path = interpreter_path
        self.test_count = 0
        self.pass_count = 0
        self.fail_count = 0
        self.failed_tests = []
        
    def generate_simple_expression(self, depth=0):
        """生成只包含+,-,*,/,括号和数字的简单表达式"""
        operators = ['+', '-', '*', '/']
        
        # 50%概率生成数字，50%概率生成更复杂的表达式
        if depth > 3 or (depth > 0 and random.random() < 0.5):
            # 生成数字（十进制或十六进制）
            if random.random() < 0.3:  # 30%概率生成十六进制数
                return f"0x{random.randint(0, 255):x}"
            else:
                return str(random.randint(1, 100))
        
        # 生成带运算符的表达式
        left = self.generate_simple_expression(depth + 1)
        right = self.generate_simple_expression(depth + 1)
        op = random.choice(operators)
        
        # 30%概率添加括号
        if random.random() < 0.3:
            return f"({left} {op} {right})"
        else:
            return f"{left} {op} {right}"
    
    def compute_expected_result(self, expression):
        """使用Python计算表达式的预期结果，模拟整数除法行为"""
        try:
            # 替换十六进制数
            def hex_replace(match):
                return str(int(match.group(0), 16))
                
            # 处理十六进制数字
            cleaned_expr = re.sub(r'0x[0-9a-fA-F]+', hex_replace, expression)
            
            # 使用AST解析和整数除法评估
            import ast
            import operator
            
            # 创建自定义求值器，使用整数除法
            class IntegerEvaluator(ast.NodeVisitor):
                def visit_BinOp(self, node):
                    left = self.visit(node.left)
                    right = self.visit(node.right)
                    
                    if isinstance(node.op, ast.Add):
                        return left + right
                    elif isinstance(node.op, ast.Sub):
                        return left - right
                    elif isinstance(node.op, ast.Mult):
                        return left * right
                    elif isinstance(node.op, ast.Div):
                        # 整数除法（向零取整）
                        if right == 0:
                            raise ZeroDivisionError("division by zero")
                        result = left / right
                        # 向零取整（与大多数编程语言一致）
                        return int(result) if result >= 0 else -int(-result)
                    elif isinstance(node.op, ast.Mod):
                        if right == 0:
                            raise ZeroDivisionError("division by zero")
                        return left % right
                    else:
                        raise ValueError(f"Unsupported operator: {type(node.op)}")
                
                def visit_Num(self, node):
                    return node.n
                
                def visit_UnaryOp(self, node):
                    operand = self.visit(node.operand)
                    if isinstance(node.op, ast.USub):
                        return -operand
                    elif isinstance(node.op, ast.UAdd):
                        return operand
                    else:
                        raise ValueError(f"Unsupported unary operator: {type(node.op)}")
                
                def visit_Expr(self, node):
                    return self.visit(node.value)
            
            # 解析和求值表达式
            tree = ast.parse(cleaned_expr, mode='eval')
            evaluator = IntegerEvaluator()
            result = evaluator.visit(tree.body)
            
            # 返回8位十六进制格式（带前导零）
            return f"{result & 0xFFFFFFFF:08x}"  # 限制为32位并添加前导零
            
        except ZeroDivisionError:
            return "zero_division"
        except Exception as e:
            return f"error: {str(e)}"
    
    def run_interpreter(self, expression):
        """运行interpreter程序并获取完整输出"""
        try:
            # 启动interpreter进程
            process = subprocess.Popen(
                [self.interpreter_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # 将stderr合并到stdout
                text=True,
                bufsize=1
            )
            
            # 发送表达式命令
            command = f"p {expression}\n"
            process.stdin.write(command)
            process.stdin.flush()
            
            # 给interpreter一些时间处理
            time.sleep(0.1)
            
            # 发送退出命令
            quit_command = "q\n"
            process.stdin.write(quit_command)
            process.stdin.flush()
            
            # 读取所有输出
            output = ""
            try:
                # 尝试读取所有输出
                while True:
                    line = process.stdout.readline()
                    if not line:
                        break
                    output += line
            except Exception:
                pass
            
            # 等待进程结束
            process.wait(timeout=2)
            
            return output
        except subprocess.TimeoutExpired:
            process.terminate()
            return output + "\n[进程超时被终止]"
        except Exception as e:
            return f"[运行interpreter时出错: {str(e)}]"
    
    def extract_result(self, output):
        """从interpreter输出中提取结果 - 专门针对你的输出格式"""
        # 查找 "Result = " 开头的行
        lines = output.split('\n')
        for line in lines:
            if line.startswith("Result = "):
                # 提取十六进制部分 (0x...)
                hex_match = re.search(r'Result\s*=\s*0x([0-9a-f]+)', line, re.IGNORECASE)
                if hex_match:
                    hex_value = hex_match.group(1).lower()
                    # 确保是8位十六进制（如果有前导零也保留）
                    return hex_value
        return None
    
    def run_test(self, num_tests=50):
        """运行多个测试"""
        print(f"开始运行 {num_tests} 个简单表达式测试...")
        print(f"Interpreter路径: {self.interpreter_path}")
        print("-" * 60)
        
        for i in range(num_tests):
            # 生成简单表达式
            expression = self.generate_simple_expression()
            
            # 计算预期结果（8位十六进制格式）
            expected_hex = self.compute_expected_result(expression)
            
            # 跳过有错误的表达式（如除零）
            if expected_hex.startswith("error") or expected_hex == "zero_division":
                continue
            
            # 运行interpreter
            output = self.run_interpreter(expression)
            
            # 提取实际结果
            actual_result = self.extract_result(output)
            
            # 检查结果（现在考虑前导零）
            if actual_result and actual_result == expected_hex:
                self.pass_count += 1
                print(f"测试 {i+1}: 通过 ✓ (表达式: {expression})")
            else:
                self.fail_count += 1
                self.failed_tests.append({
                    'expression': expression,
                    'expected': expected_hex,
                    'actual': actual_result,
                    'output': output
                })
                print(f"测试 {i+1}: 失败 ✗ (表达式: {expression})")
            
            self.test_count += 1
        
        # 打印摘要
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("测试摘要")
        print("=" * 60)
        print(f"总测试数: {self.test_count}")
        print(f"通过数: {self.pass_count}")
        print(f"失败数: {self.fail_count}")
        if self.test_count > 0:
            print(f"通过率: {self.pass_count / self.test_count * 100:.2f}%")
        
        # 打印失败的测试
        if self.failed_tests:
            print(f"\n失败的测试 ({len(self.failed_tests)}):")
            for i, test in enumerate(self.failed_tests):
                print(f"{i+1}. 表达式: {test['expression']}")
                print(f"   预期: {test['expected']}")
                print(f"   实际: {test['actual']}")
                # 显示包含结果的行
                for line in test['output'].split('\n'):
                    if 'Result =' in line:
                        print(f"   输出行: {line}")
                        break
                print()

def main():
    # 检查interpreter是否存在
    interpreter_path = "./build/riscv32-nemu-interpreter"
    if not os.path.exists(interpreter_path):
        print(f"错误: 未找到interpreter程序 {interpreter_path}")
        print("请确保:")
        print("1. 已经在项目根目录下运行此脚本")
        print("2. 已经成功编译了interpreter")
        sys.exit(1)
    
    # 创建测试器并运行测试
    tester = SimpleExpressionTester(interpreter_path)
    tester.run_test(num_tests=30)  # 运行30个测试

if __name__ == "__main__":
    main()
