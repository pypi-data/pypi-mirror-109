from wuling.tool.http_parser import parse_http_file

from wuling.tool.api_prj_init import  init_prj


def generate_test_case(txt_file, case_path):
    parse_http_file(txt_file, case_path)

def generate_api_prj(git_addr):
    # git_addr = 'https://gitee.com/guoyasoft/wuling-api-test-init.git'
    init_prj(git_addr)