import click
from phcli.ph_auto_setup.jupyter_operation.ph_jupyter_operation import PhJupyterOperation

@click.command('jupyter_operation', short_help='对ec2-jupyter的操作')
@click.option("-n", "--name",
              prompt="The jupyter name is",
              help="The jupyter name.")
@click.option("-o", "--operation",
              prompt="The operation on emr is",
              type=click.Choice(["create", "delete"]),
              help="The operation on emr.")
def jupyter_operation(**kwargs):
    """
    初始化c9 hadoop和spark的conf文件
    """
    try:

        PhJupyterOperation(**kwargs).choice_operation()
    except Exception as e:
        click.secho("操作失败: " + str(e), fg='red', blink=True, bold=True)
    else:
        click.secho("操作完成", fg='green', blink=True, bold=True)


