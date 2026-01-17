import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import io

# 设置页面配置
st.set_page_config(
    page_title="时光数绘轨迹图 MyDataTrace",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态 
if 'time_config' not in st.session_state:
    st.session_state.time_config = {
        'start_date': datetime(2025, 1, 1),
        'end_date': datetime(2025, 12, 31),
        'time_granularity': '季度'
    }

# 默认题项配置（精简版）
default_items = [
    '我的身体有多健康？',               # 身心休憩
    '我有多少自在闲暇？',               # 身心休憩
    '我的内心有多安宁平和？' ,           # 身心休憩
    '我感到多少爱与被爱？',             # 情感与善意
    '我做了多少满意的善行？',           # 情感与善意
    '我体验了丰富的风景和故事？',       # 体验与探索
    '我有多少自我觉察、理解和同情？',    # 自我状态
    '我增进了多少成长和智慧？',        # 自我状态
]

# 默认配色方案（精简版）
default_colors = [
    '#66BB6A',  # 我增进了多少成长和智慧？ - 鲜草绿
    '#FFA000',  # 我有多少自我觉察、理解和同情？ - 亮橙黄
    '#F06292',  # 我感到多少爱与被爱？ - 亮粉
    '#BA68C8',  # 我做了多少满意的善行？ - 亮紫
    '#26C6DA',  # 我体验了丰富的风景和故事？ - 亮青蓝
    '#1DE9B6',  # 我的身体有多健康？ - 亮青柠绿
    '#4DD0E1',  # 我有多少自在闲暇？ - 亮浅蓝
    '#29B6F6'   # 我的内心有多安宁平和？ - 亮天蓝
]

if 'config_items' not in st.session_state:
    st.session_state.config_items = default_items

if 'style_config' not in st.session_state:
    st.session_state.style_config = {
        'ncol': 2,
        'nrow': 6,  # 12个题项，2列6行
        'color_palette': '默认配色',
        'custom_colors': default_colors,
        'font_family': 'STKaiti',
        'background_color': '#FFFFFF',
        'margin': 10
    }

if 'data' not in st.session_state:
    st.session_state.data = {}
    for item in st.session_state.config_items:
        st.session_state.data[item] = {}

# 配置中心模块
# 时间配置函数
def generate_time_points(start_date, end_date, granularity):
    """生成时间点列表"""
    time_points = []
    
    if granularity == '季度':
        # 生成季度时间点
        start_year = start_date.year
        start_quarter = (start_date.month - 1) // 3 + 1
        end_year = end_date.year
        end_quarter = (end_date.month - 1) // 3 + 1
        
        current_year = start_year
        current_quarter = start_quarter
        
        while current_year < end_year or (current_year == end_year and current_quarter <= end_quarter):
            time_points.append(f"{current_year}Q{current_quarter}")
            current_quarter += 1
            if current_quarter > 4:
                current_quarter = 1
                current_year += 1
    
    elif granularity == '月份':
        # 生成月份时间点
        start_year = start_date.year
        start_month = start_date.month
        end_year = end_date.year
        end_month = end_date.month
        
        current_year = start_year
        current_month = start_month
        
        while current_year < end_year or (current_year == end_year and current_month <= end_month):
            time_points.append(f"{current_year}-{current_month:02d}")
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
    
    elif granularity == '年度':
        # 生成年度时间点
        for year in range(start_date.year, end_date.year + 1):
            time_points.append(f"{year}")
    
    return time_points

# 题项管理函数
def add_item():
    """添加题项"""
    new_item = f"题项{len(st.session_state.config_items) + 1}"
    st.session_state.config_items.append(new_item)
    # 初始化新题项的数据
    st.session_state.data[new_item] = {}
    # 更新已有时间点的数据结构
    update_data_structure()

def delete_item(index):
    """删除题项"""
    item = st.session_state.config_items.pop(index)
    if item in st.session_state.data:
        del st.session_state.data[item]

def update_item_name(index, new_name):
    """更新题项名称"""
    old_name = st.session_state.config_items[index]
    st.session_state.config_items[index] = new_name
    # 更新数据字典中的键
    if old_name in st.session_state.data:
        st.session_state.data[new_name] = st.session_state.data.pop(old_name)

# 数据结构更新函数
def update_data_structure():
    """更新数据结构，确保与当前配置一致"""
    time_points = generate_time_points(
        st.session_state.time_config['start_date'],
        st.session_state.time_config['end_date'],
        st.session_state.time_config['time_granularity']
    )
    
    # 遍历所有题项，确保每个题项都有所有时间点的数据
    for item in st.session_state.config_items:
        if item not in st.session_state.data:
            st.session_state.data[item] = {}
        
        # 遍历所有时间点，确保每个时间点都有默认数据
        for tp in time_points:
            if tp not in st.session_state.data[item]:
                st.session_state.data[item][tp] = {'得分': 70.0, '说明': ''}

# 样式配置函数
def generate_color_palette(n_items, palette_type='默认配色'):
    """生成配色方案"""
    default_palette = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57',
        '#FF9FF3', '#54A0FF', '#5F27CD', '#FF9F43', '#1DD1A1'
    ]
    
    if palette_type == '默认配色':
        # 循环使用默认调色板
        return [default_palette[i % len(default_palette)] for i in range(n_items)]
    else:
        # 使用自定义颜色
        custom_colors = st.session_state.style_config.get('custom_colors', [])
        if len(custom_colors) >= n_items:
            return custom_colors[:n_items]
        else:
            # 自定义颜色不足时，补充默认颜色
            return custom_colors + [default_palette[i % len(default_palette)] for i in range(len(custom_colors), n_items)]

