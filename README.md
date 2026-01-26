# MyDataTrace - 时光数绘轨迹图

一个交互式的数据分析与可视化工具，用于记录和展示个人成长轨迹。

## 功能特点

- **📅 灵活的时间配置**：支持季度、月度、年度等多种时间粒度
- **📋 自定义问题设置**：可根据个人需求添加、修改、删除及排序回顾问题
- **📝 多样的数据录入**：支持页面直接评分及文字录入，或通过 **Excel 文件一键导入**
- **📊 完善的数据管理**：支持导出 Excel 模板及备份已有数据，防止刷新丢失
- **🎨 极简美学可视化**：自动生成美观的轨迹图，支持**自定义配色方案**及行列布局
- **📷 高清图表导出**：支持 JPG 和 PNG 格式导出，可自定义 DPI 获得高清大图

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

1. **设置时间范围**：选择要回顾的开始和结束时间，以及时间粒度。
2. **配置问题**：添加或修改你想要回顾的问题（建议 4-12 个）。
3. **数据录入**：
    - 直接在页面为每个时间点进行评分和添加说明。
    - 或者下载 Excel 模板，填写后一键上传导入。
4. **个性化配置**：在“布局和颜色配置”中调整列数、行数或选择自定义配色。
5. **生成与保存**：点击“立即生成”，预览满意后下载图片或 Excel 备份数据。

## 项目结构

```
MyDataTrace/
├── app.py              # 主应用文件 (Streamlit)
├── requirements.txt    # 依赖库列表
├── STKAITI.TTF         # 预置中文字体文件
├── LICENSE             # 开源许可证
└── README.md           # 项目说明文档
```

## 技术栈

- **Python**：主要开发语言
- **Streamlit**：Web 应用框架
- **Matplotlib**：数据可视化库
- **Pandas**：数据处理与 Excel 支持
- **Openpyxl**：Excel 引擎

## 如何贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目地址：[https://github.com/MuNing071/MyDataTrace](https://github.com/MuNing071/MyDataTrace)
- 作者：小红书 [@沐宁](https://www.xiaohongshu.com/user/profile/5a05b24ce8ac2b75beec5026)

---

用数据当画笔，绘出独属于你的时光轨迹！✨