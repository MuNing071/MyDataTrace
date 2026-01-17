# MyDataTrace - 时光数绘轨迹图

一个交互式的数据分析与可视化工具，用于记录和展示个人成长轨迹。

## 功能特点

- **📅 灵活的时间配置**：支持季度、月度、年度等多种时间粒度
- **📋 自定义问题设置**：可根据个人需求添加、修改、删除回顾问题
- **📝 便捷的数据录入**：直观的评分和说明录入界面
- **🎨 精美的可视化图表**：自动生成美观的轨迹图，支持自定义配色
- **📷 一键导出图片**：支持JPG和PNG格式导出

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run app.py
```

### 使用流程

1. **设置时间范围**：选择要回顾的开始和结束时间，以及时间粒度
2. **配置问题**：添加或修改你想要回顾的问题
3. **录入数据**：为每个问题在不同时间点进行评分和添加说明
4. **生成图表**：一键生成并查看你的成长轨迹图
5. **导出图片**：保存生成的图表用于分享或记录

## 项目结构

```
image-generator/
├── app.py              # 主应用文件
├── requirements.txt    # 依赖列表
├── static/             # 静态资源目录
├── tests/              # 测试文件目录
└── README.md           # 项目说明文档
```

## 技术栈

- **Python**：主要开发语言
- **Streamlit**：Web应用框架
- **Matplotlib**：数据可视化库
- **NumPy**：数值计算库
- **Pandas**：数据分析库

## 如何贡献

欢迎提交Issue和Pull Request来帮助改进项目！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目地址：[https://github.com/MuNing071/image-generator](https://github.com/MuNing071/image-generator)
- 作者：小红书 [@沐宁](https://www.xiaohongshu.com/user/profile/5a05b24ce8ac2b75beec5026)

---

用数据当画笔，绘出独属于你的时光轨迹！✨