# 主应用布局
def main():
    # 标题
    st.title("🎨 MyDataTrace - 时光数绘轨迹图")
    
        # 使用指引
    with st.expander("📖如何使用", expanded=True):
        st.markdown("""
        🖌️用数据当画笔，绘出独属于你的时光轨迹
        1. **📅 选时间范围**：选择要总结的周期（支持季度/月度/年度），默认25年每个季度
        2. **📋 写下想要回顾的问题**：对你的回顾最重要的几个问题。可以修改、删除默认问题，也能点击「➕ 添加问题」新增（建议4~12个）
        3. **📝 开始回顾和评分**：给每个问题打0-100分，还能加说明（建议30字内）
        4. **📷 最后，一键生成时光数绘轨迹图**：数据填完后，直接点「🚀 立即生成并显示」即可

        ✋️ 更多内容可关注 小红书 [@沐宁](https://www.xiaohongshu.com/user/profile/5a05b24ce8ac2b75beec5026)
        """)
    
    # 时间配置
    st.subheader("📅 选时间范围")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start_date = st.date_input(
            "开始时间",
            value=st.session_state.time_config['start_date'],
            key="start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "结束时间",
            value=st.session_state.time_config['end_date'],
            key="end_date"
        )
    
    with col3:
        time_granularity = st.selectbox(
            "时间粒度",
            options=["季度", "月份", "年度"],
            index=["季度", "月份", "年度"].index(st.session_state.time_config['time_granularity']),
            key="time_granularity"
        )
    
    # 更新时间配置
    st.session_state.time_config['start_date'] = start_date
    st.session_state.time_config['end_date'] = end_date
    st.session_state.time_config['time_granularity'] = time_granularity
    
    # 生成并显示时间点
    time_points = generate_time_points(start_date, end_date, time_granularity)
    st.info(f"生成的时间点: {', '.join(time_points)}")
    
    # 题项配置
    st.subheader("📋 写下想要回顾的问题")
    
    # 显示当前题项列表
    st.info(f"💡 可以根据自己的价值观排序来写，我最看重哪些方面呢？我会如何采访自己呢？\n下面提供了{len(st.session_state.config_items)}个默认问题，您可以直接修改或删除它们，也可以添加新问题。建议4~12个")
    
    # 使用直接输入框和删除按钮布局，方便批量管理
    for i, item in enumerate(st.session_state.config_items):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            new_name = st.text_input(
                f"问题{i+1}",
                value=item,
                key=f"item_{i}"
            )
            if new_name != item:
                update_item_name(i, new_name)
        
        with col2:
            if st.button(
                "🗑️",
                key=f"delete_{i}",
                type="primary",
                use_container_width=True
            ):
                delete_item(i)
                st.rerun()
    
    # 添加新题项 - 整行按钮
    if st.button("➕ 添加问题", type="secondary", use_container_width=True):
        add_item()
        st.rerun()
    
    # 更新数据结构
    update_data_structure()
    
    # 数据录入
    st.header("📝 开始回顾和评分")
    
    # 显示时间点
    time_points = generate_time_points(
        st.session_state.time_config['start_date'],
        st.session_state.time_config['end_date'],
        st.session_state.time_config['time_granularity']
    )
    
    if not time_points:
        st.warning("请先配置时间点")
    else:
        # 数据录入提示
        st.info(f"✨画下你的成长曲线，每一笔都是时光的礼物\n\n📋 共 {len(time_points)} 个时间点×{len(st.session_state.config_items)} 个问题")
        
        # 按时间点划分模块
        for tp in time_points:
            with st.expander(f"{tp}", expanded=False):
                # 时间点模块标题
                st.markdown(f"### {tp}")
                
                # 每个时间点下显示所有题项
                for item in st.session_state.config_items:
                    with st.container():
                        # 题项标题 - 加大字号
                        st.markdown(f"<h4 style='font-size: 20px;'>{item}</h4>", unsafe_allow_html=True)
                        
                        # 获取当前值作为基准
                        current_value = st.session_state.data[item][tp]['得分']
                        
                        # 只保留得分输入框
                        input_score = st.number_input(
                            label="得分输入",
                            min_value=0.0,
                            max_value=100.0,
                            step=0.1,
                            value=current_value,
                            key=f"{item}_{tp}_input"
                        )
                        
                        # 更新得分
                        if input_score != current_value:
                            st.session_state.data[item][tp]['得分'] = input_score
                        
                        # 添加横柱状图实时显示当前得分
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.progress(int(st.session_state.data[item][tp]['得分']), text=f"{st.session_state.data[item][tp]['得分']:.1f}/100")
                        with col2:
                            st.text(f"{st.session_state.data[item][tp]['得分']:.1f}")
                        
                        # 说明录入区
                        note = st.text_area(
                            label="说明",
                            value=st.session_state.data[item][tp]['说明'],
                            key=f"{item}_{tp}_note",
                            placeholder="为什么是这个得分呢？可以回顾相册、朋友圈、聊天记录，写写发生的事的关键词",
                            height=80,
                            help="建议30个字内，会在生成的图表中每5个字符换行"
                        )
                        st.session_state.data[item][tp]['说明'] = note
                        
                        # 分隔线
                        st.markdown("---")

    # 在数据录入页面添加生成图片按钮
    st.subheader("📷 最后，一键生成时光数绘轨迹图")
    
    output_format = st.selectbox(
        "输出格式",
        options=["jpg", "png"],  # 默认jpg格式
        key="quick_output_format"
    )
    
    # 使用默认参数
    dpi = 300
    
    # 快速生成图片按钮
    if st.button("🚀 一键生成", type="primary", use_container_width=True):
        # 生成图片
        time_points = generate_time_points(
            st.session_state.time_config['start_date'],
            st.session_state.time_config['end_date'],
            st.session_state.time_config['time_granularity']
        )
        
        items = st.session_state.config_items
        data = st.session_state.data
        
        # 生成配色方案
        colors = generate_color_palette(len(items), st.session_state.style_config['color_palette'])
        item_colors = dict(zip(items, colors))
        
        # 调用图片生成函数
        buf = generate_chart(data, items, time_points, item_colors, output_format, dpi)
        
        # 在页面上显示生成的图片
        st.image(buf, caption="""长按图片或右键保存，可调整后再次生成
        ✋️ 更多内容可关注 小红书 [@沐宁](https://www.xiaohongshu.com/user/profile/5a05b24ce8ac2b75beec5026)""", use_container_width=True)
        # 提示用户保存图片
        st.warning("⚠️生成后记得保存内容和文本哦，网页刷新后可能就没有啦")

    # 样式配置 - 移到最后
    st.divider()
    st.subheader("🎨 布局和颜色配置")
    
    # 高级选项折叠面板
    with st.expander("高级样式选项", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            ncol = st.number_input(
                "列数 (ncol)",
                min_value=1,
                max_value=4,
                value=st.session_state.style_config['ncol'],
                key="ncol"
            )
            
            nrow = st.number_input(
                "行数 (nrow)",
                min_value=1,
                max_value=6,
                value=st.session_state.style_config['nrow'],
                key="nrow"
            )
        
        with col2:
            color_palette = st.selectbox(
                "调色板",
                options=["默认配色", "自定义配色"],
                index=["默认配色", "自定义配色"].index(st.session_state.style_config['color_palette']),
                key="color_palette"
            )
            
            # 自定义颜色输入
            if color_palette == "自定义配色":
                custom_colors = []
                # 确保custom_colors列表长度足够
                current_custom_colors = st.session_state.style_config.get('custom_colors', [])
                for i, item in enumerate(st.session_state.config_items):
                    # 使用现有颜色作为默认值，如果没有则使用默认颜色
                    default_color = current_custom_colors[i] if i < len(current_custom_colors) else '#4FC3F7'
                    color = st.color_picker(
                        f"{item}",
                        value=default_color,
                        key=f"custom_color_{i}"
                    )
                    custom_colors.append(color)
                st.session_state.style_config['custom_colors'] = custom_colors
        
        # 更新样式配置
        st.session_state.style_config['ncol'] = int(ncol)
        st.session_state.style_config['nrow'] = int(nrow)
        st.session_state.style_config['color_palette'] = color_palette

# 图片生成函数
def generate_chart(data, items, time_points, item_colors, output_format="png", dpi=400):
    """
    从Streamlit会话状态获取动态数据生成可视化图表
    :param data: 字典，格式{题项: {时间点: {得分: float, 说明: str}}}
    :param items: 列表，动态配置的题项列表
    :param time_points: 列表，动态配置的时间点列表（如['25年Q1', '25年Q2']）
    :param item_colors: 字典，题项对应的颜色值（从配置模块获取）
    :param output_format: 输出格式，png/jpg
    :param dpi: 图片分辨率
    :return: 生成的图片对象（供Streamlit下载）
    """
    # 明确设置中文字体，使用指定的字体文件
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['text.usetex'] = False  # 禁用LaTeX，避免字体冲突

    # 显式创建字体属性对象，使用指定的字体文件
    from matplotlib.font_manager import FontProperties, fontManager
    import os
    
    # 指定字体文件路径（使用相对路径，确保在GitHub和Streamlit远程运行时可用）
    font_path = os.path.join(os.path.dirname(__file__), 'STKAITI.TTF')
    # 检查字体文件是否存在
    if os.path.exists(font_path):
        # 添加字体到字体管理器
        fontManager.addfont(font_path)
        # 创建字体属性对象
        font_props = FontProperties(fname=font_path)
    else:
        # 如果字体文件不存在，使用默认字体列表
        font_props = FontProperties(family=['STKaiti', 'SimHei', 'SimSun', 'Microsoft YaHei', 'SimKai', 'FangSong'])
    
    # 设置全局字体
    plt.rcParams['font.family'] = ['STKaiti']
    plt.rcParams['font.sans-serif'] = ['STKaiti']

    # 计算子图布局 - 双列布局，适合手机观看
    n_items = len(items)
    n_cols = 2
    n_rows = (n_items + 1) // n_cols  # 自动计算行数适配题项数量

    # 创建画布 - 紧凑布局，适配手机尺寸
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(8, 3.5 * n_rows), sharex=False, sharey=True)
    # 处理只有一个子图的情况
    if n_rows == 1 and n_cols == 1:
        axes = np.array([axes])  # 转为一维数组
    else:
        axes = axes.flatten()  # 转为一维数组，方便索引

    # 设置整体风格
    fig.patch.set_facecolor('#FFFFFF')  # 画布背景色纯白

    # 绘制每个子图（适配动态题项）
    for i, item in enumerate(items):
        ax = axes[i]
        
        # 设置子图背景色
        ax.set_facecolor('#FFFFFF')
        
        # 从动态数据中提取当前题项的得分和说明
        scores = [data[item][tp]['得分'] for tp in time_points]
        notes = [data[item][tp]['说明'] if data[item][tp]['说明'] else "" for tp in time_points]
        
        # 获取当前题项的配置颜色
        item_color = item_colors.get(item, '#4FC3F7')  # 默认天蓝
        
        # 绘制背景阴影 - 低透明度，提升层次感
        ax.fill_between(range(len(time_points)), scores, alpha=0.1, color=item_color, zorder=1)
        
        # 绘制折线图
        line, = ax.plot(range(len(time_points)), scores, linewidth=2, color=item_color, zorder=2, 
                       marker='o', markersize=8, linestyle='-', alpha=0.9, 
                       markerfacecolor=item_color, markeredgecolor='white', markeredgewidth=2)
        
        # 添加数据点、得分和说明（适配动态时间点）
        for j, (x, y, note) in enumerate(zip(range(len(time_points)), scores, notes)):
            # 数据点光晕效果
            ax.scatter(x, y, s=150, color=item_color, alpha=0.2, zorder=3, edgecolor='none')
            # 得分标注
            ax.text(x, y + 0.5, f'{int(y)}', ha='center', va='bottom', fontsize=10, fontweight='bold', 
                    color=item_color, zorder=5, bbox=dict(facecolor='white', alpha=0.7, 
                    edgecolor=item_color, boxstyle='round,pad=0.25', linewidth=1), 
                    fontproperties=font_props)
            
            # 说明标注：5字符换行，空说明不显示
            if note:
                wrapped_note = '\n'.join([note[k:k+5] for k in range(0, len(note), 5)])
                note_y = y - 0.5  # 固定在数据点下方
                ax.text(x, note_y, wrapped_note, ha='center', va='top', 
                        fontsize=11, color='#555555', alpha=0.9, zorder=6, rotation=0, 
                        bbox=dict(facecolor='white', alpha=0.4, edgecolor=item_color, 
                                  boxstyle='round,pad=0.2', linewidth=1),
                        fontproperties=font_props)
        
        # 设置子图标题（题项名称）
        ax.set_title(item, fontsize=18, fontweight='bold', color=item_color, pad=15)
        
        # 设置Y轴范围（适配0-100分得分范围）
        ax.set_ylim(0, 110)
        
        # 设置网格线 - 仅保留Y轴主要网格
        ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.2, color='#E0E0E0', zorder=0)
        ax.grid(False, which='minor')
        ax.minorticks_off()
        
        # 设置X轴刻度（仅第一行显示时间标签）
        ax.xaxis.tick_top()
        if i < n_cols:  # 第一行图显示时间标签
            ax.set_xticks(range(len(time_points)))
            ax.set_xticklabels(time_points, fontsize=8, color=item_color, fontweight='bold', 
                              fontproperties=font_props, rotation=20)
        else:
            ax.set_xticks([])
            ax.set_xticklabels([])
        ax.xaxis.set_label_position('top')
        
        # 设置Y轴刻度
        ax.set_yticks(range(0, 120, 20))
        ax.set_yticklabels([f'{i}' for i in range(0, 120, 20)], fontsize=8, color='#555555', 
                         fontproperties=font_props, fontweight='500', alpha=0.4)
        
        # 添加边框线
        for spine in ax.spines.values():
            spine.set_color('#E0E0E0')
            spine.set_linewidth(1.5)
        # 底部边框用题项专属色加粗
        ax.spines['bottom'].set_color(item_color)
        ax.spines['bottom'].set_linewidth(2)
    
    # 隐藏未使用的子图（当题项数量为奇数时）
    for i in range(n_items, len(axes)):
        axes[i].set_visible(False)
    
    # 调整子图间距，提升紧凑性
    plt.tight_layout()
    
    # 保存图片到Streamlit缓存（避免本地文件依赖）
    buf = io.BytesIO()
    if output_format.lower() == "jpg":
        # 使用pil_kwargs传递quality参数，兼容不同Matplotlib版本
        plt.savefig(buf, format='jpg', dpi=dpi, bbox_inches='tight')
    else:
        plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    
    # 关闭图片，释放资源
    plt.close()
    
    return buf

# 运行主应用
if __name__ == "__main__":
    main()
