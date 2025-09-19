from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Python代码执行工具参数模型
class PythonCodeInput(BaseModel):
    py_code: str = Field(description="合法的Python代码字符串")


@tool(args_schema=PythonCodeInput)
def python_inter(py_code):
    """
    执行Python代码并返回结果
    :param py_code: Python代码字符串
    :return: 执行结果
    """
    import matplotlib
    matplotlib.use('Agg')
    g = globals()
    try:
        return str(eval(py_code, g))
    except Exception as e:
        global_vars_before = set(g.keys())
        try:
            exec(py_code, g)
        except Exception as e:
            return f"代码执行时报错{e}"
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        if new_vars:
            result = {var: g[var] for var in new_vars}
            return str(result)
        else:
            return "代码已顺利执行"