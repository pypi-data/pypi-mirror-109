import click
from phcli.ph_auto_setup.emr_operation.__main__ import emr_operation
from phcli.ph_auto_setup.jupyter_operation.__main__ import jupyter_operation

@click.group("auto_setup", short_help='自动化操作EMR集群，EC2实例系列命令')
def main():
    """
    本脚本用于执行自动化操作EMR集群，EC2实例系列命令
    """
    pass


main.add_command(emr_operation)
main.add_command(jupyter_operation)


if __name__ == '__main__':
    main()