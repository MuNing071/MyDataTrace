import sys
import os
from datetime import datetime
import io

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import generate_time_points, generate_color_palette, update_item_name, delete_item

# 测试时间生成函数
def test_generate_time_points():
    """测试时间点生成函数"""
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    # 测试季度生成
    quarterly_points = generate_time_points(start_date, end_date, '季度')
    assert quarterly_points == ['2025Q1', '2025Q2', '2025Q3', '2025Q4'], f"季度生成错误: {quarterly_points}"
    
    # 测试月份生成
    monthly_points = generate_time_points(start_date, datetime(2025, 3, 31), '月份')
    assert monthly_points == ['2025-01', '2025-02', '2025-03'], f"月份生成错误: {monthly_points}"
    
    # 测试年度生成
    yearly_points = generate_time_points(start_date, end_date, '年度')
    assert yearly_points == ['2025'], f"年度生成错误: {yearly_points}"
    
    # 测试跨年度季度生成
    cross_year_quarterly = generate_time_points(datetime(2024, 11, 1), datetime(2025, 2, 1), '季度')
    assert cross_year_quarterly == ['2024Q4', '2025Q1'], f"跨年度季度生成错误: {cross_year_quarterly}"
    
    # 测试跨年度月份生成
    cross_year_monthly = generate_time_points(datetime(2024, 11, 1), datetime(2025, 2, 1), '月份')
    assert cross_year_monthly == ['2024-11', '2024-12', '2025-01', '2025-02'], f"跨年度月份生成错误: {cross_year_monthly}"
    
    print("✓ 时间生成函数测试通过")

# 测试配色方案生成函数
def test_generate_color_palette():
    """测试配色方案生成函数"""
    # 测试默认配色
    default_colors = generate_color_palette(3, 'default')
    assert len(default_colors) == 3, f"默认配色数量错误: {len(default_colors)}"
    
    # 测试默认配色超过调色板数量的情况
    default_colors_more = generate_color_palette(15, 'default')
    assert len(default_colors_more) == 15, f"默认配色数量错误: {len(default_colors_more)}"
    
    # 测试自定义配色
    # 注意：这里需要模拟st.session_state，确保覆盖默认值
    import streamlit as st
    # 直接设置session_state，覆盖默认值
    st.session_state.style_config = {
        'custom_colors': ['#FF0000', '#00FF00', '#0000FF'],
        'color_palette': 'custom'
    }
    
    custom_colors = generate_color_palette(3, 'custom')
    assert len(custom_colors) == 3, f"自定义配色数量错误: {len(custom_colors)}"
    assert custom_colors == ['#FF0000', '#00FF00', '#0000FF'], f"自定义配色内容错误: {custom_colors}"
    
    # 测试自定义配色数量不足的情况
    custom_colors_less = generate_color_palette(5, 'custom')
    assert len(custom_colors_less) == 5, f"自定义配色数量不足时错误: {len(custom_colors_less)}"
    assert custom_colors_less[:3] == ['#FF0000', '#00FF00', '#0000FF'], f"自定义配色内容错误: {custom_colors_less}"
    
    print("✓ 配色方案生成函数测试通过")

# 测试更新题项名称函数
def test_update_item_name():
    """测试更新题项名称函数"""
    import streamlit as st
    
    # 模拟session state
    if 'config_items' not in st.session_state:
        st.session_state.config_items = ['题项1', '题项2', '题项3']
    if 'data' not in st.session_state:
        st.session_state.data = {
            '题项1': {'2025Q1': {'得分': 50.0, '备注': ''}},
            '题项2': {'2025Q1': {'得分': 60.0, '备注': ''}},
            '题项3': {'2025Q1': {'得分': 70.0, '备注': ''}}
        }
    
    # 更新题项名称
    update_item_name(0, '新题项1')
    assert st.session_state.config_items[0] == '新题项1', f"题项名称更新错误: {st.session_state.config_items[0]}"
    assert '新题项1' in st.session_state.data, f"数据字典中题项名称未更新"
    assert '题项1' not in st.session_state.data, f"旧题项名称未从数据字典中删除"
    
    print("✓ 更新题项名称函数测试通过")

# 测试删除题项函数
def test_delete_item():
    """测试删除题项函数"""
    import streamlit as st
    
    # 直接设置session_state，覆盖默认值
    st.session_state.config_items = ['题项1', '题项2', '题项3']
    st.session_state.data = {
        '题项1': {'2025Q1': {'得分': 50.0, '备注': ''}},
        '题项2': {'2025Q1': {'得分': 60.0, '备注': ''}},
        '题项3': {'2025Q1': {'得分': 70.0, '备注': ''}}
    }
    
    # 删除题项
    delete_item(1)
    assert len(st.session_state.config_items) == 2, f"题项数量删除错误: {len(st.session_state.config_items)}"
    assert '题项2' not in st.session_state.data, f"题项未从数据字典中删除"
    
    print("✓ 删除题项函数测试通过")

# 运行测试
if __name__ == "__main__":
    print("开始测试核心功能...")
    test_generate_time_points()
    test_generate_color_palette()
    test_update_item_name()
    test_delete_item()
    print("\n🎉 所有测试通过！")