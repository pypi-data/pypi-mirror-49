import setuptools

# 需要将那些包导入
# packages = ["ML_platform.utils"]

PY_MODULES = ["ML_platform.utils"]

# # 导入静态文件
# file_data = [
#     ("smart/static", ["smart/static/icon.svg", "smart/static/config.json"]),
# ]

# 第三方依赖
requires = [
    "numpy"
]

setuptools.setup(
    name="hss_ml",  # 包名称
    version="1.0.1",  # 包版本
    description="hss的机器学习包",  # 包详细描述
    author="hss",  # 作者名称
    author_email="1046525663@qq.com",  # 作者邮箱
    # packages=packages,    # 项目需要的包
    py_modules=PY_MODULES,
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
