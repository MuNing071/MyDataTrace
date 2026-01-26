
import unittest
import pandas as pd
import io
import sys
import os
from datetime import datetime

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock functions since we can't easily import app.py if it has st.set_page_config() at module level
# But looking at app.py, st.set_page_config is called at the top level.
# Ideally, we should refactor app.py to put the main logic in a function or check for __main__,
# but for now, we will duplicate the logic or import carefully if possible.
# Actually, looking at app.py again, the functions generate_time_points, etc. are importable,
# but st.* calls at top level will run on import.
# For unit testing the logic, I'll implement the logic in standalone functions in app.py first (or a utils file), 
# but per the plan I modify app.py directly.
# To test the logic without running the app, I'll rely on the fact that I'm going to implement
# the logic as pure functions in app.py: data_to_excel and excel_to_data.

# However, importing app.py will run the script and fail because streamlit context is missing.
# Strategy: I will write the test to verify the logic I AM ABOUT TO WRITE. 
# Since I can't import app.py easily without refactoring, I will create a temporary util to test the logic principles 
# or I will create the functions in a way that I can test them. 
# A better approach given the constraints: I'll trust the plan to add functions to app.py.
# But `app.py` has top-level execution code. I should probably move the top-level execution code to `if __name__ == "__main__":` 
# or wrapped in a `main()` function properly, but `st.set_page_config` must be the first command.

# Let's write the test assuming I can import the functions. 
# I will refactor app.py slightly to make it more testable if needed, or I will just simulate the logic in the test 
# if importing is impossible. 
# Wait, `tests/test_core_functions.py` imports `app`. Let's see how it handles it.
# It imports `generate_time_points`, etc. 
# This implies that `app.py` works on import?
# Ah, `st.set_page_config` might throw a warning or error if not run via `streamlit run`, 
# but `import streamlit` usually works.
# Let's try to import app in the test and see.

from app import generate_time_points

# If that works, I can define the new functions in app.py and import them.

def data_to_excel(data, items, time_points):
    """
    Simulated version of the function to be added to app.py for testing logic before implementation
    or to serve as the reference implementation for the test.
    """
    rows = []
    for tp in time_points:
        row = {'时间点': tp}
        for item in items:
            item_data = data.get(item, {}).get(tp, {})
            row[f"{item} - 得分"] = item_data.get('得分', 0.0)
            row[f"{item} - 说明"] = item_data.get('说明', '')
        rows.append(row)
    
    df = pd.DataFrame(rows)
    # Set '时间点' as first column
    cols = ['时间点'] + [c for c in df.columns if c != '时间点']
    df = df[cols]
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='数据')
    output.seek(0)
    return output

def excel_to_data(file_content, current_items):
    """
    Simulated version of the reading logic.
    """
    df = pd.read_excel(file_content)
    
    data = {}
    items = []
    
    # Identify items from columns
    # Expected format: "Item Name - 得分", "Item Name - 说明"
    columns = [c for c in df.columns if c != '时间点' and ' - ' in c]
    extracted_items = set()
    for col in columns:
        item_name = col.rsplit(' - ', 1)[0]
        extracted_items.add(item_name)
    
    # Use uploaded items or current items? 
    # Logic: Read all items present in the Excel file.
    items = list(extracted_items)
    
    # Initialize data structure
    for item in items:
        data[item] = {}
        
    # Iterate rows
    for index, row in df.iterrows():
        tp = str(row['时间点'])
        for item in items:
            score_col = f"{item} - 得分"
            note_col = f"{item} - 说明"
            
            score = row.get(score_col, 0.0)
            note = row.get(note_col, "")
            
            # Handle NaN for notes
            if pd.isna(note):
                note = ""
            # Handle NaN for scores
            if pd.isna(score):
                score = 0.0
                
            data[item][tp] = {
                '得分': float(score),
                '说明': str(note)
            }
            
    return data, items

class TestExcelUtils(unittest.TestCase):
    
    def setUp(self):
        self.items = ['A', 'B']
        self.time_points = ['2023Q1', '2023Q2']
        self.data = {
            'A': {
                '2023Q1': {'得分': 80.0, '说明': 'Good'},
                '2023Q2': {'得分': 85.0, '说明': 'Better'}
            },
            'B': {
                '2023Q1': {'得分': 60.0, '说明': 'Okay'},
                '2023Q2': {'得分': 65.0, '说明': 'Improved'}
            }
        }

    def test_round_trip(self):
        # 1. Convert to Excel
        excel_file = data_to_excel(self.data, self.items, self.time_points)
        
        # 2. Read back
        new_data, new_items = excel_to_data(excel_file, self.items)
        
        # 3. Verify
        # Check items (sets to ignore order)
        self.assertEqual(set(new_items), set(self.items))
        
        # Check data content
        for item in self.items:
            for tp in self.time_points:
                original = self.data[item][tp]
                new = new_data[item][tp]
                self.assertEqual(original['得分'], new['得分'])
                self.assertEqual(original['说明'], new['说明'])

if __name__ == '__main__':
    unittest.main()
