import argparse
from termcolor import colored
import requests

# 设置默认请求超时时间为10秒
TIMEOUT = 10

print()
print("START CHECK ...")
print()

# 状态码解释
status_codes_explanation = {
    200: "可访问",
    301: "永久重定向",
    302: "临时重定向",
    400: "请求错误",
    401: "未授权",
    403: "无权限",
    404: "未找到",
    500: "服务器错误",
    503: "服务不可用",
}

# 状态码颜色
status_colors = {
    200: "green",
    301: "blue",
    302: "blue",
    400: "yellow",
    401: "yellow",
    403: "yellow",
    404: "yellow",
    500: "red",
    503: "red",
}

def check_url(url, output_file=None):
    """检测单个网站的可访问性，并根据情况打印和保存"""
    try:
        # 进行GET请求
        response = requests.get(url, timeout=TIMEOUT)
        status_code = response.status_code
        explanation = status_codes_explanation.get(status_code, "未知状态码")
        color = status_colors.get(status_code, "magenta")  # 对于未知状态码，使用紫色打印
        output = colored(f"[{status_code}] {explanation} {url}", color)
        print(output)

        # 如果状态码指示成功并且指定了输出文件，则将URL保存到该文件
        if status_code == 200 and output_file is not None:
            with open(output_file, "a") as file:
                file.write(url + "\n")

    except requests.exceptions.Timeout:
        print(colored(f"[Error] 请求超时 {url} ", "red"))
    except requests.exceptions.ConnectionError:
        print(colored(f"[Error] 连接错误 {url} ", "red"))
    except requests.exceptions.TooManyRedirects:
        print(colored(f"[Error] 重定向过多 {url} ", "red"))
    except requests.exceptions.RequestException as e:
        print(colored(f"[Error] 请求异常 {url} [异常消息] {e}", "red"))

def process_urls(urls, output_file=None):
    """处理URL列表"""
    for url in urls:
        check_url(url, output_file)

def main():
    parser = argparse.ArgumentParser(description="批量检测网站可访问性的脚本")
    parser.add_argument("-l", "--list", type=str, help="包含网站列表的文件")
    parser.add_argument("-u", "--url", type=str, nargs='+', help="一个或多个网站URL")
    parser.add_argument("-o", "--output", type=str, help="将可访问的网站保存到文件")

    args = parser.parse_args()

    # 如果指定了列表文件
    if args.list:
        try:
            with open(args.list, "r") as file:
                urls = [line.strip() for line in file if line.strip()]
                process_urls(urls, args.output)
        except FileNotFoundError:
            print(colored(f"文件 {args.list} 未找到。", "red"))

    # 如果通过命令行参数指定了URL
    if args.url:
        process_urls(args.url, args.output)


if __name__ == "__main__":
    main()
